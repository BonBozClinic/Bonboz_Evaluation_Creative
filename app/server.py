# -*- coding: utf-8 -*-
"""
Bonboz Creative Review — backend hybrid.
Gemini (mắt+tai) -> Claude A (độc lập) ∥ Claude B (verify Gemini) -> Claude C (merge).
Chạy: pip install -r requirements.txt ; python server.py ; mở http://localhost:8000
Gemini key: dán vào config.json. Để trống = chạy Claude-only (fallback).
"""
import os, re, json, shutil, tempfile, subprocess, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

import cv2
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

BASE = Path(__file__).parent
WEB = BASE / "web"
CONFIG = BASE / "config.json"
CRITERIA = BASE / "criteria.json"
MAX_FRAMES = 16
FRAME_W = 540

app = FastAPI(title="Bonboz Creative Review")

def load_config():
    try: return json.loads(CONFIG.read_text(encoding="utf-8"))
    except Exception: return {}
def load_criteria():
    return json.loads(CRITERIA.read_text(encoding="utf-8"))
def save_criteria(d):
    CRITERIA.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

# ---- criteria + policy (compat) endpoints ----
@app.get("/api/criteria")
def get_criteria(): return load_criteria()
@app.put("/api/criteria")
def put_criteria(body: dict):
    save_criteria(body.get("criteria", body)); return {"ok": True}
@app.get("/api/policies")
def get_policies(): return load_criteria().get("policy", [])
@app.put("/api/policies")
def put_policies(body: dict):
    c = load_criteria(); c["policy"] = body.get("policies", body); save_criteria(c)
    return {"ok": True, "count": len(c["policy"])}

# ---- frames ----
def extract_frames(video_path, out_dir):
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened(): raise HTTPException(400, "Không mở được video")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    dur = total / fps if fps else 0
    times = {0.0, 1.5, 3.0, dur*0.5, dur*0.85, max(0, dur-0.4)}
    t = 0.0
    while t < dur: times.add(round(t, 2)); t += 2.0
    times = sorted(x for x in times if 0 <= x <= dur)
    if len(times) > MAX_FRAMES:
        step = len(times)/MAX_FRAMES; times = [times[int(i*step)] for i in range(MAX_FRAMES)]
    frames = []
    for i, ts in enumerate(times):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(ts*fps)); ok, fr = cap.read()
        if not ok: continue
        h, w = fr.shape[:2]
        if w > FRAME_W: fr = cv2.resize(fr, (FRAME_W, int(h*FRAME_W/w)))
        p = out_dir / ("f%02d_t%.1f.jpg" % (i, ts))
        cv2.imwrite(str(p), fr, [cv2.IMWRITE_JPEG_QUALITY, 80])
        frames.append((round(ts, 2), p))
    cap.release()
    return frames, round(dur, 2)

# ---- claude headless ----
def claude_bin():
    for n in ("claude","claude.cmd","claude.exe"):
        p = shutil.which(n)
        if p: return p
    la = os.environ.get("LOCALAPPDATA","")
    if la:
        c = list(Path(la,"Packages").glob("Claude_*/LocalCache/Roaming/Claude/claude-code/*/claude.exe"))
        if c: c.sort(key=lambda x: x.parent.name); return str(c[-1])
    return "claude"

def call_claude(prompt, add_dir=None):
    model = load_config().get("claude_model", "opus")
    cmd = [claude_bin(), "-p", "--model", model, "--output-format", "json", "--allowedTools", "Read"]
    if add_dir: cmd += ["--add-dir", str(add_dir)]
    try:
        res = subprocess.run(cmd, input=prompt, capture_output=True, text=True, encoding="utf-8", timeout=600)
    except FileNotFoundError:
        raise HTTPException(500, "Không tìm thấy CLI 'claude'.")
    except subprocess.TimeoutExpired:
        raise HTTPException(504, "Claude timeout.")
    out = (res.stdout or "").strip()
    text = out
    try: text = json.loads(out).get("result", out)
    except Exception: pass
    m = re.search(r"\{.*\}", text, re.S)
    if not m: return {}
    try: return json.loads(m.group(0))
    except Exception: return {}

