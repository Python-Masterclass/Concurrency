import asyncio
import requests


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


if __name__ == "__main__":
    asyncio.run(blocking_main())

