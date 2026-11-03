path2 = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\02_MCU_Core.kicad_sch"
txt2 = open(path2, encoding="utf-8").read()
idx2 = txt2.find('"TEST_IO_17"')
print("S2 TEST_IO_17:", txt2[idx2-50:idx2+250])

path3 = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\03_ZIF_Sockets.kicad_sch"
txt3 = open(path3, encoding="utf-8").read()
idx3 = txt3.find('"TEST_IO_17"')
print("S3 TEST_IO_17:", txt3[idx3-50:idx3+250])
