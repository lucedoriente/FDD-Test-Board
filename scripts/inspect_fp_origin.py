import pcbnew, os

kicad_fp_dir = r"C:\Program Files\KiCad\9.0\share\kicad\footprints"

def test_origin_and_box(lib, fpname, rot):
    fp = pcbnew.FootprintLoad(os.path.join(kicad_fp_dir, f"{lib}.pretty"), fpname)
    fp.SetOrientation(pcbnew.EDA_ANGLE(rot, pcbnew.DEGREES_T))
    fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(100.0), pcbnew.FromMM(50.0)))
    bb = fp.GetBoundingBox(False, False)
    print(f"{fpname} at (100, 50), rot={rot}:")
    print(f"  X span: [{bb.GetLeft()/1e6:.1f}, {bb.GetRight()/1e6:.1f}] (width={bb.GetWidth()/1e6:.1f})")
    print(f"  Y span: [{bb.GetTop()/1e6:.1f}, {bb.GetBottom()/1e6:.1f}] (height={bb.GetHeight()/1e6:.1f})")

test_origin_and_box("Connector_IDC", "IDC-Header_2x25_P2.54mm_Horizontal", 90)
test_origin_and_box("Connector_IDC", "IDC-Header_2x17_P2.54mm_Horizontal", 90)
test_origin_and_box("Connector_IDC", "IDC-Header_2x13_P2.54mm_Horizontal", 90)
test_origin_and_box("Connector_IDC", "IDC-Header_2x10_P2.54mm_Horizontal", 90)
test_origin_and_box("TerminalBlock_Phoenix", "TerminalBlock_Phoenix_MKDS-1,5-4-5.08_1x04_P5.08mm_Horizontal", 180)
test_origin_and_box("TerminalBlock_Phoenix", "TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal", 180)
