import asyncio
import time


async def delay(n):
    await asyncio.sleep(n)


async def main_sequential():
    start = time.time()
    await(delay(1))
    await(delay(2))
    print(f"main_sequential took {time.time() - start} seconds")


async def main_concurrently():
    start = time.time()
    task1 = asyncio.create_task(delay(1))
    task2 = asyncio.create_task(delay(2))
    await task1
    await task2
    print(f"main_concurrently took {time.time() - start} seconds")


if __name__ == "__main__":
    asyncio.run(main_sequential())
    asyncio.run(main_concurrently())
