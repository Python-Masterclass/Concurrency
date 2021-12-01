import time


def countdown(n):
    while n > 0:
        n -= 1


COUNT = 10_000_000


if __name__ == "__main__":
    times = []
    for _ in range(3):
        start_time = time.time()
        countdown(COUNT)
        end_time = time.time()
        times.append(end_time - start_time)
    print(f"Time: {min(times)} (best of 3)")