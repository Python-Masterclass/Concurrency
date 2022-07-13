# Copyright (c) 2022 Ruud de Jong
# This file is part of the Concurrency project which is released under the MIT license.
# See https://github.com/rhjdjong/Concurrency for details.

import asyncio


async def cpu_bound_work(n):
    print(f"Starting cpu bound worker {n}")
    counter = 0
    for _ in range(100_000_000):
        counter += 1
    print(f"Finished cpu bound worker {n}")
    return counter


async def main():
    task_one = asyncio.create_task(cpu_bound_work(1))
    task_two = asyncio.create_task(cpu_bound_work(2))
    await asyncio.gather(task_one, task_two)


if __name__ == "__main__":
    asyncio.run(main())
