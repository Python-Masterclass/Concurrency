import time
from threading import Thread


def count():
    n = 0
    while True:
        n += 1
        print(n)
        time.sleep(1)


if __name__ == "__main__":
    t = Thread(target=count)
    t.start()
    raise RuntimeError