# ---- gemini perception ----
PROMPT_GEMINI = """Bạn là MÁY TRÍCH XUẤT SỰ THẬT cho video quảng cáo thẩm mỹ tiếng Việt. CHỈ MÔ TẢ cái quan sát được, KHÔNG chấm điểm/đánh giá/đoán ý. Chỗ nào mờ thì ghi "unknown".
Xem video (cả hình lẫn TIẾNG) rồi trả về DUY NHẤT 1 JSON object:
{"voice_transcript":[{"t":giây,"text":"lời nói nguyên văn"}],
 "onscreen_text":[{"t":giây,"text":"chữ trên màn nguyên văn"}],
 "shots":[{"t":giây,"desc":"mô tả cảnh khách quan"}],
 "hook_0_3s":"mô tả 3 giây đầu",
 "pacing":"nhịp nhanh/đều/chậm, có đoạn chết không",
 "audio_profile":"tone giọng, nhạc, có ồn không",
 "claims_verbatim":["mọi câu KHẲNG ĐỊNH/cam kết nghe/thấy được, chép nguyên văn"],
 "uncertain_notes":["chỗ không chắc"]}
Không thêm chữ ngoài JSON."""

def gemini_perceive(video_path):
    cfg = load_config(); key = cfg.get("gemini_api_key", "").strip()
    if not key: return None
    from google import genai
    client = genai.Client(api_key=key)
    # copy sang tên ASCII — tránh lỗi encode filename tiếng Việt (Ũ, Đ...)
    fd, up = tempfile.mkstemp(suffix=".mp4"); os.close(fd)
    try: shutil.copy(str(video_path), up)
    except Exception: up = str(video_path)
    f = client.files.upload(file=up)
    for _ in range(90):  # đợi file ACTIVE (tối đa ~180s)
        nm = getattr(f.state, "name", str(f.state))
        if nm == "ACTIVE": break
        if nm == "FAILED": raise RuntimeError("Gemini xử lý file thất bại")
        time.sleep(2); f = client.files.get(name=f.name)
    model = cfg.get("gemini_model", "gemini-2.5-flash")
    txt = ""; last = None
    for attempt in range(6):
        try:
            resp = client.models.generate_content(model=model, contents=[f, PROMPT_GEMINI])
            txt = resp.text or ""; break
        except Exception as e:
            last = e; es = str(e)
            if any(x in es for x in ("503","429","UNAVAILABLE","overloaded","FAILED_PRECONDITION","ACTIVE state")):
                time.sleep(5 * (attempt + 1))
                try: f = client.files.get(name=f.name)
                except Exception: pass
                continue
            raise
    if not txt and last:
        raise last
    m = re.search(r"\{.*\}", txt, re.S)
    try: return json.loads(m.group(0)) if m else {"raw": txt}
    except Exception: return {"raw": txt}

# ---- prompt builders ----
def _crit_block(c):
    L = []
    L.append("POLICY (đúng/sai → cờ):")
    for p in c["policy"]:
        if p.get("enabled"): L.append("  - [%s] %s | %s | sửa: %s" % (p["severity"], p["name"], p["trigger"], p["fix"]))
    for grp, title in [("text_overlay","TEXT OVERLAY (chất lượng chữ)"),("voice","VOICE (lời thoại — dùng transcript)")]:
        L.append(title + ":")
        for x in c[grp]:
            if x.get("enabled"): L.append("  - %s: %s" % (x["label"], x["definition"]))
    L.append("VIDEO (chấm 0-10 mỗi chiều, dùng đúng id):")
    for v in c["video"]:
        if v.get("enabled"): L.append("  - %s (id=%s, w=%s): %s" % (v["label"], v["id"], v["weight"], v["definition"]))
    return "\n".join(L)

def build_A(frames, transcript, c):
    fr = "\n".join("  - t=%.1fs -> %s" % (t, p) for t, p in frames)
    return ("Bạn là GIÁM KHẢO ĐỘC LẬP chấm creative thẩm mỹ Bonboz. DÙNG Read đọc từng frame. "
        "Lý do TRƯỚC, điểm SAU; mỗi điểm phải có bằng chứng (quote transcript / mô tả frame), không thì confidence=low.\n\n"
        + _crit_block(c) + "\n\nTRANSCRIPT (voice):\n" + (transcript or "(không có)") + "\n\nFRAME:\n" + fr +
        "\n\nPhân loại creative_type (awareness|conversion). Trả về DUY NHẤT JSON:\n"
        '{"creative_type":"...","scores":{"<id video>":0-10,...},"dim_reasons":{"<id>":"lý do + bằng chứng"},'
        '"findings":[{"time":giây,"severity":"CAO|TB|NHẸ","label":"tên","text":"frame/giây này lỗi gì + cách sửa"}]}\n'
        "findings gồm: vi phạm policy + lỗi text-overlay/voice + chiều nào yếu (<6) nêu rõ yếu chỗ nào.")

