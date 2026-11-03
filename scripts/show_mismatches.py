with open("FDD-Test-Board-erc.rpt", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = re.findall(r'\[lib_symbol_mismatch\].*?\n\s+;.*?\n\s+@\(.*?\):.*?\n', text)
for m in matches[:10]:
    print(m)
