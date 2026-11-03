import os

test_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\test_single"
with open(os.path.join(test_dir, "sub.kicad_sch"), "r") as f:
    sub_j1 = f.read()

print("sub_j1 in bisect_s1_step1:")
print(sub_j1[:500])
print("\nUUID of sub_j1 at line 5:")
print(sub_j1.splitlines()[4])

# Now what was header in test_each_body_sym?
with open(os.path.join(test_dir, "01_Power_Supply.kicad_sch"), "r") as f:
    ps = f.read()

print("\nUUID of 01_Power_Supply at line 5:")
print(ps.splitlines()[4])
