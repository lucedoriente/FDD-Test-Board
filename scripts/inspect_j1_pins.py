import sys
sys.path.append(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts")
from build_zero_erc_fdd import get_symbol_pins_for_unit

pins = get_symbol_pins_for_unit("Connector", "Conn_01x02_Pin", 1)
print("Conn_01x02_Pin pins:", pins)
