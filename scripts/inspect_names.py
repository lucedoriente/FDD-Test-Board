import glob, re

for sch in sorted(glob.glob('C:/Users/aless/OneDrive/temp/Manutenzione/Kicad_Project/FDD_Tester/kicad/*.kicad_sch')):
    txt = open(sch, encoding='utf-8').read()
    fname = sch.replace('\\', '/').split('/')[-1]
    for m in re.finditer(r'\(global_label\s+"([^"]+)"', txt):
        name = m.group(1)
        if any(k in name for k in ['-12V', 'USART1', '+5V_REG', '+24V']):
            print(f"{fname}: repr={repr(name)}")
