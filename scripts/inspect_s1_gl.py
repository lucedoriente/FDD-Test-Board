with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\01_Power_Supply.kicad_sch", "r", encoding="utf-8") as f:
    s1 = f.read()

idx = s1.find("(global_label")
print("First global label in Sheet 1:")
print(s1[idx:idx+300])
