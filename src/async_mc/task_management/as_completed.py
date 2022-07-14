import asyncio
import time

import aiohttp


async def fetch_status(session: aiohttp.ClientSession, url: str, delay: int) -> int:
    await asyncio.sleep(delay)
    async with session.get(url) as result:
        return result.status


URLS = [
    ("https://example.com", 1),
    ("https://example.com", 5),
    ("https://example.com", 10),
]


async def main():
    async with aiohttp.ClientSession() as session:
        for finished_task in asyncio.as_completed(
            [fetch_status(session, url, delay) for url, delay in URLS]
        ):
            print(await finished_task)


async def main_with_timeout():
    async with aiohttp.ClientSession() as session:
        for finished_task in asyncio.as_completed(
            [fetch_status(session, url, delay) for url, delay in URLS],
            timeout=2,
        ):
            try:
                result = await finished_task
                print(result)
            except asyncio.TimeoutError:
                print("got a timeout")
        for task in asyncio.all_tasks():
            print(task)


if __name__ == "__main__":
    start = time.time()
    # asyncio.run(main())
    asyncio.run(main_with_timeout())
    duration = time.time() - start
    print(f"{duration=}")