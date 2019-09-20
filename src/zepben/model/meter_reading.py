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


from typing import Iterable
from zepben.cim.IEC61968.metering_pb2 import Reading as PBReading, ReadingType as PBReadingType, MeterReading as PBMeterReading
from google.protobuf.timestamp_pb2 import Timestamp


class Reading(object):

    def __init__(self, timestamp, value, kind, phase, unit):
        self.timestamp = timestamp
        self.value = value
        self.kind = kind
        self.phase = phase
        self.unit = unit

    def to_pb(self):
        typ = PBReadingType(kind=self.kind, phases=self.phase, unitSymbol=self.unit)
        ts = Timestamp(seconds=self.timestamp)
        return PBReading(timestamp=ts, value=self.value, type=typ)


class Meter(object):
    def __init__(self, mrid, name, psr_id):
        """

        :param mrid: Equipment ID?
        :param name: Meter ID?
        :param psr_id: PowerSystemResource ID that this meter is associated with
        """
        self._m_r_i_d = mrid
        self.name = name
        self.power_system_resource = psr_id
        self._readings = []
        self._is_sorted = False

    @property
    def mrid(self):
        return self._m_r_i_d

    @property
    def readings(self):
        """
        We sort lazily to optimise insertion times. We expect that there will only ever be a negligible number
        of readings as they should always be bucketed upstream.
        TODO: Check later if sorting lazily is a terrible idea. Might just always make sense to add readings
          in batches and sort at insertion time - depends on if we have access to insert in batches
        :return:
        """
        if not self._is_sorted:
            self._readings.sort(key=lambda x: x.timestamp)
            self._is_sorted = True
        return self._readings

    def add_reading(self, timestamp, value, kind, phase, unit):
        self._readings.append(Reading(timestamp, value, kind, phase, unit))
        self._is_sorted = False

    def add_readings(self, readings: Iterable[Reading]):
        for reading in readings:
            self._readings.append(reading)
        self._readings.sort(key=lambda x: x.timestamp)
        self._is_sorted = True

    def to_pb(self):
        readings = [reading.to_pb() for reading in self.readings]
        return PBMeterReading(mRID=self.mrid, name=self.name, powerSystemResource=self.power_system_resource, readings=readings)



