# Copyright (c) 2022 Ruud de Jong
# This file is part of the Concurrency project which is released under the MIT license.
# See https://github.com/rhjdjong/Concurrency for details.
import time


def countdown(n):
    while n > 0:
        n -= 1


def countup(n):
    start = time.time()
    result = 0
    while result < n:
        result += 1
    print(f"Finished counting to {n} in {time.time() - start} seconds.")
    return result
