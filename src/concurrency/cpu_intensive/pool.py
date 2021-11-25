import concurrent.futures
import time


def countdown(n):
    while n > 0:
        n -= 1


COUNT = 50_000_000

N_WORKERS = 8


if __name__ == "__main__":
    times = []
    for _ in range(3):
        start = time.time()
        with concurrent.futures.ProcessPoolExecutor(max_workers=N_WORKERS) as executor:
            jobs = {executor.submit(countdown, COUNT // N_WORKERS) for _ in range(N_WORKERS)}
        end = time.time()
        times.append(end - start)
    print(f"Time: {min(times)} (best of 3)")

