"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""


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


class NoAssetInfoException(MissingReferenceException):
    pass


class NetworkException(Exception):
    pass


class AlreadyExistsException(Exception):
    pass


class ReadingException(Exception):
    pass


class PhaseException(Exception):
    pass


class CoreException(Exception):
    pass


class WiringException(Exception):
    pass
