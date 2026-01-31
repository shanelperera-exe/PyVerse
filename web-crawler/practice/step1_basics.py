import asyncio

async def say_hello(name):
    print(f"Hello, {name}!")
    await asyncio.sleep(1)
    print(f"Goodbye, {name}!")

async def main():
    await say_hello("Async World")
    await say_hello("Python")
    await say_hello("Developers")

if __name__ == "__main__":
    asyncio.run(main())


# say_hello is a coroutine
# await asyncio.sleep() gives control back to the event loop
# asyncio.run() creates and manages the event loop
