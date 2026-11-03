import glob, re

for sch in glob.glob(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\*.kicad_sch"):
    txt = open(sch, encoding="utf-8").read()
    ext = re.findall(r'\(extends\s+"[^"]+"\)', txt)
    print(sch.split("\\")[-1], "extends:", ext)
