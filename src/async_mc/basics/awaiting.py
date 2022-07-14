import asyncio
import time


async def printit(text):
    print(f"{time.time()} {text}")


async def main():
    await printit("hello")
    print("start sleep")
    await asyncio.sleep(1)
    print("end sleep")
    await printit("world")


if __name__ == "__main__":
    asyncio.run(main())