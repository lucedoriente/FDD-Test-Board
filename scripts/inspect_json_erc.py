import json

with open("FDD-Test-Board-erc.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(json.dumps(data, indent=2))
