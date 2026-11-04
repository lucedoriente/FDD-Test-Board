import pcbnew
import csv
import os
import zipfile

def generate_ui_assembly():
    pcb_path = r'c:\Users\aless\.gemini\antigravity\scratch\FDD_Tester\kicad\FDD_UI_Panel\FDD_UI_Panel.kicad_pcb'
    prod_dir = r'c:\Users\aless\.gemini\antigravity\scratch\FDD_Tester\production\FDD_UI_Panel-FrontPanel\assembly'
    onedrive_dir = r'C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\production\FDD_UI_Panel-FrontPanel\assembly'
    
    board = pcbnew.LoadBoard(pcb_path)
    cpl_path = os.path.join(prod_dir, 'FDD_UI_Panel_cpl.csv')
    cpl_rows = []
    
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        if ref.startswith('H') and len(ref) <= 3 and ref[1:].isdigit():
            continue
        if ref.startswith('G***') or ref.startswith('#'):
            continue
            
        pos = fp.GetPosition()
        px = pcbnew.ToMM(pos.x)
        py = pcbnew.ToMM(pos.y)
        
        mid_x = px
        mid_y = 38.0 - py
        rot = fp.GetOrientation().AsDegrees() % 360.0
        layer = "Top" if fp.GetLayer() == pcbnew.F_Cu else "Bottom"
        val = fp.GetValue()
        pkg = str(fp.GetFPID().GetLibItemName())
        
        cpl_rows.append({
            'Designator': ref,
            'Mid X': f"{mid_x:.4f}",
            'Mid Y': f"{mid_y:.4f}",
            'Layer': layer,
            'Rotation': f"{rot:.1f}",
            'Val': val,
            'Package': pkg
        })
    
    cpl_rows.sort(key=lambda r: (r['Designator'][0], int(r['Designator'][1:]) if r['Designator'][1:].isdigit() else 999))
    
    with open(cpl_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Designator', 'Mid X', 'Mid Y', 'Layer', 'Rotation'])
        for r in cpl_rows:
            writer.writerow([r['Designator'], r['Mid X'], r['Mid Y'], r['Layer'], r['Rotation']])
            
    # BOM
    bom_path = os.path.join(prod_dir, 'FDD_UI_Panel_bom.csv')
    grouped_bom = {}
    for r in cpl_rows:
        key = (r['Val'], r['Package'])
        if key not in grouped_bom:
            grouped_bom[key] = []
        grouped_bom[key].append(r['Designator'])
        
    with open(bom_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Comment', 'Designator', 'Footprint', 'Quantity'])
        for (val, pkg), des_list in sorted(grouped_bom.items()):
            des_list.sort(key=lambda d: (d[0], int(d[1:]) if d[1:].isdigit() else 999))
            writer.writerow([val, ','.join(des_list), pkg, len(des_list)])
            
    zip_path = os.path.join(os.path.dirname(prod_dir), 'FDD_UI_Panel_rev1.0_Assembly_SMT.zip')
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(cpl_path, 'FDD_UI_Panel_cpl.csv')
        z.write(bom_path, 'FDD_UI_Panel_bom.csv')
        
    import shutil
    shutil.copy2(cpl_path, onedrive_dir)
    shutil.copy2(bom_path, onedrive_dir)
    shutil.copy2(zip_path, os.path.dirname(onedrive_dir))
    print("UI Panel assembly generated.")

if __name__ == '__main__':
    generate_ui_assembly()
