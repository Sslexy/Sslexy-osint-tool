import requests
import hashlib
from colorama import Fore, Style

def check_pwned_passwords(password):
    """
    Uses k-Anonymity model with HaveIBeenPwned API (no key required for passwords).
    We send the first 5 chars of the SHA1 hash.
    """
    print(f"\n{Fore.CYAN}[*] Checking password against breach database (safe method)...{Style.RESET_ALL}")
    
    sha1pass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5, tail = sha1pass[:5], sha1pass[5:]
    
    url = f"https://api.pwnedpasswords.com/range/{first5}"
    try:
        res = requests.get(url)
        if res.status_code != 200:
            print(f"{Fore.RED}[!] API Error: {res.status_code}{Style.RESET_ALL}")
            return

        hashes = (line.split(':') for line in res.text.splitlines())
        count = next((int(count) for t, count in hashes if t == tail), 0)
        
        if count > 0:
            print(f"{Fore.RED}[CRITICAL] Password found in {count} breaches! Change it immediately.{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}[+] Good news - password not found in known breaches.{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")

def check_email_breach(email):
    """
    Requires an API key for HIBP now. We will stub this and ask for a key.
    """
    print(f"\n{Fore.CYAN}[*] Checking email breaches (HIBP)...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[!] HIBP requires an API key for email searches.{Style.RESET_ALL}")
    api_key = input("Enter HIBP API Key (or press Enter to skip): ").strip()
    
    if not api_key:
        print(f"{Fore.YELLOW}Skipping email breach check.{Style.RESET_ALL}")
        return

    headers = {
        'hibp-api-key': api_key,
        'user-agent': 'Sslexy-Tool-1.0'
    }
    
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}?truncateResponse=false"
    
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            breaches = res.json()
            print(f"{Fore.RED}[!] FOUND IN {len(breaches)} BREACHES:{Style.RESET_ALL}")
            for b in breaches:
                print(f" - {Fore.MAGENTA}{b['Name']}{Style.RESET_ALL} (Date: {b['BreachDate']})")
        elif res.status_code == 404:
            print(f"{Fore.GREEN}[+] Email not found in breach database.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] API Error: {res.status_code} {res.text}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")

def run_breach_check():
    print(f"{Fore.BLUE}--- BREACH / LEAK CHECKER ---{Style.RESET_ALL}")
    print("1. Check Email")
    print("2. Check Password")
    choice = input("Select option: ")
    
    if choice == '1':
        email = input("Enter email: ")
        check_email_breach(email)
    elif choice == '2':
        password = input("Enter password to check: ")
        check_pwned_passwords(password)
    else:
        print("Invalid option.")
    
    print(f"\n{Fore.BLUE}--- SCAN COMPLETE ---{Style.RESET_ALL}")
