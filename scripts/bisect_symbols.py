import subprocess, os, re

test_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\test_single"
fdd_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"

with open(os.path.join(fdd_dir, "01_Power_Supply.kicad_sch"), "r", encoding="utf-8") as f:
    ps_content = f.read()

# Let's extract lib_symbols from 01_Power_Supply.kicad_sch
lib_sym_match = re.search(r'\(lib_symbols.*?\n  \)', ps_content, re.DOTALL)
lib_symbols = lib_sym_match.group(0) if lib_sym_match else ""

# Extract all symbol instances
# Find all (symbol (lib_id ...) ...)
# We can find each symbol by matching from (symbol (lib_id to the matching end
raw_symbols = []
# split by \n  (symbol (lib_id
parts = ps_content.split('\n  (symbol (lib_id ')
header = parts[0]
for p in parts[1:]:
    # end of symbol is before the next symbol or before (sheet_instances
    end_idx = p.find('\n  (symbol (lib_id ')
    if end_idx == -1:
        # last symbol before sheet_instances or wire
        # let's find the closing of instances
        inst_end = p.find('    )\n  )')
        if inst_end != -1:
            sym_text = '  (symbol (lib_id ' + p[:inst_end + 7]
            raw_symbols.append(sym_text)
    else:
        sym_text = '  (symbol (lib_id ' + p[:end_idx]
        raw_symbols.append(sym_text)

print(f"Extracted {len(raw_symbols)} symbols from 01_Power_Supply")

# Let's see the first 3 symbols
for i, s in enumerate(raw_symbols[:3]):
    ref = re.search(r'\(property "Reference" "([^"]+)"', s)
    print(f"Symbol {i}: {ref.group(1) if ref else 'UNKNOWN'}")
