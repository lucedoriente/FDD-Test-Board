import os

p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\IC-Test-Board.kicad_sym"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('(symbol "LM358_Audio"')
cnt = 0
for i, c in enumerate(text[idx:]):
    if c == '(': cnt += 1
    elif c == ')':
        cnt -= 1
        if cnt == 0:
            print(text[idx:idx+i+1])
            break
