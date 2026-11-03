import os, subprocess, re

cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"
sch = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board.kicad_sch"
net = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board.net"

res_erc = subprocess.run([cli, "sch", "erc", "--severity-all", sch], capture_output=True, text=True)
print("--- ERC OUTPUT ---")
print(res_erc.stdout.strip())
if res_erc.stderr.strip():
    print("ERC STDERR:", res_erc.stderr.strip())

res_net = subprocess.run([cli, "sch", "export", "netlist", "--output", net, sch], capture_output=True, text=True)
print("--- NETLIST EXPORT ---")
print(res_net.stdout.strip())
if res_net.stderr.strip():
    print("NETLIST STDERR:", res_net.stderr.strip())

if os.path.exists(net):
    with open(net, "r", encoding="utf-8") as f:
        content = f.read()
    comps = re.findall(r'\(comp \(ref "([^"]+)"\)', content)
    nets = re.findall(r'\(net \(code \d+\) \(name "([^"]+)"\)', content)
    print(f"Netlist exported: {len(comps)} components, {len(nets)} nets!")
    if len(comps) > 0:
        print("First 10 components:", comps[:10])
