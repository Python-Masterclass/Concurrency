import concurrent.futures
import sys
import threading
import time


class Amount:
    def __init__(self):
        self.total = 0

    def inc(self, n):
        for _ in range(n):
            self.total += 1

    def dec(self, n):
        for _ in range(n):
            self.total -= 1


N_WORKERS = 2
COUNT = 1_000_000


if __name__ == "__main__":
    amount = Amount()
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
        for _ in range(N_WORKERS):
            executor.submit(amount.inc, COUNT // N_WORKERS)
            executor.submit(amount.dec, COUNT // N_WORKERS)
    end = time.time()
    print(f"At the end, total = {amount.total}, time: {end-start}")