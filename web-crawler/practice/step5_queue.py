import asyncio
import random

# Simple producer-consumer pattern using asyncio
async def producer(queue):
    for i in range(5):
        await asyncio.sleep(0.5)
        item = f"job-{i}"
        print(f"Produced {item}")
        await queue.put(item)

# Consumer worker
async def worker(name, queue):
    # Continuously process items from the queue
    while True:
        item = await queue.get()
        print(f"{name} processing {item}")
        await asyncio.sleep(random.uniform(0.5, 1.5)) # Simulate processing time
        queue.task_done()

async def main():
    queue = asyncio.Queue()

    workers = [
        asyncio.create_task(worker(f"Worker-{i}", queue))
        for i in range(3)
    ]

    await producer(queue) # Produce items
    await queue.join() # Wait until all items are processed

    for w in workers:  
        w.cancel()     # Cancel worker tasks

if __name__ == "__main__":
    asyncio.run(main())
    

# Explaination:
# This code implements a simple producer-consumer pattern using asyncio.
# The producer generates jobs and puts them into an asyncio queue.
# Multiple worker coroutines consume jobs from the queue and process them concurrently.
# The main function orchestrates the creation of the queue, workers, and the producer,
# ensuring that all jobs are processed before shutting down the workers.