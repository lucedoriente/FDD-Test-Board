import os

fp_dir = r"C:\Program Files\KiCad\9.0\share\kicad\footprints"

# Find rotary encoder
re_path = os.path.join(fp_dir, "Rotary_Encoder.pretty")
if os.path.exists(re_path):
    fps = [f for f in os.listdir(re_path) if "PEC11" in f or "Bourns" in f]
    print("Rotary Encoder footprints:", fps)

# Find buzzer
bz_path = os.path.join(fp_dir, "Buzzer_Beeper.pretty")
if os.path.exists(bz_path):
    fps = [f for f in os.listdir(bz_path) if "12" in f or "7.62" in f]
    print("Buzzer footprints:", fps)
