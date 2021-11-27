import hashlib
import time
from threading import Thread

from concurrency.hashing.messages import get_messages

messages = get_messages()


def calculate_sha256(msg_list):
    for m in msg_list:
        _ = hashlib.sha256(m)


N_THREADS = 2

if __name__ == "__main__":
    times = []
    sl = 8 // N_THREADS  # Length of message subset
    msg_subsets = [messages[(t * sl) : ((t + 1) * sl)] for t in range(N_THREADS)]
    for _ in range(3):
        t_list = [Thread(target=calculate_sha256, args=(msg_subsets[t],)) for t in range(N_THREADS)]
        start = time.time()
        for t in t_list:
            t.start()
        for t in t_list:
            t.join()
        end = time.time()
        times.append(end - start)
    print(f"Time: {min(times)} (best of 3)")

