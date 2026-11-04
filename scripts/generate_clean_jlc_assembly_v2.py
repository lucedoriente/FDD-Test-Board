import pcbnew
import csv
import os
import zipfile
import openpyxl

def generate_clean_jlc_assembly():
    pcb_path = r'c:\Users\aless\.gemini\antigravity\scratch\FDD_Tester\kicad\FDD-Test-Board.kicad_pcb'
    prod_dir = r'c:\Users\aless\.gemini\antigravity\scratch\FDD_Tester\production\FDD-Test-Board-Mainboard\assembly'
    onedrive_dir = r'C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\production\FDD-Test-Board-Mainboard\assembly'
    
    os.makedirs(prod_dir, exist_ok=True)
    os.makedirs(onedrive_dir, exist_ok=True)
    
    board = pcbnew.LoadBoard(pcb_path)
    
    # 1. Components to EXCLUDE from SMT assembly:
    # All Through-Hole connectors, switches, buzzers, testpoints, mounting holes
    EXCLUDE_REFS = {
        'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7',
        'J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J10', 'J11', 'J12', 'J13', 'J14', 'J15',
        'BZ1',
        'SW1', 'SW2', 'SW3', 'SW4',
        'TP1', 'TP2', 'TP3', 'TP4', 'TP5', 'TP6'
    }
    
    # 2. Master LCSC Part # mapping for 100% automated matching on JLCPCB
    LCSC_MAP = {
        # Resistors 0805
        'R_1M': ('1M', '0805', 'C17514'),
        'R_10k': ('10k', '0805', 'C17414'),
        'R_5.1k': ('5.1k', '0805', 'C27834'),
        'R_22R': ('22R', '0805', 'C17561'),
        'R_100k': ('100k', '0805', 'C149504'),
        'R_1k': ('1k', '0805', 'C17513'),
        'R_6.04k': ('6.04k', '0805', 'C2933476'),
        'R_51k': ('51k', '0805', 'C17737'),
        'R_7.15k': ('7.15k', '0805', 'C2933492'),
        
        # Capacitors
        'C_100nF_0805': ('100nF', '0805', 'C49678'),
        'C_10nF_0805': ('10nF', '0805', 'C1710'),
        'C_22pF_0805': ('22pF', '0805', 'C1804'),
        'C_10uF_0805': ('10uF', '0805', 'C15850'),
        'C_22uF_0805': ('22uF', '0805', 'C45783'),
        'C_2.2uF_0805': ('2.2uF', '0805', 'C23630'),
        'C_10uF_1210': ('10uF', '1210', 'C129489'),
        'C_22uF_1206': ('22uF', '1206', 'C13585'),
        'C_47uF_1206': ('47uF', '1206', 'C9690'),
        
        # Diodes & LEDs
        'D_USBLC6-2SC6': ('USBLC6-2SC6', 'SOT-23-6', 'C7519'),
        'D_SS34': ('SS34', 'SMA', 'C8678'),
        'D_1N4148': ('1N4148W', 'SOD-123', 'C81598'),
        'LED_READY_GRN': ('Green LED', '0805', 'C2297'),
        'LED_BUSY_YEL': ('Yellow LED', '0805', 'C2296'),
        'LED_FAULT_RED': ('Red LED', '0805', 'C2286'),
        'LED_INDEX_BLU': ('Blue LED', '0805', 'C2293'),
        'LED_READ_ORG': ('Orange LED', '0805', 'C2295'),
        
        # Inductors
        'L_10uH': ('10uH', 'IND-SMD_7.3x7.3mm', 'C168341'),
        'L_4.7uH': ('4.7uH', 'IND-SMD_7.3x7.3mm', 'C168337'),
        
        # Transistors
        'Q_2N3904': ('2N3904', 'SOT-23', 'C21379'),
        'Q_AO3401A': ('AO3401A', 'SOT-23', 'C15127'),
        
        # ICs & Crystal
        'U_TPS54302': ('TPS54302DDCR', 'SOT-23-6', 'C311983'),
        'U_INA180A1': ('INA180A1IDBVR', 'SOT-23-5', 'C122228'),
        'U_7406': ('SN7406DR', 'SOIC-14', 'C6914'),
        'U_STM32F407': ('STM32F407VET6', 'LQFP-100', 'C12117'),
        'U_AMS1117-3.3': ('AMS1117-3.3', 'SOT-223', 'C6186'),
        'U_LMV358': ('LMV358IDR', 'SOIC-8', 'C7952'),
        'U_74HC14': ('74HC14D', 'SOIC-14', 'C5600'),
        'U_ULN2003A': ('ULN2003ADR', 'SOIC-16', 'C6824'),
        'Y_8MHz': ('8MHz 16pF', 'SMD-3225_4P', 'C115962')
    }
    
    def get_lcsc_info(ref, val, pkg):
        if ref.startswith('R'):
            val_clean = val.replace(' ', '')
            key = f'R_{val_clean}'
            return LCSC_MAP.get(key, (val, '0805', ''))
        elif ref.startswith('C'):
            val_clean = val.replace(' ', '')
            if '1210' in pkg:
                key = f'C_{val_clean}_1210'
            elif '1206' in pkg:
                key = f'C_{val_clean}_1206'
            else:
                key = f'C_{val_clean}_0805'
            return LCSC_MAP.get(key, (val, pkg, ''))
        elif ref.startswith('D'):
            if 'LED' in val:
                return LCSC_MAP.get(val, (val, '0805', ''))
            elif 'USBLC6' in val:
                return LCSC_MAP['D_USBLC6-2SC6']
            elif 'SS34' in val:
                return LCSC_MAP['D_SS34']
            elif '1N4148' in val:
                return LCSC_MAP['D_1N4148']
            return (val, pkg, '')
        elif ref.startswith('L'):
            val_clean = val.replace(' ', '')
            key = f'L_{val_clean}'
            return LCSC_MAP.get(key, (val, pkg, ''))
        elif ref.startswith('Q'):
            if '3904' in val:
                return LCSC_MAP['Q_2N3904']
            elif 'AO3401' in val:
                return LCSC_MAP['Q_AO3401A']
            return (val, pkg, '')
        elif ref.startswith('U'):
            if 'TPS54302' in val:
                return LCSC_MAP['U_TPS54302']
            elif 'INA180' in val:
                return LCSC_MAP['U_INA180A1']
            elif '7406' in val:
                return LCSC_MAP['U_7406']
            elif 'STM32' in val:
                return LCSC_MAP['U_STM32F407']
            elif 'AMS1117' in val:
                return LCSC_MAP['U_AMS1117-3.3']
            elif 'LMV358' in val:
                return LCSC_MAP['U_LMV358']
            elif '74HC14' in val:
                return LCSC_MAP['U_74HC14']
            elif 'ULN2003' in val:
                return LCSC_MAP['U_ULN2003A']
            return (val, pkg, '')
        elif ref.startswith('Y'):
            return LCSC_MAP['Y_8MHz']
        return (val, pkg, '')

    # Collect SMD footprints
    cpl_rows = []
    bom_groups = {}
    
    for fp in board.GetFootprints():
        ref = str(fp.GetReference())
        if ref in EXCLUDE_REFS or ref.startswith('#') or ref.startswith('G***'):
            continue
            
        pos = fp.GetPosition()
        px = pcbnew.ToMM(pos.x)
        py = pcbnew.ToMM(pos.y)
        
        # JLCPCB coordinates: Origin bottom-left of 200x140 PCB
        mid_x = px
        mid_y = 140.0 - py
        
        rot = fp.GetOrientation().AsDegrees() % 360.0
        # JLCPCB expects lowercase layer 'top' / 'bottom'
        layer = 'top' if fp.GetLayer() == pcbnew.F_Cu else 'bottom'
        
        val = str(fp.GetValue())
        pkg = str(fp.GetFPID().GetLibItemName())
        
        comment, norm_pkg, lcsc_pn = get_lcsc_info(ref, val, pkg)
        
        cpl_rows.append({
            'Designator': ref,
            'Mid X': f"{mid_x:.4f}",
            'Mid Y': f"{mid_y:.4f}",
            'Layer': layer,
            'Rotation': f"{rot:.1f}",
            'Comment': comment,
            'Footprint': norm_pkg,
            'LCSC Part #': lcsc_pn
        })
        
        # Group for BOM
        bom_key = (comment, norm_pkg, lcsc_pn)
        if bom_key not in bom_groups:
            bom_groups[bom_key] = []
        bom_groups[bom_key].append(ref)
        
    # Sort CPL by Designator
    def des_sort_key(d):
        prefix = d.rstrip('0123456789')
        num = d[len(prefix):]
        return (prefix, int(num) if num.isdigit() else 0)

    cpl_rows.sort(key=lambda r: des_sort_key(r['Designator']))
    
    # 1. Write CPL CSV (JLCPCB strictly standard)
    cpl_csv_path = os.path.join(prod_dir, 'FDD-Test-Board_cpl.csv')
    with open(cpl_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Designator', 'Mid X', 'Mid Y', 'Layer', 'Rotation'])
        for r in cpl_rows:
            writer.writerow([r['Designator'], r['Mid X'], r['Mid Y'], r['Layer'], r['Rotation']])
            
    # 2. Write CPL XLSX
    cpl_xlsx_path = os.path.join(prod_dir, 'FDD-Test-Board_cpl.xlsx')
    wb_cpl = openpyxl.Workbook()
    ws_cpl = wb_cpl.active
    ws_cpl.title = "CPL"
    ws_cpl.append(['Designator', 'Mid X', 'Mid Y', 'Layer', 'Rotation'])
    for r in cpl_rows:
        ws_cpl.append([r['Designator'], float(r['Mid X']), float(r['Mid Y']), r['Layer'], float(r['Rotation'])])
    wb_cpl.save(cpl_xlsx_path)

    # 3. Write BOM CSV
    bom_csv_path = os.path.join(prod_dir, 'FDD-Test-Board_bom.csv')
    bom_rows = []
    for (comment, norm_pkg, lcsc_pn), refs in bom_groups.items():
        refs.sort(key=des_sort_key)
        ref_str = ','.join(refs)
        bom_rows.append((comment, ref_str, norm_pkg, lcsc_pn, len(refs)))
        
    # Sort BOM rows by comment
    bom_rows.sort(key=lambda r: (r[0], r[1]))
    
    with open(bom_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Comment', 'Designator', 'Footprint', 'LCSC Part #'])
        for r in bom_rows:
            writer.writerow([r[0], r[1], r[2], r[3]])
            
    # 4. Write BOM XLSX
    bom_xlsx_path = os.path.join(prod_dir, 'FDD-Test-Board_bom.xlsx')
    wb_bom = openpyxl.Workbook()
    ws_bom = wb_bom.active
    ws_bom.title = "BOM"
    ws_bom.append(['Comment', 'Designator', 'Footprint', 'LCSC Part #'])
    for r in bom_rows:
        ws_bom.append([r[0], r[1], r[2], r[3]])
    wb_bom.save(bom_xlsx_path)

    # 5. Pack ZIP (both CSV and XLSX for maximum compatibility)
    zip_path = os.path.join(os.path.dirname(prod_dir), 'FDD-Test-Board_rev1.0_Assembly_SMT.zip')
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(cpl_csv_path, 'FDD-Test-Board_cpl.csv')
        z.write(cpl_xlsx_path, 'FDD-Test-Board_cpl.xlsx')
        z.write(bom_csv_path, 'FDD-Test-Board_bom.csv')
        z.write(bom_xlsx_path, 'FDD-Test-Board_bom.xlsx')
        
    # 6. Copy all to OneDrive
    import shutil
    shutil.copy2(cpl_csv_path, onedrive_dir)
    shutil.copy2(cpl_xlsx_path, onedrive_dir)
    shutil.copy2(bom_csv_path, onedrive_dir)
    shutil.copy2(bom_xlsx_path, onedrive_dir)
    shutil.copy2(zip_path, os.path.dirname(onedrive_dir))
    
    print(f"SUCCESS: Generated clean SMT package with {len(cpl_rows)} components, {len(bom_rows)} BOM lines.")
    print("BOM Summary:")
    for r in bom_rows:
        print(f"  {r[0]:18s} | Qty:{r[4]:2d} | LCSC:{r[3]:10s} | Footprint:{r[2]:18s} | Refs:{r[1][:40]}")

if __name__ == '__main__':
    generate_clean_jlc_assembly()
