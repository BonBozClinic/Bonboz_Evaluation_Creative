# Meta Policy Risk Check — Bonboz Clinic (Thẩm mỹ / Việt Nam)

Lớp kiểm tra bổ sung cho creative thẩm mỹ, dựa trên BỘ RULE QUẢNG CÁO Bonboz (19/06/2026).
Áp dụng SAU khi chấm 8 chiều. Mục tiêu: cảnh báo rủi ro bị Meta/luật VN từ chối — KHÔNG chặn sáng tạo quá tay.

## ⚙️ Cấu hình theo quyết định của Bonboz (KHÔNG kiểm các mục sau)
- **KHÔNG** kiểm before/after (ngành ai cũng làm — bỏ).
- **KHÔNG** kiểm targeting 18+ (cấu hình ad set, không thuộc creative).
- **KHÔNG** cờ hình bác sĩ / áo blouse / phòng khám (B09 — Bonboz dùng thoải mái).
- **KHÔNG** cờ "giả UI Facebook"/clickbait (B13 — cho linh hoạt).

## 📌 Phạm vi quét
- Quét MỌI frame + chữ overlay on-screen.
- Các cờ về câu chữ (claim, so sánh, số liệu...) chỉ "bắt trọn" khi có **caption/transcript** kèm theo;
  nếu chỉ có frame thì chỉ soi được chữ cháy trên hình (overlay). Ghi rõ phụ thuộc này trong output.

## 1. Bảng cờ rủi ro

### 🔴 CAO (xuất hiện → "KHÔNG NÊN CHẠY")
| # | Dấu hiệu | Nguồn rule | Sửa an toàn |
|---|---|---|---|
| 1 | **Body-shaming / personal attributes** — ngụ ý khiếm khuyết người xem ("bạn tự ti vì mũi tẹt?", "da xấu", "khuyết điểm", "xấu xí", "lu mờ") | B10, B11 | "Dành cho ai muốn dáng mũi hài hòa / rạng rỡ hơn" |
| 2 | **Nội dung cấm chung** — vũ khí / ma túy / người lớn / giật gân máu me / phân biệt đối xử | B17 | Bỏ/thay cảnh |

### 🟠 TRUNG BÌNH (xuất hiện → "SỬA TRƯỚC KHI CHẠY")
| # | Dấu hiệu | Nguồn rule | Sửa an toàn |
|---|---|---|---|
| 3 | **Claim tuyệt đối** — "tuyệt đối / cam kết / 100% / an toàn tuyệt đối / vĩnh viễn / 1 lần xong" (caption–overlay–audio) | B04, B14 | "kết quả bền lâu tùy cơ địa" |
| 4 | **Từ ngữ y tế "trị bệnh"** — "trị / đặc trị / chữa / điều trị dứt điểm" | B07 | "cải thiện / chăm sóc" |
| 5 | **Vô căn cứ "số 1"** — "tốt nhất / duy nhất / số 1 / độc quyền" không có tài liệu | B02 | bỏ hoặc nêu sự thật kiểm chứng được |
| 6 | **So sánh trực tiếp đối thủ** — "đẹp hơn / rẻ hơn [tên đơn vị]" | B03 | chỉ nói lợi ích của mình |
| 7 | **Số liệu không nguồn** — "%/con số" không trích nguồn ("80% thần thái do mũi…") | W02 | bỏ số hoặc dẫn nguồn; nói định tính |
| 8 | **Engagement bait** — "tag bạn bè / like nếu / share nhận quà" | W04 | đổi sang CTA tư vấn ("Nhắn tin để được tư vấn") |
| 9 | **Cảnh mổ máu me / vết rạch / dụng cụ đâm vào da** | B17, B18 | giữ góc rộng phòng mổ/bác sĩ, không lộ thao tác rạch |
| 10 | **Thiếu khối pháp lý** — tên cơ sở + địa chỉ + số GPHĐ (caption hoặc cháy trên hình) | B01 | QC máy laser → **GPHĐ 11113 (bs Kha)**; còn lại → **GPHĐ 10036 (bs Vũ)** |

### 🟡 NHẸ (lưu ý — không chặn)
| # | Dấu hiệu | Nguồn rule | Ghi chú |
|---|---|---|---|
| 11 | **Lý tưởng hóa cơ thể** (ngụ ý "phải đẹp mới ổn") | B11 | cân bằng thông điệp về sự tự tin/hài hòa |
| 12 | **Zoom cận vùng cơ thể** quá mức | — | mặt thì OK; tránh cận vùng nhạy cảm |
| 13 | **Cường điệu** — "lột xác ngoạn mục / thần kỳ / đẹp như sao Hàn" | B28, W03 | đổi "cải thiện rõ rệt" |
| 14 | **Mốc thời gian CỨNG/cam kết** — "đẹp sau đúng 7 ngày / lột xác sau X ngày" | B15 | ✅ ước lượng MỀM được phép: "thường cải thiện sau vài tuần tùy cơ địa" |
| 15 | **ALL-CAPS + cường điệu/emoji sốc** — "BIẾN ĐỔI NGOẠN MỤC 😱" | W03 | chỉ cờ khi all-caps ĐI KÈM từ giật gân/emoji sốc; viết hoa thường thì OK |
| 16 | **Flashing/nhấp nháy mạnh** | B18 | ⚠️ cần xem full video, frame rời không xác minh chắc |

## 2. Quy tắc verdict policy

```
🚩 POLICY RISK: [PASS / SỬA TRƯỚC KHI CHẠY / KHÔNG NÊN CHẠY]

- Có ≥1 cờ 🔴                        → KHÔNG NÊN CHẠY
- Có ≥1 cờ 🟠 (không có 🔴)          → SỬA TRƯỚC KHI CHẠY
- Chỉ có cờ 🟡                       → PASS (kèm lưu ý)
- (P02) Không bỏ qua cờ 🔴 với lý do "chạy thử"
```

Output bắt buộc khối:
```
🚩 POLICY RISK: <verdict>
- <từng cờ: mức + frame/timestamp + mô tả>
- Đề xuất sửa: <map sang từ an toàn>
- (nếu chỉ có frame, không có caption/audio) Lưu ý: chưa soát được caption/lời thoại.
```

## 3. Lưu ý LUẬT VN (ngoài Meta)
- Quảng cáo phẫu thuật thẩm mỹ cần **giấy xác nhận nội dung + GPHĐ** (Bonboz đã có — B06).
- Hiển thị **tên + địa chỉ + hotline** cơ sở trên creative/end-card (W18, B01).
- Disclaimer "kết quả tùy cơ địa": theo Bonboz, **KHÔNG ép vào AD** (làm mất khách); có thể thay bằng
  "Tư vấn theo phác đồ 1:1" (W01). Daily organic post thì thêm được.
