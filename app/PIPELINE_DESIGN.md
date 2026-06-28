# Pipeline review creative — thiết kế prompt (Gemini + Claude A/B/C)

Hybrid: **Gemini = mắt+tai (perception)** → **Claude A độc lập ∥ Claude B verify Gemini** → **Claude C merge**.
Engine: Gemini API (có key) + Claude headless. Tiêu chí lấy từ Settings (4 nhóm: Policy / Text-overlay / Voice / Video).

---

## Nguyên tắc thiết kế (locked, research-backed)
1. **Tách PERCEPTION khỏi JUDGMENT.** Gemini KHÔNG bao giờ thấy rubric → tránh "thấy theo kỳ vọng" (model rất suggestible). Gemini chỉ mô tả; Claude mới chấm.
2. **Mỗi điểm phải có LÝ DO + BẰNG CHỨNG (quote/frame), lý do trước điểm sau.** Điểm không bằng chứng = không hợp lệ.
3. **Policy là GATE nhị phân (pass/fail), KHÔNG trung bình vào điểm.** Creative điểm cao vẫn FAIL nếu vi phạm. Chiều "tuân thủ/rủi ro" khi merge LUÔN lấy min(A,B).
4. **Cross-verify chống bịa:** B mặc định hoài nghi Gemini, đòi quote, phân biệt SAI vs KHÔNG-CHẮC vs KHÔNG-KIỂM-CHỨNG-ĐƯỢC.
5. **Không chắc → escalate cho người**, không ép ra số "trông tự tin". Giữ audit trail (nguồn A/B/both).

---

## Luồng dữ liệu
```
video → GEMINI (perception JSON: transcript+timestamp, chữ on-screen, shots, hook 0-3s, pacing, audio, claims verbatim)
   ├─► CLAUDE A: transcript + vài frame + TIÊU CHÍ(Settings) → điểm 8 chiều + policy flags (ĐỘC LẬP, không xem Gemini)
   └─► CLAUDE B: perception của Gemini + transcript + frame → verify từng claim (giữ/sửa/bỏ + cờ rủi ro)
            └─► CLAUDE C: gộp A + B → scorecard 2 trục + findings (timestamp) + escalate nếu mâu thuẫn
```

---

## SETTINGS — cấu trúc 1 tiêu chí (nguồn nuôi prompt Agent A)
```json
{
  "id": "video_hook",            // BẤT BIẾN — dùng để cross-check A↔B↔C
  "group": "video",              // policy | text_overlay | voice | video
  "enabled": true,
  "label": "Hook 3 giây đầu",
  "definition": "3s đầu có chặn scroll: mặt/cảm xúc/nỗi đau/text hook, không mở logo tĩnh.",
  "weight": 1.5,
  "scale": {"1":"mở logo/cảnh tĩnh, không lực hút","3":"có mở nhưng nhạt","5":"giật, chặn scroll ngay"},
  "evidence_required": "Chỉ frame 0-3s + mô tả cái thấy."
}
```
- Policy = list `flags` riêng: {id, definition, severity}. Chỉ pass/fail.
- Backend chỉ render tiêu chí `enabled:true` vào prompt Agent A → schema output tự khớp.
- Gemini prompt = CỐ ĐỊNH (không phụ thuộc Settings). B, C = logic cố định.

---

## PROMPT GEMINI (perception — chỉ mô tả)
Vai trò: máy trích xuất sự thật, KHÔNG chấm/đánh giá/đoán. Quy tắc: chỉ ghi cái quan sát được;
mờ→"unknown"+confidence thấp+ghi uncertain_notes; *_verbatim chép nguyên văn. Quy trình: transcript→chữ on-screen
→shots→hook 0-3s→pacing→audio→claims. Output JSON: {video_meta, voice_transcript[], onscreen_text[], shots[],
hook_0_3s{}, pacing{}, audio_profile{}, claims_and_visuals{}, uncertain_notes[]} — mỗi nhóm có confidence. temp 0-0.2.

## PROMPT CLAUDE A (chấm độc lập)
Vai trò: giám khảo ĐỘC LẬP, không xem nguồn khác. Quy tắc: lý do trước điểm sau; mỗi điểm ≥1 bằng chứng
(quote transcript/frame) nếu không thì confidence=low + missing_evidence_notes; thang số nguyên theo scale;
policy tách pass/fail; chỉ chấm tiêu chí enabled. Inject {{#each criteria where enabled}} block. Output:
{policy_flags[], scores[{criterion_id,reasoning,score,confidence,evidence}], weighted_total, overall_verdict}.

## PROMPT CLAUDE B (verify Gemini)
Vai trò: VERIFIER, mặc định hoài nghi — coi phân tích Gemini là "bản nháp cần kiểm chứng". Tách thành claim đơn;
mỗi claim → DUNG/SAI/KHONG_CHAC/KHONG_KIEM_CHUNG (đòi quote; bắt thổi phồng mức độ "giảm sưng"≠"hết sưng");
confidence neo theo bằng chứng; gắn co_rui_ro cho cam kết y tế tuyệt đối. Output:
{meta{ty_le_gemini_dang_tin}, claims[{claim_goc, verdict, bang_chung, hanh_dong giu/sua/bo, do_tin, co_rui_ro}]}.

## PROMPT CLAUDE C (merge)
Vai trò: gộp A+B, KHÔNG chấm lại, KHÔNG bịa đồng thuận. Điểm: Δ≤1 trung bình theo confidence; 1<Δ≤3 weighted+dispute;
Δ>3 lấy min+needs_review; chiều compliance LUÔN min (gate). Findings: union→dedup(±1s,cùng chủ đề,severity cao hơn)
→lỗi nặng chỉ giữ nếu có timestamp, chỉ-1-nguồn→unverified+needs_review; mâu thuẫn→conflict+cần người.
Verdict: FAIL nếu compliance≤3 hoặc có critical xác nhận; PASS nếu overall≥7 & compliance≥5; escalate_to_human
nếu conflict/≥2 needs_review. Output: {scorecard{dimensions[],axes,overall,verdict}, findings[{time,severity,text,source}],
merge_log[], escalate_to_human}.

(Prompt đầy đủ tiếng Việt từng agent: xem chi tiết trong lịch sử research — sẽ dán vào code khi build.)
