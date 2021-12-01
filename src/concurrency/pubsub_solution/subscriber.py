import logging
import queue
import threading


class Subscriber:
    def __init__(self, name):
        self.name = name
        self._msg_queue = None
        self._subscribed = threading.Event()
        self._monitor_thread = threading.Thread(target=self.monitor, name=self.name, daemon=True)
        self._monitor_thread.start()

    def subscribe(self, pubsub):
        logging.debug("Subscriber %s is subscribing", self.name)
        self._msg_queue = pubsub.add_subscriber(self)
        self._subscribed.set()

    def unsubscribe(self, pubsub):
        logging.debug("Subscriber %s is unsubscribing", self.name)
        pubsub.remove_subscriber(self)
        self._subscribed.clear()

    def monitor(self):
        logging.debug("Waiting for subscription")
        while True:
            self._subscribed.wait()
            logging.debug("Subscription active")
            while self._subscribed.is_set():
                try:
                    source, message = self._msg_queue.get(timeout=0.1)
                except queue.Empty:
                    pass
                else:
                    logging.info("Received message %s from %s", message, source)
            logging.debug("Subscription cancelled")
