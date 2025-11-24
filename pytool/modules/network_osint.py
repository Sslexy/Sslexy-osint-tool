import whois
import requests
import socket
from colorama import Fore, Style

def get_ip_location(ip_address):
    print(f"\n{Fore.CYAN}[*] Geo-locating IP: {ip_address}...{Style.RESET_ALL}")
    try:
        # Using ip-api.com (free, no key required for basic usage)
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        data = response.json()
        
        if data['status'] == 'fail':
            print(f"{Fore.RED}[-] API Error: {data['message']}{Style.RESET_ALL}")
            return

        print(f"{Fore.GREEN}[+] Country: {data.get('country')}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] Region: {data.get('regionName')}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] City: {data.get('city')}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] ISP: {data.get('isp')}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] Coordinates: {data.get('lat')}, {data.get('lon')}{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}[!] Geolocation Error: {e}{Style.RESET_ALL}")

def get_whois_info(domain):
    print(f"\n{Fore.CYAN}[*] Running WHOIS lookup for: {domain}...{Style.RESET_ALL}")
    try:
        w = whois.whois(domain)
        print(f"{Fore.GREEN}[+] Registrar: {w.registrar}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] Creation Date: {w.creation_date}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] Expiration Date: {w.expiration_date}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] Name Servers: {w.name_servers}{Style.RESET_ALL}")
        if w.emails:
            print(f"{Fore.GREEN}[+] Emails: {w.emails}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] WHOIS Error: {e}{Style.RESET_ALL}")

def resolve_domain(domain):
    try:
        ip = socket.gethostbyname(domain)
        print(f"{Fore.GREEN}[+] Domain {domain} resolves to {ip}{Style.RESET_ALL}")
        return ip
    except socket.gaierror:
        print(f"{Fore.RED}[-] Could not resolve domain.{Style.RESET_ALL}")
        return None

def run_network_lookup():
    print(f"{Fore.BLUE}--- NETWORK / IP OSINT ---{Style.RESET_ALL}")
    target = input("Enter Domain or IP address: ")
    
    # Check if input is IP or Domain
    is_ip = False
    try:
        socket.inet_aton(target)
        is_ip = True
    except socket.error:
        is_ip = False

    ip = target
    if not is_ip:
        get_whois_info(target)
        ip = resolve_domain(target)
    
    if ip:
        get_ip_location(ip)

    # Subdomain Enumeration for domains
    if not is_ip:
        run_subdomain_scan(target)

    print(f"\n{Fore.BLUE}--- SCAN COMPLETE ---{Style.RESET_ALL}")

def run_subdomain_scan(domain):
    print(f"\n{Fore.CYAN}[*] Running Passive Subdomain Enumeration (DNS)...{Style.RESET_ALL}")
    
    # Basic list of common subdomains to check
    subdomains = [
        "www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "ns1", "web", "test",
        "dev", "admin", "forum", "blog", "email", "vpn", "cloud", "api", "app", "m", "shop",
        "secure", "demo", "portal", "support", "wiki", "docs"
    ]
    
    found_subdomains = []
    
    for sub in subdomains:
        url = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(url)
            print(f"{Fore.GREEN}[+] Found: {url} -> {ip}{Style.RESET_ALL}")
            found_subdomains.append(url)
        except socket.gaierror:
            pass
        except Exception:
            pass
    
    if not found_subdomains:
        print(f"{Fore.YELLOW}[-] No common subdomains found via basic DNS check.{Style.RESET_ALL}")
