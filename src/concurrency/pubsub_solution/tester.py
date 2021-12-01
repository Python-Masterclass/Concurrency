import logging
import time

from pubsub import PubSub
from publisher import Publisher
from subscriber import Subscriber


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] (%(threadName)s) %(message)s",
)


if __name__ == "__main__":
    pubsub = PubSub("pubsub")
    time.sleep(0.001)

    sub1 = Subscriber("Subscriber1")
    sub2 = Subscriber("Subscriber2")
    sub1.subscribe(pubsub)
    sub2.subscribe(pubsub)
    time.sleep(0.001)

    publisher1 = Publisher("Publisher1")
    publisher1.register(pubsub)
    time.sleep(0.001)
    publisher1.publish("Message 1")  # Both subscribers receive this message
    time.sleep(0.001)

    sub1.unsubscribe(pubsub)  # Subscriber 1 no longer receives messages
    time.sleep(0.001)

    publisher1.publish("Message 2")  # Subscriber 2 receives Message 2. Subscriber 1 may also get it (race condition)
    time.sleep(0.001)

    sub3 = Subscriber("Subscriber3")
    sub3.subscribe(pubsub)
    time.sleep(0.001)

    publisher1.publish("Message 3")  # Subscriber 2 and 3 receive Message3 (and possibly Subscriber 1)
    time.sleep(0.001)

    sub1.subscribe(pubsub)  # Subscriber 1 re-subscribes
    time.sleep(0.001)

    publisher2 = Publisher("Publisher2")
    publisher2.register(pubsub)
    time.sleep(0.001)
    publisher2.publish("Hi there")  # Message is received by all three subscribers
    time.sleep(0.001)

    publisher1.unregister(pubsub)
    time.sleep(0.001)

    publisher1.publish("Message 4")  # This message is not distributed anymore. Error message is logged
    publisher2.publish("Still there?")  # This message is received by all three subscribers

    time.sleep(0.5)
