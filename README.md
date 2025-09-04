# TRIG TOOL (Unicode inline)

Công cụ dòng lệnh tính **sin, cos, tan, cot** và **đổi Độ ↔ Radian**.
- Nhập góc dưới dạng biểu thức có `pi` (ví dụ: `-11*pi/4`, `pi/6`, `3*pi/2`).
- Kết quả in **một dòng** với ký hiệu toán học Unicode: `√`, `π`, dấu nhân `·`.

## Cách chạy nhanh (Python)

```bash
pip install -r requirements.txt
python main.py
```

Chạy nhanh không menu, truyền tham số:
```bash
python main.py cos "-11*pi/4"
python main.py sin "pi/6"
python main.py deg2rad "90"
python main.py rad2deg "pi/3"
```

## Build thành file .exe (Windows)

1) Cài đặt:
```bash
pip install -r requirements.txt
pip install pyinstaller
```

2) Đóng gói:
```bash
pyinstaller --onefile --name trig main.py
```
- File xuất ra: `dist/trig.exe`

3) Chạy:
```bash
dist\trig.exe
dist\trig.exe cos "-11*pi/4"
```

## Gợi ý publish code lên GitHub

- Tạo repo mới (ví dụ `trig-tool`) rồi đẩy các file:
  - `main.py`
  - `requirements.txt`
  - `README.md`

```bash
git init
git add .
git commit -m "Initial commit: trig CLI"
git branch -M main
git remote add origin https://github.com/<your-username>/trig-tool.git
git push -u origin main
```

Sau đó có thể mở **Actions** để tự động build artifact `.exe` bằng GitHub Actions (workflow dùng PyInstaller).
