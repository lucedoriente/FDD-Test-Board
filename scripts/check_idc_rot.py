import pcbnew, os

kicad_fp_dir = r"C:\Program Files\KiCad\9.0\share\kicad\footprints"
fp = pcbnew.FootprintLoad(os.path.join(kicad_fp_dir, "Connector_IDC.pretty"), "IDC-Header_2x17_P2.54mm_Horizontal")

for rot in [0, 90, 180, 270]:
    fp.SetOrientation(pcbnew.EDA_ANGLE(rot, pcbnew.DEGREES_T))
    pads = list(fp.Pads())
    pad_y = sum(p.GetPosition().y/1e6 for p in pads) / len(pads)
    full_bbox = fp.GetBoundingBox(True, True)
    center_y = full_bbox.GetCenter().y/1e6
    # If shroud is facing negative Y (towards rear top of board), center_y should be LESS than pad_y (closer to Y=0)!
    print(f"Rot {rot:3d}: Pads Center Y = {pad_y:6.2f}, Shroud Center Y = {center_y:6.2f}, Opening direction = {'UP (-Y, REAR)' if center_y < pad_y else 'DOWN (+Y, FRONT)'}")
