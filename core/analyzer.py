import subprocess
import json
import os

def analyze_cap(file_path):
    """Analyze capture file for handshakes."""
    if not os.path.exists(file_path):
        return {"error": "File not found"}
        
    cmd = ["aircrack-ng", file_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    output = result.stdout
    handshakes = []
    
    # Simple parsing of aircrack-ng output
    if "1 handshake" in output:
        lines = output.split('\n')
        for line in lines:
            if " handshake" in line:
                parts = line.split()
                bssid = parts[1]
                handshakes.append(bssid)
                
    return {
        "file": file_path,
        "handshakes_found": len(handshakes) > 0,
        "targets": handshakes
    }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required=True)
    args = parser.parse_args()
    
    data = analyze_cap(args.file)
    print(json.dumps(data))