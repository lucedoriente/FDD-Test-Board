import re

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\02_MCU_Core.kicad_sch", "r", encoding="utf-8") as f:
    s2 = f.read()

wires = re.findall(r'\(wire \(pts \(xy ([0-9\.-]+) ([0-9\.-]+)\) \(xy ([0-9\.-]+) ([0-9\.-]+)\)\)[^\)]*\)', s2)
print("Total wires in Sheet 2:", len(wires))

# Let's trace connectivity from (71.12, 99.06)
adj = {}
for x1, y1, x2, y2 in wires:
    p1 = (float(x1), float(y1))
    p2 = (float(x2), float(y2))
    adj.setdefault(p1, []).append(p2)
    adj.setdefault(p2, []).append(p1)

start = (71.12, 99.06)
visited = set([start])
queue = [start]
while queue:
    curr = queue.pop(0)
    for nxt in adj.get(curr, []):
        if nxt not in visited:
            visited.add(nxt)
            queue.append(nxt)

print(f"Points connected to {start}: {len(visited)}")
for p in sorted(visited):
    print("  ", p)
