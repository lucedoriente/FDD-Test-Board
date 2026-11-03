import os

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\test_single\test_dbg.net", "r") as f:
    text = f.read()

print("Length:", len(text))
idx = text.find('(components')
print(text[idx:])
