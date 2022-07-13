# Copyright (c) 2022 Ruud de Jong
# This file is part of the Concurrency project which is released under the MIT license.
# See https://github.com/rhjdjong/Concurrency for details.
#%%
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
