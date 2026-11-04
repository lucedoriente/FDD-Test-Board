"""
=============================================================================
FDD TESTER & EXERCISER - Parametric 3D CAD Enclosure Generator for FreeCAD
Author: Alessio Iodice <alessio67@gmail.com>
True Operator Frame of Reference:
  - Origin (0,0,0) at Front-Left Corner (Operator's Left Hand, Front Palm Rest)
  - X: 0 to 320 mm (Left to Right: Left=PSU, Right=PCB)
  - Y: 0 to 185 mm (Front to Rear: Front=40mm low, Rear=70mm high)
  - Z: 0 to 40mm at Front (Y=0), sloping UP to 70mm at Rear (Y=185)
Features:
  - 5 Lightweight Ribbed Bosses for Hood Fastening (Low Material Volume, Anti-Warp)
  - 7 PCB Standoffs (H1..H7, including H7 extraction strain relief between IDC-34/50)
  - 2.5 mm pilot holes for M3 self-tapping / tapping
=============================================================================
"""

import os
import math
import FreeCAD
import Part
import Import
import MeshPart

def generate_lightweight_case():
    print(">>> Generating Lightweight Enclosure Assembly for FreeCAD...")
    doc = FreeCAD.newDocument("FDD_Tester_Case")
    
    # -------------------------------------------------------------------------
    # PARAMETRIC CONSTANTS (mm)
    # -------------------------------------------------------------------------
    CASE_W = 320.0       # External Width (X)
    CASE_D = 185.0       # External Depth (Y)
    CASE_H_FRONT = 40.0  # Front Min Height (Z at Y=0)
    CASE_H_REAR = 70.0   # Rear Max Height  (Z at Y=185)
    WALL_T = 3.0         # Wall thickness
    BASE_T = 3.0         # Base plate thickness
    LIP_H = 4.0          # Guide lip height
    LIP_T = 1.5          # Guide lip thickness
    LIP_CLEAR = 0.25     # Tolerance clearance
    
    # PCB Offsets inside base tray
    PCB_X0 = 116.0
    PCB_Y_REAR = 181.0
    PCB_STANDOFF_H = 8.0
    PCB_T = 1.6
    Z_PCB_TOP = BASE_T + PCB_STANDOFF_H + PCB_T # 12.6 mm
    
    PILOT_HOLE_R = 1.25      # Dia 2.50 mm (M3 self-tapping / threading)
    CLEARANCE_HOLE_R = 1.7   # Dia 3.40 mm (M3 clearance pass-through)
    
    BOSS_R = 3.75            # Outer Dia 7.50 mm for hood bosses
    BOSS_H = 14.0            # Height 14.0 mm (adequate for 12mm thread engagement)
    RIB_W = 2.0              # Rib thickness 2.0 mm
    
    SLOPE_ANG = math.atan2(CASE_H_REAR - CASE_H_FRONT, CASE_D) # ~9.21 deg
    
    # -------------------------------------------------------------------------
    # 1. BASE TRAY GEOMETRY (Bottom Chassis Plate)
    # -------------------------------------------------------------------------
    print(">>> 1. Base Tray (Lower Chassis Plate)...")
    base_plate = Part.makeBox(CASE_W, CASE_D, BASE_T, FreeCAD.Vector(0, 0, 0))
    
    # Interlocking Guide Lip on perimeter
    lip_outer = Part.makeBox(
        CASE_W - 2 * (WALL_T + LIP_CLEAR),
        CASE_D - 2 * (WALL_T + LIP_CLEAR),
        LIP_H,
        FreeCAD.Vector(WALL_T + LIP_CLEAR, WALL_T + LIP_CLEAR, BASE_T)
    )
    lip_inner = Part.makeBox(
        CASE_W - 2 * (WALL_T + LIP_CLEAR + LIP_T),
        CASE_D - 2 * (WALL_T + LIP_CLEAR + LIP_T),
        LIP_H + 1.0,
        FreeCAD.Vector(WALL_T + LIP_CLEAR + LIP_T, WALL_T + LIP_CLEAR + LIP_T, BASE_T - 0.5)
    )
    lip = lip_outer.cut(lip_inner)
    
    # Clear corners of the lip so hood bosses seat flush on base plate
    c_fl = Part.makeBox(20.0, 20.0, LIP_H + 2.0, FreeCAD.Vector(0, 0, BASE_T - 0.5))
    c_rl = Part.makeBox(20.0, 20.0, LIP_H + 2.0, FreeCAD.Vector(0, CASE_D - 20.0, BASE_T - 0.5))
    c_fr = Part.makeBox(20.0, 20.0, LIP_H + 2.0, FreeCAD.Vector(CASE_W - 20.0, 0, BASE_T - 0.5))
    c_rr = Part.makeBox(20.0, 20.0, LIP_H + 2.0, FreeCAD.Vector(CASE_W - 20.0, CASE_D - 20.0, BASE_T - 0.5))
    c_part = Part.makeBox(16.0, 20.0, LIP_H + 2.0, FreeCAD.Vector(83.0, CASE_D - 20.0, BASE_T - 0.5))
    lip = lip.cut(c_fl).cut(c_rl).cut(c_fr).cut(c_rr).cut(c_part)
    base_tray = base_plate.fuse(lip)
    
    # Internal Partition Wall (Separates Left PSU and Right Logic PCB)
    partition = Part.makeBox(2.5, CASE_D - 2 * (WALL_T + LIP_CLEAR + LIP_T), 35.0,
                            FreeCAD.Vector(90.0, WALL_T + LIP_CLEAR + LIP_T, BASE_T))
    p_notch = Part.makeBox(10.0, 30.0, 16.0, FreeCAD.Vector(86.0, 80.0, BASE_T))
    partition = partition.cut(p_notch)
    base_tray = base_tray.fuse(partition)
    
    # -------------------------------------------------------------------------
    # 2. PCB STANDOFFS (7x Bosses on Base Tray)
    # -------------------------------------------------------------------------
    print(">>> 2. PCB Standoffs (7x Bosses: H1, H2, H3, H4, H5, H6, H7)...")
    pcb_standard_mounts = [
        (PCB_X0 + 5.0,   PCB_Y_REAR - 5.0),   # H1 (Rear Left)
        (PCB_X0 + 114.0, PCB_Y_REAR - 24.0),  # H7 (Rear Center - IDC strain relief)
        (PCB_X0 + 195.0, PCB_Y_REAR - 101.0), # H6 (Right Edge)
        (PCB_X0 + 195.0, PCB_Y_REAR - 135.0), # H3 (Front Right)
        (PCB_X0 + 100.0, PCB_Y_REAR - 135.0), # H5 (Front Center)
        (PCB_X0 + 5.0,   PCB_Y_REAR - 135.0)  # H4 (Front Left)
    ]
    
    # 6 Standard PCB standoffs: Dia 7.0mm, Height 8.0mm, Pilot Hole 2.5mm deep 7.5mm
    for hx, hy in pcb_standard_mounts:
        b_cyl = Part.makeCylinder(3.5, PCB_STANDOFF_H, FreeCAD.Vector(hx, hy, BASE_T))
        b_hole = Part.makeCylinder(PILOT_HOLE_R, PCB_STANDOFF_H + 1.0, FreeCAD.Vector(hx, hy, BASE_T + 1.0))
        boss = b_cyl.cut(b_hole)
        base_tray = base_tray.fuse(boss)
        
    # H2 Standoff: Dia 7.0mm, Height 8.0mm, Through-Hole 3.4mm (for Hood screw pass-through)
    h2_x = PCB_X0 + 195.0 # 311.0
    h2_y = PCB_Y_REAR - 5.0 # 176.0
    h2_cyl = Part.makeCylinder(3.5, PCB_STANDOFF_H, FreeCAD.Vector(h2_x, h2_y, BASE_T))
    h2_through = Part.makeCylinder(CLEARANCE_HOLE_R, PCB_STANDOFF_H + 2.0, FreeCAD.Vector(h2_x, h2_y, BASE_T - 1.0))
    h2_boss = h2_cyl.cut(h2_through)
    base_tray = base_tray.fuse(h2_boss)
    
    # PSU Mount Bosses (Left compartment)
    psu_mounts = [(15.0, 50.0), (75.0, 50.0), (15.0, 140.0), (75.0, 140.0)]
    for px, py in psu_mounts:
        psu_cyl = Part.makeCylinder(3.5, 4.0, FreeCAD.Vector(px, py, BASE_T))
        psu_hole = Part.makeCylinder(PILOT_HOLE_R, 5.0, FreeCAD.Vector(px, py, BASE_T + 0.5))
        psu_boss = psu_cyl.cut(psu_hole)
        base_tray = base_tray.fuse(psu_boss)
        
    # Bottom Intake Ventilation Slots for PSU
    for i in range(10):
        bslot = Part.makeBox(3.0, 45.0, BASE_T * 3, FreeCAD.Vector(25.0 + (i % 5) * 11.0, 55.0 + (i // 5) * 55.0, -BASE_T))
        base_tray = base_tray.cut(bslot)
        
    # -------------------------------------------------------------------------
    # 3. HOOD FASTENING COUNTERSUNK HOLES IN BASE TRAY
    # -------------------------------------------------------------------------
    hood_screws = [
        (10.0, 10.0),    # V1: Front Left Corner
        (10.0, 175.0),   # V2: Rear Left Corner
        (310.0, 10.0),   # V3: Front Right Corner
        (311.0, 176.0),  # V4: Rear Right Corner (Coaxial with H2)
        (91.25, 175.0)   # V5: Rear Partition Center
    ]
    for vx, vy in hood_screws:
        v_hole = Part.makeCylinder(CLEARANCE_HOLE_R, BASE_T * 3, FreeCAD.Vector(vx, vy, -BASE_T))
        v_csink = Part.makeCone(3.1, CLEARANCE_HOLE_R, 1.5, FreeCAD.Vector(vx, vy, 0))
        base_tray = base_tray.cut(v_hole).cut(v_csink)

    # -------------------------------------------------------------------------
    # 4. UPPER CONSOLE HOOD GEOMETRY
    # -------------------------------------------------------------------------
    print(">>> 3. Upper Console Hood...")
    pts_outer = [
        FreeCAD.Vector(0, 0, 0),
        FreeCAD.Vector(0, CASE_D, 0),
        FreeCAD.Vector(0, CASE_D, CASE_H_REAR),
        FreeCAD.Vector(0, 0, CASE_H_FRONT),
        FreeCAD.Vector(0, 0, 0)
    ]
    wire_outer = Part.makePolygon(pts_outer)
    face_outer = Part.Face(wire_outer)
    hood_outer = face_outer.extrude(FreeCAD.Vector(CASE_W, 0, 0))
    
    pts_inner = [
        FreeCAD.Vector(WALL_T, WALL_T, -1.0),
        FreeCAD.Vector(WALL_T, CASE_D - WALL_T, -1.0),
        FreeCAD.Vector(WALL_T, CASE_D - WALL_T, CASE_H_REAR - WALL_T / math.cos(SLOPE_ANG)),
        FreeCAD.Vector(WALL_T, WALL_T, CASE_H_FRONT - WALL_T / math.cos(SLOPE_ANG)),
        FreeCAD.Vector(WALL_T, WALL_T, -1.0)
    ]
    wire_inner = Part.makePolygon(pts_inner)
    face_inner = Part.Face(wire_inner)
    hood_cavity = face_inner.extrude(FreeCAD.Vector(CASE_W - 2 * WALL_T, 0, 0))
    
    upper_hood = hood_outer.cut(hood_cavity)
    
    # -------------------------------------------------------------------------
    # 5. LIGHTWEIGHT RIBBED BOSSES (Ultra-Low Volume, Anti-Warp, Zero Floating)
    # -------------------------------------------------------------------------
    print(">>> 4. Adding 5 Lightweight Ribbed Screw Bosses to Hood...")
    def make_ribbed_boss(cx, cy, cz, rib_dirs):
        cyl = Part.makeCylinder(BOSS_R, BOSS_H, FreeCAD.Vector(cx, cy, cz))
        shapes = [cyl]
        for d in rib_dirs:
            if d == '-X': # towards left wall
                rx = Part.makeBox(cx - 1.5, RIB_W, BOSS_H, FreeCAD.Vector(1.5, cy - RIB_W/2.0, cz))
                shapes.append(rx)
            elif d == '+X': # towards right wall
                rx = Part.makeBox(CASE_W - cx - 1.5, RIB_W, BOSS_H, FreeCAD.Vector(cx, cy - RIB_W/2.0, cz))
                shapes.append(rx)
            elif d == '-Y': # towards front wall
                ry = Part.makeBox(RIB_W, cy - 1.5, BOSS_H, FreeCAD.Vector(cx - RIB_W/2.0, 1.5, cz))
                shapes.append(ry)
            elif d == '+Y': # towards rear wall
                ry = Part.makeBox(RIB_W, CASE_D - cy - 1.5, BOSS_H, FreeCAD.Vector(cx - RIB_W/2.0, cy, cz))
                shapes.append(ry)
        compound = shapes[0]
        for s in shapes[1:]:
            compound = compound.fuse(s)
        hole = Part.makeCylinder(PILOT_HOLE_R, 12.0, FreeCAD.Vector(cx, cy, cz - 0.5))
        return compound.cut(hole)

    b1 = make_ribbed_boss(10.0, 10.0, 0.0, ['-X', '-Y'])
    b2 = make_ribbed_boss(10.0, 175.0, 0.0, ['-X', '+Y'])
    b3 = make_ribbed_boss(310.0, 10.0, 0.0, ['+X', '-Y'])
    b4 = make_ribbed_boss(311.0, 176.0, Z_PCB_TOP, ['+X', '+Y'])
    b5 = make_ribbed_boss(91.25, 175.0, 0.0, ['+Y'])

    bosses = b1.fuse(b2).fuse(b3).fuse(b4).fuse(b5)
    upper_hood = upper_hood.fuse(bosses)
    print(f"    * Total Volume of 5 Bosses: {bosses.Volume / 1000.0:.2f} cm3 (Optimized for JLCPCB)")

    # -------------------------------------------------------------------------
    # 6. OPEN-BOTTOM "U" CUTOUTS - REAR PANEL (Y = 185 mm)
    # -------------------------------------------------------------------------
    print(">>> 5. Open-Bottom 'U' Slots on Rear Panel...")
    iec_cut = Part.makeBox(48.0, WALL_T * 3, 28.0, FreeCAD.Vector(24.0, CASE_D - WALL_T * 2, 21.0))
    iec_h1 = Part.makeCylinder(1.7, WALL_T * 3, FreeCAD.Vector(14.0, CASE_D - WALL_T * 2, 35.0), FreeCAD.Vector(0, 1, 0))
    iec_h2 = Part.makeCylinder(1.7, WALL_T * 3, FreeCAD.Vector(82.0, CASE_D - WALL_T * 2, 35.0), FreeCAD.Vector(0, 1, 0))
    upper_hood = upper_hood.cut(iec_cut).cut(iec_h1).cut(iec_h2)
    
    j6_u = Part.makeBox(12.0, WALL_T * 3, 18.0, FreeCAD.Vector(PCB_X0 + 16.5 - 6.0, CASE_D - WALL_T * 2, -1.0))
    upper_hood = upper_hood.cut(j6_u)
    
    j2_u = Part.makeBox(22.0, WALL_T * 3, 23.5, FreeCAD.Vector(PCB_X0 + 43.0 - 11.0, CASE_D - WALL_T * 2, -1.0))
    upper_hood = upper_hood.cut(j2_u)
    
    j3_u = Part.makeBox(16.0, WALL_T * 3, 21.5, FreeCAD.Vector(PCB_X0 + 52.0 - 8.0, CASE_D - WALL_T * 2, -1.0))
    upper_hood = upper_hood.cut(j3_u)
    
    j11_u = Part.makeBox(54.0, WALL_T * 3, 24.0, FreeCAD.Vector(PCB_X0 + 67.5 - 27.0, CASE_D - WALL_T * 2, -1.0))
    upper_hood = upper_hood.cut(j11_u)
    
    j10_u = Part.makeBox(74.0, WALL_T * 3, 24.0, FreeCAD.Vector(PCB_X0 + 120.0 - 37.0, CASE_D - WALL_T * 2, -1.0))
    upper_hood = upper_hood.cut(j10_u)

    # -------------------------------------------------------------------------
    # 7. OPEN-BOTTOM "U" CUTOUTS - RIGHT SIDE PANEL (X = CASE_W = 320 mm)
    # -------------------------------------------------------------------------
    print(">>> 6. Open-Bottom 'U' Slots on Right Side Panel...")
    j12_u = Part.makeBox(WALL_T * 3, 43.0, 24.0, FreeCAD.Vector(CASE_W - WALL_T * 2, (PCB_Y_REAR - 22.0) - 21.5, -1.0))
    upper_hood = upper_hood.cut(j12_u)
    
    j13_u = Part.makeBox(WALL_T * 3, 35.0, 24.0, FreeCAD.Vector(CASE_W - WALL_T * 2, (PCB_Y_REAR - 66.0) - 17.5, -1.0))
    upper_hood = upper_hood.cut(j13_u)
    
    j4_u = Part.makeBox(WALL_T * 3, 22.0, 23.0, FreeCAD.Vector(CASE_W - WALL_T * 2, (PCB_Y_REAR - 110.0) - 11.0, -1.0))
    upper_hood = upper_hood.cut(j4_u)
    
    j14_u = Part.makeBox(WALL_T * 3, 17.0, 22.0, FreeCAD.Vector(CASE_W - WALL_T * 2, (PCB_Y_REAR - 124.0) - 8.5, -1.0))
    upper_hood = upper_hood.cut(j14_u)

    # -------------------------------------------------------------------------
    # 8. LEFT PANEL COOLING SLOTS (PSU Compartment)
    # -------------------------------------------------------------------------
    print(">>> 7. Left Panel Cooling Slots...")
    for i in range(8):
        slot_y = 50.0 + i * 12.0
        side_slot = Part.makeBox(WALL_T * 3, 35.0, 3.5, FreeCAD.Vector(-WALL_T, slot_y, 16.0))
        upper_hood = upper_hood.cut(side_slot)

    # -------------------------------------------------------------------------
    # 9. DISPLAY & DAUGHTERBOARD INTEGRATION ON INCLINED CONSOLE ROOF
    # -------------------------------------------------------------------------
    print(">>> 8. Display & UI Controls on Sloped Roof...")
    deg_ang = math.degrees(SLOPE_ANG)
    
    DISP_X0 = 160.0 - 154.0 / 2.0  # 83.0 mm
    DISP_Y_SLOPE = 75.0
    disp_cut_box = Part.makeBox(154.0, 86.0, 25.0, FreeCAD.Vector(DISP_X0, DISP_Y_SLOPE, -12.0))
    disp_recess_box = Part.makeBox(182.0, 109.0, 2.5, FreeCAD.Vector(160.0 - 91.0, DISP_Y_SLOPE - 11.5, -2.5))
    for cut_tool in [disp_cut_box, disp_recess_box]:
        cut_tool.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), deg_ang)
        cut_tool.translate(FreeCAD.Vector(0, 0, CASE_H_FRONT))
        upper_hood = upper_hood.cut(cut_tool)
        
    UI_X0 = 160.0
    UI_Y_SLOPE = 18.0
    enc_x = UI_X0 + 72.0
    enc_y = UI_Y_SLOPE + 16.5
    enc_cyl = Part.makeCylinder(3.75, 25.0, FreeCAD.Vector(enc_x, enc_y, -12.0))
    enc_cyl.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), deg_ang)
    enc_cyl.translate(FreeCAD.Vector(0, 0, CASE_H_FRONT))
    upper_hood = upper_hood.cut(enc_cyl)
    
    btn_x_list = [UI_X0 + 15.0, UI_X0 + 33.0, UI_X0 + 51.0]
    for bx in btn_x_list:
        btn_cyl = Part.makeCylinder(3.5, 25.0, FreeCAD.Vector(bx, UI_Y_SLOPE + 24.0, -12.0))
        btn_cyl.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), deg_ang)
        btn_cyl.translate(FreeCAD.Vector(0, 0, CASE_H_FRONT))
        upper_hood = upper_hood.cut(btn_cyl)
        
    led_x_list = [UI_X0 + 16.0, UI_X0 + 26.0, UI_X0 + 36.0, UI_X0 + 46.0, UI_X0 + 56.0]
    for lx in led_x_list:
        led_cyl = Part.makeCylinder(1.6, 25.0, FreeCAD.Vector(lx, UI_Y_SLOPE + 10.0, -12.0))
        led_cyl.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), deg_ang)
        led_cyl.translate(FreeCAD.Vector(0, 0, CASE_H_FRONT))
        upper_hood = upper_hood.cut(led_cyl)

    # -------------------------------------------------------------------------
    # VALIDATION & EXPORT
    # -------------------------------------------------------------------------
    print(f"Base Tray Solid: Valid={base_tray.isValid()}, Closed={base_tray.isClosed()}")
    print(f"Upper Hood Solid: Valid={upper_hood.isValid()}, Closed={upper_hood.isClosed()}")
    
    obj_base = doc.addObject("Part::Feature", "Base_Tray")
    obj_base.Shape = base_tray
    
    obj_hood = doc.addObject("Part::Feature", "Upper_Console_Hood")
    obj_hood.Shape = upper_hood
    
    doc.recompute()
    
    output_dir = os.path.dirname(os.path.abspath(__file__))
    fcstd_path = os.path.join(output_dir, "FDD_Tester_Case_Assembly.FCStd")
    step_base  = os.path.join(output_dir, "FDD_Tester_Base_Tray.step")
    step_hood  = os.path.join(output_dir, "FDD_Tester_Upper_Hood.step")
    step_assy  = os.path.join(output_dir, "FDD_Tester_Case_Full_Assembly.step")
    stl_base   = os.path.join(output_dir, "FDD_Tester_Base_Tray.stl")
    stl_hood   = os.path.join(output_dir, "FDD_Tester_Upper_Hood.stl")
    
    print(f">>> Saving FreeCAD Project: {fcstd_path}")
    doc.saveAs(fcstd_path)
    
    print(">>> Exporting Production STEP Files...")
    Import.export([obj_base], step_base)
    Import.export([obj_hood], step_hood)
    Import.export([obj_base, obj_hood], step_assy)
    
    print(">>> Exporting Production STL Mesh Files...")
    mesh_base = MeshPart.meshFromShape(Shape=obj_base.Shape, LinearDeflection=0.08, AngularDeflection=0.26)
    mesh_base.write(stl_base)
    
    mesh_hood = MeshPart.meshFromShape(Shape=obj_hood.Shape, LinearDeflection=0.08, AngularDeflection=0.26)
    mesh_hood.write(stl_hood)
    
    print("=========================================================================")
    print("SUCCESS: Lightweight Enclosure Assembly Generated & Exported!")
    print(f"  * Base Tray STEP         : {step_base}")
    print(f"  * Upper Hood STEP        : {step_hood}")
    print(f"  * Full Assembly STEP     : {step_assy}")
    print("=========================================================================")

if __name__ == '__main__':
    generate_lightweight_case()
