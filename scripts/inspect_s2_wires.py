import re

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\02_MCU_Core.kicad_sch", "r", encoding="utf-8") as f:
    s2 = f.read()

# Let's find wires connected to 358.14 111.76
wires = re.findall(r'\(wire \(pts \(xy [^\)]+\) \(xy [^\)]+\)\)[^\)]*\)', s2)
for w in wires:
    if "358.14 111.76" in w:
        print("Wire near 358.14 111.76:", w)

# Also check CC2_USB / GND overlap:
for w in wires:
    if "25.40 123.19" in w or "71.12 88.90" in w:
        print("Wire near CC2_USB:", w)

# Also check USB_DM / USB_RAW_DP:
for w in wires:
    if "71.12 99.06" in w or "233.68 106.68" in w:
        print("Wire near USB_DM/DP:", w)
