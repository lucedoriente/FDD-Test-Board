import os, re

p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\02_MCU_Core.kicad_sch"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('(symbol "MCU_ST_STM32F4:STM32F407VETx"')
cnt = 0
for i, c in enumerate(text[idx:]):
    if c == '(': cnt += 1
    elif c == ')':
        cnt -= 1
        if cnt == 0:
            mcu_def = text[idx:idx+i+1]
            break

print("Length of MCU definition in IC-Test-Board:", len(mcu_def))
print("Has extends?", "extends" in mcu_def)
subs = re.findall(r'\(symbol "([^"]+)"', mcu_def)
print("Subsymbols in MCU def:", subs)
