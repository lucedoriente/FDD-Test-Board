import os
from test_clean_flatten import extract_raw, get_flattened

raw = extract_raw("Transistor_BJT", "2N3904")
flat = get_flattened("Transistor_BJT", "2N3904")

print("--- RAW 2N3904 ---")
print(raw)
print("--- FLATTENED 2N3904 ---")
print(flat)
