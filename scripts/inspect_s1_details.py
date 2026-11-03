with open('C:/Users/aless/OneDrive/temp/Manutenzione/Kicad_Project/FDD_Tester/kicad/01_Power_Supply.kicad_sch', 'r', encoding='utf-8') as f:
    txt = f.read()

idx = txt.find('"J5"')
print(txt[idx:idx+800])
