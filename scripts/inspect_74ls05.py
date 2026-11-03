import os, re

kicad_sym_dir = r"C:\Program Files\KiCad\9.0\share\kicad\symbols"
with open(os.path.join(kicad_sym_dir, "74xx.kicad_sym"), "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('(symbol "74LS05"')
cnt = 0
for i, c in enumerate(text[idx:]):
    if c == '(': cnt += 1
    elif c == ')':
        cnt -= 1
        if cnt == 0:
            ls05 = text[idx:idx+i+1]
            break

print("74LS05 definition length:", len(ls05))
subs = re.findall(r'\(symbol "([^"]+)"', ls05)
print("74LS05 sub-symbols:", subs)

idx = text.find('(symbol "74LS06"')
cnt = 0
for i, c in enumerate(text[idx:]):
    if c == '(': cnt += 1
    elif c == ')':
        cnt -= 1
        if cnt == 0:
            ls06 = text[idx:idx+i+1]
            break

print("74LS06 definition length:", len(ls06))
subs06 = re.findall(r'\(symbol "([^"]+)"', ls06)
print("74LS06 sub-symbols:", subs06)
