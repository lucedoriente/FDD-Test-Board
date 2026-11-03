"""
Retro-Diag FDD Master Tester & Exerciser - PC Control Suite Launcher
Author: Alessio Iodice <alessio67@gmail.com>
License: CC BY-NC-SA 4.0
KiCad 9.0 Verified Architecture
"""

import os
import sys
import webbrowser
import http.server
import socketserver
import threading
import subprocess

PORT = 8088
HTML_FILE = "fdd_pc_control_suite.html"

def list_windows_com_ports():
    """List available serial COM ports on Windows using registry or mode command."""
    ports = []
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DEVICEMAP\SERIALCOMM")
        i = 0
        while True:
            try:
                name, val, _ = winreg.EnumValue(key, i)
                ports.append(val)
                i += 1
            except WindowsError:
                break
        winreg.CloseKey(key)
    except Exception:
        pass
    return sorted(ports)

def start_server():
    web_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(web_dir)
    
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass # Quiet console

    with socketserver.TCPServer(("127.0.0.1", PORT), QuietHandler) as httpd:
        print(f"[*] Local HTTP server listening at http://127.0.0.1:{PORT}/")
        httpd.serve_forever()

def main():
    print("=" * 60)
    print("  Retro-Diag FDD Master Tester - PC Control Suite")
    print("  Author: Alessio Iodice <alessio67@gmail.com>")
    print("=" * 60)
    
    com_ports = list_windows_com_ports()
    if com_ports:
        print(f"[+] Porte Seriali COM rilevate su Windows: {', '.join(com_ports)}")
    else:
        print("[-] Nessuna porta COM fisica attiva rilevata (il dispositivo puo' essere simulato in Demo Mode)")
        
    suite_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), HTML_FILE)
    if not os.path.exists(suite_path):
        print(f"[!] ERRORE: File {HTML_FILE} non trovato in {os.path.dirname(suite_path)}")
        sys.exit(1)

    url = f"http://127.0.0.1:{PORT}/{HTML_FILE}"
    
    # Start web server in background daemon thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    print(f"[*] Apertura browser di sistema su: {url}")
    print("[*] Premi Ctrl+C in questa finestra per arrestare il server locale.")
    print("=" * 60)
    webbrowser.open(url)
    
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Arresto server completato.")

if __name__ == "__main__":
    main()
