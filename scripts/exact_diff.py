import os, difflib, subprocess, re
from bisect_wires_labels import top_exprs, full_ls

prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
with open(os.path.join(prj_dir, "01_Power_Supply.kicad_sch"), "r", encoding="utf-8") as f:
    orig = f.read()

sub_body = "\n".join(top_exprs)
working_sch = f"""(kicad_sch
  (version 20250114)
  (generator "eeschema")
  (generator_version "9.0")
  (uuid "b20a3201-2001-4001-8001-000000000002")
  (paper "A3")
  {full_ls}
  {sub_body}
  (sheet_instances
    (path "/"
      (page "1")
    )
  )
)
"""

diff = list(difflib.unified_diff(orig.splitlines(keepends=True), working_sch.splitlines(keepends=True), fromfile='orig', tofile='working', n=2))
print("Diff length lines:", len(diff))
for line in diff[:80]:
    print(line, end='')
