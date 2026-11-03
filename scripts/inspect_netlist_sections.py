import os, re

p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board.net"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

sections = re.findall(r'\n  \(([a-zA-Z0-9_-]+)', text)
print("Sections found:", set(sections))
for s in set(sections):
    idx = text.find(f"\n  ({s}")
    print(f"Section {s}:", text[idx:idx+200])
