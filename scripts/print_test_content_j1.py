import os, re

test_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\test_single"

with open(os.path.join(test_dir, "01_Power_Supply.kicad_sch"), "r", encoding="utf-8") as f:
    text = f.read()

hdr_idx = text.find('\n  (symbol (lib_id')
header = text[:hdr_idx]
body = text[hdr_idx:text.rfind('(sheet_instances')]
footer = """  (sheet_instances
    (path "/"
      (page "1")
    )
  )
)
"""

sym_blocks = []
pos = 0
while True:
    idx = body.find('(symbol (lib_id', pos)
    if idx == -1: break
    cnt = 0
    for j, c in enumerate(body[idx:]):
        if c == '(': cnt += 1
        elif c == ')':
            cnt -= 1
            if cnt == 0:
                sym_blocks.append(body[idx:idx+j+1])
                pos = idx + j + 1
                break

sb = sym_blocks[2]
test_content = f"{header}\n  {sb}\n{footer}"
print("=== FILE TESTED FOR J1 ===")
print(test_content)
