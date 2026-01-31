import asyncio
import time

async def fake_io(task_name, delay):
    print(f"{task_name} started")
    await asyncio.sleep(delay)
    print(f"{task_name} finished after {delay}s")

async def main():
    start = time.perf_counter()

    task1 = asyncio.create_task(fake_io("Task-1", 2))
    task2 = asyncio.create_task(fake_io("Task-2", 1))
    task3 = asyncio.create_task(fake_io("Task-3", 3))

    # await task1
    # await task2
    # await task3

    await asyncio.gather(task1, task2, task3)

    end = time.perf_counter()
    print(f"Total time: {end - start:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())

# Coroutine
    # A function definition (async def)
    # Does nothing until awaited or scheduled

# Task
    # A coroutine that’s been scheduled on the event loop
    # Runs concurrently with other tasks

# create_task() registers the coroutine with the event loop
# All tasks start immediately
# gather() waits for all tasks to complete
# await waits for completion, not execution
# Total runtime ≈ 3 seconds, not 6
# 📌 The event loop switches tasks only at await points