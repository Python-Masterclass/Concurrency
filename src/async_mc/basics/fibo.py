import asyncio


total_tasks = 0
simultaneous_tasks = 0


async def fib(n):
    global total_tasks
    global simultaneous_tasks
    total_tasks += 1
    simultaneous_tasks = max(simultaneous_tasks, len(asyncio.all_tasks()))
    if n < 2:
        return 1
    f_1 = asyncio.create_task(fib(n-1))
    f_2 = asyncio.create_task(fib(n-2))
    return sum(await(asyncio.gather(f_1, f_2)))


async def main():
    global total_tasks
    total_tasks += 1
    n = 24
    result = await(fib(n))
    print(f"fib({n}) = {result}")
    print(f"{total_tasks=}, {simultaneous_tasks=}")


if __name__ == "__main__":
    asyncio.run(main())
