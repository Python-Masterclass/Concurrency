import logging
from queue import Queue
from publisher import Publisher
from subscriber import Subscriber


class PubSub:
    def __init__(self, name: str) -> None:
        """
        This prepares the infrastructure:
        - Storage for an arbitrary number of publisher,
          together with their queue and associated data and processing
        - Storage for an arbitrary number of subscribers,
          together with their queue and any associated data and processing
        - A mechanism for getting data from the publishers and distributing
          this to the subscribers.

        Args:
            name: the name of the PubSub instance
        """

    def add_publisher(self, pub: Publisher) -> Queue:
        """Add a publisher

        Returns a queue to the caller.
        Messages that are put into this queue are distributed to all known subscribers.

        Note: the pub parameter must be saved, because a later call to remove_publisher
        must be able to release all data structures and resources related to the publisher.

        Args:
            pub: the publisher object

        Returns:
             The queue via which the publisher can send messages
        """

    def remove_publisher(self, pub: Publisher) -> None:
        """Remove a publisher

        Remove all data structures related to the publisher.

        Args:
            pub: the publisher to be removed
        """

    def add_subscriber(self, sub: Subscriber) -> Queue:
        """Add a subscriber

        This returns a queue via which the subscriber receives messages.
        Note that the sub parameter must be saved, to ensure that the subscriber can unsubscribe later

        Args:
            sub: the subscriber

        Returns:
            A queue via which messages are received
        """

    def remove_subscriber(self, sub):
        """Remove a subscriber

        Remove all data structures related to the subscriber.

        Args:
            sub: the subscriber to be removed
        """
