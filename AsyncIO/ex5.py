import asyncio
import time


async def fetch_data(param):
    print(f"Do something with {param}...")
    time.sleep(param) 
    print(f"Done with {param}")
    return f"Result of {param}"


async def main():
    task1 = asyncio.create_task(fetch_data(1))
    task2 = asyncio.create_task(fetch_data(2))
    result1 = await task1
    print("Task 1 fully completed")
    result2 = await task2
    print("Task 2 fully completed")
    return [result1, result2]


t1 = time.perf_counter()

results = asyncio.run(main())
print(results)

t2 = time.perf_counter()
print(f"Finished in {t2 - t1:.2f} seconds")

# Full explanation:
# In this code, the fetch_data function uses time.sleep instead of asyncio.sleep.
# This means that when fetch_data is called, it blocks the entire event loop for the duration of the sleep.
# As a result, even though we create tasks for fetch_data(1) and fetch_data(2),
# they cannot run concurrently. The first call to fetch_data(1) will block the event loop for 1 second,
# and only after it completes will fetch_data(2) start, blocking for an additional 2 seconds.
# Therefore, the total execution time will be approximately 3 seconds, demonstrating that the tasks are not running concurrently.#Full explanation:
# In this code, the fetch_data function uses time.sleep instead of asyncio.sleep.
# This means that when fetch_data is called, it blocks the entire event loop for the duration of the sleep.
# As a result, even though we create tasks for fetch_data(1) and fetch_data(2),
# they cannot run concurrently. The first call to fetch_data(1) will block the event loop for 1 second,
# and only after it completes will fetch_data(2) start, blocking for an additional 2 seconds.
# Therefore, the total execution time will be approximately 3 seconds, demonstrating that the tasks are not running concurrently.