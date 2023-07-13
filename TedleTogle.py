import os
import time
import sys
from colorama import init, Fore, Style
import socket


init()

def print_banner():
    animation = r"""
  _____       _ _     _____          _     
 |_   _|__ __| | |___|_   _|__  __ _| |___ 
   | |/ -_) _` | / -_) | |/ _ \/ _` | / -_)
   |_|\___\__,_|_\___| |_|\___/\__, |_\___|
                              |___/        
    """
    for line in animation.splitlines():
        print(line)
        time.sleep(0.1)

def run_nmap_scan():
    print_banner()
    if os.geteuid() != 0:
        print(Fore.RED + "Please run the script with sudo privileges." + Style.RESET_ALL)
        return

    target_ip = input(Fore.YELLOW + "Enter the target IP address or range: " + Style.RESET_ALL)

    def resolve_ip_to_domain(ip_address):
        try:
            domain_name = socket.gethostbyaddr(ip_address)[0]
            return domain_name
        except socket.herror:
            return "Unable to resolve domain for the given IP."

    domain_name = resolve_ip_to_domain(target_ip)
    print(f"{Fore.BLUE}Domain name:", domain_name)

    print(Fore.RED + "\n*** WARNING: This script should not be used for any illegal activity. Use it responsibly and with proper authorization. ***\n" + Style.RESET_ALL)

    try:
        while True:
            print("\nScan Options:")
            print("1. " + Fore.YELLOW + "TCP SYN Scan (-sS)" + Style.RESET_ALL)
            print("2. " + Fore.YELLOW + "UDP Scan (-sU)" + Style.RESET_ALL)
            print("3. " + Fore.YELLOW + "Service Version Scan (-sV)" + Style.RESET_ALL)
            print("4. " + Fore.YELLOW + "OS Detection Scan (-O)" + Style.RESET_ALL)
            print("5. " + Fore.YELLOW + "Aggressive Scan (-A)" + Style.RESET_ALL)
            print("6. " + Fore.YELLOW + "Port Range Scan (-p <number-number>)" + Style.RESET_ALL)
            print("7. " + Fore.YELLOW + "Vulnerability Scan (--script vuln)" + Style.RESET_ALL)
            print("8. " + Fore.YELLOW + "Custom Scan" + Style.RESET_ALL)
            print("0. " + Fore.RED + "Exit" + Style.RESET_ALL)

            choice = input("Enter your choice: ")

            if choice == '1':
                scan_args = "-sS"
                scan_type = "tcp_syn"
            elif choice == '2':
                scan_args = "-sU"
                scan_type = "udp"
            elif choice == '3':
                scan_args = "-sV"
                scan_type = "service_version"
            elif choice == '4':
                scan_args = "-O"
                scan_type = "os_detection"
            elif choice == '5':
                scan_args = "-A"
                scan_type = "aggressive"
            elif choice == '6':
                port_range = input("Enter the port range (e.g., 1-1000): ")
                scan_args = f"-p {port_range}"
                scan_type = f"port_range_{port_range.replace('-', '_')}"
            elif choice == '7':
                scan_args = "--script vuln"
                scan_type = "vulnerability"
            elif choice == '8':
                scan_args = input("Enter custom scan arguments: ")
                scan_type = "custom"
            elif choice == '0':
                break
            else:
                print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)
                continue

            sub_scan_categories = {
                '1': ['-sZ', 'Zombie Scan'],
                '2': ['-f', 'Fragmentation Scan'],
                '3': ['-sA', 'ACK Scan'],
                '9': ['-sO', 'IP Protocol Scan'],
                '10': ['-sI', 'Idle Scan'],
                '11': ['-sW', 'TCP Window Scan'],
                '12': ['-b', 'FTP Bounce Scan'],
            }

            if choice in sub_scan_categories:
                sub_choice = choice
                print(f"\nSelected Scan: {sub_scan_categories[choice][1]}")
                include_sub_scan = input("Do you want to include this sub-scan? (y/n): ")
                if include_sub_scan.lower() == 'y':
                    scan_args += f" {sub_scan_categories[choice][0]}"
                    scan_type += f"_sub_{sub_choice}"

            scan_command = f"nmap {scan_args} {target_ip}"
            print(Fore.YELLOW + "\nRunning Nmap scan..." + Style.RESET_ALL)
            print(Fore.CYAN + "Scan in progress. Please wait..." + Style.RESET_ALL)
            scan_output = os.popen(scan_command).read()

            file_name = f"{target_ip}_{scan_type}.txt"
            with open(file_name, 'w') as file:
                file.write(scan_output)

            print(Fore.MAGENTA + f"\nScan {file_name}" + Fore.GREEN + " ======= DONE")

            print(Fore.GREEN + f"\nScan results saved to {file_name}" + Style.RESET_ALL)

    except KeyboardInterrupt:
        print(Fore.RED + "\nQuitting..." + Style.RESET_ALL)
        time.sleep(1)
        sys.exit()


run_nmap_scan()
