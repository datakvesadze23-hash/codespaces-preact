import socket
# 1. მომხმარებლისგან მონაცემების მიღება
target_host = input("შეიყვანე სამიზნე საიტი ან IP (მაგ: scanme.nmap.org): ")
start_port = int(input("საწყისი პორტი (მაგ: 1): "))
end_port = int(input("საბოლოო პორტი (მაგ: 100): "))

print(f"\n[+] იწყება {target_host}-ის სკანირება ({start_port}-დან {end_port}-მდე)...\n")

# 2. პორტების შემოწმება
for port in range(start_port, end_port + 1):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(0.5)
    
    result = client.connect_ex((target_host, port))
    
    if result == 0:
        print(f"[+] Port {port:<5} is OPEN! 🟢")
        
    client.close()

print("\n[✓] სკანირება დასრულდა! 🚀")