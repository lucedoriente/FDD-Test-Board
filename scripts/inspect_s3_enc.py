with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\03_UI_Controls.kicad_sch", "r", encoding="utf-8") as f:
    s3 = f.read()

for l in s3.splitlines():
    if "ENC_A" in l:
        print("S3 ENC_A:", l)
