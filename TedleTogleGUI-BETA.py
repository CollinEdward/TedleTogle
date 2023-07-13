import os
import sys
import socket
import tkinter as tk
from tkinter import ttk
from colorama import init, Fore, Style
import time

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


    def resolve_ip_to_domain(ip_address):
        try:
            domain_name = socket.gethostbyaddr(ip_address)[0]
            return domain_name
        except socket.herror:
            return "Unable to resolve domain for the given IP."

    def start_scan():
        target_ip = target_entry.get()
        domain_name = resolve_ip_to_domain(target_ip)
        domain_label.config(text=f"Domain name: {domain_name}", foreground="blue")

        scan_choice = scan_var.get()

        if scan_choice == 0:
            return

        if scan_choice == 8:
            custom_args = custom_entry.get()
            scan_args = custom_args
            scan_type = "custom"
        else:
            scan_args = scan_options[scan_choice][1]
            scan_type = scan_options[scan_choice][0]

        scan_command = f"nmap {scan_args} {target_ip}"
        scan_output = os.popen(scan_command).read()

        file_name = f"{target_ip}_{scan_type}.txt"
        with open(file_name, 'w') as file:
            file.write(scan_output)

        result_label.config(text=f"Scan results saved to {file_name}", foreground="green")

    def exit_app():
        root.destroy()

    root = tk.Tk()
    root.title("Nmap Scan")
    root.geometry("400x400")

    target_label = ttk.Label(root, text="Enter the target IP address or range:")
    target_label.pack()

    target_entry = ttk.Entry(root)
    target_entry.pack()

    domain_label = ttk.Label(root)
    domain_label.pack()

    scan_options = [
        ("TCP SYN Scan (-sS)", "-sS", "tcp_syn"),
        ("UDP Scan (-sU)", "-sU", "udp"),
        ("Service Version Scan (-sV)", "-sV", "service_version"),
        ("OS Detection Scan (-O)", "-O", "os_detection"),
        ("Aggressive Scan (-A)", "-A", "aggressive"),
        ("Port Range Scan (-p <number-number>)", "-p", "port_range"),
        ("Vulnerability Scan (--script vuln)", "--script vuln", "vulnerability"),
        ("Custom Scan", "", "custom"),
    ]

    scan_var = tk.IntVar()
    scan_var.set(0)

    scan_frame = ttk.Frame(root)
    scan_frame.pack(pady=10)

    scan_label = ttk.Label(scan_frame, text="Scan Options:")
    scan_label.pack()

    for i, option in enumerate(scan_options):
        option_radio = ttk.Radiobutton(scan_frame, text=option[0], variable=scan_var, value=i+1)
        option_radio.pack(anchor=tk.W)

    custom_entry = ttk.Entry(root)
    custom_entry.pack()

    scan_button = ttk.Button(root, text="Start Scan", command=start_scan)
    scan_button.pack(pady=10)

    result_label = ttk.Label(root)
    result_label.pack()

    exit_button = ttk.Button(root, text="Exit", command=exit_app)
    exit_button.pack(pady=10)

    root.mainloop()

run_nmap_scan()
