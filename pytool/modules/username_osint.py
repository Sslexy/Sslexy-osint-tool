import requests
import sys
from colorama import Fore, Style
import concurrent.futures

# Try to import sherlock. Since it is installed as sherlock-project, but the module might be different.
try:
    from sherlock_project import sherlock
except ImportError:
    try:
        import sherlock
    except ImportError:
        print(f"{Fore.RED}[!] Sherlock module not found. Please install it via pip.{Style.RESET_ALL}")
        sherlock = None

def custom_fast_check(username):
    """
    A simple custom checker to demonstrate 'combining' tools.
    It checks a few major sites manually, simulating a second opinion.
    """
    print(f"\n{Fore.MAGENTA}[+] Running Secondary Fast-Check (Custom Module)...{Style.RESET_ALL}")
    
    sites = {
        "GitHub": f"https://github.com/{username}",
        "Instagram": f"https://www.instagram.com/{username}/",
        "Twitter/X": f"https://twitter.com/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "Facebook": f"https://www.facebook.com/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Pinterest": f"https://www.pinterest.com/{username}/",
        "Telegram": f"https://t.me/{username}",
        "Steam": f"https://steamcommunity.com/id/{username}",
        "Twitch": f"https://www.twitch.tv/{username}",
        "SoundCloud": f"https://soundcloud.com/{username}",
        "Medium": f"https://medium.com/@{username}",
        "Vimeo": f"https://vimeo.com/{username}",
        "Patreon": f"https://www.patreon.com/{username}",
        "About.me": f"https://about.me/{username}",
        "Flickr": f"https://www.flickr.com/people/{username}",
        "Wikipedia": f"https://en.wikipedia.org/wiki/User:{username}",
        "HackerNews": f"https://news.ycombinator.com/user?id={username}",
    }
    
    found = []
    
    def check_site(name, url):
        try:
            # Simple status check - note: this is basic and can have false positives depending on the site
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=headers, timeout=5)
            if r.status_code == 200:
                return f"{Fore.GREEN}[+] {name}: Found at {url}{Style.RESET_ALL}"
            elif r.status_code == 404:
                return f"{Fore.RED}[-] {name}: Not found{Style.RESET_ALL}"
            else:
                return f"{Fore.YELLOW}[?] {name}: Status {r.status_code}{Style.RESET_ALL}"
        except Exception as e:
            return f"{Fore.RED}[!] {name}: Error {e}{Style.RESET_ALL}"

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_site = {executor.submit(check_site, name, url): name for name, url in sites.items()}
        for future in concurrent.futures.as_completed(future_to_site):
            print(future.result())

def run_sherlock_scan(username):
    if not sherlock:
        return
    
    print(f"\n{Fore.CYAN}[*] Running Sherlock Scan for '{username}'...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[!] This may take a while depending on the number of sites.{Style.RESET_ALL}")
    
    # Sherlock's main function usually takes arguments via sys.argv or ArgumentParser.
    # To run it programmatically without subprocessing sys.argv, we might need to look at how 'main' works.
    # However, creating a subprocess is often safer for CLI tools to avoid messing with global state.
    
    import subprocess
    try:
        # We assume 'sherlock' command is available in path since we installed sherlock-project
        # Or we call it via python -m. Note: The package is 'sherlock-project' but the module is often 'sherlock'.
        # We try 'sherlock' first.
        cmd = [sys.executable, "-m", "sherlock", username, "--timeout", "5", "--print-found"]
        
        # We stream output to show progress
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                # Colorize sherlock output if it isn't already
                if "[+]" in output:
                    print(f"{Fore.GREEN}{output.strip()}{Style.RESET_ALL}")
                else:
                    print(output.strip())
        
        rc = process.poll()
        if rc != 0:
            # If the module approach fails, try the library call (more complex due to arg parsing)
            pass

    except Exception as e:
        print(f"{Fore.RED}[!] Error running Sherlock: {e}{Style.RESET_ALL}")

def run_username_lookup():
    print(f"{Fore.BLUE}--- MULTI-TOOL USERNAME SCANNER ---{Style.RESET_ALL}")
    username = input("Enter username to search: ")
    
    if not username:
        print("Username cannot be empty.")
        return

    # Tool 1: Custom Fast Check
    custom_fast_check(username)
    
    # Tool 2: Sherlock
    run_sherlock_scan(username)
    
    print(f"\n{Fore.BLUE}--- SCAN COMPLETE ---{Style.RESET_ALL}")

if __name__ == "__main__":
    run_username_lookup()
