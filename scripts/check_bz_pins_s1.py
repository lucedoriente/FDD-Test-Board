import build_zero_erc_fdd as bz

for lib, sym in [
    ("Connector", "Conn_01x02_Pin"),
    ("Connector", "Conn_01x04_Pin"),
    ("Connector_Generic", "Conn_01x04"),
    ("Regulator_Switching", "TPS54302"),
    ("Amplifier_Current", "INA180A1"),
    ("Transistor_FET", "AO3401A"),
    ("Device", "L"),
    ("Device", "C"),
    ("Device", "R"),
]:
    pins = bz.get_symbol_pins_for_unit(lib, sym, 1)
    print(f"{lib}:{sym} -> {len(pins)} pins found: {sorted(list(pins.keys()))}")
