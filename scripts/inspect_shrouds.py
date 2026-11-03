import pcbnew
import os

kicad_fp_dir = r"C:\Program Files\KiCad\9.0\share\kicad\footprints"

def test_fp_shroud(lib, fpname):
    dirpath = os.path.join(kicad_fp_dir, f"{lib}.pretty")
    fp = pcbnew.FootprintLoad(dirpath, fpname)
    print(f"\n=== {fpname} ===")
    pads = list(fp.Pads())
    pad_xs = [p.GetPosition().x/1e6 for p in pads]
    pad_ys = [p.GetPosition().y/1e6 for p in pads]
    print(f"Pads range: X=[{min(pad_xs):.2f}, {max(pad_xs):.2f}], Y=[{min(pad_ys):.2f}, {max(pad_ys):.2f}]")
    
    # Check graphical elements (lines/courtyards)
    cy_pts_x = []
    cy_pts_y = []
    for g in fp.GraphicalItems():
        if g.GetLayer() in (pcbnew.F_SilkS, pcbnew.F_Fab, pcbnew.F_CrtYd):
            bbox = g.GetBoundingBox()
            cy_pts_x.extend([bbox.GetLeft()/1e6, bbox.GetRight()/1e6])
            cy_pts_y.extend([bbox.GetTop()/1e6, bbox.GetBottom()/1e6])
    if cy_pts_x:
        print(f"Body range: X=[{min(cy_pts_x):.2f}, {max(cy_pts_x):.2f}], Y=[{min(cy_pts_y):.2f}, {max(cy_pts_y):.2f}]")

test_fp_shroud("Connector_IDC", "IDC-Header_2x17_P2.54mm_Horizontal")
test_fp_shroud("Connector_IDC", "IDC-Header_2x25_P2.54mm_Horizontal")
test_fp_shroud("Connector_IDC", "IDC-Header_2x13_P2.54mm_Horizontal")
test_fp_shroud("Connector_IDC", "IDC-Header_2x10_P2.54mm_Horizontal")
test_fp_shroud("Connector_USB", "USB_C_Receptacle_HRO_TYPE-C-31-M-12")
test_fp_shroud("TerminalBlock_Phoenix", "TerminalBlock_Phoenix_MKDS-1,5-4-5.08_1x04_P5.08mm_Horizontal")
test_fp_shroud("TerminalBlock_Phoenix", "TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal")
test_fp_shroud("Connector_Coaxial", "SMA_Amphenol_132134-10_Vertical")
