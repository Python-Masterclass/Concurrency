# Copyright (c) 2022 Ruud de Jong
# This file is part of the Concurrency project which is released under the MIT license.
# See https://github.com/rhjdjong/Concurrency for details.

#%%
import asyncio
import dis

#%%

async def my_coroutine():
    return "Hello world!"

mc = my_coroutine()

print(type(my_coroutine))
print(type(mc))

#%%
def my_generator():
    yield "Hello world!"

mg = my_generator()

print(type(my_generator))
print(type(mg))

#%%
print("** my_coroutine **")
print(dis.dis(my_coroutine))
print("** mc **")
print(dis.dis(mc))
print("** my_generator **")
print(dis.dis(my_generator))
print("** mg **")
print(dis.dis(mg))

#%%
result = asyncio.run(mc)
print(result)