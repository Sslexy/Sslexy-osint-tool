from colorama import Fore, Style, init
import shutil

init()

# New "Sslexy Tool" ASCII art as requested by the user.
BLOODY_TEXT = fr"""
{Fore.RED}
  ██████   ██████  ██▓    ▓█████ ▒██   ██▒▓██   ██▓   ▄▄▄█████▓ ▒█████   ▒█████   ██▓    
▒██    ▒ ▒██    ▒ ▓██▒    ▓█   ▀ ▒▒ █ █ ▒░ ▒██  ██▒   ▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒    
░ ▓██▄   ░ ▓██▄   ▒██░    ▒███   ░░  █   ░  ▒██ ██░   ▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░    
  ▒   ██▒  ▒   ██▒▒██░    ▒▓█  ▄  ░ █ █ ▒   ░ ▐██▓░   ░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░    
▒██████▒▒▒██████▒▒░██████▒░▒████▒▒██▒ ▒██▒  ░ ██▒▓░     ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒
▒ ▒▓▒ ▒ ░▒ ▒▓▒ ▒ ░░ ▒░▓  ░░░ ▒░ ░▒▒ ░ ░▓ ░   ██▒▒▒      ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░
░ ░▒  ░ ░░ ░▒  ░ ░░ ░ ▒  ░ ░ ░  ░░░   ░▒ ░ ▓██ ░▒░        ░      ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░
░  ░  ░  ░  ░  ░    ░ ░      ░    ░    ░   ▒ ▒ ░░       ░      ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░   
      ░        ░      ░  ░   ░  ░ ░    ░   ░ ░                     ░ ░      ░ ░      ░  ░
                                           ░ ░                                           
{Style.RESET_ALL}
{Fore.WHITE}              [ THE ULTIMATE OSINT FRAMEWORK ]
"""

def print_banner():
    # Attempt to center the banner
    columns, _ = shutil.get_terminal_size()
    for line in BLOODY_TEXT.split('\n'):
        # We print it as is or centered. The user asked for this specific art.
        # Using center() might shift it oddly if columns is huge, but is safer than hardcode.
        print(line.center(columns))

def print_menu():
    print(f"{Fore.RED}[1]{Style.RESET_ALL} Username Lookup")
    print(f"{Fore.RED}[2]{Style.RESET_ALL} Email Lookup")
    print(f"{Fore.RED}[3]{Style.RESET_ALL} Network/IP OSINT")
    print(f"{Fore.RED}[4]{Style.RESET_ALL} Breach Checker")
    print(f"{Fore.RED}[5]{Style.RESET_ALL} Phone Number Lookup")
    print(f"{Fore.RED}[6]{Style.RESET_ALL} Metadata Extract")
    print(f"{Fore.RED}[99]{Style.RESET_ALL} Exit")
    print()
