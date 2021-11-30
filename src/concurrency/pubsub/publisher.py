import logging
import queue


class Publisher:
    def __init__(self, name):
        self.name = name
        self.out_queue = queue.Queue()
        self.registered = False

    def register(self, pubsub):
        logging.debug("Registering %s", self.name)
        pubsub.add_source(self.out_queue, self.name)
        self.registered = True

    def unregister(self, pubsub):
        pubsub.remove_source(self.out_queue)
        self.registered = False
        logging.debug("Unregistered %s", self.name)

    def publish(self, message):
        if self.registered:
            self.out_queue.put(message)
        else:
            logging.error("Publisher %s is not registered", self.name)
