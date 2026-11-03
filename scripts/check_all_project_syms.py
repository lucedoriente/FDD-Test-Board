import os, re
from test_clean_flatten import get_flattened

# Find all components across the 4 sheet generators in build_zero_erc_fdd.py
with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\build_zero_erc_fdd.py", "r", encoding="utf-8") as f:
    code = f.read()

comps = re.findall(r'"lib":\s*"([^"]+)",\s*"sym":\s*"([^"]+)"', code)
print(f"Total comp references found: {len(comps)}")
unique_comps = sorted(list(set(comps)))
print(f"Unique symbol pairs: {len(unique_comps)}")

all_ok = True
for lib, sym in unique_comps:
    try:
        txt = get_flattened(lib, sym)
        if not txt:
            print(f"FAIL: {lib}:{sym} -> returned empty!")
            all_ok = False
        elif "(extends" in txt:
            print(f"FAIL: {lib}:{sym} -> still contains extends!")
            all_ok = False
        else:
            sub_count = len(re.findall(r'\(symbol "', txt)) - 1
            # print(f"OK: {lib}:{sym} (sub-symbols: {sub_count})")
    except Exception as e:
        print(f"EXCEPTION: {lib}:{sym} -> {e}")
        all_ok = False

if all_ok:
    print(f"ALL {len(unique_comps)} SYMBOLS FLATTENED CLEANLY WITH ZERO EXTENDS!")
