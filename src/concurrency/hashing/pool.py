import concurrent.futures
import hashlib
import time

from concurrency.hashing.messages import get_messages

messages = get_messages()


N_WORKERS = 4

if __name__ == "__main__":
    times = []
    for _ in range(3):
        start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
            jobs = {executor.submit(hashlib.sha256, msg) for msg in messages}
        end = time.time()
        times.append(end - start)
    print(f"Time: {min(times)} (best of 3)")
