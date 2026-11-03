import os

rpt_path = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board-erc.rpt"
with open(rpt_path, "r", encoding="utf-8") as f:
    text = f.read()

s2 = text.split("***** Sheet /MCU_Core/")[1].split("***** Sheet")[0]
for l in s2.splitlines()[:30]:
    print(l)
