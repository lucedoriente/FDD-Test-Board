"""
=============================================================================
FDD TESTER & EXERCISER - Modular V2 Enclosure Generator (FreeCAD)
Author: Alessio Iodice <alessio67@gmail.com>

Architecture V2:
  - Completely Independent 2-Module Desktop Console:
    1. PSU_Module (Left, 95mm wide): Segregated 230V AC + Mean Well LRS-50/75-24
    2. Logic_Console (Right, 235mm wide): Motherboard PCB + 7" Touchscreen + UI Controls
    3. Shield_Plate (Center, 1.5mm aluminum): Interposed Galvanic/EMC Grounded Shield
  - Features:
    * 2 Independent Roofs / Hoods (Safe open-bench maintenance of low-voltage logic)
    * Aligned Cable Pass-Through Notch at Y in [80, 110mm], Z in [3, 19mm]
    * 5x M4 Bolted Clamping Grid uniting both modules through the Shield Plate
    * Centered 7.0-inch Display and UI Panel on Logic Console
    * Lightweight Ribbed Bosses for fast, economical SLA / Nylon printing
=============================================================================
"""

import os
import math
import FreeCAD
import Part
import Import
import MeshPart

def generate_modular_v2():
    print(">>> Initializing FreeCAD Modular V2 Case Generator...")
    doc = FreeCAD.newDocument("FDD_Tester_Modular_V2")
    
    # -------------------------------------------------------------------------
    # PARAMETRIC CONSTANTS (mm)
    # -------------------------------------------------------------------------
    CASE_D = 185.0       # External Depth (Y)
    CASE_H_FRONT = 40.0  # Front Min Height (Z at Y=0)
    CASE_H_REAR = 70.0   # Rear Max Height  (Z at Y=185)
    WALL_T = 3.0         # Wall thickness
    BASE_T = 3.0         # Base plate thickness
    LIP_H = 4.0          # Guide lip height
    LIP_T = 1.5          # Guide lip thickness
    LIP_CLEAR = 0.25     # Tolerance clearance
    
    PSU_W = 95.0         # PSU Module Width (Left)
    LOGIC_W = 235.0      # Logic Console Width (Right)
    SHIELD_T = 1.5       # Aluminum Shield Plate Thickness
    
    PCB_STANDOFF_H = 8.0 # PCB Standoff Height
    PCB_T = 1.6          # PCB Thickness
    Z_PCB_TOP = BASE_T + PCB_STANDOFF_H + PCB_T # 12.6 mm
    
    PILOT_HOLE_R = 1.25      # Dia 2.50 mm (M3 self-tapping / threading)
    CLEARANCE_HOLE_R = 1.7   # Dia 3.40 mm (M3 clearance pass-through)
    M4_CLEARANCE_R = 2.1     # Dia 4.20 mm (M4 clearance bolt)
    
    BOSS_R = 3.75            # Outer Dia 7.50 mm
    BOSS_H = 14.0            # Height 14.0 mm
    RIB_W = 2.0              # Rib thickness 2.0 mm
    
    SLOPE_ANG = math.atan2(CASE_H_REAR - CASE_H_FRONT, CASE_D) # ~9.21 deg
    deg_ang = math.degrees(SLOPE_ANG)

    # Helper: Create generic wedge solid
    def make_wedge_shell(width):
        pts_out = [
            FreeCAD.Vector(0, 0, 0),
            FreeCAD.Vector(0, CASE_D, 0),
            FreeCAD.Vector(0, CASE_D, CASE_H_REAR),
            FreeCAD.Vector(0, 0, CASE_H_FRONT),
            FreeCAD.Vector(0, 0, 0)
        ]
        w_out = Part.makePolygon(pts_out)
        f_out = Part.Face(w_out)
        solid_out = f_out.extrude(FreeCAD.Vector(width, 0, 0))
        
        pts_in = [
            FreeCAD.Vector(WALL_T, WALL_T, -1.0),
            FreeCAD.Vector(WALL_T, CASE_D - WALL_T, -1.0),
            FreeCAD.Vector(WALL_T, CASE_D - WALL_T, CASE_H_REAR - WALL_T / math.cos(SLOPE_ANG)),
            FreeCAD.Vector(WALL_T, WALL_T, CASE_H_FRONT - WALL_T / math.cos(SLOPE_ANG)),
            FreeCAD.Vector(WALL_T, WALL_T, -1.0)
        ]
        w_in = Part.makePolygon(pts_in)
        f_in = Part.Face(w_in)
        solid_in = f_in.extrude(FreeCAD.Vector(width - 2 * WALL_T, 0, 0))
        return solid_out, solid_out.cut(solid_in)

    # Helper: Create generic base tray
    def make_base_tray(width):
        plate = Part.makeBox(width, CASE_D, BASE_T, FreeCAD.Vector(0, 0, 0))
        lip_out = Part.makeBox(
            width - 2 * (WALL_T + LIP_CLEAR),
            CASE_D - 2 * (WALL_T + LIP_CLEAR),
            LIP_H,
            FreeCAD.Vector(WALL_T + LIP_CLEAR, WALL_T + LIP_CLEAR, BASE_T)
        )
        lip_in = Part.makeBox(
            width - 2 * (WALL_T + LIP_CLEAR + LIP_T),
            CASE_D - 2 * (WALL_T + LIP_CLEAR + LIP_T),
            LIP_H + 1.0,
            FreeCAD.Vector(WALL_T + LIP_CLEAR + LIP_T, WALL_T + LIP_CLEAR + LIP_T, BASE_T - 0.5)
        )
        lip = lip_out.cut(lip_in)
        
        # Clear corners for bosses
        c1 = Part.makeBox(18.0, 18.0, LIP_H + 2.0, FreeCAD.Vector(0, 0, BASE_T - 0.5))
        c2 = Part.makeBox(18.0, 18.0, LIP_H + 2.0, FreeCAD.Vector(0, CASE_D - 18.0, BASE_T - 0.5))
        c3 = Part.makeBox(18.0, 18.0, LIP_H + 2.0, FreeCAD.Vector(width - 18.0, 0, BASE_T - 0.5))
        c4 = Part.makeBox(18.0, 18.0, LIP_H + 2.0, FreeCAD.Vector(width - 18.0, CASE_D - 18.0, BASE_T - 0.5))
        lip = lip.cut(c1).cut(c2).cut(c3).cut(c4)
        return plate.fuse(lip)

    # -------------------------------------------------------------------------
    # 1. MODULE 1: PSU MODULE (Left, Width = 95.0 mm)
    # -------------------------------------------------------------------------
    print(">>> 1. Generating PSU Module (Left, 95.0 mm)...")
    psu_base = make_base_tray(PSU_W)
    
    # PSU Mount Bosses (LRS-50/75-24)
    psu_mounts = [(17.5, 47.5), (77.5, 47.5), (17.5, 137.5), (77.5, 137.5)]
    for px, py in psu_mounts:
        p_cyl = Part.makeCylinder(3.5, 4.0, FreeCAD.Vector(px, py, BASE_T))
        p_hole = Part.makeCylinder(PILOT_HOLE_R, 5.0, FreeCAD.Vector(px, py, BASE_T + 0.5))
        psu_base = psu_base.fuse(p_cyl.cut(p_hole))
        
    # Bottom Intake Ventilation Slots
    for i in range(10):
        bslot = Part.makeBox(3.0, 45.0, BASE_T * 3, FreeCAD.Vector(25.0 + (i % 5) * 11.0, 55.0 + (i // 5) * 55.0, -BASE_T))
        psu_base = psu_base.cut(bslot)
        
    # Countersunk Hood Screws in PSU Base
    psu_hood_screws = [(10.0, 10.0), (10.0, 175.0), (PSU_W - 10.0, 10.0), (PSU_W - 10.0, 175.0)]
    for vx, vy in psu_hood_screws:
        v_hole = Part.makeCylinder(CLEARANCE_HOLE_R, BASE_T * 3, FreeCAD.Vector(vx, vy, -BASE_T))
        v_csink = Part.makeCone(3.1, CLEARANCE_HOLE_R, 1.5, FreeCAD.Vector(vx, vy, 0))
        psu_base = psu_base.cut(v_hole).cut(v_csink)
        
    # PSU Upper Hood
    psu_wedge, psu_hood = make_wedge_shell(PSU_W)
    
    # Ribbed Bosses for PSU Hood (4 Corners)
    def make_psu_boss(cx, cy, rdirs):
        cyl = Part.makeCylinder(BOSS_R, BOSS_H, FreeCAD.Vector(cx, cy, 0))
        shapes = [cyl]
        for d in rdirs:
            if d == '-X': shapes.append(Part.makeBox(cx - 1.5, RIB_W, BOSS_H, FreeCAD.Vector(1.5, cy - RIB_W/2.0, 0)))
            elif d == '+X': shapes.append(Part.makeBox(PSU_W - cx - 1.5, RIB_W, BOSS_H, FreeCAD.Vector(cx, cy - RIB_W/2.0, 0)))
            elif d == '-Y': shapes.append(Part.makeBox(RIB_W, cy - 1.5, BOSS_H, FreeCAD.Vector(cx - RIB_W/2.0, 1.5, 0)))
            elif d == '+Y': shapes.append(Part.makeBox(RIB_W, CASE_D - cy - 1.5, BOSS_H, FreeCAD.Vector(cx - RIB_W/2.0, cy, 0)))
        comp = shapes[0]
        for s in shapes[1:]: comp = comp.fuse(s)
        hole = Part.makeCylinder(PILOT_HOLE_R, 12.0, FreeCAD.Vector(cx, cy, -0.5))
        return comp.cut(hole)

    pb1 = make_psu_boss(10.0, 10.0, ['-X', '-Y'])
    pb2 = make_psu_boss(10.0, 175.0, ['-X', '+Y'])
    pb3 = make_psu_boss(PSU_W - 10.0, 10.0, ['+X', '-Y'])
    pb4 = make_psu_boss(PSU_W - 10.0, 175.0, ['+X', '+Y'])
    psu_hood = psu_hood.fuse(pb1.fuse(pb2).fuse(pb3).fuse(pb4))
    
    # Rear IEC C14 Mains Inlet Cutout
    iec_cut = Part.makeBox(48.0, WALL_T * 3, 28.0, FreeCAD.Vector(23.5, CASE_D - WALL_T * 2, 21.0))
    iec_h1 = Part.makeCylinder(1.7, WALL_T * 3, FreeCAD.Vector(13.5, CASE_D - WALL_T * 2, 35.0), FreeCAD.Vector(0, 1, 0))
    iec_h2 = Part.makeCylinder(1.7, WALL_T * 3, FreeCAD.Vector(81.5, CASE_D - WALL_T * 2, 35.0), FreeCAD.Vector(0, 1, 0))
    psu_hood = psu_hood.cut(iec_cut).cut(iec_h1).cut(iec_h2)
    
    # Left Side Cooling Slots (PSU Fresh Air Intake)
    for i in range(8):
        slot_y = 50.0 + i * 12.0
        side_slot = Part.makeBox(WALL_T * 3, 35.0, 3.5, FreeCAD.Vector(-WALL_T, slot_y, 16.0))
        psu_hood = psu_hood.cut(side_slot)
        
    # Top Panel Roof Exhaust Louvers (Convection cooling directly above Mean Well)
    for i in range(6):
        top_y = 65.0 + i * 14.0
        tslot = Part.makeBox(50.0, 4.0, 15.0, FreeCAD.Vector(22.5, top_y, -5.0))
        tslot.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), deg_ang)
        tslot.translate(FreeCAD.Vector(0, 0, CASE_H_FRONT))
        psu_hood = psu_hood.cut(tslot)

    # -------------------------------------------------------------------------
    # INTER-MODULE INTERFACE (Cable Notch & 5x M4 Bolt Holes)
    # Cable Notch: Y in [80, 110], Z in [3, 19]
    # -------------------------------------------------------------------------
    cable_notch_tool = Part.makeBox(WALL_T * 4, 30.0, 16.0, FreeCAD.Vector(-WALL_T, 80.0, BASE_T))
    
    # 5 M4 Clamping Bolt Holes on Right Wall of PSU Module (at X = PSU_W)
    bolt_coords = [
        (25.0, 12.0),
        (25.0, 30.0),
        (95.0, 38.0),
        (160.0, 15.0),
        (160.0, 50.0)
    ]
    
    # Cut Cable Notch and Bolt Holes on Right Wall of PSU Hood
    psu_hood = psu_hood.cut(cable_notch_tool.translated(FreeCAD.Vector(PSU_W - WALL_T * 2, 0, 0)))
    for by, bz in bolt_coords:
        b_hole = Part.makeCylinder(M4_CLEARANCE_R, WALL_T * 3, FreeCAD.Vector(PSU_W - WALL_T * 2, by, bz), FreeCAD.Vector(1, 0, 0))
        psu_hood = psu_hood.cut(b_hole)

    # -------------------------------------------------------------------------
    # 2. SHIELD PLATE (Interposed Center Metal Shield, 1.5 mm Aluminum)
    # -------------------------------------------------------------------------
    print(">>> 2. Generating Shield Plate (Center 1.5mm Aluminum)...")
    pts_sp = [
        FreeCAD.Vector(0, 0, 0),
        FreeCAD.Vector(0, CASE_D, 0),
        FreeCAD.Vector(0, CASE_D, CASE_H_REAR),
        FreeCAD.Vector(0, 0, CASE_H_FRONT),
        FreeCAD.Vector(0, 0, 0)
    ]
    w_sp = Part.makePolygon(pts_sp)
    f_sp = Part.Face(w_sp)
    shield_plate = f_sp.extrude(FreeCAD.Vector(SHIELD_T, 0, 0))
    
    # Cut Cable Notch on Shield Plate
    sp_notch = Part.makeBox(SHIELD_T * 3, 30.0, 16.0, FreeCAD.Vector(-SHIELD_T, 80.0, BASE_T))
    shield_plate = shield_plate.cut(sp_notch)
    
    # Cut 5 Bolt Holes on Shield Plate
    for by, bz in bolt_coords:
        sp_hole = Part.makeCylinder(M4_CLEARANCE_R, SHIELD_T * 3, FreeCAD.Vector(-SHIELD_T, by, bz), FreeCAD.Vector(1, 0, 0))
        shield_plate = shield_plate.cut(sp_hole)
        
    # Translate Shield Plate to its assembly position (X = PSU_W)
    shield_plate.translate(FreeCAD.Vector(PSU_W, 0, 0))

    # -------------------------------------------------------------------------
    # 3. MODULE 2: LOGIC CONSOLE (Right, Width = 235.0 mm)
    # -------------------------------------------------------------------------
    print(">>> 3. Generating Logic Console (Right, 235.0 mm)...")
    logic_base = make_base_tray(LOGIC_W)
    
    # PCB Coordinates inside Logic Console (Local origin X=0 at Left wall of Logic Console)
    # Motherboard PCB: 200.0 x 140.0 mm
    # Position: Right edge at X = 231.0 (1.0mm clearance from right inner wall 232.0)
    # PCB_X0 = 231.0 - 200.0 = 31.0 mm (Leaves 28mm on left for cable harness and nuts)
    # PCB_Y_REAR = 181.0 mm
    L_PCB_X0 = 31.0
    L_PCB_Y_REAR = 181.0
    
    # 7 PCB Standoffs (H1, H2, H3, H4, H5, H6, H7)
    l_pcb_mounts = [
        (L_PCB_X0 + 5.0,   L_PCB_Y_REAR - 5.0),   # H1 (Rear Left)
        (L_PCB_X0 + 114.0, L_PCB_Y_REAR - 24.0),  # H7 (Rear Center - IDC Strain Relief)
        (L_PCB_X0 + 195.0, L_PCB_Y_REAR - 101.0), # H6 (Right Edge)
        (L_PCB_X0 + 195.0, L_PCB_Y_REAR - 135.0), # H3 (Front Right)
        (L_PCB_X0 + 100.0, L_PCB_Y_REAR - 135.0), # H5 (Front Center)
        (L_PCB_X0 + 5.0,   L_PCB_Y_REAR - 135.0)  # H4 (Front Left)
    ]
    for hx, hy in l_pcb_mounts:
        b_cyl = Part.makeCylinder(3.5, PCB_STANDOFF_H, FreeCAD.Vector(hx, hy, BASE_T))
        b_hole = Part.makeCylinder(PILOT_HOLE_R, PCB_STANDOFF_H + 1.0, FreeCAD.Vector(hx, hy, BASE_T + 1.0))
        logic_base = logic_base.fuse(b_cyl.cut(b_hole))
        
    # H2 Standoff: Through-hole for coaxial corner screw
    lh2_x = L_PCB_X0 + 195.0 # 226.0
    lh2_y = L_PCB_Y_REAR - 5.0 # 176.0
    lh2_cyl = Part.makeCylinder(3.5, PCB_STANDOFF_H, FreeCAD.Vector(lh2_x, lh2_y, BASE_T))
    lh2_through = Part.makeCylinder(CLEARANCE_HOLE_R, PCB_STANDOFF_H + 2.0, FreeCAD.Vector(lh2_x, lh2_y, BASE_T - 1.0))
    logic_base = logic_base.fuse(lh2_cyl.cut(lh2_through))
    
    # 4 Countersunk Hood Screws in Logic Base
    logic_hood_screws = [
        (10.0, 10.0),
        (10.0, 175.0),
        (LOGIC_W - 10.0, 10.0),
        (lh2_x, lh2_y) # Coaxial with H2
    ]
    for vx, vy in logic_hood_screws:
        v_hole = Part.makeCylinder(CLEARANCE_HOLE_R, BASE_T * 3, FreeCAD.Vector(vx, vy, -BASE_T))
        v_csink = Part.makeCone(3.1, CLEARANCE_HOLE_R, 1.5, FreeCAD.Vector(vx, vy, 0))
        logic_base = logic_base.cut(v_hole).cut(v_csink)

    # Logic Upper Hood
    logic_wedge, logic_hood = make_wedge_shell(LOGIC_W)
    
    # Ribbed Bosses for Logic Hood (4 Corners)
    def make_logic_boss(cx, cy, cz, rdirs):
        cyl = Part.makeCylinder(BOSS_R, BOSS_H, FreeCAD.Vector(cx, cy, cz))
        shapes = [cyl]
        for d in rdirs:
            if d == '-X': shapes.append(Part.makeBox(cx - 1.5, RIB_W, BOSS_H, FreeCAD.Vector(1.5, cy - RIB_W/2.0, cz)))
            elif d == '+X': shapes.append(Part.makeBox(LOGIC_W - cx - 1.5, RIB_W, BOSS_H, FreeCAD.Vector(cx, cy - RIB_W/2.0, cz)))
            elif d == '-Y': shapes.append(Part.makeBox(RIB_W, cy - 1.5, BOSS_H, FreeCAD.Vector(cx - RIB_W/2.0, 1.5, cz)))
            elif d == '+Y': shapes.append(Part.makeBox(RIB_W, CASE_D - cy - 1.5, BOSS_H, FreeCAD.Vector(cx - RIB_W/2.0, cy, cz)))
        comp = shapes[0]
        for s in shapes[1:]: comp = comp.fuse(s)
        hole = Part.makeCylinder(PILOT_HOLE_R, 12.0, FreeCAD.Vector(cx, cy, cz - 0.5))
        return comp.cut(hole)

    lb1 = make_logic_boss(10.0, 10.0, 0.0, ['-X', '-Y'])
    lb2 = make_logic_boss(10.0, 175.0, 0.0, ['-X', '+Y'])
    lb3 = make_logic_boss(LOGIC_W - 10.0, 10.0, 0.0, ['+X', '-Y'])
    lb4 = make_logic_boss(lh2_x, lh2_y, Z_PCB_TOP, ['+X', '+Y'])
    logic_hood = logic_hood.fuse(lb1.fuse(lb2).fuse(lb3).fuse(lb4))
    
    # Cut Cable Notch on Left Wall of Logic Hood (Matching PSU and Shield)
    logic_hood = logic_hood.cut(cable_notch_tool.translated(FreeCAD.Vector(-WALL_T, 0, 0)))
    
    # Cut 5 Bolt Holes on Left Wall of Logic Hood (with Counterbores for M4 Nuts)
    for by, bz in bolt_coords:
        lb_hole = Part.makeCylinder(M4_CLEARANCE_R, WALL_T * 3, FreeCAD.Vector(-WALL_T, by, bz), FreeCAD.Vector(1, 0, 0))
        # Nut pocket on inside of left wall (dia 8.0mm, depth 2.0mm)
        lb_pocket = Part.makeCylinder(4.2, 2.0, FreeCAD.Vector(WALL_T + 1.0, by, bz), FreeCAD.Vector(-1, 0, 0))
        logic_hood = logic_hood.cut(lb_hole).cut(lb_pocket)

    # -------------------------------------------------------------------------
    # OPEN-BOTTOM "U" CUTOUTS - LOGIC REAR PANEL (Y = 185 mm)
    # -------------------------------------------------------------------------
    print(">>> 4. Cutting Open-Bottom 'U' Slots on Logic Rear Panel...")
    # J6 - USB Type-C (Local X = L_PCB_X0 + 16.5 = 47.5 mm)
    j6_u = Part.makeBox(12.0, WALL_T * 3, 18.0, FreeCAD.Vector(L_PCB_X0 + 16.5 - 6.0, CASE_D - WALL_T * 2, -1.0))
    # J2 - Molex 5.25" (Local X = L_PCB_X0 + 43.0 = 74.0 mm)
    j2_u = Part.makeBox(22.0, WALL_T * 3, 23.5, FreeCAD.Vector(L_PCB_X0 + 43.0 - 11.0, CASE_D - WALL_T * 2, -1.0))
    # J3 - Berg 3.5" (Local X = L_PCB_X0 + 52.0 = 83.0 mm)
    j3_u = Part.makeBox(16.0, WALL_T * 3, 21.5, FreeCAD.Vector(L_PCB_X0 + 52.0 - 8.0, CASE_D - WALL_T * 2, -1.0))
    # J11 - IDC-34 90 deg (Local X = L_PCB_X0 + 67.5 = 98.5 mm)
    j11_u = Part.makeBox(54.0, WALL_T * 3, 24.0, FreeCAD.Vector(L_PCB_X0 + 67.5 - 27.0, CASE_D - WALL_T * 2, -1.0))
    # J10 - IDC-50 90 deg (Local X = L_PCB_X0 + 120.0 = 151.0 mm)
    j10_u = Part.makeBox(74.0, WALL_T * 3, 24.0, FreeCAD.Vector(L_PCB_X0 + 120.0 - 37.0, CASE_D - WALL_T * 2, -1.0))
    logic_hood = logic_hood.cut(j6_u).cut(j2_u).cut(j3_u).cut(j11_u).cut(j10_u)

    # -------------------------------------------------------------------------
    # OPEN-BOTTOM "U" CUTOUTS - LOGIC RIGHT SIDE PANEL (X = LOGIC_W = 235 mm)
    # -------------------------------------------------------------------------
    print(">>> 5. Cutting Open-Bottom 'U' Slots on Logic Right Side Panel...")
    # J12 - IDC-26 (Y = 181 - 22 = 159 mm)
    j12_u = Part.makeBox(WALL_T * 3, 43.0, 24.0, FreeCAD.Vector(LOGIC_W - WALL_T * 2, (L_PCB_Y_REAR - 22.0) - 21.5, -1.0))
    # J13 - IDC-20 (Y = 181 - 66 = 115 mm)
    j13_u = Part.makeBox(WALL_T * 3, 35.0, 24.0, FreeCAD.Vector(LOGIC_W - WALL_T * 2, (L_PCB_Y_REAR - 66.0) - 17.5, -1.0))
    # J4 - Phoenix 4-pin (Y = 181 - 110 = 71 mm)
    j4_u = Part.makeBox(WALL_T * 3, 22.0, 23.0, FreeCAD.Vector(LOGIC_W - WALL_T * 2, (L_PCB_Y_REAR - 110.0) - 11.0, -1.0))
    # J14 - Stepper Motor 6-pin (Y = 181 - 124 = 57 mm)
    j14_u = Part.makeBox(WALL_T * 3, 17.0, 22.0, FreeCAD.Vector(LOGIC_W - WALL_T * 2, (L_PCB_Y_REAR - 124.0) - 8.5, -1.0))
    logic_hood = logic_hood.cut(j12_u).cut(j13_u).cut(j4_u).cut(j14_u)

    # -------------------------------------------------------------------------
    # DISPLAY & UI INTEGRATION (BEAUTIFULLY CENTERED ON LOGIC CONSOLE!)
    # -------------------------------------------------------------------------
    print(">>> 6. Centering 7.0\" Display & UI Panel on Logic Console Roof...")
    # Display Sunton 7.0": Window 154 x 86 mm, Recess 182 x 109 mm
    # Center on LOGIC_W (235.0 mm): Center X = 117.5 mm
    DISP_X_CENTER = LOGIC_W / 2.0 # 117.5 mm
    DISP_X0 = DISP_X_CENTER - 154.0 / 2.0 # 40.5 mm
    DISP_Y_SLOPE = 75.0
    
    disp_cut_box = Part.makeBox(154.0, 86.0, 25.0, FreeCAD.Vector(DISP_X0, DISP_Y_SLOPE, -12.0))
    disp_recess_box = Part.makeBox(182.0, 109.0, 2.5, FreeCAD.Vector(DISP_X_CENTER - 91.0, DISP_Y_SLOPE - 11.5, -2.5))
    for tool in [disp_cut_box, disp_recess_box]:
        tool.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), deg_ang)
        tool.translate(FreeCAD.Vector(0, 0, CASE_H_FRONT))
        logic_hood = logic_hood.cut(tool)
        
    # Daughterboard FDD_UI_Panel (120 x 38 mm) - Centered below display
    UI_X_CENTER = LOGIC_W / 2.0 # 117.5 mm
    UI_X0 = UI_X_CENTER - 120.0 / 2.0 # 57.5 mm
    UI_Y_SLOPE = 18.0
    
    # Rotary Encoder
    enc_x = UI_X0 + 72.0
    enc_y = UI_Y_SLOPE + 16.5
    enc_cyl = Part.makeCylinder(3.75, 25.0, FreeCAD.Vector(enc_x, enc_y, -12.0))
    enc_cyl.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), deg_ang)
    enc_cyl.translate(FreeCAD.Vector(0, 0, CASE_H_FRONT))
    logic_hood = logic_hood.cut(enc_cyl)
    
    # 3 Pushbuttons
    btn_x_list = [UI_X0 + 15.0, UI_X0 + 33.0, UI_X0 + 51.0]
    for bx in btn_x_list:
        btn_cyl = Part.makeCylinder(3.5, 25.0, FreeCAD.Vector(bx, UI_Y_SLOPE + 24.0, -12.0))
        btn_cyl.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), deg_ang)
        btn_cyl.translate(FreeCAD.Vector(0, 0, CASE_H_FRONT))
        logic_hood = logic_hood.cut(btn_cyl)
        
    # 5 Status LEDs
    led_x_list = [UI_X0 + 16.0, UI_X0 + 26.0, UI_X0 + 36.0, UI_X0 + 46.0, UI_X0 + 56.0]
    for lx in led_x_list:
        led_cyl = Part.makeCylinder(1.6, 25.0, FreeCAD.Vector(lx, UI_Y_SLOPE + 10.0, -12.0))
        led_cyl.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), deg_ang)
        led_cyl.translate(FreeCAD.Vector(0, 0, CASE_H_FRONT))
        logic_hood = logic_hood.cut(led_cyl)

    # -------------------------------------------------------------------------
    # VALIDATION
    # -------------------------------------------------------------------------
    print(">>> Validating Solids...")
    print(f"  * PSU Base Tray     : Valid={psu_base.isValid()}, Closed={psu_base.isClosed()}")
    print(f"  * PSU Upper Hood    : Valid={psu_hood.isValid()}, Closed={psu_hood.isClosed()}")
    print(f"  * Shield Plate      : Valid={shield_plate.isValid()}, Closed={shield_plate.isClosed()}")
    print(f"  * Logic Base Tray   : Valid={logic_base.isValid()}, Closed={logic_base.isClosed()}")
    print(f"  * Logic Upper Hood  : Valid={logic_hood.isValid()}, Closed={logic_hood.isClosed()}")
    
    # -------------------------------------------------------------------------
    # ASSEMBLE IN FREECAD (Positioned in True Global Coordinates)
    # -------------------------------------------------------------------------
    print(">>> Registering Objects into FreeCAD Document...")
    
    # 1. PSU Module at X = 0
    obj_psu_base = doc.addObject("Part::Feature", "PSU_Base_Tray")
    obj_psu_base.Shape = psu_base
    
    obj_psu_hood = doc.addObject("Part::Feature", "PSU_Upper_Hood")
    obj_psu_hood.Shape = psu_hood
    
    # 2. Shield Plate at X = PSU_W (95.0 mm)
    obj_shield = doc.addObject("Part::Feature", "EMC_Shield_Plate")
    obj_shield.Shape = shield_plate
    
    # 3. Logic Module at X = PSU_W + SHIELD_T (96.5 mm)
    LOGIC_X_OFFSET = PSU_W + SHIELD_T # 96.5 mm
    logic_base_assembled = logic_base.copy()
    logic_base_assembled.translate(FreeCAD.Vector(LOGIC_X_OFFSET, 0, 0))
    obj_logic_base = doc.addObject("Part::Feature", "Logic_Base_Tray")
    obj_logic_base.Shape = logic_base_assembled
    
    logic_hood_assembled = logic_hood.copy()
    logic_hood_assembled.translate(FreeCAD.Vector(LOGIC_X_OFFSET, 0, 0))
    obj_logic_hood = doc.addObject("Part::Feature", "Logic_Upper_Hood")
    obj_logic_hood.Shape = logic_hood_assembled
    
    doc.recompute()
    
    # -------------------------------------------------------------------------
    # EXPORT INDIVIDUAL PRODUCTION STEP & STL FILES
    # -------------------------------------------------------------------------
    out_dir = os.path.dirname(os.path.abspath(__file__))
    fcstd_path = os.path.join(out_dir, "FDD_Tester_Modular_V2.FCStd")
    
    # STEP files (Individual components exported at local coordinates for manufacturing)
    step_psu_base   = os.path.join(out_dir, "01_PSU_Base_Tray.step")
    step_psu_hood   = os.path.join(out_dir, "02_PSU_Upper_Hood.step")
    step_shield     = os.path.join(out_dir, "03_EMC_Shield_Plate_1.5mm.step")
    step_logic_base = os.path.join(out_dir, "04_Logic_Base_Tray.step")
    step_logic_hood = os.path.join(out_dir, "05_Logic_Upper_Hood.step")
    step_full_assy  = os.path.join(out_dir, "00_Modular_V2_Full_Assembly.step")
    
    # STL files for 3D Printing
    stl_psu_base   = os.path.join(out_dir, "01_PSU_Base_Tray.stl")
    stl_psu_hood   = os.path.join(out_dir, "02_PSU_Upper_Hood.stl")
    stl_logic_base = os.path.join(out_dir, "04_Logic_Base_Tray.stl")
    stl_logic_hood = os.path.join(out_dir, "05_Logic_Upper_Hood.stl")

    print(f">>> Saving Native FreeCAD Project: {fcstd_path}")
    doc.saveAs(fcstd_path)
    
    print(">>> Exporting Production STEP CAD Solids...")
    # Export individual parts in origin frame for JLCPCB quotation/printing
    obj_tmp = doc.addObject("Part::Feature", "tmp")
    
    obj_tmp.Shape = psu_base; Import.export([obj_tmp], step_psu_base)
    obj_tmp.Shape = psu_hood; Import.export([obj_tmp], step_psu_hood)
    obj_tmp.Shape = shield_plate.translated(FreeCAD.Vector(-PSU_W, 0, 0)); Import.export([obj_tmp], step_shield)
    obj_tmp.Shape = logic_base; Import.export([obj_tmp], step_logic_base)
    obj_tmp.Shape = logic_hood; Import.export([obj_tmp], step_logic_hood)
    
    # Full Assembly export
    Import.export([obj_psu_base, obj_psu_hood, obj_shield, obj_logic_base, obj_logic_hood], step_full_assy)
    doc.removeObject("tmp")
    
    print(">>> Exporting High-Resolution Mesh STL Files for 3D Printing...")
    MeshPart.meshFromShape(Shape=psu_base, LinearDeflection=0.08, AngularDeflection=0.26).write(stl_psu_base)
    MeshPart.meshFromShape(Shape=psu_hood, LinearDeflection=0.08, AngularDeflection=0.26).write(stl_psu_hood)
    MeshPart.meshFromShape(Shape=logic_base, LinearDeflection=0.08, AngularDeflection=0.26).write(stl_logic_base)
    MeshPart.meshFromShape(Shape=logic_hood, LinearDeflection=0.08, AngularDeflection=0.26).write(stl_logic_hood)
    
    print("=========================================================================")
    print("SUCCESS: Full Modular V2 Architecture Generated & Exported!")
    print(f"  * Native FreeCAD Project : {fcstd_path}")
    print(f"  * Full Assembly STEP     : {step_full_assy}")
    print(f"  * 01_PSU_Base_Tray       : {step_psu_base}")
    print(f"  * 02_PSU_Upper_Hood      : {step_psu_hood}")
    print(f"  * 03_EMC_Shield_Plate    : {step_shield}")
    print(f"  * 04_Logic_Base_Tray     : {step_logic_base}")
    print(f"  * 05_Logic_Upper_Hood    : {step_logic_hood}")
    print("=========================================================================")

if __name__ == '__main__':
    generate_modular_v2()
