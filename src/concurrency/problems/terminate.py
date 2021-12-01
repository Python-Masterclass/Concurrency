import time
from threading import Thread, Event


def count(stop_event):
    n = 0
    while not stop_event.is_set():
        n += 1
        print(n)
        time.sleep(1)


def other_work():
    time.sleep(5)
    raise RuntimeError


def main():
    stop_event = Event()
    t = Thread(target=count, args=(stop_event,))
    try:
        t.start()
        other_work()
    except Exception as e:
        print("caught expection")
    finally:
        stop_event.set()
    t.join()


if __name__ == "__main__":
    main()
