from abc import abstractmethod, ABC

class BaseTracker(ABC):
    """
    An interface used by :class:`zepben.model.tracing.Traversal`'s to 'track' items that have been visited.

    A `Traversal` will utilise `has_visited`, `visit`, and `clear`.
    """
    @abstractmethod
    def has_visited(self, item):
        """
        Check if the tracker has already seen an item.
        :param item: The item to check if it has been visited.
        :return: true if the item has been visited, otherwise false.
        """
        raise NotImplementedError()

    @abstractmethod
    def visit(self, item):
        """
        Visit an item. Item will not be visited if it has previously been visited.
        :param item: The item to visit.
        :return: True if visit succeeds. False otherwise.
        """
        raise NotImplementedError()

    @abstractmethod
    def clear(self):
        """
        Clear the tracker, removing all visited items.
        """
        raise NotImplementedError()


class Tracker(BaseTracker):
    """
    An interface used by :class:`zepben.model.tracing.Traversal`'s to 'track' items that have been visited.
    """
    def __init__(self):
        self.visited = set()

    def has_visited(self, item):
        """
        Check if the tracker has already seen an item.
        :param item: The item to check if it has been visited.
        :return: true if the item has been visited, otherwise false.
        """
        return item in self.visited

    def visit(self, item):
        """
        Visit an item. Item will not be visited if it has previously been visited.
        :param item: The item to visit.
        :return: True if visit succeeds. False otherwise.
        """
        if item in self.visited:
            return False
        else:
            self.visited.add(item)
            return True

    def clear(self):
        """
        Clear the tracker, removing all visited items.
        """
        self.visited.clear()
