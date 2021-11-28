import time
from threading import Thread


def count():
    n = 0
    while True:
        n += 1
        print(n)
        time.sleep(1)


def main():
    t = Thread(target=count)
    # t = Thread(target=count, daemon=True)
    t.start()
    time.sleep(3)
    print("Stopping program")


if __name__ == "__main__":
    main()
