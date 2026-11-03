import os

sym_dir = r"C:\Program Files\KiCad\9.0\share\kicad\symbols"
with open(os.path.join(sym_dir, "Transistor_FET.kicad_sym"), "r", encoding="utf-8") as f:
    text_official = f.read()

idx = text_official.find('(symbol "AO3401A"')
cnt = 0
for i, c in enumerate(text_official[idx:]):
    if c == '(': cnt += 1
    elif c == ')':
        cnt -= 1
        if cnt == 0:
            ao_off = text_official[idx:idx+i+1]
            break

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\01_Power_Supply.kicad_sch", "r", encoding="utf-8") as f:
    text_ic = f.read()

idx = text_ic.find('(symbol "Transistor_FET:AO3401A"')
cnt = 0
for i, c in enumerate(text_ic[idx:]):
    if c == '(': cnt += 1
    elif c == ')':
        cnt -= 1
        if cnt == 0:
            ao_ic = text_ic[idx:idx+i+1]
            break

print("Official AO3401A:")
print(ao_off)
print("\n" + "="*40 + "\n")
print("IC AO3401A:")
print(ao_ic[:500])
