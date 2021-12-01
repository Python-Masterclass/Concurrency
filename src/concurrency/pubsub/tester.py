import logging
import time

from concurrency.pubsub_solution.pubsub import PubSub
from publisher import Publisher
from subscriber import Subscriber


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(levelname)s] (%(threadName)s) %(message)s",
)


if __name__ == "__main__":
    pubsub = PubSub("pubsub")
    pubsub.start()

    sub1 = Subscriber("Subscriber1")
    sub2 = Subscriber("Subscriber2")
    sub1.subscribe(pubsub)
    sub2.subscribe(pubsub)

    publisher1 = Publisher("Publisher1")
    publisher1.register(pubsub)
    publisher1.publish("Message 1")  # Both subscribers receive this message
    time.sleep(0)

    pubsub.stop()  # Pubsub can be paused and later resumed

    publisher1.publish("Message 2")  # Messages are buffered while pubsub is paused
    time.sleep(0)

    sub1.unsubscribe(pubsub)  # Subscriber 1 no longer receives messages
    time.sleep(0)

    pubsub.start()  # Resume pubsub. Subscriber 2 receives Message 2

    sub3 = Subscriber("Subscriber3")
    sub3.subscribe(pubsub)

    publisher1.publish("Message 3")  # Subscriber 2 and 3 receive Message3 (and possibly Subscriber 1)
    time.sleep(0)

    sub1.subscribe(pubsub)  # Subscriber 1 re-subscribes

    publisher2 = Publisher("Publisher2")
    publisher2.register(pubsub)
    publisher2.publish("Hi there")  # Message is received by all three subscribers
    time.sleep(0)

    publisher1.unregister(pubsub)

    publisher1.publish("Message 4")  # This message is not distributed anymore. Error message is logged
    publisher2.publish("Still there?")  # This message is received by all three subscribers

    time.sleep(0.5)
