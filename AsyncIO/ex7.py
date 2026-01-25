import asyncio
import time


async def fetch_data(param):
    await asyncio.sleep(param)
    return f"Result of {param}"


async def main():
    # Create Tasks Manually
    task1 = asyncio.create_task(fetch_data(1))
    task2 = asyncio.create_task(fetch_data(2))
    result1 = await task1
    result2 = await task2
    print(f"Task 1 and 2 awaited results: {[result1, result2]}")

    # Gather Coroutines
    coroutines = [fetch_data(i) for i in range(1, 3)]
    results = await asyncio.gather(*coroutines, return_exceptions=True)
    print(f"Coroutine Results: {results}")

    # Gather Tasks
    tasks = [asyncio.create_task(fetch_data(i)) for i in range(1, 3)]
    results = await asyncio.gather(*tasks)
    print(f"Task Results: {results}")

    # Task Group
    async with asyncio.TaskGroup() as tg:
        results = [tg.create_task(fetch_data(i)) for i in range(1, 3)]
        # All tasks are awaited when the context manager exits.
    print(f"Task Group Results: {[result.result() for result in results]}")

    return "Main Coroutine Done"


t1 = time.perf_counter()

results = asyncio.run(main())
print(results)

t2 = time.perf_counter()
print(f"Finished in {t2 - t1:.2f} seconds")

# Full explanation:
# This code demonstrates four different methods of managing and executing asynchronous tasks using asyncio in Python.
# 1. Creating Tasks Manually: We create tasks using asyncio.create_task and await them individually.
# 2. Gathering Coroutines: We use asyncio.gather to run multiple coroutines concurrently and collect their results.
# 3. Gathering Tasks: Similar to gathering coroutines, but we first create tasks and then gather them.
# 4. Task Group: We use asyncio.TaskGroup to manage a group of tasks within a context manager, ensuring all tasks are awaited when exiting the context.
# Each method allows for concurrent execution of the fetch_data function, which simulates an I/O-bound operation using asyncio.sleep.
# The total execution time will be approximately 2 seconds, demonstrating that the tasks are running concurrently. 
# The final output confirms that all tasks have completed successfully and their results are collected.
