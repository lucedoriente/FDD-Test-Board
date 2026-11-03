import build_zero_erc_fdd as bz

print("Search for +24V in S4:")
for k, v in bz.net_map_s4.items():
    if "24" in v or "12" in v:
        print(" ", k, "->", v)

print("\nSearch for USART in S2:")
for k, v in bz.net_map_s2.items():
    if "USART" in v or "UART" in v or "TX" in v or "RX" in v:
        print(" ", k, "->", v)

print("\nSearch for +5V in S2:")
for k, v in bz.net_map_s2.items():
    if "5V" in v:
        print(" ", k, "->", v)
