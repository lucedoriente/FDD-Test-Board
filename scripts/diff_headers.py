with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\01_Power_Supply.kicad_sch", "r", encoding="utf-8") as f:
    s1_lines = f.readlines()
with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\02_MCU_Core.kicad_sch", "r", encoding="utf-8") as f:
    s2_lines = f.readlines()

print("S1 lines 1-35:")
for l in s1_lines[:35]:
    print(l.rstrip())

print("\nS2 lines 1-35:")
for l in s2_lines[:35]:
    print(l.rstrip())
