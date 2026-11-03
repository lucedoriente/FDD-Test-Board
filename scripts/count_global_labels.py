import glob, re
from collections import Counter

counts = Counter()
files_per_label = {}

for sch in glob.glob(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\*.kicad_sch"):
    txt = open(sch, encoding="utf-8").read()
    fname = sch.split("\\")[-1]
    matches = re.findall(r'\(global_label\s+"([^"]+)"', txt)
    for m in matches:
        counts[m] += 1
        files_per_label.setdefault(m, []).append(fname)

print("Global labels with count == 1:")
for lbl, c in sorted(counts.items()):
    if c == 1:
        print(f"  {lbl}: {files_per_label[lbl]}")

print("\nGlobal labels with count > 1:")
for lbl, c in sorted(counts.items()):
    if c > 1:
        print(f"  {lbl}: count={c}, files={set(files_per_label[lbl])}")
