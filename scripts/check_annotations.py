import os, re
from collections import defaultdict

kicad_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
sch_files = [f for f in os.listdir(kicad_dir) if f.endswith(".kicad_sch")]

unannotated = []
all_refs = defaultdict(list)

for sf in sch_files:
    p = os.path.join(kicad_dir, sf)
    with open(p, "r", encoding="utf-8") as f:
        text = f.read()
    
    # Check for unannotated references (e.g. U?, R?, C?)
    m_q = re.findall(r'\(property "Reference" "([^"]*\?[^"]*)"', text)
    if m_q:
        unannotated.extend([(sf, q) for q in m_q])
    
    refs = re.findall(r'\(property "Reference" "([^#"][^"]*)"', text)
    for r in refs:
        all_refs[sf].append(r)

print("Unannotated components count:", len(unannotated))
if unannotated:
    print("Found unannotated:", unannotated)
else:
    print("ZERO UNANNOTATED COMPONENTS! All components annotated cleanly.")

for sf, rlist in all_refs.items():
    print(f"Sheet {sf}: {len(rlist)} components ({len(set(rlist))} unique references)")
