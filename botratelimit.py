import requests
from bs4 import BeautifulSoup
import time
import random
import threading
from colorama import init, Fore
import re

init(autoreset=True)

# Change this to ur View count URL
URL = "https://komarev.com/ghpvc/?username=xpertthecat&label=Profile%20views&color=0e75b6&style=flat%22%20alt=%22xpertthecat"

session = requests.Session() 

def viewc():
    try:
        response = session.get(URL, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text_elements = soup.find_all("text")
            
            for element in text_elements:
                text = element.get_text(strip=True)
                if "Profile views" in text: 
                    continue
                numbers = re.findall(r"\d+", text) 
                if numbers:
                    return int("".join(numbers)) 

        return None
    except requests.RequestException:
        return None

def send_request():
    try:
        response = session.get(URL, timeout=5)
        if response.status_code == 200:
            print(Fore.MAGENTA + f"[xpert]$- {Fore.GREEN}[+] Success")
        elif response.status_code == 429:
            print(f"{Fore.MAGENTA}[xpert]$- {Fore.LIGHTRED_EX}[!] Rate limit reached. Waiting...")
            time.sleep(5)  
        else:
            print(f"{Fore.MAGENTA}[xpert]$- {Fore.LIGHTRED_EX}[!] Failed to open the website. HTTP Status code:", response.status_code)
    except requests.RequestException:
        print(f"{Fore.MAGENTA}[xpert]$- {Fore.RED}[!] Request failed.")

def requ():
    request_count = 0
    last_checked_count = 0

    def reqth(num_threads=5):
        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=send_request)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

    while True:
        reqth()

        request_count += 500

        if request_count % 50 == 0:
            current_count = viewc()
            if current_count is not None and current_count // 10 > last_checked_count // 10:
                print(Fore.MAGENTA + f"[xpert]$- {Fore.GREEN}[+] Reached {current_count} views after {request_count} requests!")
                last_checked_count = current_count

        rate = random.uniform(0.05, 0.2)
        print(f"{Fore.MAGENTA}[xpert]$- {Fore.YELLOW}[!] Waiting for {rate:.2f} seconds before next batch...\n")
        time.sleep(rate)

if __name__ == "__main__":
    requ()