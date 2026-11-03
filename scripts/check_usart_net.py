prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
with open(os.path.join(prj_dir, "FDD-Test-Board.net"), "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('(name "USART1_TX")')
if idx != -1:
    print(text[idx-50:idx+300])
else:
    print("USART1_TX not found in netlist")
