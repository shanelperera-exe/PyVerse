import asyncio
import aiohttp

async def fetch(session, url):
    async with session.get(url) as response:
        await response.text()
        return url

async def main():
    urls = [
        "https://httpbin.org/delay/3",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, u) for u in urls]

        for task in asyncio.as_completed(tasks):
            result = await task
            print(f"Finished: {result}")

asyncio.run(main())

# As Completed
# -----------------
# Instead of waiting for all tasks to complete, we can process them as they finish.
# This is done using asyncio.as_completed(), which yields tasks as they complete.   

# Results arrive out of order
# Perfect for:
# progress bars
# streaming pipelines
# saving data immediately