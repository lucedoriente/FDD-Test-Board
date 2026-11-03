import os

p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\scripts\generate_clean_erc0_project.py"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('def extract_symbol_exact')
print(text[idx:idx+2500])
