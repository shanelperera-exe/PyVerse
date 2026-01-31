import asyncio
import time

async def bad_task():
    print("Bad task started")
    time.sleep(2)  # ❌ BLOCKS the event loop
    print("Bad task finished")

async def good_task():
    print("Good task started")
    await asyncio.sleep(1)
    print("Good task finished")

async def main():
    t1 = asyncio.create_task(bad_task())
    t2 = asyncio.create_task(good_task())

    await asyncio.gather(t1, t2)

if __name__ == "__main__":
    asyncio.run(main())

# Blocking Kills AsyncIO
# If it doesn’t await, it blocks everything.