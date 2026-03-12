import subprocess
import sys

def sniff_packets(interface, output_file, channel=None):
    """Generic packet sniffer."""
    cmd = ["airodump-ng", interface, "-w", output_file]
    if channel:
        cmd.extend(["-c", str(channel)])
    
    print(f"[*] Sniffing on {interface}... Writing to {output_file}-01.cap")
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n[*] Stopped sniffing.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", required=True)
    parser.add_argument("-o", "--output", default="sniff_capture")
    parser.add_argument("-c", "--channel", type=int)
    args = parser.parse_args()
    
    sniff_packets(args.interface, args.output, args.channel)