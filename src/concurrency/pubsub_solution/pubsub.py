import logging
from queue import Queue, Empty
from threading import Event, Thread
from collections import namedtuple


PublisherData = namedtuple("PublisherData", ["queue", "name", "agent", "stop_event"])
SubscriberData = namedtuple("SubscriberData", ["queue", "name"])


class PubSub:
    def __init__(self, name):
        self.name = name
        self._publishers = {}
        self._subscribers = {}
        self._agents = {}
        self._agent_stop_events = {}
        self._databus = Queue()
        self._pubsub_thread = None
        self._is_running = False

    def start(self):
        self._pubsub_thread = Thread(
            target=self.distribute,
            name=f"{self.name}-distribute",
            daemon=True,
        )
        logging.debug("Starting thread %s", self._pubsub_thread.name)
        self._is_running = True
        self._pubsub_thread.start()

    def stop(self):
        if self._pubsub_thread:
            logging.debug("Stopping thread %s", self._pubsub_thread.name)
            self._is_running = False
            self._pubsub_thread.join(0.5)
            if self._pubsub_thread.is_alive():
                logging.error("Thread %s did not terminate", self._pubsub_thread.name)
            else:
                logging.debug("Thread %s terminated", self._pubsub_thread.name)
            self._pubsub_thread = None

    def add_publisher(self, pub):
        pub_queue = Queue()
        pub_name = pub.name if hasattr(pub, "name") else repr(pub)
        pub_stop_event = Event()
        pub_agent = Thread(
            target=self.agent,
            name=f"{self.name}-agent[{pub_name}]", args=(pub_queue, pub_stop_event, pub_name),
            daemon=True,
        )
        self._publishers[pub] = PublisherData(pub_queue, pub_name, pub_agent, pub_stop_event)
        pub_agent.start()
        logging.debug("Added publisher %s", pub_name)
        return pub_queue

    def remove_publisher(self, pub):
        if pub not in self._publishers:
            logging.error("Request to remove an unregistered publisher <%r>", pub)
            return
        pub_data = self._publishers[pub]
        logging.debug("Removing publisher %s", pub_data.name)
        pub_data.stop_event.set()
        pub_data.agent.join(0.5)
        if pub_data.agent.is_alive():
            logging.error("Thread %s did not terminate", pub_data.name)
        del self._publishers[pub]

    def add_subscriber(self, sub):
        sub_queue = Queue()
        sub_name = sub.name if hasattr(sub, "name") else repr(sub)
        self._subscribers[sub] = SubscriberData(sub_queue, sub_name)
        logging.debug("Added subscriber %s", sub_name)
        return sub_queue

    def remove_subscriber(self, sub):
        if sub not in self._subscribers:
            logging.error("Request to remove an unsubscribed subscriber <%r>", sub)
            return
        logging.debug("Removing subscriber %s", self._subscribers[sub].name)
        del self._subscribers[sub]

    def agent(self, pub_queue, stop_event, pub_name):
        while not stop_event.is_set():
            try:
                message = pub_queue.get(timeout=0.1)
            except Empty:
                pass
            else:
                logging.debug("Received message %s", message)
                self._databus.put((pub_name, message))
        logging.debug("Terminating agent thread")

    def distribute(self):
        while self._is_running:
            try:
                pub_name, message = self._databus.get(timeout=0.1)
            except Empty:
                pass
            else:
                for sub_data in tuple(self._subscribers.values()):
                    logging.debug("Sending message %s from %s to %s", message, pub_name, sub_data.name)
                    sub_data.queue.put((pub_name, message))
