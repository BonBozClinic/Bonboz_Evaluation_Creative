# -*- coding: utf-8 -*-
import sys, json, glob, tempfile, time, traceback
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, str(Path(__file__).parent.parent))
import server

BD = Path(__file__).parent
items = {it["id"]: it for it in json.load(open(BD/"creatives_b2.json", encoding="utf-8"))}
TARGETS = ["16", "17", "18", "19", "20", "21", "22", "23"]
OUT = BD / "results_b2.json"
results = []
if OUT.exists():
    try: results = json.load(open(OUT, encoding="utf-8"))
    except Exception: results = []
done = {r["id"] for r in results}

def find_vid(i):
    fs = [f for f in glob.glob(str(BD/"dl"/i/"**"/"*"), recursive=True) if f.lower().endswith((".mp4",".mov",".m4v"))]
    return fs[0] if fs else None

c = server.load_criteria()
for i in TARGETS:
    it = items[i]; print("=== #%s %s ===" % (i, it["title"]), flush=True)
    if i in done: print("  đã có, bỏ qua", flush=True); continue
    try:
        vid = find_vid(i)
        if not vid: print("  no video", flush=True); continue
        tmp = Path(tempfile.mkdtemp(prefix="b2_"))
        frames, dur = server.extract_frames(vid, tmp)
        print("  frames", len(frames), "dur", dur, "| gemini…", flush=True)
        t0 = time.time()
        per = server.gemini_perceive(vid) or {}
        gtrans = "\n".join("[%.1fs] %s" % (x.get("t",0), x.get("text","")) for x in per.get("voice_transcript", []))
        trans = "CAPTION (primary text FB):\n" + it["caption"] + "\n\nVOICE (Gemini nghe):\n" + (gtrans or "(trống)")
        print("  gemini done %.0fs, transcript %d dòng | A∥B…" % (time.time()-t0, len(per.get("voice_transcript",[]))), flush=True)
        with ThreadPoolExecutor(max_workers=2) as ex:
            fa = ex.submit(server.call_claude, server.build_A(frames, trans, c), tmp)
            fb = ex.submit(server.call_claude, server.build_B(per, frames, c), tmp)
            A, B = fa.result(), fb.result()
        print("  A findings %d | B trust %s | C merge…" % (len(A.get("findings",[])), B.get("gemini_trust")), flush=True)
        C = server.call_claude(server.build_C(A, B, c))
        res = C if isinstance(C, dict) and C.get("scores") else A
        findings = res.get("findings", []) or []
        sc = server.compute_verdict(res.get("scores",{}), findings, res.get("creative_type","conversion"))
        sc["dim_reasons"] = res.get("dim_reason") or res.get("dim_reasons") or {}
        rec = {"id": i, "title": it["title"], "duration": dur, "scorecard": sc,
               "findings": server.to_notes(findings), "escalate": bool(res.get("escalate_to_human")),
               "gemini_trust": B.get("gemini_trust"),
               "perception": {
                   "transcript": per.get("voice_transcript", []),
                   "onscreen_text": per.get("onscreen_text", []),
                   "shots": per.get("shots", []),
                   "hook_0_3s": per.get("hook_0_3s", ""),
                   "pacing": per.get("pacing", ""),
                   "audio_profile": per.get("audio_profile", ""),
                   "claims_verbatim": per.get("claims_verbatim", [])
               }}
        results.append(rec)
        json.dump(results, open(OUT,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
        print("  -> %s | điểm %s | %.0fs" % (sc["final"], sc["total"], time.time()-t0), flush=True)
    except Exception as e:
        print("  ERROR:", str(e)[:200], flush=True); traceback.print_exc()
print("=== ALL DONE, saved", OUT, "(%d/%d)" % (len(results), len(TARGETS)), flush=True)
