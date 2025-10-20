import asyncio
import httpx
import re
import random
from colorama import init, Fore

init(autoreset=True)

# Change this to ur View count URL
URL = "https://komarev.com/ghpvc/?username=xpertthecat&label=Profile%20views&color=0e75b6&style=flat"

client = httpx.AsyncClient(http2=True, timeout=5)

pattern = re.compile(r"\d+")

async def view_count():
    try:
        r = await client.get(URL)
        if r.status_code == 200:
            numbers = pattern.findall(r.text)
            if numbers:
                return int("".join(numbers))
        return None
    except Exception:
        return None

async def send_request():
    try:
        r = await client.get(URL)
        if r.status_code == 200:
            print(Fore.MAGENTA + f"[xpert]$- {Fore.GREEN}[+] Success")
        elif r.status_code == 429:
            print(Fore.MAGENTA + f"[xpert]$- {Fore.RED}[!] Rate limited, pausing...")
            await asyncio.sleep(3)
        else:
            print(Fore.MAGENTA + f"[xpert]$- {Fore.YELLOW}[!] HTTP {r.status_code}")
    except Exception:
        print(Fore.MAGENTA + f"[xpert]$- {Fore.RED}[!] Request failed")

async def run_batch(limit=25):
    sem = asyncio.Semaphore(limit)

    async def worker():
        async with sem:
            await send_request()
            await asyncio.sleep(random.uniform(0.01, 0.05)) 

    tasks = [worker() for _ in range(limit)]
    await asyncio.gather(*tasks)

async def main():
    total = 0
    last_seen = 0
    while True:
        await run_batch(limit=100)
        total += 100

        if total % 500 == 0:
            count = await view_count()
            if count and count // 10 > last_seen // 10:
                print(Fore.MAGENTA + f"[xpert]$- {Fore.GREEN}[+] Reached {count} views after {total} requests!")
                last_seen = count

        wait_time = random.uniform(0.05, 0.15)
        print(Fore.YELLOW + f"[!] Waiting {wait_time:.2f}s before next batch...")
        await asyncio.sleep(wait_time)

if __name__ == "__main__":
    asyncio.run(main()