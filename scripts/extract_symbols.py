import os

# Test di estrazione simboli standard da KiCad
sym_dir = r"C:\Program Files\KiCad\9.0\share\kicad\symbols"
device_sym = os.path.join(sym_dir, "Device.kicad_sym")

with open(device_sym, "r", encoding="utf-8") as f:
    text = f.read()

# Estraiamo esattamente la definizione di Device:R e Device:C
def get_symbol_def(text, sym_name):
    target = f'(symbol "{sym_name}"'
    start = text.find(target)
    if start == -1:
        return ""
    # Troviamo la fine bilanciando le parentesi
    count = 0
    for i in range(start, len(text)):
        if text[i] == '(':
            count += 1
        elif text[i] == ')':
            count -= 1
            if count == 0:
                return text[start:i+1]
    return ""

r_def = get_symbol_def(text, "R")
c_def = get_symbol_def(text, "C")
print("R def length:", len(r_def))
print("C def length:", len(c_def))
