import os

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\01_Power_Supply.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

count = 0
for i, c in enumerate(text):
    if c == '(':
        count += 1
    elif c == ')':
        count -= 1
        if count < 0:
            print(f"Extra closing paren at char {i}!")
            break

print("Final balance:", count)
