import os

kicad_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
subsheets = ["01_Power_Supply.kicad_sch", "02_MCU_Core.kicad_sch", "03_UI_Controls.kicad_sch", "04_FDD_Interfaces.kicad_sch"]

target_old = """  (sheet_instances
    (path "/b20a3201-1001-4001-8001-000000000001"
"""
target_new = """  (sheet_instances
    (path "/"
      (page "1")
    )
  )
)
"""

for s in subsheets:
    p = os.path.join(kicad_dir, s)
    with open(p, "r", encoding="utf-8") as f:
        text = f.read()
    idx = text.rfind('(sheet_instances')
    if idx != -1:
        text = text[:idx] + target_new
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)

print("Updated sheet_instances in all subsheets.")
