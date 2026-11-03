import os

p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\01_Power_Supply.kicad_sch"
with open(p, "r", encoding="utf-8") as f:
    ps = f.read()

idx = ps.find('(symbol "Transistor_FET:AO3401A"')
if idx != -1:
    cnt = 0
    for j in range(idx, len(ps)):
        if ps[j] == '(': cnt += 1
        elif ps[j] == ')':
            cnt -= 1
            if cnt == 0:
                print(ps[idx:j+1])
                break
