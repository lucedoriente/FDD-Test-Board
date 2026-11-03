import re

# Check Sheet 2 overlaps
with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\02_MCU_Core.kicad_sch", "r", encoding="utf-8") as f:
    s2 = f.read()

print("--- Sheet 2 Overlap Inspection ---")
for target in ["USB_DM", "USB_RAW_DP", "CC2_USB", "DIFF_DET_FB", "RECT_OUT"]:
    matches = re.findall(r'\(.*?' + target + r'.*?\)', s2)
    print(f"Occurrences of {target}: {len(matches)}")
    for m in matches[:3]:
        print("  ", m[:100])

# Check Sheet 4 overlaps
with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\04_FDD_Interfaces.kicad_sch", "r", encoding="utf-8") as f:
    s4 = f.read()

print("\n--- Sheet 4 Overlap Inspection ---")
for target in ["+5V_REG", "BUS_WRITE_PROTECT_N"]:
    matches = re.findall(r'\(.*?' + re.escape(target) + r'.*?\)', s4)
    print(f"Occurrences of {target}: {len(matches)}")
    for m in matches[:3]:
        print("  ", m[:100])
