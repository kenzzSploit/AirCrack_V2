import subprocess
import os

def crack_handshake(cap_file, wordlist, bssid=None):
    if not os.path.exists(wordlist):
        print(f"[!] Wordlist not found: {wordlist}")
        return None

    cmd = ["aircrack-ng", "-w", wordlist, cap_file]
    if bssid:
        cmd.extend(["-b", bssid])
        
    print(f"[*] Cracking {cap_file} using {wordlist}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if "KEY FOUND!" in result.stdout:
        # Extract key
        try:
            key_part = result.stdout.split("KEY FOUND! [")[1].split("]")[0]
            return key_part.strip()
        except IndexError:
            return "Found, but parsing failed."
    else:
        return None

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required=True)
    parser.add_argument("-w", "--wordlist", required=True)
    parser.add_argument("-b", "--bssid")
    args = parser.parse_args()
    
    key = crack_handshake(args.file, args.wordlist, args.bssid)
    if key:
        print(f"[+] Password Found: {key}")
    else:
        print("[-] Password not found.")