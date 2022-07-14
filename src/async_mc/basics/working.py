import asyncio

running = True


async def worker():
    print("Worker starting")
    while running:
        await asyncio.sleep(0.5)
        print("I'm working while other code sleeps")
    print("Worker finished")


async def delay(n):
    print(f"Starting sleep for {n} seconds")
    await asyncio.sleep(n)
    print(f"Finished sleep for {n} seconds")


async def main():
    global running
    delay1 = asyncio.create_task(delay(2))
    delay2 = asyncio.create_task(delay(3))
    working = asyncio.create_task(worker())
    await delay1
    await delay2
    running = False
    await working
    print("main finished")


if __name__ == "__main__":
    asyncio.run(main())

