import pcbnew

print("Has UpdateBoard?", hasattr(pcbnew, "UpdateBoard"))
print("Has LoadNetlist?", hasattr(pcbnew, "LoadNetlist"))
print("Has SCH_EMBED?", hasattr(pcbnew, "SCH_EMBED"))
for attr in dir(pcbnew):
    if "Update" in attr or "Netlist" in attr:
        print("  Found:", attr)