def build_B(perception, frames, c):
    fr = "\n".join("  - t=%.1fs -> %s" % (t, p) for t, p in frames)
    return ("Bạn là VERIFIER, MẶC ĐỊNH HOÀI NGHI. Dưới đây là phân tích của Gemini (xem video native) — coi như BẢN NHÁP CẦN KIỂM CHỨNG. "
        "DÙNG Read đối chiếu với frame. Bắt chỗ Gemini BỊA/THỔI PHỒNG (vd 'giảm sưng'≠'hết sưng'). "
        "Sau đó tự chấm lại theo tiêu chí.\n\n"
        + _crit_block(c) + "\n\nGEMINI PERCEPTION:\n" + json.dumps(perception, ensure_ascii=False)[:6000] + "\n\nFRAME:\n" + fr +
        "\n\nTrả về DUY NHẤT JSON (cùng cấu trúc với giám khảo độc lập, THÊM gemini_trust 0-1 + rejected_claims):\n"
        '{"creative_type":"...","gemini_trust":0-1,"rejected_claims":["claim Gemini bịa"],'
        '"scores":{"<id video>":0-10},"dim_reasons":{"<id>":"..."},'
        '"findings":[{"time":giây,"severity":"CAO|TB|NHẸ","label":"...","text":"..."}]}')

def build_C(A, B, c):
    return ("Bạn là Agent MERGE. Gộp 2 luồng A (độc lập) và B (đã verify Gemini) thành 1 kết quả CUỐI. "
        "KHÔNG chấm lại, KHÔNG bịa đồng thuận. Quy tắc: mỗi chiều, lệch ≤1 → trung bình; lệch >3 → lấy MIN + needs_review. "
        "Chiều rủi ro/tuân thủ → luôn lấy MIN. Findings: union + dedup (cùng ±1s & cùng ý → giữ severity cao hơn). "
        "Lỗi nặng chỉ-1-nguồn → giữ nhưng severity='NHẸ' + ghi (chưa xác nhận). Mâu thuẫn trực diện → severity='conflict' + escalate.\n\n"
        "LUỒNG A:\n" + json.dumps(A, ensure_ascii=False)[:5000] + "\n\nLUỒNG B:\n" + json.dumps(B, ensure_ascii=False)[:5000] +
        "\n\nQUAN TRỌNG — viết cho CREATOR đọc, KHÔNG phải kỹ sư:\n"
        "- dim_reason: 1 câu SẠCH (yếu/mạnh chỗ nào + cách sửa). TUYỆT ĐỐI không nhắc 'A/B', không nhắc số điểm, không 'lệch/trung bình/min'.\n"
        "- dim_audit: ghi cách gộp kỹ thuật (A.../B.../lệch.../lấy min) — phần này ẩn, cho người kiểm chứng.\n"
        "- findings.text: PLAIN 'sai gì → sửa sao', KHÔNG ghi [A-only]/[conflict]/'chưa xác nhận' vào text. Dùng cờ unverified=true cho cái chỉ 1 nguồn / mâu thuẫn chưa chốt.\n"
        "\nTrả về DUY NHẤT JSON:\n"
        '{"creative_type":"...","scores":{"<id video>":0-10},'
        '"dim_reason":{"<id>":"câu sạch cho creator"},'
        '"dim_audit":{"<id>":"cách gộp A/B"},'
        '"findings":[{"time":giây,"severity":"CAO|TB|NHẸ","text":"sai gì → sửa sao","unverified":true/false}],'
        '"escalate_to_human":true/false}')

