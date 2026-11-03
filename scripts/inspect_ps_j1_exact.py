import os

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\test_single\01_Power_Supply.kicad_sch", "r", encoding="utf-8") as f:
    ps_text = f.read()

# Let's inspect J1 in 01_Power_Supply.kicad_sch
idx = ps_text.find('(property "Reference" "J1"')
s = ps_text.rfind('(symbol ', 0, idx)
cnt = 0
for i, c in enumerate(ps_text[s:]):
    if c == '(': cnt += 1
    elif c == ')':
        cnt -= 1
        if cnt == 0:
            j1_in_ps = ps_text[s:s+i+1]
            break

print("J1 in 01_Power_Supply:")
print(j1_in_ps)
