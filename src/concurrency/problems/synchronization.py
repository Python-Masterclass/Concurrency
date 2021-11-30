import concurrent.futures
import queue
import random
import threading
import time
from collections import deque


class DoublerWithEvents:
    def __init__(self):
        self.waiting_for_data = threading.Event()
        self.data_available = threading.Event()
        self.waiting_for_data.set()
        self.data_available.clear()
        self.data = None

    def generate(self):
        if self.waiting_for_data.wait():
            self.waiting_for_data.clear()
            self.data = random.randint(0, 10)
            print(f"generated {self.data}")
            self.data_available.set()

    def report(self):
        if self.data_available.wait():
            self.data_available.clear()
            print(f"{self.data} -> {2 * self.data}")
            self.waiting_for_data.set()


class DoublerWithEventsAndLocks:
    def __init__(self):
        self.waiting_for_data_lock = threading.Lock()
        self.waiting_for_data = threading.Event()
        self.data_available_lock = threading.Lock()
        self.data_available = threading.Event()
        self.waiting_for_data.set()
        self.data_available.clear()
        self.data = None

    def generate(self):
        # Grab lock first, to avoid multiple generate functions running simultaneously
        with self.waiting_for_data_lock:
            # Wait for waiting_for_data to be set
            if self.waiting_for_data.wait():
                self.data = random.randint(0, 10)
                print(f"Generated {self.data}")
                self.waiting_for_data.clear()  # Note: order is important
                self.data_available.set()

    def report(self):
        with self.data_available_lock:
            if self.data_available.wait():
                print(f"{self.data} -> {2 * self.data}")
                self.data = None
                self.data_available.clear()
                self.waiting_for_data.set()


class DoublerWithCondition:
    def __init__(self):
        self.data_available = threading.Condition()
        self.data = None

    def generate(self):
        with self.data_available:
            data = random.randint(0, 10)
            self.data = data
            print(f"Generated {data}.")
            self.data_available.notify()

    def report(self):
        with self.data_available:
            while self.data is None:
                self.data_available.wait()
            print(f"{self.data} -> {2 * self.data}\n")
            self.data = None


class DoublerWithTwoConditions:
    def __init__(self):
        self.data_available = threading.Condition()
        self.data_consumed = threading.Condition()
        self.data = None

    def generate(self):
        with self.data_consumed:
            while self.data is not None:
                self.data_consumed.wait()
            with self.data_available:
                data = random.randint(0, 10)
                self.data = data
                print(f"Generated {data}.")
                self.data_available.notify()

    def report(self):
        with self.data_available:
            while self.data is None:
                self.data_available.wait()
            print(f"{self.data} -> {2 * self.data}\n")
            with self.data_consumed:
                self.data = None
                self.data_consumed.notify()


class AndGate:
    def __init__(self):
        self.barrier = threading.Barrier(2, action=self.report)
        self.data1 = queue.Queue()
        self.data2 = queue.Queue()
        self.d1 = None
        self.d2 = None
        self.lock1 = threading.Lock()
        self.lock2 = threading.Lock()

    def input1(self):
        with self.lock1:
            self.d1 = self.data1.get()
            print(f"input 1 got {self.d1}")
            self.barrier.wait()

    def input2(self):
        with self.lock2:
            self.d2 = self.data2.get()
            print(f"input 2 got {self.d2}")
            self.barrier.wait()

    def report(self):
        print(f"{self.d1} and {self.d2} -> {self.d1 and self.d2}")


class DoublerWithQueue:
    def __init__(self):
        self.data_queue = queue.Queue(maxsize=1)

    def generate(self):
        data = random.randint(0, 10)
        self.data_queue.put(data)
        print(f"Generated {data}\n")

    def report(self):
        data = self.data_queue.get()
        print(f"{data} -> {2 * data}\n")


def main():
    doubler = DoublerWithTwoConditions()
    tasks = [doubler.generate, doubler.report] * 20
    random.shuffle(tasks)
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        for t in tasks:
            executor.submit(t)


def main_and_gate():
    and_gate = AndGate()
    tasks = [and_gate.input1, and_gate.input2] * 10
    random.shuffle(tasks)
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        for t in tasks:
            executor.submit(t)
        data = [True, False] * 10
        queue = [and_gate.data1, and_gate.data2] * 10
        random.shuffle(data)
        random.shuffle(queue)
        for q, d in zip(queue, data):
            q.put(d)


if __name__ == "__main__":
    main_and_gate()
