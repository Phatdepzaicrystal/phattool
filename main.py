# -*- coding: utf-8 -*-
"""
CLI Trig Tool (Unicode inline printing)
- Hỗ trợ nhập góc dạng biểu thức có 'pi' (ví dụ: -11*pi/4, pi/6, 3*pi/2)
- Tính sin, cos, tan, cot (kết quả dạng chính xác với ký hiệu toán học một dòng)
- Tùy chọn đổi Độ ↔ Radian
- In kết quả trên CÙNG MỘT HÀNG (inline)
"""

import sys
import math
import sympy as sp

# ---------- Helpers ----------

def sym_eval_angle(expr_text: str) -> sp.Expr:
    """
    Parse chuỗi góc (theo rad) thành biểu thức sympy an toàn.
    Hỗ trợ 'pi' và các phép toán +, -, *, /, (). Ví dụ: '-11*pi/4'.
    """
    expr_text = (expr_text or "").strip()
    try:
        angle = sp.sympify(expr_text, locals={"pi": sp.pi})
        # Đưa về miền [0, 2π) để giảm rủi ro tràn số khi tan/cot
        angle = sp.simplify(angle)
        return angle
    except Exception as e:
        raise ValueError(f"Biểu thức góc không hợp lệ: {expr_text}") from e


def inline_unicode(expr: sp.Expr) -> str:
    """
    Chuyển biểu thức sympy thành chuỗi một dòng với ký hiệu toán học Unicode.
    Ví dụ: sqrt(2)/2 -> '√2/2', pi -> 'π'.
    """
    # Đưa về dạng đơn giản (exact)
    expr = sp.simplify(expr)

    # Định dạng cơ sở bằng sstr (1 dòng), rồi thay thế bằng ký hiệu Unicode.
    s = sp.sstr(expr)

    # Thay thế từ khóa bằng ký hiệu
    replacements = {
        "sqrt(": "√(",
        "pi": "π",
        "*": "·",
        "**": "^",   # mũ
    }
    for k, v in replacements.items():
        s = s.replace(k, v)

    # Một số tinh chỉnh nhỏ cho hiển thị
    s = s.replace("·(", "(")         # bỏ dấu nhân trước ngoặc
    s = s.replace(")·", ")")         # bỏ dấu nhân sau ngoặc
    s = s.replace("·π", "π")         # 1·π -> π
    s = s.replace(")·π", ")π")
    s = s.replace("π·", "π")
    s = s.replace(")·(", ")(")
    return s


def deg_to_rad_str(deg_text: str) -> str:
    try:
        deg = float(deg_text.strip())
    except Exception:
        raise ValueError("Giá trị độ không hợp lệ.")
    rad = sp.nsimplify(deg * sp.pi / 180)
    return inline_unicode(rad)


def rad_to_deg_str(rad_text: str) -> str:
    angle = sym_eval_angle(rad_text)
    deg = sp.nsimplify(sp.simplify(angle) * 180 / sp.pi)
    return inline_unicode(deg)


def trig_compute(func_name: str, angle_text: str) -> str:
    angle = sym_eval_angle(angle_text)
    func_map = {
        "sin": sp.sin,
        "cos": sp.cos,
        "tan": sp.tan,
        "cot": sp.cot,
    }
    if func_name not in func_map:
        raise ValueError("Hàm lượng giác không hợp lệ.")
    val = sp.simplify(func_map[func_name](angle))
    return inline_unicode(val)


# ---------- CLI Menu ----------

def print_menu():
    print("\n=== TRIG TOOL (Unicode inline) ===")
    print("1) sin(angle)")
    print("2) cos(angle)")
    print("3) tan(angle)")
    print("4) cot(angle)")
    print("5) Độ (°) → Radian (rad)")
    print("6) Radian (rad) → Độ (°)")
    print("0) Thoát")


def main():
    # Nếu có đối số kiểu: python main.py cos "-11*pi/4"
    if len(sys.argv) >= 3:
        func = sys.argv[1].lower()
        angle_text = " ".join(sys.argv[2:])
        try:
            if func in {"sin", "cos", "tan", "cot"}:
                res = trig_compute(func, angle_text)
                print(f"{func}({inline_unicode(sym_eval_angle(angle_text))}) = {res}")
            elif func == "deg2rad":
                print(f"{angle_text}° = {deg_to_rad_str(angle_text)} rad")
            elif func == "rad2deg":
                print(f"{inline_unicode(sym_eval_angle(angle_text))} rad = {rad_to_deg_str(angle_text)}°")
            else:
                print("Cú pháp:")
                print('  trig.exe sin "-11*pi/4"')
                print('  trig.exe cos "pi/6"')
                print('  trig.exe tan "3*pi/4"')
                print('  trig.exe cot "pi"')
                print('  trig.exe deg2rad "90"')
                print('  trig.exe rad2deg "pi/3"')
        except Exception as e:
            print("Lỗi:", e)
        return

    # Chế độ menu tương tác
    while True:
        print_menu()
        choice = input("Chọn: ").strip()
        try:
            if choice == "0":
                print("Tạm biệt!")
                break
            elif choice in {"1", "2", "3", "4"}:
                angle_text = input("Nhập góc (rad), ví dụ: -11*pi/4, pi/6, 3*pi/2: ").strip()
                func = {"1": "sin", "2": "cos", "3": "tan", "4": "cot"}[choice]
                res = trig_compute(func, angle_text)
                # In trên CÙNG MỘT HÀNG
                print(f"{func}({inline_unicode(sym_eval_angle(angle_text))}) = {res}")
            elif choice == "5":
                deg_text = input("Nhập độ (°), ví dụ 90, 45, -30: ").strip()
                print(f"{deg_text}° = {deg_to_rad_str(deg_text)} rad")
            elif choice == "6":
                rad_text = input("Nhập rad (vd: pi/3, -11*pi/4): ").strip()
                print(f"{inline_unicode(sym_eval_angle(rad_text))} rad = {rad_to_deg_str(rad_text)}°")
            else:
                print("❌ Lựa chọn không hợp lệ.")
        except Exception as e:
            print("❌ Lỗi:", e)


if __name__ == "__main__":
    main()
