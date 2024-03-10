#!/usr/bin/env python

import socket
import concurrent.futures

OUT_FILE = "active_hosts.txt"

def scan_ip(ip, port):
    print(f"scanning {ip}:{port}...")
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  # Set a timeout for the connection attempt
        
        # Attempt to connect to the target IP and port
        result = s.connect_ex((ip, port))
        
        # Check if the connection was successful (port is open)
        if result == 0:
            print(f"Port {port} is open on {ip}")
            with open(OUT_FILE, "a+") as file:
                # Write some text to the file
                file.write(f"Port {port} is open on {ip}\n")

        # Close the socket
        s.close()
    except Exception as e:
        print(f"Error: {e}")

def scan_subnet(subnet, mask, port):
    with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
        # Generate a list of IP addresses in the subnet
        ips = [f"{subnet}.{i}.{j}" for i in range(0, 256) for j in range(0, 256)]
        if(mask == 24):
            ips = [f"{subnet}.{i}" for i in range(0, 256)]
        
        # Submit the scan_ip function to the thread pool for each IP address
        results = [executor.submit(scan_ip, ip, port) for ip in ips]

        # Wait for all tasks to complete
        for result in concurrent.futures.as_completed(results):
            pass

if __name__ == "__main__":
    subnet = "10.0"
    scan_subnet(subnet, 16, 31337)
