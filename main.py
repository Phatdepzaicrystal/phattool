# -*- coding: utf-8 -*-
import sys
import sympy as sp
from sympy import pi
from pystyle import Colors, Colorate, Center
import os
import requests

def sym_eval_angle(expr_text: str) -> sp.Expr:
    expr_text = (expr_text or "").strip()
    try:
        angle = sp.sympify(expr_text, locals={"pi": sp.pi})
        return sp.simplify(angle)
    except Exception as e:
        raise ValueError(f"Biểu thức góc không hợp lệ: {expr_text}") from e

def inline_unicode(expr: sp.Expr) -> str:
    expr = sp.simplify(expr)
    s = sp.sstr(expr)
    replacements = {
        "sqrt(": "√(",
        "pi": "π",
        "*": "·",
        "**": "^",
    }
    for k, v in replacements.items():
        s = s.replace(k, v)
    s = s.replace("·(", "(").replace(")·", ")")
    s = s.replace("·π", "π").replace(")·π", ")π").replace("π·", "π")
    return s


def deg_to_rad_str(deg_text: str) -> str:
    deg = float(deg_text.strip())
    rad = sp.nsimplify(deg * sp.pi / 180)
    return inline_unicode(rad)


def rad_to_deg_str(rad_text: str) -> str:
    angle = sym_eval_angle(rad_text)
    deg = sp.nsimplify(angle * 180 / sp.pi)
    return inline_unicode(deg)


def trig_compute(func_name: str, angle_text: str) -> str:
    func_map = {"sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "cot": sp.cot}
    if func_name not in func_map:
        raise ValueError("Hàm lượng giác không hợp lệ.")
    angle = sym_eval_angle(angle_text)
    val = sp.simplify(func_map[func_name](angle))
    return inline_unicode(val)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    re = requests.get('https://ipinfo.io/json')
    ip=re.json()['ip']
    country=re.json()['country']
    org = re.json()['org']
    print(Colorate.Horizontal(Colors.red_to_black,"════════════════════════════════════════════════",1))
    print("\033[1;37m                 \033[1;91mP\033[1;97mH\033[1;36mA\033[1;32mT\033[1;35mC\033[1;33mR\033[1;34mY\033[1;36mS\033[1;32mT\033[1;37mA\033[1;33mL")
    print(Colorate.Horizontal(Colors.red_to_black,"════════════════════════════════════════════════",1))
    print(LIGHT_PURPLE+r"""
 _____                 _____            
/__  /________        /__  /________
  / //_  /_  /          / //_  /_  /
 / /__/ /_/ /_         / /__/ /_/ /_
/____/___/___/        /____/___/___/   
    """+END)
    print("\033[1;97m════════════════════════════════════════════════")
    print("\033[1;97mDev      : \033[1;36mPhat_Crystal ≽^•⩊•^≼")
    print("\033[1;97mBio      : \033[1;36mhttps://guns.lol/phat_crystal")
    print("\033[1;97m════════════════════════════════════════════════")
    print("\033[1;91m[💀] Lưu ý 1: \033[1;32mTool Mới Làm")
    print("\033[1;91m[💀] Lưu ý 2: \033[1;32mBật 1.1.1.1 nếu không nhập đc Authorization!")
    print("\033[1;91m[💀] Lưu ý 3: \033[1;32mTổ hợp phím dừng chương trình: Ctrl + C !")
    print("\033[97m════════════════════════════════════════════════")
    print("\033[91m[🔰] IP ADDRESS: \033[97m",ip)
    print("\033[91m[🔰] COUNTRY: \033[97m",country)
    print("\033[91m[🔰] NHÀ MẠNG: \033[97m",org.split()[1])
    print("\033[97m════════════════════════════════════════════════")

def print_menu():
    print(Colorate.Horizontal(Colors.red_to_yellow, """
    1️⃣  sin(angle)
    2️⃣  cos(angle)
    3️⃣  tan(angle)
    4️⃣  cot(angle)
    5️⃣  🔄 Độ (°) → Radian (rad)
    6️⃣  🔄 Radian (rad) → Độ (°)
    0️⃣  ❎ Thoát
    """))

def main():
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
                print("❌ Lệnh không hợp lệ.")
        except Exception as e:
            print("❌ Lỗi:", e)
        return

    while True:
        clear_screen()
        banner()
        print_menu()
        choice = input("👉 Chọn: ").strip()
        try:
            if choice == "0":
                print(Colorate.Horizontal(Colors.red_to_purple, "👋 Tạm biệt!"))
                break
            elif choice in {"1", "2", "3", "4"}:
                angle_text = input("⏩ Nhập góc (vd: -11*pi/4, pi/6, 3*pi/2): ").strip()
                func = {"1": "sin", "2": "cos", "3": "tan", "4": "cot"}[choice]
                res = trig_compute(func, angle_text)
                print(Colorate.Horizontal(Colors.blue_to_green,
                      f"{func}({inline_unicode(sym_eval_angle(angle_text))}) = {res}"))
            elif choice == "5":
                deg_text = input("⏩ Nhập độ (vd: 180): ").strip()
                print(Colorate.Horizontal(Colors.green_to_cyan,
                      f"{deg_text}° = {deg_to_rad_str(deg_text)} rad"))
            elif choice == "6":
                rad_text = input("⏩ Nhập rad (vd: pi/3): ").strip()
                print(Colorate.Horizontal(Colors.purple_to_blue,
                      f"{inline_unicode(sym_eval_angle(rad_text))} rad = {rad_to_deg_str(rad_text)}°"))
            else:
                print(Colorate.Horizontal(Colors.red_to_yellow, "❌ Lựa chọn không hợp lệ!"))
        except Exception as e:
            print(Colorate.Horizontal(Colors.red_to_yellow, f"❌ Lỗi: {e}"))

        input("\n👉 Nhấn Enter để tiếp tục...")

if __name__ == "__main__":
    main()
