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
    TYPE = 'UNKNOWN'

    def __init__(self, referenced_mrid: str, referrer=None, **kwargs):
        self.referenced_mrid = referenced_mrid
        self.referrer = referrer

        super().__init__(kwargs)

    @property
    def info(self):
        if self.referrer is not None:
            if hasattr(self.referrer, 'DESCRIPTOR'):
                self.referrer_type = self.referrer.DESCRIPTOR.name
                self.referrer_mrid = self.referrer.mRID
            else:
                self.referrer_type = type(self.referrer).__name__
                self.referrer_mrid = self.referrer.mrid
        return f"{self.TYPE} {self.referenced_mrid} was not found in the network. It must be created before {self.referrer_type}[{self.referrer_mrid}] can reference it."


class NoBaseVoltageException(MissingReferenceException):
    TYPE = 'BaseVoltage'


class NoAssetInfoException(MissingReferenceException):
    TYPE = 'AssetInfo'


class NoTerminalException(MissingReferenceException):
    TYPE = 'Terminal'


class NoPerLengthSeqImpException(MissingReferenceException):
    TYPE = 'PerLengthSequenceImpedance'


class NoConnectivityNodeException(MissingReferenceException):
    TYPE = 'ConnectivityNode'


class NoUsagePointException(MissingReferenceException):
    TYPE = 'UsagePoint'


class NoCustomerException(MissingReferenceException):
    TYPE = 'Customer'


class NoEquipmentException(MissingReferenceException):
    TYPE = 'Equipment'


class NoMeterException(MissingReferenceException):
    TYPE = 'Meter'


class NoBreakerException(MissingReferenceException):
    TYPE = 'Breaker'


class NoACLineSegmentException(MissingReferenceException):
    TYPE = 'AcLineSegment'


class NoTransformerException(MissingReferenceException):
    TYPE = 'PowerTransformer'


class NoJunctionException(MissingReferenceException):
    TYPE = 'Junction'


class NoEnergySourceException(MissingReferenceException):
    TYPE = 'EnergySource'


class NoEnergyConsumerException(MissingReferenceException):
    TYPE = 'EnergyConsumer'


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
