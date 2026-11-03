import os

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\populate_power_supply.py", "r", encoding="utf-8") as f:
    text = f.read()

print("File length:", len(text))
print("First 500 chars:")
print(text[:500])
