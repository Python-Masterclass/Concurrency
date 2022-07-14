import asyncio
import logging
import time

import aiohttp


async def fetch_status(session: aiohttp.ClientSession, url: str, delay: int | None = None) -> int:
    if delay is not None:
        await asyncio.sleep(delay)
    async with session.get(url) as result:
        return result.status


URLS = [
    "https://example.com",
    "https://example.com",
    "https://example.com",
]


async def main_all_complete():
    async with aiohttp.ClientSession() as session:
        done, pending = await asyncio.wait(
            [asyncio.create_task(fetch_status(session, url)) for url in URLS]
        )
        print(f"{len(done)=}")
        print(f"{len(pending)=}")
        for done_task in done:
            result = await done_task
            print(result)


async def main_exception():
    async with aiohttp.ClientSession() as session:
        done, pending = await asyncio.wait(
            [
                asyncio.create_task(fetch_status(session, url))
                for url in URLS + ["python://bad.url", "https://www.example.com"]
            ]
        )
        print(f"{len(done)=}")
        print(f"{len(pending)=}")
        for done_task in done:
            if (exc := done_task.exception()) is None:
                print(f"{done_task.result()=}")
            else:
                logging.error("Request got an exception", exc_info=exc)


async def main_first_exception():
    async with aiohttp.ClientSession() as session:
        done, pending = await asyncio.wait(
            [
                asyncio.create_task(fetch_status(session, url))
                for url in URLS + ["python://bad.url", "https://www.example.com"]
            ],
            return_when=asyncio.FIRST_EXCEPTION
        )
        print(f"{len(done)=}")
        print(f"{len(pending)=}")
        for done_task in done:
            if (exc := done_task.exception()) is None:
                print(f"{done_task.result()=}")
            else:
                logging.error("Request got an exception", exc_info=exc)
        for pending_task in pending:
            print(f"Canceling {pending_task}")
            pending_task.cancel()


async def main_first_completed():
    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.create_task(fetch_status(session, url))
            for url in URLS + ["python://bad.url", "https://www.example.com"]
        ]
        pending = tasks[:]  # Copy the original tasks into pending
        while pending:
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
            print(f"{len(done)=}")
            print(f"{len(pending)=}")
            for done_task in done:
                if (exc := done_task.exception()) is None:
                    print(f"Task {tasks.index(done_task)}: {done_task.result()=}")
                else:
                    logging.error(f"Task {tasks.index(done_task)} got an exception", exc_info=exc)


async def main_timeout():
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(fetch_status(session, url)) for url in URLS]
        tasks.append(asyncio.create_task(fetch_status(session, "https://www.example.com", 10)))
        done, pending = await asyncio.wait(tasks, timeout=2)
        print(f"{len(done)=}")
        print(f"{len(pending)=}")
        for done_task in done:
            result = await done_task
            print(result)


if __name__ == "__main__":
    start = time.time()
    # asyncio.run(main_all_complete())
    # asyncio.run(main_exception())
    # asyncio.run(main_first_exception())
    # asyncio.run(main_first_completed())
    asyncio.run(main_timeout())
    duration = time.time() - start
    print(f"{duration=}")