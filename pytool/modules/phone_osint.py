import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from colorama import Fore, Style

def run_phone_lookup():
    print(f"{Fore.BLUE}--- PHONE NUMBER OSINT ---{Style.RESET_ALL}")
    print("Format: +<CountryCode><Number> (e.g., +393331234567)")
    number_input = input("Enter phone number: ")

    try:
        # Parse the number
        parsed_number = phonenumbers.parse(number_input, None)
        
        # Validation
        is_valid = phonenumbers.is_valid_number(parsed_number)
        is_possible = phonenumbers.is_possible_number(parsed_number)

        if not is_valid:
            print(f"{Fore.RED}[!] Number is invalid or does not exist.{Style.RESET_ALL}")
            if not is_possible:
                 print(f"{Fore.YELLOW}[!] Format seems incorrect.{Style.RESET_ALL}")
            return

        print(f"\n{Fore.GREEN}[+] Number is Valid!{Style.RESET_ALL}")
        
        # Formatting
        print(f"{Fore.CYAN}[*] International: {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] National: {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] E164: {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)}{Style.RESET_ALL}")

        # Geography
        region = geocoder.description_for_number(parsed_number, "en")
        print(f"{Fore.GREEN}[+] Location: {region}{Style.RESET_ALL}")

        # Carrier
        service_provider = carrier.name_for_number(parsed_number, "en")
        if service_provider:
            print(f"{Fore.GREEN}[+] Carrier: {service_provider}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[!] Carrier info unavailable (number might be fixed-line).{Style.RESET_ALL}")

        # Timezone
        tz = timezone.time_zones_for_number(parsed_number)
        print(f"{Fore.CYAN}[*] Timezone(s): {', '.join(tz)}{Style.RESET_ALL}")

        # Future: Numverify Integration (Placeholder)
        # print(f"{Fore.YELLOW}[!] Advanced Carrier Lookup (Numverify) requires API Key (Not configured){Style.RESET_ALL}")

    except phonenumbers.NumberParseException as e:
        print(f"{Fore.RED}[!] Parsing Error: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")

    print(f"\n{Fore.BLUE}--- SCAN COMPLETE ---{Style.RESET_ALL}")
