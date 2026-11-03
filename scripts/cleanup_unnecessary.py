"""
Cleanup unnecessary temporary and test files
Retro-Diag FDD Master Tester & Exerciser
Author: Alessio Iodice <alessio67@gmail.com>
"""

import os
import shutil

LOCATIONS = [
    r"c:\Users\aless\.gemini\antigravity\scratch\FDD_Tester",
    r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester"
]

def clean_location(base):
    print(f"\nCleaning location: {base}")
    if not os.path.exists(base):
        return

    # 1. Clean root temporary reports
    for item in os.listdir(base):
        item_path = os.path.join(base, item)
        if os.path.isfile(item_path):
            if item.endswith(('.rpt', '.json.rpt', '.dsn.rpt', '.log')) and 'catalog' not in item:
                print(f"  Removing root report: {item}")
                os.remove(item_path)
        elif os.path.isdir(item_path):
            if item in ['_norton_', '__pycache__', '.pytest_cache']:
                print(f"  Removing temp dir: {item}")
                shutil.rmtree(item_path, ignore_errors=True)

    # 2. Clean kicad directory
    kicad_dir = os.path.join(base, "kicad")
    if os.path.exists(kicad_dir):
        for root, dirs, files in os.walk(kicad_dir, topdown=False):
            # remove dirs
            for d in dirs:
                if d in ['test_export', 'test_single', '__pycache__'] or d.endswith('-backups'):
                    dp = os.path.join(root, d)
                    print(f"  Removing kicad test/backup dir: {dp}")
                    shutil.rmtree(dp, ignore_errors=True)
            # remove files
            for f in files:
                fp = os.path.join(root, f)
                if (f.startswith('test_') or 
                    'nozones' in f or 
                    f.endswith(('.rpt', '.ses', '.dsn', '.net', '.kicad_prl', '.lck', '.bak')) or
                    f in ['fp-info-cache', 'erc_main.json', 'drc_main.json', 'erc_ui.json', 'drc_ui.json']):
                    print(f"  Removing kicad temp/test file: {f}")
                    try:
                        os.remove(fp)
                    except Exception as e:
                        print(f"    Error removing {f}: {e}")

    # 3. Clean scripts directory (remove scratch test_*.py while keeping build/export scripts)
    scripts_dir = os.path.join(base, "scripts")
    if os.path.exists(scripts_dir):
        for item in os.listdir(scripts_dir):
            ip = os.path.join(scripts_dir, item)
            if os.path.isfile(ip):
                if item.startswith('test_') or item.endswith(('.pyc', '.pyo')):
                    print(f"  Removing obsolete test script: {item}")
                    os.remove(ip)
            elif os.path.isdir(ip) and item == '__pycache__':
                shutil.rmtree(ip, ignore_errors=True)

def main():
    for loc in LOCATIONS:
        clean_location(loc)
    print("\nCleanup finished successfully.")

if __name__ == "__main__":
    main()
