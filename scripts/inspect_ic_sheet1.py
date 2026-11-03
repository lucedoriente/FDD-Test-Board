import os, re

p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\01_Power_Supply.kicad_sch"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

refs = re.findall(r'\(property "Reference" "([^"]+)"', text)
print("IC Sheet 1 Refs:", set(refs))

# Find U symbols
u_syms = re.findall(r'\(symbol \(lib_id "([^"]+)"\).*?\(property "Reference" "(U[^"]+)"', text, re.DOTALL)
print("\nIC Sheet 1 ICs:")
for lib, ref in u_syms:
    print(f"  {ref}: {lib}")
