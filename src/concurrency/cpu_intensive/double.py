import time
from threading import Thread


def countdown(n):
    while n > 0:
        n -= 1


COUNT = 10_000_000


if __name__ == "__main__":
    times = []
    for _ in range(3):
        start_time = time.time()
        t1 = Thread(target=countdown, args=(COUNT // 2,))
        t2 = Thread(target=countdown, args=(COUNT // 2,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        end_time = time.time()
        times.append(end_time - start_time)
    print(f"Average time: {sum(times)/len(times)}")