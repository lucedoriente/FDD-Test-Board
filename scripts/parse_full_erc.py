with open("FDD-Test-Board-erc.rpt", "r", encoding="utf-8") as f:
    text = f.read()

import re
errors = re.findall(r'\[([^\]]+)\]: (.*?)\n\s+;\s*(error|warning)', text)
print(f"Total ERC findings: {len(errors)}")
import collections
counts = collections.defaultdict(lambda: collections.defaultdict(int))
for code, desc, sev in errors:
    counts[sev][code] += 1

print("\nErrors:")
for code, c in counts['error'].items():
    print(f"  {code}: {c}")

print("\nWarnings:")
for code, c in counts['warning'].items():
    print(f"  {code}: {c}")
