import re

txt = open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board.kicad_sch", encoding='utf-8').read()
root_uuid = re.search(r'\(uuid "([^"]+)"\)', txt).group(1)
print(f"Root UUID: {root_uuid}")
for m in re.finditer(r'\(sheet \(at [^)]+\)\s*\(size [^)]+\)\s*\(fields_autoplaced yes\)\s*\(stroke [^)]+\)\s*\(fill [^)]+\)\s*\(uuid "([^"]+)"\)\s*\(property "Sheetname" "([^"]+)"', txt):
    print(f"Sheet: {m.group(2)} -> UUID: {m.group(1)}")
