import os, re

p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\01_Power_Supply.kicad_sch"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

# Get lib_symbols
ls_start = text.find('(lib_symbols')
cnt = 0
for i, c in enumerate(text[ls_start:]):
    if c == '(': cnt += 1
    elif c == ')':
        cnt -= 1
        if cnt == 0:
            ls_block = text[ls_start:ls_start+i+1]
            break

defined_symbols = set(re.findall(r'\(symbol "([^"]+)"', ls_block))
# Filter out sub-symbols (e.g. name_0_1, name_1_1)
main_symbols = {s for s in defined_symbols if not re.search(r'_\d+_\d+$', s)}
print("Defined symbols in lib_symbols:", sorted(list(main_symbols)))

# Now find all lib_id used by symbols in the schematic
used_symbols = set(re.findall(r'\(symbol \(lib_id "([^"]+)"\)', text))
print("Used symbols in schematic:", sorted(list(used_symbols)))

missing = used_symbols - main_symbols
print("MISSING SYMBOLS:", missing)
