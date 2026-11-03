import re

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\build_zero_erc_fdd.py", "r", encoding="utf-8") as f:
    code = f.read()

calls = re.findall(r'extract_symbol_exact_with_parent\("([^"]+)",\s*"([^"]+)"\)', code)
print(f"Total symbol extract calls: {len(calls)}")
unique_calls = list(set(calls))
print(f"Unique symbols: {len(unique_calls)}")
for lib, sym in sorted(unique_calls):
    print(f"  {lib}:{sym}")
