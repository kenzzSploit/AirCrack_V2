import subprocess
import json
import time
import os

def scan_networks(interface, duration=15):
    """Scan for networks and return JSON output."""
    output_file = "/tmp/aircrack_scan"
    
    # Start airodump-ng in background
    cmd = ["airodump-ng", interface, "-w", output_file, "--output-format", "csv", "--write-interval", "1"]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    time.sleep(duration)
    proc.terminate()
    
    networks = []
    csv_path = f"{output_file}-01.csv"
    
    if os.path.exists(csv_path):
        with open(csv_path, 'r') as f:
            lines = f.readlines()
        
        # Parse CSV (skip header)
        for line in lines:
            if "Station MAC" in line: break # Stop when reaching client section
            if "BSSID" in line: continue
            
            parts = line.split(',')
            if len(parts) > 13:
                bssid = parts[0].strip()
                channel = parts[3].strip()
                essid = parts[13].strip()
                
                if bssid and essid:
                    networks.append({
                        "bssid": bssid, 
                        "channel": channel, 
                        "essid": essid
                    })
        
        os.remove(csv_path)
    
    return networks

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", required=True)
    parser.add_argument("-t", "--time", type=int, default=10)
    args = parser.parse_args()
    
    data = scan_networks(args.interface, args.time)
    print(json.dumps(data)) # Output JSON for Ruby CLI to parse