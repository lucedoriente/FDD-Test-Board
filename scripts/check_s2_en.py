import build_zero_erc_fdd as bz

for k, v in bz.net_map_s2.items():
    if v in ("EN_24V", "EN_12V", "EN_5V", "ISENSE_24V", "ISENSE_12V", "ISENSE_5V"):
        print(k, "->", v)
