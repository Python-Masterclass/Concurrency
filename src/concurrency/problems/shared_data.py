import concurrent.futures
import sys

total = 0


def inc(n):
    global total
    for _ in range(n):
        total += 1


def dec(n):
    global total
    for _ in range(n):
        total -= 1


N_WORKERS = 2
COUNT = 1_000_000

if __name__ == "__main__":
    sys.setswitchinterval(1e-4)
    with concurrent.futures.ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
        for _ in range(N_WORKERS):
            executor.submit(inc, COUNT // N_WORKERS)
            executor.submit(dec, COUNT // N_WORKERS)
    print(f"At the end, total = {total}")