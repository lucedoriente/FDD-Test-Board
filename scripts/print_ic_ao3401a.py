import os

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\01_Power_Supply.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('(symbol "Transistor_FET:AO3401A"')
cnt = 0
for i, c in enumerate(text[idx:]):
    if c == '(':
        cnt += 1
    elif c == ')':
        cnt -= 1
        if cnt == 0:
            print(text[idx:idx+i+1])
            break
