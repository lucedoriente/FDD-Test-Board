import os

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\test_single\test_s1_single_path.net", "r") as f:
    text = f.read()

idx1 = text.find('(design')
idx2 = text.find('(components')
print(text[idx1:idx2])
