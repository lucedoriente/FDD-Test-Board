import os, re

prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
for f in ["01_Power_Supply.kicad_sch", "02_MCU_Core.kicad_sch"]:
    p = os.path.join(prj_dir, f)
    with open(p, "r", encoding="utf-8") as file:
        t = file.read()
    m = re.findall(r'\(global_label "USART1_TX".*?\n  \)', t, re.DOTALL)
    print(f"File {f}: {len(m)} occurrences of USART1_TX")
    for item in m:
        print(item)
