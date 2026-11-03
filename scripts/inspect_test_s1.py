import os
p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\test_single\01_Power_Supply.kicad_sch"
with open(p, "r") as f:
    t = f.read()
print("Length:", len(t))
print("First 500 chars:")
print(t[:500])
print("\nLast 500 chars:")
print(t[-500:])
