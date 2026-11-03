import os, re

sym_dir = r"C:\Program Files\KiCad\9.0\share\kicad\symbols"
p = os.path.join(sym_dir, "74xx.kicad_sym")
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

target = '(symbol "74LS06"'
idx = text.find(target)
count = 0
end = 0
for i in range(idx, len(text)):
    if text[i] == '(': count += 1
    elif text[i] == ')':
        count -= 1
        if count == 0:
            end = i + 1; break

chunk = text[idx:end]
sub_syms = re.findall(r'\(symbol\s+"([^"]+)"', chunk)
print("74LS06 sub symbols:", sub_syms)
