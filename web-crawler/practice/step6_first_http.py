import asyncio
import aiohttp

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(f"Status: {response.status}")
            text = await response.text()
            print(f"Fetched {len(text)} characters")

if __name__ == "__main__":
    asyncio.run(fetch("https://www.formula1.com/"))

# ClientSession: Manages and persists settings across multiple requests (cookies, headers, connection pooling)
# async with: Ensures proper acquisition and release of resources (like network connections)
# await response.text(): Asynchronously reads the response body as text

# *** Creating a session per request is slow and wasteful.
# async def fetch(url):
#     async with aiohttp.ClientSession() as session:
#         ...