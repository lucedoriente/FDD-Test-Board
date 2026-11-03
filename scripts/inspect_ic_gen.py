import os, re

p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\scripts\generate_clean_erc0_project.py"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

# Search for symbol extraction or lib_symbols
matches = [line for line in text.splitlines() if "lib_symbols" in line or "def get_sym" in line or "extract" in line or "extends" in line]
print(f"Found {len(matches)} matching lines:")
for m in matches[:20]:
    print(" ", m)
