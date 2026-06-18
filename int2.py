import socket
from datetime import datetime

def scan_ports(target, ports):
    print(f"\nScanning {target}...")
    print("-" * 40)

    open_ports = []

    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        result = sock.connect_ex((target, port))

        if result == 0:
            print(f"Port {port}: OPEN")
            open_ports.append(port)

        sock.close()

    return open_ports

def generate_report(target, open_ports):
    filename = "vulnerability_report.txt"

    with open(filename, "w") as report:
        report.write("VULNERABILITY SCAN REPORT\n")
        report.write("=" * 30 + "\n")
        report.write(f"Target: {target}\n")
        report.write(f"Date: {datetime.now()}\n\n")

        if open_ports:
            report.write("Open Ports Found:\n")
            for port in open_ports:
                report.write(f"- Port {port}\n")
        else:
            report.write("No open ports detected.\n")

    print(f"\nReport saved as {filename}")

def main():
    target = input("Enter IP Address or Hostname: ")

    common_ports = [
        21,   # FTP
        22,   # SSH
        23,   # Telnet
        25,   # SMTP
        53,   # DNS
        80,   # HTTP
        110,  # POP3
        143,  # IMAP
        443,  # HTTPS
        3306  # MySQL
    ]

    open_ports = scan_ports(target, common_ports)
    generate_report(target, open_ports)

if __name__ == "__main__":
    main()
