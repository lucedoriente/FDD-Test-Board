import os, re
sym_dir = r"C:\Program Files\KiCad\9.0\share\kicad\symbols"
p = os.path.join(sym_dir, "MCU_ST_STM32F4.kicad_sym")
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

target = '(symbol "STM32F407VETx"'
start = text.find(target)
count = 0
end = 0
for i in range(start, len(text)):
    if text[i] == '(':
        count += 1
    elif text[i] == ')':
        count -= 1
        if count == 0:
            end = i + 1
            break

s_def = text[start:end]
sub_syms = re.findall(r'\(symbol\s+"([^"]+)"', s_def)
print("STM32F407 sub symbols:", sub_syms)
