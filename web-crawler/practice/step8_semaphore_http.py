import asyncio
import aiohttp

sem = asyncio.Semaphore(2)

async def fetch(session, url):
    async with sem:
        print(f"Fetching {url}")
        async with session.get(url) as response:
            await response.text()
            print(f"Done {url}")

async def main():
    urls = [
        "https://httpbin.org/delay/2",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/delay/2",
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(fetch(session, u)) for u in urls]
        await asyncio.gather(*tasks)

asyncio.run(main())

# Concurreny limit --> Servers will ban you if you don’t limit this.

# async with semaphore, only 2 requests will be processed concurrently.
# async with session.get(url), fetches the URL using aiohttp session.

# Semaphore = Politeness + Stability
# This will become:
# MAX_CONCURRENT_REQUESTS = 10
# Configurable
# Mandatory for crawlers