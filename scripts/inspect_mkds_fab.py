import pcbnew, os

kicad_fp_dir = r"C:\Program Files\KiCad\9.0\share\kicad\footprints"
fp = pcbnew.FootprintLoad(os.path.join(kicad_fp_dir, "TerminalBlock_Phoenix.pretty"), "TerminalBlock_Phoenix_MKDS-1,5-4-5.08_1x04_P5.08mm_Horizontal")

for g in fp.GraphicalItems():
    if g.GetLayerName() == "F.Fab":
        print(f"Fab item {g.GetShapeStr()}: start=({g.GetStart().x/1e6:.1f}, {g.GetStart().y/1e6:.1f}) end=({g.GetEnd().x/1e6:.1f}, {g.GetEnd().y/1e6:.1f})")
