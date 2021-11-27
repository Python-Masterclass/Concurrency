import threading


def oops():
    raise RuntimeError


if __name__ == "__main__":
    t = threading.Thread(target=oops)
    t.start()
    t.join()
    print("mission completed")