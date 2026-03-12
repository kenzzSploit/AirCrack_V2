import subprocess
import os

def start_capture(interface, bssid, channel, output_dir="reports/"):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, bssid.replace(":", ""))
    
    cmd = [
        "airodump-ng", 
        interface, 
        "--bssid", bssid, 
        "-c", channel, 
        "-w", output_path
    ]
    
    print(f"[*] Capturing handshake for {bssid} on channel {channel}...")
    print(f"[*] Output file: {output_path}-01.cap")
    
    try:
        # This runs in foreground. The Ruby CLI might background this or run it in a separate thread.
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n[*] Capture stopped.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", required=True)
    parser.add_argument("-b", "--bssid", required=True)
    parser.add_argument("-c", "--channel", required=True)
    args = parser.parse_args()
    
    start_capture(args.interface, args.bssid, args.channel)