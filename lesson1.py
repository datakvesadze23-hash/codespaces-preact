import socket
# 1. სამიზნე ჰოსტი
target_host = "scanme.nmap.org"

# 2. პორტების სია, რომელთა შემოწმებაც გვინდა
ports_to_scan = [21, 22, 80, 443, 8080]

print(f"Scanning {target_host} for multiple ports...\n")

# 3. თითოეული პორტის შემოწმება
for port in ports_to_scan:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(1)
    
    result = client.connect_ex((target_host, port))
    
    if result == 0:
        print(f"[+] Port {port:<5} is OPEN! 🟢")
    else:
        print(f"[-] Port {port:<5} is CLOSED. 🔴")
        
    client.close()