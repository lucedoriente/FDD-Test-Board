import os, re
import pcbnew

prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
kicad_fp_dir = r"C:\Program Files\KiCad\9.0\share\kicad\footprints"

# Let's inspect J6 (USB-C) and IDC connectors orientation
def inspect_fp(lib, fpname):
    dirpath = os.path.join(kicad_fp_dir, f"{lib}.pretty")
    fp = pcbnew.FootprintLoad(dirpath, fpname)
    if not fp:
        print(f"FAILED to load {lib}:{fpname}")
        return
    bbox = fp.GetBoundingBox(True, True)
    print(f"\nFootprint {lib}:{fpname}:")
    print(f"  BBox: w={bbox.GetWidth()/1e6:.2f}mm, h={bbox.GetHeight()/1e6:.2f}mm")
    print(f"  Center: ({bbox.GetCenter().x/1e6:.2f}, {bbox.GetCenter().y/1e6:.2f})")
    # check pads
    for p in list(fp.Pads())[:4]:
        pos = p.GetPosition()
        print(f"  Pad {p.GetNumber()}: ({pos.x/1e6:.2f}, {pos.y/1e6:.2f})")

inspect_fp("Connector_USB", "USB_C_Receptacle_HRO_TYPE-C-31-M-12")
inspect_fp("Connector_IDC", "IDC-Header_2x17_P2.54mm_Horizontal")
inspect_fp("TerminalBlock_Phoenix", "TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal")
