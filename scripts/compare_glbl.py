with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\01_Power_Supply.kicad_sch", "r", encoding="utf-8") as f:
    s1 = f.read()
with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\02_MCU_Core.kicad_sch", "r", encoding="utf-8") as f:
    s2 = f.read()

import re

def get_label_sexpr(txt, name):
    idx = txt.find(f'"{name}"')
    while idx != -1:
        start = txt.rfind('(global_label', 0, idx)
        # find matching paren
        c, end = 0, start
        for i in range(start, len(txt)):
            if txt[i] == '(': c += 1
            elif txt[i] == ')':
                c -= 1
                if c == 0:
                    end = i + 1
                    break
        yield txt[start:end]
        idx = txt.find(f'"{name}"', idx + len(name) + 2)

print("--- S1 USART1_TX ---")
for x in get_label_sexpr(s1, "USART1_TX"):
    print(repr(x))

print("--- S2 USART1_TX ---")
for x in get_label_sexpr(s2, "USART1_TX"):
    print(repr(x))
