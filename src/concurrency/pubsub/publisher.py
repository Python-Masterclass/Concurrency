import logging


class Publisher:
    def __init__(self, name):
        self.name = name
        self._channel = None

    def register(self, pubsub):
        logging.debug("Registering %s", self.name)
        self._channel = pubsub.add_publisher(self)

    def unregister(self, pubsub):
        pubsub.remove_publisher(self)
        self._channel = None
        logging.debug("Unregistered %s", self.name)

    def publish(self, message):
        if self._channel:
            self._channel.put(message)
        else:
            logging.error("Publisher %s is not registered", self.name)
