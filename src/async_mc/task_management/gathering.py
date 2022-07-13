# Copyright (c) 2022 Ruud de Jong
# This file is part of the Concurrency project which is released under the MIT license.
# See https://github.com/rhjdjong/Concurrency for details.
import asyncio
import time

import aiohttp


async def fetch_status(session: aiohttp.ClientSession, url: str) -> int:
    async with session.get(url) as result:
        return result.status


URLS = [
    "https://example.com" for _ in range(100)
]


async def main():
    async with aiohttp.ClientSession() as session:
        request = [fetch_status(session, url) for url in URLS]
        status_codes = await asyncio.gather(*request)
        # status_codes = [await fetch_status(session, url) for url in URLS]  # In essence sequential execution
        return status_codes


if __name__ == "__main__":
    start = time.time()
    results = asyncio.run(main())
    duration = time.time() - start
    print(f"{results=}\n{duration=}")