
import asyncio
import time
from concurrent.futures import ProcessPoolExecutor


def fetch_data(param):
    print(f"Do something with {param}...", flush=True)
    time.sleep(param)
    print(f"Done with {param}", flush=True)
    return f"Result of {param}"


async def main():
    # Run in Threads
    task1 = asyncio.create_task(asyncio.to_thread(fetch_data, 1))
    task2 = asyncio.create_task(asyncio.to_thread(fetch_data, 2))
    result1 = await task1
    print("Thread 1 fully completed")
    result2 = await task2
    print("Thread 2 fully completed")

    # Run in Process Pool
    loop = asyncio.get_running_loop()

    with ProcessPoolExecutor() as executor:
        task1 = loop.run_in_executor(executor, fetch_data, 1)
        task2 = loop.run_in_executor(executor, fetch_data, 2)

        result1 = await task1
        print("Process 1 fully completed")
        result2 = await task2
        print("Process 2 fully completed")

    return [result1, result2]


if __name__ == "__main__":
    t1 = time.perf_counter()

    results = asyncio.run(main())
    print(results)

    t2 = time.perf_counter()
    print(f"Finished in {t2 - t1:.2f} seconds")

# Full explanation:
# In this code, the fetch_data function uses time.sleep, which is a blocking call.
# To avoid blocking the event loop, we run fetch_data in separate threads using asyncio.to_thread
# and in separate processes using ProcessPoolExecutor.
# This allows the tasks to run concurrently without blocking the main event loop.
# When we create tasks for fetch_data(1) and fetch_data(2) in threads,
# they can run concurrently, resulting in a total execution time of approximately 2 seconds.
# Similarly, when we run fetch_data in a process pool, the tasks also run concurrently,
# leading to a total execution time of approximately 2 seconds. 
# This demonstrates how to handle blocking I/O-bound tasks in an asynchronous context
# by offloading them to threads or processes.

# Terminology:
# - Blocking Call: A function that stops the execution of further code until it completes.
# - Thread: A separate flow of execution within the same process.
# - Process: An independent program in execution with its own memory space.
# - asyncio.to_thread: A function that runs a blocking function in a separate thread.
# - ProcessPoolExecutor: A class that manages a pool of processes to run blocking functions concurrently.  
# - Event Loop: The core of every asyncio application that runs asynchronous tasks and callbacks.
# - Concurrency: The ability to run multiple tasks in overlapping time periods, improving efficiency.
# - I/O-bound Task: A task that spends most of its time waiting for input/output operations to complete.
# - CPU-bound Task: A task that requires significant CPU processing time.
# - await: A keyword used to pause the execution of a coroutine until the awaited task is complete.
# - asyncio.run: A function that runs the main entry point of an asyncio program.
# - asyncio.create_task: A function that schedules the execution of a coroutine as a task.
# - loop.run_in_executor: A method that runs a blocking function in a specified executor (thread or process).
# - coroutine: A special function that can pause and resume its execution, allowing for asynchronous programming.
# - synchronous: Code that runs sequentially, one operation at a time.
# - asynchronous: Code that can run multiple operations concurrently, allowing for non-blocking execution.