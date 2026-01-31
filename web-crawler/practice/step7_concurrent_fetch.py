import asyncio
import aiohttp
import time

URLS = [
    "https://example.com",
    "https://www.python.org",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/delay/1",
]

async def fetch(session, url):
    print(f"Fetching {url}")
    async with session.get(url) as response:
        return url, response.status
    
async def main():
    start = time.perf_counter()
    
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(fetch(session, url)) for url in URLS]
        
        results = await asyncio.gather(*tasks)
        for url, status in results:
            print(url, status)
        
    print(f"Total time: {time.perf_counter() - start:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())