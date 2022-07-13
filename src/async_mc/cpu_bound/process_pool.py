# Copyright (c) 2022 Ruud de Jong
# This file is part of the Concurrency project which is released under the MIT license.
# See https://github.com/rhjdjong/Concurrency for details.

from multiprocessing import Pool
import time

from async_mc.cpu_bound.cpu_work import countdown

COUNT = 50_000_000

if __name__ == "__main__":
    start = time.time()
    with Pool() as process_pool:
        process_pool.apply(countdown, args=(COUNT,))
        process_pool.apply(countdown, args=(COUNT,))
    print(f"Time (apply): {time.time() - start}")

    start = time.time()
    with Pool() as process_pool:
        p1 = process_pool.apply_async(countdown, args=(COUNT,))
        p2 = process_pool.apply_async(countdown, args=(COUNT,))
        p1.get()
        p2.get()
    print(f"Time (apply_async): {time.time() - start}")

