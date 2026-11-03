path = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\02_MCU_Core.kicad_sch"
txt = open(path, encoding="utf-8").read()

idx = txt.find('(symbol "MCU_ST_STM32F4:STM32F407VETx"')
idx2 = txt.find('(symbol "Connector:USB_C_Receptacle_USB2.0_16P"')
print(txt[idx:idx+800])
print("...")
print(txt[idx2-200:idx2])
