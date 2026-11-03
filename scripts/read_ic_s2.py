import os

p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\scripts\generate_clean_erc0_project.py"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

s2_idx = text.find("# ----------------- SHEET 2: MCU CORE -----------------")
s3_idx = text.find("# ----------------- SHEET 3:")
print(text[s2_idx:s2_idx+3500])
