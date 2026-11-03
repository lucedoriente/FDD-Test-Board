from build_full_zero_erc import get_symbol_pins_for_unit

tps_pins = get_symbol_pins_for_unit("Regulator_Switching", "TPS54302", 1)
print("TPS54302 pins:")
for p, info in tps_pins.items():
    print(f"  Pin {p}: {info[0]} ({info[1]}) at ({info[2]}, {info[3]}, rot={info[4]})")

ina_pins = get_symbol_pins_for_unit("Amplifier_Current", "INA180A1", 1)
print("\nINA180A1 pins:")
for p, info in ina_pins.items():
    print(f"  Pin {p}: {info[0]} ({info[1]}) at ({info[2]}, {info[3]}, rot={info[4]})")
