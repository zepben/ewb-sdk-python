
class ConnectivityResult(object):
    """
    The connectivity between two connected terminals
    Attributes:
        from_terminal : Originating :class:`zepben.model.Terminal`
        to_terminal : Destination :class:`zepben.model.Terminal`
    """
    def __init__(self, from_terminal, to_terminal):
        """
        Create a ConnectivityResult.
        :param from_terminal: The originating :class:`zepben.model.Terminal`
        :param to_terminal: The destination :class:`zepben.model.Terminal`
        """
        self.from_terminal = from_terminal
        self.to_terminal = to_terminal
