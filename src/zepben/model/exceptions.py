class MissingReferenceException(Exception):
    def __init__(self, info: str = None, **kwargs):
        if info is None:
            self.info = f"{self} was not found in the network. It must be created prior to dependencies."
        else:
            self.info = info
        super().__init__(kwargs)


class NoBaseVoltageException(MissingReferenceException):
    pass


class NoAssetInfoException(MissingReferenceException):
    pass


class NoTerminalException(MissingReferenceException):
    pass


class NoPerLengthSeqImpException(MissingReferenceException):
    pass


class NoConnectivityNodeException(MissingReferenceException):
    pass


class NoUsagePointException(MissingReferenceException):
    pass


class NoCustomerException(MissingReferenceException):
    pass


class NoEquipmentException(MissingReferenceException):
    pass


class NoMeterException(MissingReferenceException):
    pass


class NoBreakerException(MissingReferenceException):
    pass


class NoACLineSegmentException(MissingReferenceException):
    pass


class NoTransformerException(MissingReferenceException):
    pass


class NoEnergySourceException(MissingReferenceException):
    pass


class NoEnergyConsumerException(MissingReferenceException):
    pass


class AlreadyExistsException(Exception):
    pass

class ReadingException(Exception):
    pass


class PhaseException(Exception):
    pass
