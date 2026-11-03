with open('C:/Users/aless/OneDrive/temp/Manutenzione/Kicad_Project/FDD_Tester/kicad/01_Power_Supply.kicad_sch', 'r', encoding='utf-8') as f:
    s1 = f.read()

idx = s1.find('Conn_01x04')
while idx != -1:
    print(s1[idx-10:idx+60])
    idx = s1.find('Conn_01x04', idx+1)
