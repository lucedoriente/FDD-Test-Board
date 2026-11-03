import os

kicad_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"

sym_lib_content = """(sym_lib_table
  (version 7)
  (lib (name "FDD-Test-Board")(type "KiCad")(uri "${KIPRJMOD}/FDD-Test-Board.kicad_sym")(options "")(descr "Libreria simboli di progetto Retro-Diag FDD-Test-Board"))
)
"""

fp_lib_content = """(fp_lib_table
  (version 7)
  (lib (name "FDD-Test-Board")(type "KiCad")(uri "${KIPRJMOD}/FDD-Test-Board.pretty")(options "")(descr "Libreria impronte di progetto Retro-Diag FDD-Test-Board"))
)
"""

with open(os.path.join(kicad_dir, "sym-lib-table"), "w", encoding="utf-8") as f:
    f.write(sym_lib_content)

with open(os.path.join(kicad_dir, "fp-lib-table"), "w", encoding="utf-8") as f:
    f.write(fp_lib_content)

# Inizializziamo anche la libreria simboli vuota valida KiCad 9
kicad_sym_path = os.path.join(kicad_dir, "FDD-Test-Board.kicad_sym")
if not os.path.exists(kicad_sym_path):
    with open(kicad_sym_path, "w", encoding="utf-8") as f:
        f.write('(kicad_symbol_lib (version 20231120) (generator "kicad_symbol_editor")\n)\n')

print("Progetto KiCad 9 inizializzato correttamente con sym-lib-table e fp-lib-table!")
