import logging
import queue
import threading


class Subscriber:
    def __init__(self, name):
        self.name = name
        self.in_queue = queue.Queue()
        self.subscribed = threading.Event()
        self.subscription_thread = threading.Thread(target=self.monitor, name=self.name, daemon=True)
        self.subscription_thread.start()

    def subscribe(self, pubsub):
        logging.debug("Subscriber %s is subscribing", self.name)
        pubsub.add_destination(self.in_queue, self.name)
        self.subscribed.set()

    def unsubscribe(self, pubsub):
        logging.debug("Subscriber %s is unsubscribing", self.name)
        pubsub.remove_destination(self.in_queue)
        self.subscribed.clear()

    def monitor(self):
        logging.debug("Waiting for subscription")
        while True:
            self.subscribed.wait()
            logging.debug("Subscription active")
            while self.subscribed.is_set():
                try:
                    source, topic = self.in_queue.get(timeout=0.1)
                except queue.Empty:
                    pass
                else:
                    logging.info("Received message %s from %s", topic, source)
            logging.debug("Subscription cancelled")
