import sys
sys.path.append(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts")
from build_zero_erc_fdd import get_symbol_pins_for_unit

pins = get_symbol_pins_for_unit("Connector_Generic", "Conn_01x04", 1)
print("Conn_01x04 pins:", pins)

pins2 = get_symbol_pins_for_unit("Connector", "Conn_01x04_Pin", 1)
print("Conn_01x04_Pin pins:", pins2)
