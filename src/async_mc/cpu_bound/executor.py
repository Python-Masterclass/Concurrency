import asyncio
from concurrent.futures import ProcessPoolExecutor
from functools import partial

from async_mc.cpu_bound.cpu_work import countup


numbers = (
    100_000_000,
    1,
    3,
    5,
    22,
)


def main_synchronous():
    with ProcessPoolExecutor() as process_pool:
        for result in process_pool.map(countup, numbers):
            print(result)


async def main_async_gather():
    with ProcessPoolExecutor() as process_pool:
        loop = asyncio.get_running_loop()
        calls = (partial(countup, num) for num in numbers)
        call_futures = [loop.run_in_executor(process_pool, call) for call in calls]
        results = await asyncio.gather(*call_futures)
        for result in results:
            print(result)


async def main_async_as_completed():
    with ProcessPoolExecutor() as process_pool:
        loop = asyncio.get_running_loop()
        calls = (partial(countup, num) for num in numbers)
        call_futures = [loop.run_in_executor(process_pool, call) for call in calls]
        for finished_job in asyncio.as_completed(call_futures):
            result = await finished_job
            print(result)


async def main_async_wait():
    with ProcessPoolExecutor() as process_pool:
        loop = asyncio.get_running_loop()
        calls = (partial(countup, num) for num in numbers)
        call_futures = [loop.run_in_executor(process_pool, call) for call in calls]

if __name__ == "__main__":
    main_synchronous()
    asyncio.run(main_async_gather())
    asyncio.run(main_async_as_completed())
