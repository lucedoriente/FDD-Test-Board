import os, re

sym_dir = r"C:\Program Files\KiCad\9.0\share\kicad\symbols"
p = os.path.join(sym_dir, "MCU_ST_STM32F4.kicad_sym")
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

target = '(symbol "STM32F407VETx"'
start = text.find(target)
count, end = 0, 0
for i in range(start, len(text)):
    if text[i] == '(':
        count += 1
    elif text[i] == ')':
        count -= 1
        if count == 0:
            end = i + 1
            break

s_def = text[start:end]
pattern = re.compile(r'\(pin\s+([^\s]+)\s+[^\s]+\s+\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?\).*?\(name\s+"([^"]*)".*?\(number\s+"([^"]*)"', re.DOTALL)
pins = {}
for m in pattern.finditer(s_def):
    pins[m.group(6)] = (m.group(5), m.group(1), float(m.group(2)), float(m.group(3)), int(float(m.group(4) or 0)))

print("Total pins found:", len(pins))
for num in sorted(pins.keys(), key=lambda x: int(x) if x.isdigit() else 999):
    print(f"Pin {num:3s}: {pins[num][0]:20s} ({pins[num][1]}) at ({pins[num][2]:6.2f}, {pins[num][3]:6.2f}, {pins[num][4]:3d} deg)")
