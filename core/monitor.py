import subprocess
import os
import sys

def check_root():
    if os.geteuid() != 0:
        print("[!] Error: This tool requires root privileges.")
        sys.exit(1)

def toggle_mode(interface, enable=True):
    """Enable or disable monitor mode."""
    check_root()
    try:
        if enable:
            subprocess.run(["airmon-ng", "check", "kill"], check=True, capture_output=True)
            subprocess.run(["airmon-ng", "start", interface], check=True, capture_output=True)
            mon_iface = interface + "mon"
            print(f"[+] Monitor mode enabled on {mon_iface}")
            return mon_iface
        else:
            subprocess.run(["airmon-ng", "stop", interface], check=True, capture_output=True)
            print(f"[-] Monitor mode disabled on {interface}")
            return interface.replace("mon", "")
    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to toggle mode: {e.stderr.decode().strip()}")
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", required=True)
    parser.add_argument("--stop", action="store_true", help="Stop monitor mode")
    args = parser.parse_args()
    
    toggle_mode(args.interface, enable=not args.stop)