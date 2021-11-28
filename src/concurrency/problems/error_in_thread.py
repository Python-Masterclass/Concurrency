import concurrent.futures
import time
from threading import Thread


def oops():
    for i in range(3):
        print("oops", i)
        time.sleep(0.5)
    raise RuntimeError


def count():
    for i in range(6):
        print("count", i)
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
    t1 = Thread(target=oops)
    t2 = Thread(target=count)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


def main2():
    t1 = ReRaiseThread(target=oops)
    t2 = ReRaiseThread(target=count)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


def main3():
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        t1 = executor.submit(oops)
        t2 = executor.submit(count)
    for t in (t1, t2):
        if e := t.exception():
            raise e


def main4():
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        t1 = executor.submit(oops)
        t2 = executor.submit(count)
        for f in concurrent.futures.as_completed([t1, t2]):
            if e := f.exception():
                print(e)


if __name__ == "__main__":
    main1()