import requests
import concurrent.futures

# Custom Banner Function
def display_banner():
        print("""     _                          
 ___| |__   __ _ _ __| | __  / _(_)_ __   __| | ___ _ __ 
/ __| '_ \ / _` | '__| |/ / | |_| | '_ \ / _` |/ _ \ '__|
\__ \ | | | (_| | |  |   <  |  _| | | | | (_| |  __/ |   
|___/_| |_|\__,_|_|  |_|\_\ |_| |_|_| |_|\__,_|\___|_|   
                    (~|_ |_| _ ._ _   |\ | _ _|_ _ ._ _  o _ ._ 
                ~~  _)| | _|(_|| | |  | \|(_| | (_|| (_|_|(_|| |
        """)

# Function to validate subdomains
def validate_subdomain(subdomain, seen_subdomains, result_file, found_subdomains):
    if subdomain in seen_subdomains:
        return
    seen_subdomains.add(subdomain)
    try:
        response = requests.get(f"http://{subdomain}", timeout=2)
        if response.status_code < 400:
            print(f"[+] Found: {subdomain}")
            with open(result_file, "a") as file:
                file.write(f"{subdomain}\n")
            found_subdomains.append(subdomain)
    except requests.RequestException:
        pass

# Main Function
def main():
    display_banner()

    # User Input
    domain = input("Enter the Domain name  : ").strip()
    wordlist_path = input("Enter the path to the subdomain wordlist: ").strip()
    result_file = input("Enter the path for the output file: ").strip()

    # Read subdomain prefixes from the wordlist
    try:
        with open(wordlist_path, "r") as file:
            subdomains = [f"{line.strip()}.{domain}" for line in file]
    except FileNotFoundError:
        print("[!] Wordlist file not found.")
        return

    print("[+] Starting subdomain validation...")

    # Validate subdomains concurrently
    seen_subdomains = set()
    found_subdomains = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(lambda subdomain: validate_subdomain(subdomain, seen_subdomains, result_file, found_subdomains), subdomains)

    print(f"[+] Subdomain scan completed! Results saved in {result_file}")
    print(f"[+] Total subdomains found: {len(found_subdomains)}")

if __name__ == "__main__":
    main()
