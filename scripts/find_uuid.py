import glob

target_uuid = "b356d5e3-7c17-4e88-a902-73e7ec2c9107"
for sch in glob.glob(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\*.kicad_sch"):
    txt = open(sch, encoding="utf-8").read()
    if target_uuid in txt:
        print("Found in:", sch)
