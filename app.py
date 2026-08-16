import urllib.request
import json

print("🌐 IP Checker Tool")
print("-" * 40)

# იღებს IP მისამართს მომხმარებლისგან
target_ip = input("👤 Enter target IP address (or press Enter for default): ").strip()

# თუ არაფერი ჩაწერე, შეამოწმებს მიმდინარე სერვერს, თუ ჩაწერე - იმ IP-ს
if target_ip:
    url = f"http://ip-api.com/json/{target_ip}"
else:
    url = "http://ip-api.com/json/"

try:
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode())

    if data.get("status") == "fail":
        print(f"❌ Error: {data.get('message', 'Invalid IP address')}")
    else:
        print("\n✅ IP Information:")
        print(f"🌐 IP: {data.get('query')}")
        print(f"📍 Country: {data.get('country')}")
        print(f"🏙️ City: {data.get('city')}")
        print(f"🏢 Provider: {data.get('isp')}")

except Exception as e:
    print(f"❌ Connection error: {e}")
    # ==========================================
# 🌐 New Function: Check Website IP Details
# ==========================================
def check_website_ip(domain_name):
    import socket
    import urllib.request
    import json
    
    # Extract clean domain name (e.g., convert "https://google.com/path" to "google.com")
    clean_domain = domain_name.replace("https://", "").replace("http://", "").split("/")[0]
    
    try:
        # Resolve domain name to IP address
        site_ip = socket.gethostbyname(clean_domain)
        print(f"\n🌐 Target Domain: {clean_domain}")
        print(f"🎯 Resolved IP: {site_ip}")
        
        # Fetch IP information from ip-api.com
        api_url = f"http://ip-api.com/json/{site_ip}"
        req = urllib.request.urlopen(api_url)
        res_data = json.loads(req.read().decode())
        
        if res_data.get("status") == "fail":
            print(f"❌ Error: {res_data.get('message')}")
        else:
            print("📊 Website Server Details:")
            print(f"📍 Country: {res_data.get('country')}")
            print(f"🏙️ City: {res_data.get('city')}")
            print(f"🏢 Provider/ISP: {res_data.get('isp')}")
            print(f"🏢 Organization: {res_data.get('org')}")
            
    except Exception as err:
        print(f"❌ Failed to resolve website IP: {err}")

# Example usage:
# target_website = input("Enter website address (e.g. google.com): ")
# check_website_ip(target_website)
# ==========================================
# 🎮 ტერმინალის მენიუში გამოძახება
# ==========================================
while True:
    command = input("\n👤 Enter command (ip / location / hack / site / exit): ").strip().lower()
    if command == "site":
        target = input("Enter website address (e.g. google.com): ")
        check_website_ip(target)
    elif command == "ip":
        target = input("Enter IP address to check (or press Enter for default): ").strip()
        check_website_ip(target if target else "api.ipify.org")
    elif command == "location":
        print("Location feature called!")
    elif command == "hack":
        import time
        print("⚡ Simulation starting...")
        for i in range(1, 101, 20):
            print(f"Loading data... {i}%")
            time.sleep(0.5)
        print("✅ Simulation complete! (No real action taken)")
    elif command == "exit":
        print("Goodbye!")
        break
    else:
        print("❌ Unknown command! Try: ip, location, hack, site, or exit.")