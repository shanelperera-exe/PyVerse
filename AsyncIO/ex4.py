import asyncio
import time


async def fetch_data(param):
    print(f"Do something with {param}...")
    await asyncio.sleep(param)
    print(f"Done with {param}")
    return f"Result of {param}"


async def main():
    task1 = asyncio.create_task(fetch_data(1))
    task2 = asyncio.create_task(fetch_data(2))
    result2 = await task2
    print("Task 2 fully completed")
    result1 = await task1
    print("Task 1 fully completed")
    return [result1, result2]


t1 = time.perf_counter()

results = asyncio.run(main())
print(results)

t2 = time.perf_counter()
print(f"Finished in {t2 - t1:.2f} seconds")


# Full explanation:
# In this code, the fetch_data function uses await asyncio.sleep instead of time.sleep.
# This allows the event loop to remain unblocked while waiting for the sleep to complete.
# As a result, when we create tasks for fetch_data(1) and fetch_data(2),
# they can run concurrently. The first call to fetch_data(1) will sleep for 1 second,
# and during that time, fetch_data(2) can also start and sleep for 2 seconds.
# Therefore, the total execution time will be approximately 2 seconds,
# demonstrating that the tasks are running concurrently.