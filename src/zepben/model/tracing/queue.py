from collections import deque
from abc import abstractmethod, ABC
from typing import TypeVar, Generic
from heapq import heappush, heappop

T = TypeVar('T')


class Queue(Generic[T], ABC):
    def __init__(self, queue=None):
        if queue is None:
            self.queue = deque()
        else:
            self.queue = queue

    @abstractmethod
    def put(self, item):
        raise NotImplementedError()

    @abstractmethod
    def get(self):
        raise NotImplementedError()

    @abstractmethod
    def empty(self):
        """
        Check if queue is empty
        :return: True if empty, False otherwise
        """
        raise NotImplementedError()

    @abstractmethod
    def peek(self):
        """
        Retrieve next item on queue, but don't remove from queue.
        :return: Next item on the queue
        """
        raise NotImplementedError()

    @abstractmethod
    def clear(self):
        """Clear the queue."""
        raise NotImplementedError()


class FifoQueue(Queue[T]):
    def put(self, item):
        self.queue.append(item)

    def get(self):
        return self.queue.popleft()

    def empty(self):
        """
        Check if queue is empty
        :return: True if empty, False otherwise
        """
        return len(self.queue) == 0

    def peek(self):
        """
        Retrieve next item on queue, but don't remove from queue.
        :return: Next item on the queue
        """
        return self.queue[0]

    def clear(self):
        """Clear the queue."""
        self.queue.clear()


class LifoQueue(Queue[T]):
    def put(self, item):
        self.queue.append(item)

    def get(self):
        return self.queue.pop()

    def empty(self):
        """
        Check if queue is empty
        :return: True if empty, False otherwise
        """
        return len(self.queue) == 0

    def peek(self):
        """
        Retrieve next item on queue, but don't remove from queue.
        :return: Next item on the queue
        """
        return self.queue[-1]

    def clear(self):
        """Clear the queue."""
        self.queue.clear()


class PriorityQueue(Queue[T]):

    def __init__(self):
        """
        """
        super().__init__([])

    def __len__(self):
        return len(self.queue)

    def put(self, item):
        """
        Place an item in the queue based on its priority.
        :param item: The item to place on the queue. Must implement `__lt__`
        :return: True if put was successful, False otherwise.
        """
        heappush(self.queue, item)

    def get(self):
        """
        Get the next item in the queue, removing it from the queue.
        :return: The next item in the queue by priority.
        """
        return heappop(self.queue)

    def peek(self):
        """
        Retrieve the next item in the queue, but don't remove it from the queue.
        Note that you shouldn't modify the returned item after using this function, as you could change its
        priority and thus corrupt the queue. Always use `get` if you intend on modifying the result.
        :return: The next item in the queue
        """
        return self.queue[0]

    def empty(self):
        return len(self) == 0

    def clear(self):
        """Clear the queue."""
        self.queue.clear()
