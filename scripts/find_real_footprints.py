import os, glob

fp_dir = r"C:\Program Files\KiCad\9.0\share\kicad\footprints"

# Find Molex 4-pin footprints
molex_fps = glob.glob(os.path.join(fp_dir, "Connector_Molex.pretty", "*1x04*.kicad_mod"))
print("Molex 1x04 footprints:")
for f in molex_fps[:10]:
    print(" ", os.path.basename(f).replace(".kicad_mod", ""))

# Find 4-pin pin headers or Phoenix terminal blocks
conn_fps = glob.glob(os.path.join(fp_dir, "TerminalBlock_Phoenix.pretty", "*MKDS*1x04*.kicad_mod"))
print("\nPhoenix MKDS 1x04 footprints:")
for f in conn_fps[:10]:
    print(" ", os.path.basename(f).replace(".kicad_mod", ""))

# Find Berg / Floppy power
te_fps = glob.glob(os.path.join(fp_dir, "Connector_TE-Connectivity.pretty", "*1x04*.kicad_mod"))
print("\nTE 1x04 footprints:")
for f in te_fps[:10]:
    print(" ", os.path.basename(f).replace(".kicad_mod", ""))

hdr_fps = glob.glob(os.path.join(fp_dir, "Connector_PinHeader_2.54mm.pretty", "*1x04*.kicad_mod"))
print("\nPinHeader 2.54mm 1x04 footprints:")
for f in hdr_fps[:5]:
    print(" ", os.path.basename(f).replace(".kicad_mod", ""))
