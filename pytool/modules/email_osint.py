import sys
import hashlib
import requests
import dns.resolver
from colorama import Fore, Style

def check_gravatar(email):
    """
    Checks if the email has a Gravatar profile.
    """
    print(f"\n{Fore.CYAN}[*] Checking Gravatar...{Style.RESET_ALL}")
    email_hash = hashlib.md5(email.lower().strip().encode('utf-8')).hexdigest()
    url = f"https://www.gravatar.com/avatar/{email_hash}?d=404"
    profile_url = f"https://en.gravatar.com/{email_hash}.json"
    
    try:
        r = requests.get(url)
        if r.status_code == 200:
            print(f"{Fore.GREEN}[+] Gravatar Found!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}    -> Image: {url}{Style.RESET_ALL}")
            
            # Try to fetch profile info
            r_profile = requests.get(profile_url, headers={'User-Agent': 'Mozilla/5.0'})
            if r_profile.status_code == 200:
                data = r_profile.json()
                entry = data['entry'][0]
                if 'preferredUsername' in entry:
                    print(f"{Fore.GREEN}    -> Username: {entry['preferredUsername']}{Style.RESET_ALL}")
                if 'displayName' in entry:
                    print(f"{Fore.GREEN}    -> Name: {entry['displayName']}{Style.RESET_ALL}")
                if 'aboutMe' in entry:
                    print(f"{Fore.GREEN}    -> About: {entry['aboutMe']}{Style.RESET_ALL}")
                if 'currentLocation' in entry:
                    print(f"{Fore.GREEN}    -> Location: {entry['currentLocation']}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[-] No Gravatar found.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Gravatar Check Error: {e}{Style.RESET_ALL}")

def check_emailrep(email):
    """
    Checks reputation via EmailRep.io (Free tier).
    """
    print(f"\n{Fore.CYAN}[*] Checking EmailRep.io (Reputation & Data)...{Style.RESET_ALL}")
    url = f"https://emailrep.io/{email}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            
            reputation = data.get('reputation', 'unknown')
            suspicious = data.get('suspicious', False)
            references = data.get('references', 0)
            
            if suspicious:
                print(f"{Fore.RED}[!] STATUS: SUSPICIOUS{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}[+] STATUS: CLEAN{Style.RESET_ALL}")
                
            print(f"{Fore.CYAN}    -> Reputation: {reputation}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}    -> Web References: {references}{Style.RESET_ALL}")
            
            details = data.get('details', {})
            if details.get('blacklisted'):
                print(f"{Fore.RED}    -> Blacklisted: YES{Style.RESET_ALL}")
            if details.get('malicious_activity'):
                print(f"{Fore.RED}    -> Malicious Activity: YES{Style.RESET_ALL}")
            if details.get('data_breach'):
                print(f"{Fore.RED}    -> Data Breach: YES{Style.RESET_ALL}")
            if details.get('spam'):
                print(f"{Fore.RED}    -> Spam: YES{Style.RESET_ALL}")
                
        elif r.status_code == 429:
            print(f"{Fore.YELLOW}[!] EmailRep.io Rate Limit exceeded.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] EmailRep API Error: {r.status_code}{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"{Fore.RED}[!] EmailRep Error: {e}{Style.RESET_ALL}")

def check_disposable(email):
    """
    Checks if the domain is a disposable email provider.
    """
    print(f"\n{Fore.CYAN}[*] Checking for Disposable Email Domain...{Style.RESET_ALL}")
    domain = email.split('@')[-1]
    # Using a known public API for this or a list. 
    # disify.com API is simple and free.
    url = f"https://disify.com/api/email/{email}"
    
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            disposable = data.get('disposable', False)
            dns_valid = data.get('dns', True)
            
            if disposable:
                print(f"{Fore.RED}[!] WARNING: This is a DISPOSABLE email address!{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}[+] Domain is not a known disposable provider.{Style.RESET_ALL}")
            
            if not dns_valid:
                print(f"{Fore.RED}[!] DNS lookup failed for this domain.{Style.RESET_ALL}")
                
        else:
            # Fallback if API fails
            pass
    except Exception:
        pass

def check_mx_record(email):
    """
    Checks if the domain of the email has valid MX records.
    """
    domain = email.split('@')[-1]
    print(f"\n{Fore.CYAN}[*] Checking DNS MX records for domain: {domain}...{Style.RESET_ALL}")
    
    try:
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = records[0].exchange
        mx_record = str(mx_record)
        print(f"{Fore.GREEN}[+] Valid MX Record found: {mx_record}{Style.RESET_ALL}")
        return True
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
        print(f"{Fore.RED}[-] No valid MX records found for {domain}. Email likely invalid.{Style.RESET_ALL}")
        return False
    except Exception as e:
        print(f"{Fore.RED}[!] DNS Check Error: {e}{Style.RESET_ALL}")
        return False

def run_holehe_scan(email):
    """
    Runs holehe to check registered accounts.
    We run the CLI version via subprocess as it is more stable across versions than importing internal functions.
    """
    print(f"\n{Fore.CYAN}[*] Running Holehe (Account Registration Check)...{Style.RESET_ALL}")

    import subprocess
    
    try:
        # Run holehe via our wrapper script or the installed script if available.
        # Since python -m holehe fails (no __main__.py), we use a runner pattern.
        # We will assume 'holehe' command is in the path or we construct a call.
        
        # First try calling 'holehe' directly as a command
        cmd = ["holehe", email, "--only-used", "--no-color"]
        
        # If that might fail due to path, we can try importing and running via a script string
        # cmd = [sys.executable, "-c", "from holehe.core import main; main()", email, "--only-used", "--no-color"]
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        print(f"{Fore.YELLOW}[!] Scanning 120+ sites... please wait.{Style.RESET_ALL}")
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                # Format output
                if "[+]" in output:
                    print(f"{Fore.GREEN}{output.strip()}{Style.RESET_ALL}")
                elif "[-]" in output:
                    # Optional: hide negatives to reduce noise
                    pass 
                else:
                    print(output.strip())
                    
    except Exception as e:
        print(f"{Fore.RED}[!] Error running Holehe: {e}{Style.RESET_ALL}")

def run_email_lookup():
    print(f"{Fore.BLUE}--- MULTI-TOOL EMAIL SCANNER ---{Style.RESET_ALL}")
    email = input("Enter email address: ")
    
    if "@" not in email:
        print(f"{Fore.RED}Invalid email format.{Style.RESET_ALL}")
        return

    # Step 1: DNS/MX Check
    mx_valid = check_mx_record(email)
    
    # Step 2: Gravatar Check
    check_gravatar(email)
    
    # Step 3: EmailRep Check
    check_emailrep(email)
    
    # Step 4: Disposable Check
    check_disposable(email)

    # Step 5: Holehe Check
    if mx_valid:
        run_holehe_scan(email)
    else:
        print(f"{Fore.YELLOW}[!] Skipping Account Check due to invalid domain.{Style.RESET_ALL}")
        choice = input("Force check anyway? (y/N): ")
        if choice.lower() == 'y':
            run_holehe_scan(email)

    print(f"\n{Fore.BLUE}--- SCAN COMPLETE ---{Style.RESET_ALL}")
