import pcbnew, os

kicad_fp_dir = r"C:\Program Files\KiCad\9.0\share\kicad\footprints"
fp = pcbnew.FootprintLoad(os.path.join(kicad_fp_dir, "Connector_PinHeader_2.54mm.pretty"), "PinHeader_1x04_P2.54mm_Horizontal")

for rot in [0, 90, 180, 270]:
    fp.SetOrientation(pcbnew.EDA_ANGLE(rot, pcbnew.DEGREES_T))
    fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(100.0), pcbnew.FromMM(50.0)))
    bb = fp.GetBoundingBox(False, False)
    print(f"Rot {rot}: X=[{bb.GetLeft()/1e6:.1f}, {bb.GetRight()/1e6:.1f}], Y=[{bb.GetTop()/1e6:.1f}, {bb.GetBottom()/1e6:.1f}]")
