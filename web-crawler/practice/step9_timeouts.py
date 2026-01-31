import asyncio
import aiohttp

async def fetch(session, url):
    try:
        async with session.get(url, timeout=1) as response:
            return response.status
    except asyncio.TimeoutError:
        return "TIMEOUT"

async def main():
    urls = [
        "https://httpbin.org/delay/3",
        "https://httpbin.org/delay/1",
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, u) for u in urls]
        results = await asyncio.gather(*tasks)
        print(results)

asyncio.run(main())

# Timeouts & Failures
# -------------------
# In this example, we attempt to fetch two URLs that introduce delays.
# The first URL delays the response by 3 seconds, while the second delays it by 1 second.
# We set a timeout of 1 second for each request.
# As a result, the first request will timeout and return "TIMEOUT",
# while the second request will succeed and return the HTTP status code 200.

# Timeouts are normal
# Don’t crash the loop
# Handle errors per task