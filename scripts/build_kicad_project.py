import os
import uuid
import json

base_kicad = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"

# 1. Creazione FDD-Test-Board.kicad_pro
pro_content = {
  "board": {
    "3dviewports": [],
    "design_settings": {
      "defaults": {
        "apply_defaults_to_fp_fields": False,
        "apply_defaults_to_fp_shapes": False,
        "apply_defaults_to_fp_text": False,
        "board_outline_line_width": 0.1,
        "copper_line_width": 0.25,
        "copper_text_italic": False,
        "copper_text_size_h": 1.5,
        "copper_text_size_v": 1.5,
        "copper_text_thickness": 0.3,
        "copper_text_upright": False,
        "courtyard_line_width": 0.05,
        "dimension_precision": 4,
        "dimension_units": 3,
        "fab_line_width": 0.1,
        "silk_line_width": 0.15,
        "silk_text_size_h": 1.0,
        "silk_text_size_v": 1.0,
        "silk_text_thickness": 0.15
      },
      "rules": {
        "min_clearance": 0.15,
        "min_copper_edge_clearance": 0.3,
        "min_hole_clearance": 0.2,
        "min_hole_to_hole": 0.25,
        "min_through_hole_annular_ring": 0.15,
        "min_track_width": 0.18
      }
    },
    "layer_presets": []
  },
  "boards": [],
  "cvpcb": {
    "equivalence_files": []
  },
  "erc": {
    "erc_exclusions": [],
    "meta": {
      "version": 0
    },
    "rule_severities": {
      "bus_label_syntax": "error",
      "bus_to_bus_conflict": "error",
      "bus_to_net_conflict": "error",
      "conflicting_netclasses": "error",
      "different_unit_footprint": "error",
      "different_unit_net": "error",
      "duplicate_reference": "error",
      "duplicate_sheet_names": "error",
      "endpoint_off_grid": "warning",
      "extra_units": "error",
      "global_label_dangling": "error",
      "hier_label_mismatch": "error",
      "label_dangling": "error",
      "lib_symbol_issues": "error",
      "missing_bidi_pin": "warning",
      "missing_power_pin": "error",
      "missing_unit": "warning",
      "multiple_net_names": "warning",
      "net_not_bus_member": "error",
      "no_connect_connected": "error",
      "no_connect_dangling": "warning",
      "pin_not_connected": "error",
      "pin_not_driven": "error",
      "pin_to_pin": "error",
      "power_pin_not_driven": "error",
      "similar_labels": "warning",
      "simulation_model_issue": "ignore",
      "unannotated": "error",
      "unit_value_mismatch": "error",
      "unresolved_variable": "error",
      "wire_dangling": "error"
    }
  },
  "libraries": {
    "pinned_footprint_libs": [],
    "pinned_symbol_libs": []
  },
  "meta": {
    "filename": "FDD-Test-Board.kicad_pro",
    "version": 1
  },
  "net_settings": {
    "classes": [
      {
        "bus_width": 12,
        "clearance": 0.15,
        "diff_pair_gap": 0.25,
        "diff_pair_via_gap": 0.25,
        "diff_pair_width": 0.2,
        "line_style": 0,
        "microvia_diameter": 0.3,
        "microvia_drill": 0.1,
        "name": "Default",
        "pcb_color": "rgba(0, 0, 0, 0.000)",
        "schematic_color": "rgba(0, 0, 0, 0.000)",
        "track_width": 0.25,
        "via_diameter": 0.8,
        "via_drill": 0.4,
        "wire_width": 0
      },
      {
        "clearance": 0.25,
        "name": "Power_HighCurrent",
        "track_width": 0.8,
        "via_diameter": 1.2,
        "via_drill": 0.6
      }
    ],
    "meta": {
      "version": 3
    },
    "net_colors": None
  },
  "pcbnew": {
    "last_paths": {
      "gencad": "",
      "idf": "",
      "netlist": "",
      "plot": "",
      "pos": "",
      "specctra_dsn": "",
      "step": "",
      "svg": "",
      "vrml": ""
    }
  },
  "schematic": {
    "legacy_lib_dir": "",
    "legacy_lib_list": []
  },
  "sheets": [
    [
      "b20a3201-1001-4001-8001-000000000001",
      ""
    ]
  ],
  "text_variables": {}
}

with open(os.path.join(base_kicad, "FDD-Test-Board.kicad_pro"), "w", encoding="utf-8") as f:
    json.dump(pro_content, f, indent=2)

print("FDD-Test-Board.kicad_pro salvato correttamente.")
