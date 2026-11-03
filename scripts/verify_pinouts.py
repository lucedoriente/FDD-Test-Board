import os, sys

scripts_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\scripts"
sys.path.append(scripts_dir)
from generate_clean_erc0_project import extract_symbol_exact, get_symbol_pins

for sym in ["AMS1117-3.3", "USBLC6-2SC6", "RotaryEncoder_Switch", "Conn_01x02_Pin", "Conn_01x04_Pin", "TestPoint", "ULN2003A"]:
    lib = "Device"
    if "AMS" in sym: lib = "Regulator_Linear"
    elif "USB" in sym: lib = "Power_Protection"
    elif "Conn" in sym or "TestPoint" in sym: lib = "Connector"
    elif "ULN" in sym: lib = "Transistor_Array"
    stxt = extract_symbol_exact(lib, sym)
    pins = get_symbol_pins(stxt)
    print(f"{sym} ({lib}) pins:")
    for p in sorted(pins.keys()):
        print(f"  pin {p}: {pins[p][2]} ({pins[p][3]})")
