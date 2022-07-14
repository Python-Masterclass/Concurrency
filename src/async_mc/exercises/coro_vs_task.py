# Copyright (c) 2022 Ruud de Jong
# This file is part of the Concurrency project which is released under the MIT license.
# See https://github.com/rhjdjong/Concurrency for details.

import asyncio


async def bg_task():
    while True:
        print(f"Background task runs")
        await asyncio.sleep(0)


async def coro(n):
    if n > 0:
        print(f"coro {n} runs. {len(asyncio.all_tasks())} tasks in event loop")
        await coro(n-1)


async def main():
    print(f"{len(asyncio.all_tasks())} tasks in event loop")
    bg = asyncio.create_task(bg_task())
    print(f"{len(asyncio.all_tasks())} tasks in event loop")
    # await asyncio.sleep(0)
    await coro(10)
    print(f"{len(asyncio.all_tasks())} tasks in event loop")
    bg.cancel()


if __name__ == "__main__":
    asyncio.run(main())