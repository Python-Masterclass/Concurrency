import concurrent.futures
import queue
import time
from threading import Thread, Event


def oops(stop):
    for i in range(3):
        if stop.is_set():
            break
        print(f"oops {i}")
        time.sleep(0.5)
    else:
        raise RuntimeError


def count(stop):
    for i in range(6):
        if stop.is_set():
            break
        print(f"count {i}")
        time.sleep(0.5)


class ReRaiseThread(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exc = None

    def run(self):
        try:
            super().run()
        except BaseException as e:
            self.exc = e

    def join(self, *args, **kwargs):
        super().join(*args, **kwargs)
        if self.exc:
            raise self.exc


def main1():
    stop_event = Event()
    t1 = Thread(target=oops, args=(stop_event,))
    t2 = Thread(target=count, args=(stop_event,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


def main2():
    stop_event = Event()
    t1 = ReRaiseThread(target=oops, args=(stop_event,))
    t2 = ReRaiseThread(target=count, args=(stop_event,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


def main3():
    stop_event = Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        t1 = executor.submit(oops, stop_event)
        t2 = executor.submit(count, stop_event)
    for t in (t1, t2):
        if e := t.exception():
            raise e


def main4():
    stop_event = Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        t1 = executor.submit(oops, stop_event)
        t2 = executor.submit(count, stop_event)
        for f in concurrent.futures.as_completed([t1, t2]):
            if exc := f.exception():
                # Don't raise yet, because that would be caught by the with statement
                stop_event.set()
        if exc:
            raise exc


class QueueExceptionThread(Thread):
    exception_queue = queue.Queue()

    def run(self):
        try:
            super().run()
        except BaseException as e:
            self.exception_queue.put(e)


def main5():
    stop_event = Event()
    threads = [
        QueueExceptionThread(target=oops, args=(stop_event,)),
        QueueExceptionThread(target=count, args=(stop_event,)),
    ]
    for t in threads:
        t.start()
    while True:
        try:
            exc = QueueExceptionThread.exception_queue.get(block=False)
        except queue.Empty:
            # do other useful stuff
            print(".")
            time.sleep(0.2)
        else:
            # Exception occurred
            stop_event.set()
            for t in threads:
                t.join()
            raise exc


if __name__ == "__main__":
    main5()