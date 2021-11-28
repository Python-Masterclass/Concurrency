import concurrent.futures
import sys
import threading
import time


total = 0


def inc(n):
    global total
    for _ in range(n):
        total += 1


def dec(n):
    global total
    for _ in range(n):
        total -= 1


N_WORKERS = 1
COUNT = 1_000_000


if __name__ == "__main__":
    sys.setswitchinterval(1e-4)
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
        for _ in range(N_WORKERS):
            executor.submit(inc, COUNT // N_WORKERS)
            executor.submit(dec, COUNT // N_WORKERS)
    end = time.time()
    print(f"At the end, total = {total}, time: {end-start}")