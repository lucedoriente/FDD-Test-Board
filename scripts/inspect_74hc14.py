import os, sys

scripts_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\scripts"
sys.path.append(scripts_dir)
from generate_clean_erc0_project import extract_symbol_exact, get_symbol_pins

stxt = extract_symbol_exact("74xx", "74HC14")
pins = get_symbol_pins(stxt)
print("74HC14 pins:", pins)
