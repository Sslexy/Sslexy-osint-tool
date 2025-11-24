import os
import shutil
import requests
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import exifread
from colorama import Fore, Style

def _get_if_exist(data, key):
    if key in data:
        return data[key]
    return None

def _convert_to_degrees(value):
    """Helper to convert GPS coordinates."""
    d = float(value[0])
    m = float(value[1])
    s = float(value[2])
    return d + (m / 60.0) + (s / 3600.0)

def extract_metadata_pillow(filepath):
    print(f"\n{Fore.CYAN}[*] Analyzing with Pillow...{Style.RESET_ALL}")
    try:
        image = Image.open(filepath)
        exif_data = image._getexif()
        
        if not exif_data:
            print(f"{Fore.YELLOW}[!] No EXIF data found in image.{Style.RESET_ALL}")
            return

        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            # Filter out binary data which is too long
            if isinstance(value, bytes):
                if len(value) > 50:
                    value = "[Binary Data]"
            print(f"{Fore.GREEN}[+] {tag_name}: {value}{Style.RESET_ALL}")

            # GPS Decoding
            if tag_name == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_tag = GPSTAGS.get(t, t)
                    gps_data[sub_tag] = value[t]
                
                print(f"{Fore.MAGENTA}  -> GPS Data Found: {gps_data}{Style.RESET_ALL}")
                
    except Exception as e:
        print(f"{Fore.RED}[!] Pillow Analysis Error: {e}{Style.RESET_ALL}")

def extract_metadata_exifread(filepath):
    print(f"\n{Fore.CYAN}[*] Analyzing with ExifRead...{Style.RESET_ALL}")
    try:
        with open(filepath, 'rb') as f:
            tags = exifread.process_file(f)
            if not tags:
                print(f"{Fore.YELLOW}[!] No Tags found.{Style.RESET_ALL}")
                return

            for tag in tags.keys():
                if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                    print(f"{Fore.GREEN}[+] {tag}: {tags[tag]}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] ExifRead Error: {e}{Style.RESET_ALL}")

def run_metadata_extract():
    print(f"{Fore.BLUE}--- METADATA EXTRACTOR ---{Style.RESET_ALL}")
    target = input("Enter file path or URL to image: ")

    local_path = target
    temp_file = False

    if target.startswith("http"):
        print(f"{Fore.CYAN}[*] Downloading image from URL...{Style.RESET_ALL}")
        try:
            r = requests.get(target, stream=True)
            if r.status_code == 200:
                local_path = "temp_image_download.jpg"
                with open(local_path, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                temp_file = True
            else:
                print(f"{Fore.RED}[!] Failed to download image.{Style.RESET_ALL}")
                return
        except Exception as e:
            print(f"{Fore.RED}[!] Download Error: {e}{Style.RESET_ALL}")
            return

    if not os.path.exists(local_path):
        print(f"{Fore.RED}[!] File does not exist.{Style.RESET_ALL}")
        return

    # Run Tools
    extract_metadata_pillow(local_path)
    extract_metadata_exifread(local_path)

    if temp_file and os.path.exists(local_path):
        os.remove(local_path)
        print(f"\n{Fore.YELLOW}[*] Temporary file removed.{Style.RESET_ALL}")

    print(f"\n{Fore.BLUE}--- SCAN COMPLETE ---{Style.RESET_ALL}")
