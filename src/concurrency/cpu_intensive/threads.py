import time
from threading import Thread


def countdown(n):
    while n > 0:
        n -= 1


COUNT = 50_000_000

N_THREADS = 4


if __name__ == "__main__":
    times = []
    for _ in range(3):
        threads = [Thread(target=countdown, args=(COUNT // N_THREADS,)) for _ in range(N_THREADS)]
        start_time = time.time()
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        end_time = time.time()
        times.append(end_time - start_time)
    print(f"Time: {min(times)} (best of 3)")