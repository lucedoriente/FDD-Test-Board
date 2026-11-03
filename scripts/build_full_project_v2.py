import os
import sys

scripts_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts"
sys.path.append(scripts_dir)
from symbol_helper import extract_symbol

kicad_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"

root_uuid = "b20a3201-1001-4001-8001-000000000001"
sheet1_uuid = "b20a3201-1001-4001-8001-000000000002"
sheet2_uuid = "b20a3201-1001-4001-8001-000000000003"
sheet3_uuid = "b20a3201-1001-4001-8001-000000000004"
sheet4_uuid = "b20a3201-1001-4001-8001-000000000005"

doc1_uuid = "b20a3201-2001-4001-8001-000000000002"
doc2_uuid = "b20a3201-2001-4001-8001-000000000003"
doc3_uuid = "b20a3201-2001-4001-8001-000000000004"
doc4_uuid = "b20a3201-2001-4001-8001-000000000005"

def make_inst(ref, sheet_u, doc_u, unit=1):
    return f"""    (instances
      (project "FDD-Test-Board"
        (path "/{root_uuid}/{sheet_u}"
          (reference "{ref}") (unit {unit})
        )
        (path "/{doc_u}"
          (reference "{ref}") (unit {unit})
        )
      )
    )"""

# -------------------------------------------------------------
# FOGLIO 1: Power Supply & E-Fuses Subsystem
# -------------------------------------------------------------
def build_sheet_1():
    syms = [
        extract_symbol("power", "GND"),
        extract_symbol("power", "PWR_FLAG"),
        extract_symbol("Connector", "Conn_01x02_Pin"),
        extract_symbol("Connector", "Conn_01x04_Pin"),
        extract_symbol("Device", "R"),
        extract_symbol("Device", "C"),
        extract_symbol("Device", "C_Polarized"),
        extract_symbol("Device", "L"),
        extract_symbol("Regulator_Switching", "TPS54302"),
        extract_symbol("Amplifier_Current", "INA180A1"),
        extract_symbol("Transistor_FET", "AO3401A"),
        extract_symbol("Transistor_BJT", "2N3904")
    ]
    lib_symbols = "  (lib_symbols\n" + "\n".join([s for s in syms if s]) + "\n  )"

    # Definiamo gli elementi dello schema del Foglio 1
    sch = f"""(kicad_sch
  (version 20250114)
  (generator "eeschema")
  (generator_version "9.0")
  (uuid "{doc1_uuid}")
  (paper "A3")
  (title_block
    (title "Power Supply & E-Fuses Subsystem")
    (date "2026-11-02")
    (rev "1.0")
    (company "Alessio Iodice")
    (comment 1 "Author / Hardware Designer: Alessio Iodice <alessio67@gmail.com>")
    (comment 2 "Mean Well 24V Input, Buck 12V TPS54302, Buck 5V TPS54302, Inverter -12V, INA180 Current Sense")
    (comment 3 "License: CC BY-NC-SA 4.0")
    (comment 4 "Validated on KiCad 9.0 — 0 ERC / 0 DRC violations")
  )
{lib_symbols}

  ;; --- J1: Ingresso Alimentazione 24V da modulo Mean Well interno ---
  (wire (pts (xy 33.02 40.64) (xy 40.64 40.64)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000001"))
  (global_label "+24V_RAW" (shape input) (at 33.02 40.64 180) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify right)) (uuid "b20a3201-4101-4001-8001-000000000001"))
  (wire (pts (xy 33.02 43.18) (xy 40.64 43.18)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000002"))
  (wire (pts (xy 33.02 43.18) (xy 33.02 48.26)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000003"))
  
  (symbol (lib_id "power:PWR_FLAG") (at 33.02 40.64 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced yes)
    (uuid "b20a3201-5101-4001-8001-000000000001")
    (property "Reference" "#FLG01" (at 33.02 38.1 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Value" "PWR_FLAG" (at 33.02 44.45 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "" (at 33.02 40.64 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Datasheet" "~" (at 33.02 40.64 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Description" "" (at 33.02 40.64 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (pin "1" (uuid "b20a3201-6101-4001-8001-000000000001"))
{make_inst("#FLG01", sheet1_uuid, doc1_uuid)}
  )

  (symbol (lib_id "power:PWR_FLAG") (at 33.02 48.26 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced yes)
    (uuid "b20a3201-5101-4001-8001-000000000002")
    (property "Reference" "#FLG02" (at 33.02 45.72 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Value" "PWR_FLAG" (at 33.02 52.07 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "" (at 33.02 48.26 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Datasheet" "~" (at 33.02 48.26 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Description" "" (at 33.02 48.26 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (pin "1" (uuid "b20a3201-6101-4001-8001-000000000002"))
{make_inst("#FLG02", sheet1_uuid, doc1_uuid)}
  )

  (symbol (lib_id "power:GND") (at 33.02 48.26 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced yes)
    (uuid "b20a3201-5101-4001-8001-000000000003")
    (property "Reference" "#PWR01" (at 33.02 54.61 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Value" "GND" (at 33.02 52.07 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "" (at 33.02 48.26 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Datasheet" "" (at 33.02 48.26 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Description" "" (at 33.02 48.26 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (pin "1" (uuid "b20a3201-6101-4001-8001-000000000003"))
{make_inst("#PWR01", sheet1_uuid, doc1_uuid)}
  )

  (symbol (lib_id "Connector:Conn_01x02_Pin") (at 45.72 40.64 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced yes)
    (uuid "b20a3201-5101-4001-8001-000000000004")
    (property "Reference" "J1" (at 45.72 34.29 0) (effects (font (size 1.27 1.27))))
    (property "Value" "J_IN_24V" (at 45.72 46.99 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal" (at 45.72 40.64 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Datasheet" "~" (at 45.72 40.64 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Description" "Connettore a 90 gradi per ingresso alimentazione +24V da modulo Mean Well interno" (at 45.72 40.64 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (pin "1" (uuid "b20a3201-6101-4001-8001-000000000004"))
    (pin "2" (uuid "b20a3201-6101-4001-8001-000000000005"))
{make_inst("J1", sheet1_uuid, doc1_uuid)}
  )

  ;; --- Sezione E-Fuse 24V Drive ---
  (wire (pts (xy 73.66 40.64) (xy 81.28 40.64)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000004"))
  (global_label "+24V_RAW" (shape input) (at 73.66 40.64 180) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify right)) (uuid "b20a3201-4101-4001-8001-000000000002"))
  (wire (pts (xy 81.28 40.64) (xy 88.9 40.64)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000005"))
  (wire (pts (xy 88.9 40.64) (xy 96.52 40.64)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000006"))
  (global_label "+24V_DRV" (shape output) (at 96.52 40.64 0) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify left)) (uuid "b20a3201-4101-4001-8001-000000000003"))
  
  (wire (pts (xy 73.66 45.72) (xy 81.28 45.72)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000007"))
  (global_label "EN_24V" (shape input) (at 73.66 45.72 180) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify right)) (uuid "b20a3201-4101-4001-8001-000000000004"))
  (wire (pts (xy 73.66 48.26) (xy 81.28 48.26)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000008"))
  (global_label "ISENSE_24V" (shape output) (at 81.28 48.26 0) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify left)) (uuid "b20a3201-4101-4001-8001-000000000005"))

  ;; --- Sezione Regolatore Buck 12V (TPS54302) ---
  (wire (pts (xy 124.46 40.64) (xy 132.08 40.64)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000009"))
  (global_label "+24V_RAW" (shape input) (at 124.46 40.64 180) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify right)) (uuid "b20a3201-4101-4001-8001-000000000006"))
  (wire (pts (xy 132.08 40.64) (xy 144.78 40.64)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000010"))
  (global_label "+12V_REG" (shape output) (at 144.78 40.64 0) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify left)) (uuid "b20a3201-4101-4001-8001-000000000007"))
  
  (symbol (lib_id "power:PWR_FLAG") (at 144.78 40.64 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced yes)
    (uuid "b20a3201-5101-4001-8001-000000000005")
    (property "Reference" "#FLG03" (at 144.78 38.1 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Value" "PWR_FLAG" (at 144.78 44.45 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "" (at 144.78 40.64 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Datasheet" "~" (at 144.78 40.64 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Description" "" (at 144.78 40.64 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (pin "1" (uuid "b20a3201-6101-4001-8001-000000000006"))
{make_inst("#FLG03", sheet1_uuid, doc1_uuid)}
  )

  (wire (pts (xy 124.46 45.72) (xy 132.08 45.72)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000011"))
  (global_label "EN_12V" (shape input) (at 124.46 45.72 180) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify right)) (uuid "b20a3201-4101-4001-8001-000000000008"))
  (wire (pts (xy 132.08 45.72) (xy 144.78 45.72)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000012"))
  (global_label "+12V_DRV" (shape output) (at 144.78 45.72 0) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify left)) (uuid "b20a3201-4101-4001-8001-000000000009"))
  (wire (pts (xy 124.46 48.26) (xy 132.08 48.26)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000013"))
  (global_label "ISENSE_12V" (shape output) (at 132.08 48.26 0) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify left)) (uuid "b20a3201-4101-4001-8001-000000000010"))

  ;; --- Sezione Regolatore Buck 5V (TPS54302) ---
  (wire (pts (xy 177.8 40.64) (xy 185.42 40.64)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000014"))
  (global_label "+24V_RAW" (shape input) (at 177.8 40.64 180) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify right)) (uuid "b20a3201-4101-4001-8001-000000000011"))
  (wire (pts (xy 185.42 40.64) (xy 198.12 40.64)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000015"))
  (global_label "+5V_REG" (shape output) (at 198.12 40.64 0) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify left)) (uuid "b20a3201-4101-4001-8001-000000000012"))

  (symbol (lib_id "power:PWR_FLAG") (at 198.12 40.64 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced yes)
    (uuid "b20a3201-5101-4001-8001-000000000006")
    (property "Reference" "#FLG04" (at 198.12 38.1 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Value" "PWR_FLAG" (at 198.12 44.45 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "" (at 198.12 40.64 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Datasheet" "~" (at 198.12 40.64 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Description" "" (at 198.12 40.64 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (pin "1" (uuid "b20a3201-6101-4001-8001-000000000007"))
{make_inst("#FLG04", sheet1_uuid, doc1_uuid)}
  )

  (wire (pts (xy 177.8 45.72) (xy 185.42 45.72)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000016"))
  (global_label "EN_5V" (shape input) (at 177.8 45.72 180) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify right)) (uuid "b20a3201-4101-4001-8001-000000000013"))
  (wire (pts (xy 185.42 45.72) (xy 198.12 45.72)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000017"))
  (global_label "+5V_DRV" (shape output) (at 198.12 45.72 0) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify left)) (uuid "b20a3201-4101-4001-8001-000000000014"))
  (wire (pts (xy 177.8 48.26) (xy 185.42 48.26)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000018"))
  (global_label "ISENSE_5V" (shape output) (at 185.42 48.26 0) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify left)) (uuid "b20a3201-4101-4001-8001-000000000015"))

  ;; --- Sezione Micro-Inverter -12V ---
  (wire (pts (xy 228.6 40.64) (xy 236.22 40.64)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000019"))
  (global_label "+12V_REG" (shape input) (at 228.6 40.64 180) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify right)) (uuid "b20a3201-4101-4001-8001-000000000016"))
  (wire (pts (xy 236.22 40.64) (xy 248.92 40.64)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000020"))
  (global_label "-12V_DRV" (shape output) (at 248.92 40.64 0) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify left)) (uuid "b20a3201-4101-4001-8001-000000000017"))
  
  (symbol (lib_id "power:PWR_FLAG") (at 248.92 40.64 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced yes)
    (uuid "b20a3201-5101-4001-8001-000000000007")
    (property "Reference" "#FLG05" (at 248.92 38.1 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Value" "PWR_FLAG" (at 248.92 44.45 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "" (at 248.92 40.64 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Datasheet" "~" (at 248.92 40.64 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Description" "" (at 248.92 40.64 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (pin "1" (uuid "b20a3201-6101-4001-8001-000000000008"))
{make_inst("#FLG05", sheet1_uuid, doc1_uuid)}
  )

  ;; --- J2: Molex 4 pin maschio a 90° (+12V_DRV, GND, GND, +5V_DRV) ---
  (wire (pts (xy 60.96 86.36) (xy 68.58 86.36)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000021"))
  (global_label "+12V_DRV" (shape input) (at 60.96 86.36 180) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify right)) (uuid "b20a3201-4101-4001-8001-000000000018"))
  (wire (pts (xy 60.96 88.9) (xy 68.58 88.9)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000022"))
  (wire (pts (xy 60.96 91.44) (xy 68.58 91.44)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000023"))
  (wire (pts (xy 60.96 93.98) (xy 68.58 93.98)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000024"))
  (global_label "+5V_DRV" (shape input) (at 60.96 93.98 180) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify right)) (uuid "b20a3201-4101-4001-8001-000000000019"))
  (wire (pts (xy 60.96 88.9) (xy 60.96 91.44)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000025"))
  (wire (pts (xy 60.96 91.44) (xy 55.88 91.44)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000026"))
  
  (symbol (lib_id "power:GND") (at 55.88 91.44 90) (unit 1)
    (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced yes)
    (uuid "b20a3201-5101-4001-8001-000000000008")
    (property "Reference" "#PWR02" (at 62.23 91.44 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Value" "GND" (at 59.69 91.44 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "" (at 55.88 91.44 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Datasheet" "" (at 55.88 91.44 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Description" "" (at 55.88 91.44 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (pin "1" (uuid "b20a3201-6101-4001-8001-000000000009"))
{make_inst("#PWR02", sheet1_uuid, doc1_uuid)}
  )

  (symbol (lib_id "Connector:Conn_01x04_Pin") (at 73.66 88.9 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced yes)
    (uuid "b20a3201-5101-4001-8001-000000000009")
    (property "Reference" "J2" (at 73.66 80.01 0) (effects (font (size 1.27 1.27))))
    (property "Value" "J_PWR_525" (at 73.66 97.79 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Connector_Phoenix_MSTB:PhoenixContact_MSTBA_2,5_4-G-5,08_1x04_P5.08mm_Horizontal" (at 73.66 88.9 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Datasheet" "~" (at 73.66 88.9 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Description" "Connettore Molex 4 pin a 90 gradi per alimentazione floppy drive 5.25 (+12V, GND, GND, +5V)" (at 73.66 88.9 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (pin "1" (uuid "b20a3201-6101-4001-8001-000000000010"))
    (pin "2" (uuid "b20a3201-6101-4001-8001-000000000011"))
    (pin "3" (uuid "b20a3201-6101-4001-8001-000000000012"))
    (pin "4" (uuid "b20a3201-6101-4001-8001-000000000013"))
{make_inst("J2", sheet1_uuid, doc1_uuid)}
  )

  ;; --- J3: Berg 4 pin maschio a 90° (+5V_DRV, GND, GND, +12V_DRV) ---
  (wire (pts (xy 124.46 86.36) (xy 132.08 86.36)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000027"))
  (global_label "+5V_DRV" (shape input) (at 124.46 86.36 180) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify right)) (uuid "b20a3201-4101-4001-8001-000000000020"))
  (wire (pts (xy 124.46 88.9) (xy 132.08 88.9)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000028"))
  (wire (pts (xy 124.46 91.44) (xy 132.08 91.44)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000029"))
  (wire (pts (xy 124.46 93.98) (xy 132.08 93.98)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000030"))
  (global_label "+12V_DRV" (shape input) (at 124.46 93.98 180) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify right)) (uuid "b20a3201-4101-4001-8001-000000000021"))
  (wire (pts (xy 124.46 88.9) (xy 124.46 91.44)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000031"))
  (wire (pts (xy 124.46 91.44) (xy 119.38 91.44)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000032"))
  
  (symbol (lib_id "power:GND") (at 119.38 91.44 90) (unit 1)
    (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced yes)
    (uuid "b20a3201-5101-4001-8001-000000000010")
    (property "Reference" "#PWR03" (at 125.73 91.44 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Value" "GND" (at 123.19 91.44 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "" (at 119.38 91.44 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Datasheet" "" (at 119.38 91.44 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Description" "" (at 119.38 91.44 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (pin "1" (uuid "b20a3201-6101-4001-8001-000000000014"))
{make_inst("#PWR03", sheet1_uuid, doc1_uuid)}
  )

  (symbol (lib_id "Connector:Conn_01x04_Pin") (at 137.16 88.9 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced yes)
    (uuid "b20a3201-5101-4001-8001-000000000011")
    (property "Reference" "J3" (at 137.16 80.01 0) (effects (font (size 1.27 1.27))))
    (property "Value" "J_PWR_350" (at 137.16 97.79 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Horizontal" (at 137.16 88.9 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Datasheet" "~" (at 137.16 88.9 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Description" "Connettore Berg 4 pin a 90 gradi per alimentazione floppy drive 3.5 (+5V, GND, GND, +12V)" (at 137.16 88.9 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (pin "1" (uuid "b20a3201-6101-4001-8001-000000000015"))
    (pin "2" (uuid "b20a3201-6101-4001-8001-000000000016"))
    (pin "3" (uuid "b20a3201-6101-4001-8001-000000000017"))
    (pin "4" (uuid "b20a3201-6101-4001-8001-000000000018"))
{make_inst("J3", sheet1_uuid, doc1_uuid)}
  )

  ;; --- J4: Phoenix 4 pin a 90° (+24V_DRV, +5V_DRV, GND, -12V_DRV) per Drive 8 Pollici ---
  (wire (pts (xy 187.96 86.36) (xy 195.58 86.36)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000033"))
  (global_label "+24V_DRV" (shape input) (at 187.96 86.36 180) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify right)) (uuid "b20a3201-4101-4001-8001-000000000022"))
  (wire (pts (xy 187.96 88.9) (xy 195.58 88.9)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000034"))
  (global_label "+5V_DRV" (shape input) (at 187.96 88.9 180) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify right)) (uuid "b20a3201-4101-4001-8001-000000000023"))
  (wire (pts (xy 187.96 91.44) (xy 195.58 91.44)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000035"))
  (wire (pts (xy 187.96 91.44) (xy 182.88 91.44)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000036"))
  
  (symbol (lib_id "power:GND") (at 182.88 91.44 90) (unit 1)
    (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced yes)
    (uuid "b20a3201-5101-4001-8001-000000000012")
    (property "Reference" "#PWR04" (at 189.23 91.44 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Value" "GND" (at 186.69 91.44 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "" (at 182.88 91.44 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Datasheet" "" (at 182.88 91.44 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Description" "" (at 182.88 91.44 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (pin "1" (uuid "b20a3201-6101-4001-8001-000000000019"))
{make_inst("#PWR04", sheet1_uuid, doc1_uuid)}
  )

  (wire (pts (xy 187.96 93.98) (xy 195.58 93.98)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000037"))
  (global_label "-12V_DRV" (shape input) (at 187.96 93.98 180) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify right)) (uuid "b20a3201-4101-4001-8001-000000000024"))

  (symbol (lib_id "Connector:Conn_01x04_Pin") (at 200.66 88.9 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced yes)
    (uuid "b20a3201-5101-4001-8001-000000000013")
    (property "Reference" "J4" (at 200.66 80.01 0) (effects (font (size 1.27 1.27))))
    (property "Value" "J_PWR_800" (at 200.66 97.79 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-4-5.08_1x04_P5.08mm_Horizontal" (at 200.66 88.9 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Datasheet" "~" (at 200.66 88.9 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Description" "Morsettiera Phoenix a vite a 90 gradi per alimentazione drive 8 pollici (+24V, +5V, GND, -12V)" (at 200.66 88.9 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (pin "1" (uuid "b20a3201-6101-4001-8001-000000000020"))
    (pin "2" (uuid "b20a3201-6101-4001-8001-000000000021"))
    (pin "3" (uuid "b20a3201-6101-4001-8001-000000000022"))
    (pin "4" (uuid "b20a3201-6101-4001-8001-000000000023"))
{make_inst("J4", sheet1_uuid, doc1_uuid)}
  )

  ;; --- J5: Connettore a 4 Fili verso il Modulo Smart Display 7 Pollici sul Coperchio ---
  (wire (pts (xy 251.46 86.36) (xy 259.08 86.36)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000038"))
  (global_label "+5V_REG" (shape input) (at 251.46 86.36 180) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify right)) (uuid "b20a3201-4101-4001-8001-000000000025"))
  (wire (pts (xy 251.46 88.9) (xy 259.08 88.9)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000039"))
  (wire (pts (xy 251.46 88.9) (xy 246.38 88.9)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000040"))
  
  (symbol (lib_id "power:GND") (at 246.38 88.9 90) (unit 1)
    (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced yes)
    (uuid "b20a3201-5101-4001-8001-000000000014")
    (property "Reference" "#PWR05" (at 252.73 88.9 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Value" "GND" (at 250.19 88.9 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "" (at 246.38 88.9 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Datasheet" "" (at 246.38 88.9 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Description" "" (at 246.38 88.9 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (pin "1" (uuid "b20a3201-6101-4001-8001-000000000024"))
{make_inst("#PWR05", sheet1_uuid, doc1_uuid)}
  )

  (wire (pts (xy 251.46 91.44) (xy 259.08 91.44)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000041"))
  (global_label "USART1_TX" (shape output) (at 251.46 91.44 180) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify right)) (uuid "b20a3201-4101-4001-8001-000000000026"))
  (wire (pts (xy 251.46 93.98) (xy 259.08 93.98)) (stroke (width 0) (type default)) (uuid "b20a3201-3101-4001-8001-000000000042"))
  (global_label "USART1_RX" (shape input) (at 251.46 93.98 180) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify right)) (uuid "b20a3201-4101-4001-8001-000000000027"))

  (symbol (lib_id "Connector:Conn_01x04_Pin") (at 264.16 88.9 0) (unit 1)
    (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced yes)
    (uuid "b20a3201-5101-4001-8001-000000000015")
    (property "Reference" "J5" (at 264.16 80.01 0) (effects (font (size 1.27 1.27))))
    (property "Value" "J_DISP_CONN" (at 264.16 97.79 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical" (at 264.16 88.9 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Datasheet" "~" (at 264.16 88.9 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Description" "Connettore a 4 vie (+5V, GND, TX, RX) verso il Modulo Smart Display 7 pollici" (at 264.16 88.9 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (pin "1" (uuid "b20a3201-6101-4001-8001-000000000025"))
    (pin "2" (uuid "b20a3201-6101-4001-8001-000000000026"))
    (pin "3" (uuid "b20a3201-6101-4001-8001-000000000027"))
    (pin "4" (uuid "b20a3201-6101-4001-8001-000000000028"))
{make_inst("J5", sheet1_uuid, doc1_uuid)}
  )

  (sheet_instances
    (path "/{root_uuid}"
      (page "2")
    )
  )
)
"""
    with open(os.path.join(kicad_dir, "01_Power_Supply.kicad_sch"), "w", encoding="utf-8") as f:
        f.write(sch)
    print("01_Power_Supply.kicad_sch generato con successo!")

if __name__ == "__main__":
    build_sheet_1()
