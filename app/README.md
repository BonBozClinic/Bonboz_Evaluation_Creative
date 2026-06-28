# Bonboz Creative Review

Công cụ review creative quảng cáo (ảnh/video) cho phòng khám thẩm mỹ: chấm chất lượng + bắt lỗi compliance, hiện note theo từng frame trên thanh tua.

## Flow (engine)
```
1 video (+ caption)
   ├─ GEMINI 2.5  → XEM video + NGHE tiếng → perception (transcript, chữ on-screen, cảnh, hook, pacing, claim)
   ├─ CLAUDE A    → chấm ĐỘC LẬP theo tiêu chí (Settings)        ┐
   ├─ CLAUDE B    → VERIFY lại Gemini (chống bịa)                ┘ chạy song song
   └─ CLAUDE C    → MERGE A+B → scorecard 2 trục + findings
```
- **Gemini = mắt + tai** (xem video động + nghe voice — thứ Claude không làm được).
- **Claude = bộ não** (chấm theo tiêu chí + verify chéo + merge). Chạy qua **Claude headless**, KHÔNG cần API key.
- **Tiêu chí** ở `criteria.json` (4 nhóm: Policy / Text overlay / Voice / Video) — sửa trong màn Settings.

## ⚙️ Yêu cầu để chạy (kể cả trên máy khác)

**1. Claude Desktop — BẮT BUỘC** ⭐
Backend gọi Claude qua CLI `claude.exe` đi kèm app Claude Desktop. Trên máy mới phải:
- Tải & cài **Claude Desktop** (claude.ai/download).
- Mở app, **bật chế độ Code hoặc Cowork** (chế độ này mới cài kèm `claude.exe` headless mà backend dùng).
- **Đăng nhập** tài khoản Claude (Pro/Max) — backend dùng phiên đăng nhập này, không cần API key.
- (Backend tự dò `claude.exe` trong thư mục app; nếu không thấy, đảm bảo `claude` chạy được trong terminal.)

**2. Python 3.10+**
```bash
pip install -r requirements.txt
```

**3. Gemini API key** (cho phần xem video + nghe voice)
- Lấy free ở https://aistudio.google.com
- `copy config.example.json config.json` rồi dán key vào `gemini_api_key`.
- *(Bỏ trống cũng chạy được nhưng mất voice + xem video native — chỉ còn Claude xem frame tĩnh.)*

## ▶️ Chạy
```bash
python server.py
```
Mở **http://localhost:8000**

- **Review:** Mở video → Phân tích bằng AI → note hiện trên tua (màu theo người; AI là 1 user) + bảng điểm 2 trục.
- **Settings:** bật/tắt/thêm tiêu chí 4 nhóm.

## Chấm hàng loạt (tùy chọn)
`batch/` có script chấm nhiều video + xuất docx (xem `batch_analyze.py`, `build_docx_b2.py`).

## Bảo mật
- `config.json` (chứa Gemini key) **đã gitignore** — không bao giờ commit.
- Video/kết quả chạy (`dl/`, `results_*.json`, `*.mp4`, `*.docx`) cũng gitignore.

## Sau này
Frontend chuyển React + lưu note ở backend (đa người dùng) + chồng retention thật từ Meta.
