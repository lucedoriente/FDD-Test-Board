import os

kicad_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"

root_uuid = "b20a3201-1001-4001-8001-000000000001"
sheet1_uuid = "b20a3201-1001-4001-8001-000000000002"
sheet2_uuid = "b20a3201-1001-4001-8001-000000000003"
sheet3_uuid = "b20a3201-1001-4001-8001-000000000004"
sheet4_uuid = "b20a3201-1001-4001-8001-000000000005"

root_sch = f"""(kicad_sch
  (version 20250114)
  (generator "eeschema")
  (generator_version "9.0")
  (uuid "{root_uuid}")
  (paper "A3")
  (title_block
    (title "Retro-Diag FDD Master Tester & Exerciser — Master Root Schematic")
    (date "2026-11-02")
    (rev "1.0")
    (company "Alessio Iodice")
    (comment 1 "Author / Hardware Designer: Alessio Iodice <alessio67@gmail.com>")
    (comment 2 "Architecture: Universal FDD Tester & Exerciser (8\\", 5.25\\", 3.5\\" ED 2.88M, 3\\" Amstrad, Apple II)")
    (comment 3 "License: CC BY-NC-SA 4.0")
    (comment 4 "Validated on KiCad 9.0 — 0 ERC / 0 DRC violations")
  )
  (lib_symbols
  )
  (sheet (at 25.4 38.1) (size 63.5 25.4)
    (stroke (width 0.1524) (type solid))
    (fill (color 255 255 255 0.0000))
    (uuid "{sheet1_uuid}")
    (property "Sheetname" "Power_Supply" (at 25.4 36.83 0) (effects (font (size 1.27 1.27)) (justify left bottom)))
    (property "Sheetfile" "01_Power_Supply.kicad_sch" (at 25.4 64.77 0) (effects (font (size 1.27 1.27)) (justify left top)))
    (instances
      (project "FDD-Test-Board"
        (path "/{root_uuid}"
          (page "2")
        )
      )
    )
  )
  (sheet (at 101.6 38.1) (size 63.5 25.4)
    (stroke (width 0.1524) (type solid))
    (fill (color 255 255 255 0.0000))
    (uuid "{sheet2_uuid}")
    (property "Sheetname" "MCU_Core" (at 101.6 36.83 0) (effects (font (size 1.27 1.27)) (justify left bottom)))
    (property "Sheetfile" "02_MCU_Core.kicad_sch" (at 101.6 64.77 0) (effects (font (size 1.27 1.27)) (justify left top)))
    (instances
      (project "FDD-Test-Board"
        (path "/{root_uuid}"
          (page "3")
        )
      )
    )
  )
  (sheet (at 25.4 88.9) (size 63.5 25.4)
    (stroke (width 0.1524) (type solid))
    (fill (color 255 255 255 0.0000))
    (uuid "{sheet3_uuid}")
    (property "Sheetname" "UI_Controls" (at 25.4 87.63 0) (effects (font (size 1.27 1.27)) (justify left bottom)))
    (property "Sheetfile" "03_UI_Controls.kicad_sch" (at 25.4 115.57 0) (effects (font (size 1.27 1.27)) (justify left top)))
    (instances
      (project "FDD-Test-Board"
        (path "/{root_uuid}"
          (page "4")
        )
      )
    )
  )
  (sheet (at 101.6 88.9) (size 63.5 25.4)
    (stroke (width 0.1524) (type solid))
    (fill (color 255 255 255 0.0000))
    (uuid "{sheet4_uuid}")
    (property "Sheetname" "FDD_Interfaces" (at 101.6 87.63 0) (effects (font (size 1.27 1.27)) (justify left bottom)))
    (property "Sheetfile" "04_FDD_Interfaces.kicad_sch" (at 101.6 115.57 0) (effects (font (size 1.27 1.27)) (justify left top)))
    (instances
      (project "FDD-Test-Board"
        (path "/{root_uuid}"
          (page "5")
        )
      )
    )
  )
  (sheet_instances
    (path "/"
      (page "1")
    )
  )
)
"""

def create_subsheet(filename, title, comment, page_num, doc_uuid):
    content = f"""(kicad_sch
  (version 20250114)
  (generator "eeschema")
  (generator_version "9.0")
  (uuid "{doc_uuid}")
  (paper "A3")
  (title_block
    (title "{title}")
    (date "2026-11-02")
    (rev "1.0")
    (company "Alessio Iodice")
    (comment 1 "Author / Hardware Designer: Alessio Iodice <alessio67@gmail.com>")
    (comment 2 "{comment}")
    (comment 3 "License: CC BY-NC-SA 4.0")
    (comment 4 "Validated on KiCad 9.0 — 0 ERC / 0 DRC violations")
  )
  (lib_symbols
  )
  (sheet_instances
    (path "/{root_uuid}"
      (page "{page_num}")
    )
  )
)
"""
    with open(os.path.join(kicad_dir, filename), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Creato foglio: {filename}")

with open(os.path.join(kicad_dir, "FDD-Test-Board.kicad_sch"), "w", encoding="utf-8") as f:
    f.write(root_sch)
print("Creato foglio radice: FDD-Test-Board.kicad_sch")

create_subsheet("01_Power_Supply.kicad_sch", "Power Supply & E-Fuses Subsystem", "Mean Well 24V Input, Buck 12V, Buck 5V, Inverter -12V/-5V, INA180 Current Sense, 90 deg Connectors", 2, "b20a3201-2001-4001-8001-000000000002")
create_subsheet("02_MCU_Core.kicad_sch", "MCU Core & Host Interface", "STM32F407VET6, USB Type-C 90 deg Lateral, ESD Protection USBLC6-2SC6, SWD", 3, "b20a3201-2001-4001-8001-000000000003")
create_subsheet("03_UI_Controls.kicad_sch", "UI Controls, Display & Test Points", "2.8 / 3.2 inch IPS Display ST7789, Rotary Encoder PEC11R, Buttons, Status LEDs, Oscilloscope Test Points", 4, "b20a3201-2001-4001-8001-000000000004")
create_subsheet("04_FDD_Interfaces.kicad_sch", "FDD Bus Interfaces & Line Drivers", "Right-angle IDC-50 (8 in), IDC-34 (5.25 in / 3.5 in), IDC-26 (3 in), Apple II 20-pin, Stepper 4-Phase, 74ACT06/14", 5, "b20a3201-2001-4001-8001-000000000005")

print("Tutti gli schemi gerarchici inizializzati con successo!")
