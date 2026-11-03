import glob
import re

for sch in sorted(glob.glob('C:/Users/aless/OneDrive/temp/Manutenzione/Kicad_Project/FDD_Tester/kicad/*.kicad_sch')):
    with open(sch, 'r', encoding='utf-8') as f:
        txt = f.read()
    print('===', sch.replace('\\', '/').split('/')[-1])
    for m in re.finditer(r'\((global_label|hierarchical_label|label)\s+"([^"]+)"\s*(?:\(shape\s+(\w+)\)\s*)?\(at\s+([\d\.\-]+)\s+([\d\.\-]+)(?:\s+([\d\.\-]+))?\)', txt):
        print(f'  {m.group(1)}: "{m.group(2)}" shape={m.group(3)} at ({m.group(4)}, {m.group(5)}) rot={m.group(6)}')
