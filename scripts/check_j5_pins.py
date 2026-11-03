import build_zero_erc_fdd as bz

pins = bz.get_symbol_pins_for_unit("Connector_Generic", "Conn_01x04", 1)
for p, info in sorted(pins.items()):
    print(f"Pin {p}: ({info[0]}, {info[1]}, rot={info[4]})")
