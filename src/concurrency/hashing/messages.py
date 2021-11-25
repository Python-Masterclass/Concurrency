import random
from pathlib import Path


def get_messages():
    messages = []
    with open(Path(__file__).parent / "messages", "rb") as f:
        for _ in range(8):
            messages.append(f.read(2 ** 27))
    return messages


if __name__ == "__main__":
    with open(Path(__file__).parent / "messages", "wb") as f:
        for _ in range(8):
            f.write(random.randbytes(2 ** 27))
