import logging
import queue
import threading


class PubSub:
    def __init__(self, name):
        self.name = name
        self.sources = {}
        self.destinations = {}
        self.listeners = {}
        self.stop_listener = {}
        self.databus = queue.Queue()
        self.is_running = False
        self.pubsub_thread = None

    def start(self):
        self.is_running = True
        self.pubsub_thread = threading.Thread(
            target=self.distribute,
            name=f"{self.name}-distribute",
            daemon=True,
        )
        logging.debug("Starting thread %s", self.pubsub_thread.name)
        self.pubsub_thread.start()

    def stop(self):
        if self.is_running:
            logging.debug("Stopping thread %s", self.pubsub_thread.name)
            self.is_running = False
            self.pubsub_thread.join(0.5)
            if self.pubsub_thread.is_alive():
                logging.error("Thread %s did not terminate", self.pubsub_thread.name)
            else:
                logging.debug("Thread %s terminated", self.pubsub_thread.name)
            self.pubsub_thread = None

    def add_source(self, src, name):
        self.sources[src] = name
        self.stop_listener[src] = threading.Event()
        self.listeners[src] = threading.Thread(
            target=self.listen,
            name=f"{self.name}-listen[{name}]", args=(src, self.stop_listener[src]),
            daemon=True,
        )
        logging.debug("Added source %s", name)
        self.listeners[src].start()

    def remove_source(self, src):
        logging.debug("Removing source %s", self.sources[src])
        self.stop_listener[src].set()
        self.listeners[src].join(0.5)
        if self.listeners[src].is_alive():
            logging.error("Thread %s did not terminate", self.listeners[src].name)
        del self.sources[src]
        del self.stop_listener[src]
        del self.listeners[src]

    def add_destination(self, dest, name):
        self.destinations[dest] = name
        logging.debug("Added destination %s", name)

    def remove_destination(self, dest):
        logging.debug("Removing destination %s", self.destinations[dest])
        del self.destinations[dest]

    def listen(self, src, stop_event):
        while not stop_event.is_set():
            try:
                message = src.get(timeout=0.1)
            except queue.Empty:
                pass
            else:
                logging.debug("Received message %s from %s", message, self.sources[src])
                self.databus.put((self.sources[src], message))
        logging.debug("Terminating listener thread")

    def distribute(self):
        while self.is_running:
            try:
                data = self.databus.get(timeout=0.1)
            except queue.Empty:
                pass
            else:
                for dest, name in self.destinations.copy().items():
                    logging.debug("Sending message %s from %s to %s", data[1], data[0], name)
                    dest.put(data)
