import asyncio


async def worker():
    print("Worker starting")
    while True:
        await asyncio.sleep(0.5)
        print("I'm working while other code sleeps")


async def delay(n):
    print(f"Starting sleep for {n} seconds")
    await asyncio.sleep(n)
    print(f"Finished sleep for {n} seconds")


async def main():
    delay1 = asyncio.create_task(delay(2))
    delay2 = asyncio.create_task(delay(3))
    working = asyncio.create_task(worker())
    await delay1
    await delay2
    print("canceling worker")
    # working.cancel()
    print("main finished")


if __name__ == "__main__":
    asyncio.run(main())
