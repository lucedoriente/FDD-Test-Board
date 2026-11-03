import os

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\01_Power_Supply.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

idx_start = text.find('(lib_symbols')
print("lib_symbols starts at:", idx_start)

# Let's count parentheses starting from idx_start
open_count = 0
for i, c in enumerate(text[idx_start:]):
    if c == '(':
        open_count += 1
    elif c == ')':
        open_count -= 1
        if open_count == 0:
            print("lib_symbols closes at:", idx_start + i)
            print("Around closing:")
            print(text[idx_start + i - 100 : idx_start + i + 100])
            break
else:
    print("lib_symbols NEVER CLOSES!")
