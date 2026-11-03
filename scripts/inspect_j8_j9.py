with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board.net", "r", encoding="utf-8") as f:
    c = f.read()

for ref in ["J8", "J9", "TP1", "TP2", "TP3", "TP4", "TP5", "TP6", "BZ1"]:
    idx = c.find(f'(comp (ref "{ref}")')
    end = c.find(')', idx + 30)
    print(c[idx:idx+150])
