import asyncio
import time


async def coro(n):
    await asyncio.sleep(1)
    return 2 * n


async def main_dont_do_this(n):
    return [await asyncio.create_task(coro(i)) for i in range(n)]


async def main_this_is_better(n):
    tasks = [asyncio.create_task(coro(i)) for i in range(n)]
    return [await task for task in tasks]


if __name__ == "__main__":
    start = time.time()
    # result = asyncio.run(main_dont_do_this(4))
    result = asyncio.run(main_this_is_better(4))
    duration = time.time() - start
    print(f"{result=}, {duration=}")