import asyncio
import dis


def simple_generator():
    for i in range(10):
        yield i


sg = simple_generator()

print(dir(sg))
print(dis.dis(sg.gi_code))

 #%%

async def simple_coroutine():
    for i in range(10):
        await asyncio.sleep(0)
        yield i

sc = simple_coroutine()

print(dir(sc))
print(dis.dis(sc.ag_code))
