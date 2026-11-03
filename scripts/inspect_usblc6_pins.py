from test_clean_flatten import extract_raw
from build_zero_erc_fdd import get_symbol_pins_for_unit

pins = get_symbol_pins_for_unit("Power_Protection", "USBLC6-2SC6", 1)
print("USBLC6-2SC6 pins:")
for pnum, (dx, dy, name, ptype, ang) in pins.items():
    print(f"  Pin {pnum} ({name}): dx={dx}, dy={dy}, angle={ang}")
