import os

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\01_Power_Supply.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

ls_start = text.find('(lib_symbols')
cnt = 0
for i, c in enumerate(text[ls_start:]):
    if c == '(': cnt += 1
    elif c == ')':
        cnt -= 1
        if cnt == 0:
            ls_block = text[ls_start:ls_start+i+1]
            break

body_start = ls_start + len(ls_block)
sections = text[body_start:].split(';; --- ')
print("Prelude section content:")
print(sections[0])
