for f in ['01_Power_Supply.kicad_sch', '02_MCU_Core.kicad_sch']:
    path = f'C:/Users/aless/OneDrive/temp/Manutenzione/Kicad_Project/FDD_Tester/kicad/{f}'
    lines = open(path, encoding='utf-8').readlines()
    print(f"=== {f} ===")
    for i in range(15):
        print(lines[i].rstrip())
    print("...")
    for i in range(len(lines)-10, len(lines)):
        print(lines[i].rstrip())
