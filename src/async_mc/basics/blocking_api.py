# Copyright (c) 2022 Ruud de Jong
# This file is part of the Concurrency project which is released under the MIT license.
# See https://github.com/rhjdjong/Concurrency for details.

import asyncio
import requests
from concurrent.futures import ThreadPoolExecutor


async def get_status(n):
    print(f"Get status nr. {n}")
    status = requests.get("http://www.example.com").status_code
    print(f"Finished getting status nr. {n}")
    return status


async def blocking_main():
    task_1 = asyncio.create_task(get_status(1))
    task_2 = asyncio.create_task(get_status(2))
    task_3 = asyncio.create_task(get_status(3))
    await asyncio.gather(task_1, task_2, task_3)


async def threading_main():
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        urls = ("https://www.example.com" for _ in range(1000))


if __name__ == "__main__":
    asyncio.run(blocking_main())

