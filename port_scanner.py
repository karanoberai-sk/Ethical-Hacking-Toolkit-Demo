#!/usr/bin/env python3

# --- Tool 2: Fast Port Scanner ---
# No external libraries needed. Uses built-in 'socket'.

import socket
import sys
from datetime import datetime

def scan_ports(target_ip, port_range):
    """
    Scans a target IP for open ports within a specified range.
    """
    
    print(f"[+] Scanning target: {target_ip}")
    print(f"[+] Time started: {datetime.now()}")
    print("-" * 50)
    
    open_ports = []
    
    try:
        for port in port_range:
            # Create a new socket object
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Set a timeout for the connection attempt
            socket.setdefaulttimeout(0.5)
            
            # Try to connect
            result = sock.connect_ex((target_ip, port))
            
            if result == 0:
                # If connect_ex returns 0, the port is open
                print(f"[✓] Port {port} is OPEN")
                open_ports.append(port)
            
            # Close the socket
            sock.close()

    except socket.gaierror:
        print(f"[!] Error: Hostname '{target_ip}' could not be resolved.")
        return
    except socket.error:
        print(f"[!] Error: Couldn't connect to server.")
        return
    except KeyboardInterrupt:
        print("\n[-] Exiting scan (User interruption).")
        sys.exit()

    print("-" * 50)
    print(f"[+] Scan complete. Found {len(open_ports)} open ports.")
    if open_ports:
        print(f"[+] Open ports: {open_ports}")

# --- Main execution ---
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("\n[+] USAGE:")
        print(f"    python {sys.argv[0]} example.com")
        print("    (This will scan the most common 20 ports)")
    else:
        target_name = sys.argv[1]
        try:
            # Resolve the domain name to an IP address
            target_ip_addr = socket.gethostbyname(target_name)
        except socket.gaierror:
            print(f"[!] Error: Cannot resolve '{target_name}'. Check the hostname.")
            sys.exit()
            
        # List of common ports to scan
        common_ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443]
        
        scan_ports(target_ip_addr, common_ports)
