import re

tb_main_sch = '''  (title_block
    (title "Retro-Diag FDD Master Tester & Exerciser — Master Root Schematic")
    (date "2026-11-03")
    (rev "1.0")
    (company "Alessio Iodice")
    (comment 1 "Author / Hardware Designer: Alessio Iodice <alessio67@gmail.com>")
    (comment 2 "Architecture: Universal FDD Tester & Exerciser (8\\", 5.25\\", 3.5\\" ED 2.88M, 3\\" Amstrad, Apple II)")
    (comment 3 "License: CC BY-NC-SA 4.0")
    (comment 4 "Validated on KiCad 9.0 — 0 ERC / 0 DRC violations")
  )'''

tb_main_pcb = '''  (title_block
    (title "Retro-Diag FDD Master Tester & Exerciser — Mainboard")
    (date "2026-11-03")
    (rev "1.0")
    (company "Alessio Iodice")
    (comment 1 "Author / Hardware Designer: Alessio Iodice <alessio67@gmail.com>")
    (comment 2 "Architecture: Universal FDD Tester & Exerciser (8\\", 5.25\\", 3.5\\" ED 2.88M, 3\\" Amstrad, Apple II)")
    (comment 3 "License: CC BY-NC-SA 4.0")
    (comment 4 "Validated on KiCad 9.0 — 0 ERC / 0 DRC violations")
  )'''

tb_ui = '''  (title_block
    (title "Retro-Diag FDD Master Tester — Front Panel UI Daughterboard")
    (date "2026-11-03")
    (rev "1.0")
    (company "Alessio Iodice")
    (comment 1 "Author / Hardware Designer: Alessio Iodice <alessio67@gmail.com>")
    (comment 2 "Front Panel Daughterboard with Rotary Encoder, Buttons and Status LEDs")
    (comment 3 "License: CC BY-NC-SA 4.0")
    (comment 4 "Validated on KiCad 9.0 — 0 ERC / 0 DRC violations")
  )'''

def replace_tb(filepath, new_tb):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = re.sub(r'  \(title_block.*?\n  \)', new_tb, content, flags=re.DOTALL)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('Updated:', filepath)

replace_tb(r'c:\Users\aless\.gemini\antigravity\scratch\FDD_Tester\kicad\FDD-Test-Board.kicad_sch', tb_main_sch)
replace_tb(r'c:\Users\aless\.gemini\antigravity\scratch\FDD_Tester\kicad\FDD-Test-Board.kicad_pcb', tb_main_pcb)
replace_tb(r'c:\Users\aless\.gemini\antigravity\scratch\FDD_Tester\kicad\FDD_UI_Panel\FDD_UI_Panel.kicad_sch', tb_ui)
replace_tb(r'c:\Users\aless\.gemini\antigravity\scratch\FDD_Tester\kicad\FDD_UI_Panel\FDD_UI_Panel.kicad_pcb', tb_ui)
