import asyncio

sem = asyncio.Semaphore(2)

async def limited_task(name):
    async with sem:
        print(f"{name} acquired semaphore")
        await asyncio.sleep(2)
        print(f"{name} released semaphore")

async def main():
    tasks = [  # Create multiple tasks
        asyncio.create_task(limited_task(f"Task-{i}"))
        for i in range(5)
    ]
    await asyncio.gather(*tasks) # * <-- Unpack the list of tasks

if __name__ == "__main__":
    asyncio.run(main())

# Semaphore to limit the number of concurrent tasks.
# In this example, only 2 tasks can run concurrently.
# Semaphore: https://docs.python.org/3/library/asyncio-sync.html#asyncio.Semaphore
# Explanation: Semaphore used to limit concurrent access to a resource.