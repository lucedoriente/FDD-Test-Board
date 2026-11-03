import os

sym_dir = r"C:\Program Files\KiCad\9.0\share\kicad\symbols"

def extract_symbol(lib_name, sym_name):
    path = os.path.join(sym_dir, f"{lib_name}.kicad_sym")
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    
    # Cerchiamo (symbol "sym_name"
    target = f'(symbol "{sym_name}"'
    start = text.find(target)
    if start == -1:
        return ""
    
    count = 0
    for i in range(start, len(text)):
        if text[i] == '(':
            count += 1
        elif text[i] == ')':
            count -= 1
            if count == 0:
                s_def = text[start:i+1]
                # Prefissiamo il nome simbolo con la libreria
                s_def = s_def.replace(f'(symbol "{sym_name}"', f'(symbol "{lib_name}:{sym_name}"', 1)
                return s_def
    return ""

if __name__ == "__main__":
    s = extract_symbol("Regulator_Switching", "TPS54302")
    print("TPS54302 extracted length:", len(s))
    g = extract_symbol("power", "GND")
    print("GND extracted length:", len(g))
