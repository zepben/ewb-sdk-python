class MissingReferenceException(Exception):
    def __init__(self, *args, **kwargs):
        self.info = f"{self} was not found in the network. It must be created prior to dependencies."
        super().__init__(args, kwargs)


class NoBaseVoltageException(MissingReferenceException):
    pass


class NoAssetInfoException(MissingReferenceException):
    pass


class NoPerLengthSeqImpException(MissingReferenceException):
    pass


class NoUsagePointException(MissingReferenceException):
    pass


class NoCustomerException(MissingReferenceException):
    pass


class NoEquipmentException(MissingReferenceException):
    pass

class NoMeterException(MissingReferenceException):
    pass

class ReadingException(Exception):
    pass
