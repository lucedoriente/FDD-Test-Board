import build_zero_erc_fdd as bz

for k, v in bz.net_map_s2.items():
    if k[0] == "C1":
        print(k, "->", v)
