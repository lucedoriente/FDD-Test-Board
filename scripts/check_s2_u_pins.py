import build_zero_erc_fdd as bz

print("U6 net map:")
for k, v in bz.net_map_s2.items():
    if k[0] == "U6":
        print(" ", k, "->", v)

print("LMV358 net map:")
for k, v in bz.net_map_s2.items():
    if k[0] == "U7":
        print(" ", k, "->", v)
