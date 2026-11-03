# Let's inspect git diff or check what changed in 02_MCU_Core
import subprocess

res = subprocess.run(["git", "diff", "kicad/02_MCU_Core.kicad_sch"], capture_output=True, text=True, cwd=r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester")
print("Git diff len:", len(res.stdout))
print(res.stdout[:1500])