# ---- verdict ----
def compute_verdict(scores, findings, ctype):
    c = load_criteria()
    vids = [(v["id"], v["weight"]) for v in c["video"] if v.get("enabled")]
    s = {vid: float(scores.get(vid, 0) or 0) for vid, _ in vids}
    wsum = sum(w for _, w in vids) or 1
    total = round(sum(s[vid]*w for vid, w in vids)/wsum*1.0, 1)
    core = [s.get("vd_hook",0), s.get("vd_message",0), s.get("vd_cta",0)]
    cmin = min(core) if core else 0
    if total >= 7.0 and cmin >= 5: quality = "ĐẠT"
    elif total < 6.0: quality = "YẾU"
    else: quality = "CẦN TỐI ƯU"
    if s.get("vd_cta",10) < 5 and ctype != "awareness" and quality == "ĐẠT": quality = "CẦN TỐI ƯU"
    sevs = set((f.get("severity") or "").upper() for f in findings)
    if "CAO" in sevs: policy = "KHÔNG NÊN CHẠY"
    elif "TB" in sevs: policy = "SỬA TRƯỚC"
    else: policy = "PASS"
    if policy == "KHÔNG NÊN CHẠY": final = "KHÔNG CHẠY"
    elif policy == "SỬA TRƯỚC": final = "SỬA POLICY TRƯỚC"
    elif quality == "ĐẠT": final = "SẴN SÀNG CHẠY"
    else: final = "TỐI ƯU CHẤT LƯỢNG TRƯỚC"
    return {"scores": s, "total": total, "quality": quality, "policy": policy, "final": final, "type": ctype}

def to_notes(findings):
    notes = []
    for it in findings:
        try:
            notes.append({"time": float(it.get("time", 0)), "author": "AI (Claude)",
                          "severity": (it.get("severity") or "").upper(),
                          "unverified": bool(it.get("unverified")),
                          "text": str(it.get("text", "")).strip()})
        except Exception: continue
    return notes

# ---- analyze ----
@app.post("/api/analyze")
def analyze(file: UploadFile = File(...)):
    tmp = Path(tempfile.mkdtemp(prefix="bcr_"))
    try:
        vid = tmp / (file.filename or "video.mp4")
        with open(vid, "wb") as f: shutil.copyfileobj(file.file, f)
        frames, dur = extract_frames(vid, tmp)
        if not frames: raise HTTPException(400, "Không cắt được frame nào")
        c = load_criteria()
        perception = None
        try: perception = gemini_perceive(vid)
        except Exception as e: perception = {"_error": str(e)[:300]}

        if perception and "_error" not in perception:
            transcript = "\n".join("[%.1fs] %s" % (x.get("t",0), x.get("text","")) for x in perception.get("voice_transcript", []))
            with ThreadPoolExecutor(max_workers=2) as ex:
                fa = ex.submit(call_claude, build_A(frames, transcript, c), tmp)
                fb = ex.submit(call_claude, build_B(perception, frames, c), tmp)
                A, B = fa.result(), fb.result()
            C = call_claude(build_C(A, B, c))
            mode = "hybrid (Gemini + Claude A/B/C)"
            result = C if isinstance(C, dict) and C.get("scores") else A
        else:
            # fallback Claude-only
            result = call_claude(build_A(frames, "", c), tmp)
            mode = "claude-only (chưa có Gemini key)" if not load_config().get("gemini_api_key") else "claude-only (Gemini lỗi)"
            A = B = None

        if not isinstance(result, dict): result = {}
        findings = result.get("findings", []) or []
        ctype = result.get("creative_type", "conversion")
        scorecard = compute_verdict(result.get("scores", {}), findings, ctype)
        scorecard["dim_reasons"] = result.get("dim_reason") or result.get("dim_reasons") or {}
        scorecard["dim_audit"] = result.get("dim_audit") or {}
        scorecard["escalate"] = bool(result.get("escalate_to_human"))
        scorecard["gemini_trust"] = (B or {}).get("gemini_trust") if isinstance(B, dict) else None
        return {"duration": dur, "frames": len(frames), "mode": mode,
                "scorecard": scorecard, "notes": to_notes(findings)}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

# ---- static ----
@app.get("/")
def index(): return FileResponse(WEB / "index.html")
@app.get("/settings")
def settings(): return FileResponse(WEB / "settings.html")
if WEB.exists(): app.mount("/static", StaticFiles(directory=str(WEB)), name="static")

if __name__ == "__main__":
    k = "có" if load_config().get("gemini_api_key") else "CHƯA (chạy Claude-only)"
    print("Bonboz Creative Review -> http://localhost:8000  | Gemini key:", k)
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")
