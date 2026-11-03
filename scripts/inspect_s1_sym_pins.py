import sys
sys.path.append(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts")
from build_zero_erc_fdd import get_symbol_pins_for_unit

syms = [
    ("Connector", "Conn_01x02_Pin"),
    ("Connector", "Conn_01x04_Pin"),
    ("Connector_Generic", "Conn_01x04"),
    ("Regulator_Switching", "TPS54302"),
    ("Device", "L"),
    ("Device", "C"),
    ("Device", "R"),
    ("Transistor_FET", "AO3401A"),
    ("Amplifier_Current", "INA180A1"),
    ("power", "PWR_FLAG"),
]

for lib, sym in syms:
    pins = get_symbol_pins_for_unit(lib, sym, 1)
    print(f"=== {lib}:{sym} ===")
    for pnum, pdata in sorted(pins.items()):
        print(f"  Pin {pnum}: offset=({pdata[0]}, {pdata[1]}), name={pdata[2]}, type={pdata[3]}, angle={pdata[4]}")
