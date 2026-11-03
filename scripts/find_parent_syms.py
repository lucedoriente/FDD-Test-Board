import subprocess, os, re

test_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\test_single"

# Let's inspect official Q_NPN_EBC and TP0610T in KiCad standard symbols
kicad_sym_dir = r"C:\Program Files\KiCad\9.0\share\kicad\symbols"

with open(os.path.join(kicad_sym_dir, "Transistor_FET.kicad_sym"), "r", encoding="utf-8") as f:
    tfet = f.read()

with open(os.path.join(kicad_sym_dir, "Transistor_BJT.kicad_sym"), "r", encoding="utf-8") as f:
    tbjt = f.read()

# Find TP0610T in tfet
idx = tfet.find('(symbol "TP0610T"')
cnt = 0
for i, c in enumerate(tfet[idx:]):
    if c == '(':
        cnt += 1
    elif c == ')':
        cnt -= 1
        if cnt == 0:
            tp0610t = tfet[idx:idx+i+1]
            break

print("Found TP0610T in official lib:")
print(tp0610t[:300])

# Find Q_NPN_EBC in tbjt
idx = tbjt.find('(symbol "Q_NPN_EBC"')
cnt = 0
for i, c in enumerate(tbjt[idx:]):
    if c == '(':
        cnt += 1
    elif c == ')':
        cnt -= 1
        if cnt == 0:
            q_npn_ebc = tbjt[idx:idx+i+1]
            break

print("Found Q_NPN_EBC in official lib:")
print(q_npn_ebc[:300])
