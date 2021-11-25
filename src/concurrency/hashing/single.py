import hashlib
import time

from concurrency.hashing.messages import get_messages

messages = get_messages()


def calculate_sha256(msg_list):
    for m in msg_list:
        _ = hashlib.sha256(m)


if __name__ == "__main__":
    times = []
    for _ in range(3):
        start = time.time()
        calculate_sha256(messages)
        end = time.time()
        times.append(end - start)
    print(f"Time: {min(times)} (best of 3)")


