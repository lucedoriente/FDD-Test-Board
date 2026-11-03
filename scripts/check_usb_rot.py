import pcbnew, os

kicad_fp_dir = r"C:\Program Files\KiCad\9.0\share\kicad\footprints"
fp = pcbnew.FootprintLoad(os.path.join(kicad_fp_dir, "Connector_USB.pretty"), "USB_C_Receptacle_HRO_TYPE-C-31-M-12")

for rot in [0, 90, 180, 270]:
    fp.SetOrientation(pcbnew.EDA_ANGLE(rot, pcbnew.DEGREES_T))
    pads = list(fp.Pads())
    pad_x = sum(p.GetPosition().x/1e6 for p in pads) / len(pads)
    full_bbox = fp.GetBoundingBox(True, True)
    center_x = full_bbox.GetCenter().x/1e6
    # In USB-C receptacle, the mating mouth extends towards the plug
    # At rot=0, pins are at Y < 0, mouth is at Y > 0
    print(f"Rot {rot:3d}: Pads Center X = {pad_x:6.2f}, Center X = {center_x:6.2f}")
