import glob, re, os

PRJ_DIR = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
for f in glob.glob(os.path.join(PRJ_DIR, "*.kicad_sch")):
    with open(f, encoding='utf-8') as fh:
        txt = fh.read()
    for ref in ['L1', 'L2']:
        idx = txt.find(f'"Reference" "{ref}"')
        if idx != -1:
            snippet = txt[max(0, idx-100):min(len(txt), idx+400)]
            print(f"File: {os.path.basename(f)}, Ref: {ref}")
            print(snippet)
