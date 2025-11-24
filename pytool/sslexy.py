import sys
import os
from utils.banner import print_banner, print_menu
from colorama import Fore, Style

def clear_screen():
    # Windows
    if os.name == 'nt':
        os.system('cls')
    # Posix (Linux, macOS)
    else:
        os.system('clear')

def main():
    while True:
        clear_screen()
        print_banner()
        print_menu()
        
        try:
            choice = input(f"{Fore.RED}Scegli un opzione ! {Style.RESET_ALL}")
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit()

        if choice == '1':
            print(f"\n{Fore.GREEN}[*] Launching Username Lookup Module...{Style.RESET_ALL}")
            from modules.username_osint import run_username_lookup
            run_username_lookup()
        elif choice == '2':
            print(f"\n{Fore.GREEN}[*] Launching Email Lookup Module...{Style.RESET_ALL}")
            from modules.email_osint import run_email_lookup
            run_email_lookup()
        elif choice == '3':
            print(f"\n{Fore.GREEN}[*] Launching Network/IP Module...{Style.RESET_ALL}")
            from modules.network_osint import run_network_lookup
            run_network_lookup()
        elif choice == '4':
            print(f"\n{Fore.GREEN}[*] Launching Breach Checker...{Style.RESET_ALL}")
            from modules.breach_check import run_breach_check
            run_breach_check()
        elif choice == '5':
            print(f"\n{Fore.GREEN}[*] Launching Phone Number Lookup...{Style.RESET_ALL}")
            from modules.phone_osint import run_phone_lookup
            run_phone_lookup()
        elif choice == '6':
            print(f"\n{Fore.GREEN}[*] Launching Metadata Extractor...{Style.RESET_ALL}")
            from modules.metadata_osint import run_metadata_extract
            run_metadata_extract()
        elif choice == '99':
            print("Goodbye!")
            sys.exit()
        else:
            print(f"\n{Fore.YELLOW}Invalid option, try again.{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Press Enter to return to menu...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
