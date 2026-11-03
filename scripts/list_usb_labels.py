import re

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\02_MCU_Core.kicad_sch", "r", encoding="utf-8") as f:
    s2 = f.read()

labels = re.findall(r'(\(label "([^"]+)" \(at ([0-9\.-]+) ([0-9\.-]+))', s2)
for full, name, x, y in labels:
    if name in ["USB_DM", "USB_RAW_DP", "USB_DP", "USB_RAW_DM"]:
        print(f"Label {name} at ({x}, {y})")

glabels = re.findall(r'(\(global_label "([^"]+)" [^\(]*\(at ([0-9\.-]+) ([0-9\.-]+))', s2)
for full, name, x, y in glabels:
    if name in ["USB_DM", "USB_RAW_DP", "USB_DP", "USB_RAW_DM"]:
        print(f"Global Label {name} at ({x}, {y})")
