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

import logging
from typing import Iterable
from zepben.model.identified_object import IdentifiedObject
from zepben.model.common import Location
from zepben.model.diagram_layout import DiagramObject
from zepben.model.customer import Customer
from zepben.model.exceptions import NoEquipmentException, NoCustomerException, NoMeterException, ReadingException
from zepben.cim.iec61968 import Reading as PBReading, MeterReading as PBMeterReading, Meter as PBMeter, UsagePoint as PBUsagePoint
from google.protobuf.timestamp_pb2 import Timestamp
from typing import List, Union
from enum import Enum

logger = logging.getLogger(__name__)


class ReadingType(Enum):
    VOLTAGE = 1
    REACTIVE_POWER = 2
    REAL_POWER = 3


class Reading(object):
    """
    All readings are just a timestamp and value, however the type and unit is inferred from the subtype of Reading that
    is used.
    """
    def __init__(self, timestamp, value):
        self.timestamp = timestamp
        self.value = value

    def to_pb(self):
        ts = Timestamp(seconds=self.timestamp)
        return PBReading(timestamp=ts, value=self.value)

    @staticmethod
    def from_pb(pb_r, reading_type):
        if reading_type == ReadingType.VOLTAGE:
            return VoltageReading(pb_r.timestamp.seconds, pb_r.value)
        elif reading_type == ReadingType.REACTIVE_POWER:
            return ReactivePowerReading(pb_r.timestamp.seconds, pb_r.value)
        elif reading_type == ReadingType.REAL_POWER:
            return RealPowerReading(pb_r.timestamp.seconds, pb_r.value)
        else:
            raise ReadingException(f"Reading type {reading_type} is not supported. Supported types are {[x for x in ReadingType.__members__]}")


class VoltageReading(Reading):
    pass


class ReactivePowerReading(Reading):
    pass


class RealPowerReading(Reading):
    pass


class EndDevice(IdentifiedObject):
    """
    Asset container that performs one or more end device functions. One type of end device is a meter which can perform
    metering, load management, connect/disconnect, accounting functions, etc. Some end devices, such as ones monitoring
    and controlling air conditioners, refrigerators, pool pumps may be connected to a meter. All end devices may have
    communication capability defined by the associated communication function(s).

    An end device may be owned by a consumer, a service provider, utility or otherwise.

    There may be a related end device function that identifies a sensor or control point within a metering application
    or communications systems (e.g., water, gas, electricity).

    Some devices may use an optical port that conforms to the ANSI C12.18 standard for communications.

    Attributes:
        customer : The :class:`zepben.model.Customer` associated with this EndDevice.
        service_location : The :class:`zepben.model.Location` of this EndDevice
    """
    def __init__(self, mrid: str = "", name: str = "", customer: Customer = None, location: Location = None,
                 diag_objs: List[DiagramObject] = None):
        """
        Create an EndDevice
        :param mrid: mRID for this object
        :param name: Any free human readable and possibly non unique text naming the object.
        :param customer: The :class:`zepben.model.Customer` associated with this EndDevice.
        :param location: The :class:`zepben.model.Location` of this EndDevice
        :param diag_objs: An ordered list of :class:`zepben.model.DiagramObject`'s.
        """
        self.customer = customer
        self.service_location = location
        super().__init__(mrid, name, diag_objs)


class UsagePoint(IdentifiedObject):
    """
    Logical or physical point in the network to which readings or events may be attributed.
    Used at the place where a physical or virtual meter may be located; however, it is not required that a meter be present.

    Attributes:
        usage_point_location : The :class:`zepben.model.Location` of this UsagePoint
        end_devices : The :class:`EndDevice`'s (Meter's) associated with this UsagePoint.
        equipment : The :class:`zepben.model.Equipment` associated with this UsagePoint.
    """
    def __init__(self, mrid: str, name: str = "", equipment=None, location=None, end_devices=None,
                 diag_objs: List[DiagramObject] = None):
        """
        A UsagePoint must have at least one piece of equipment present.
        :param mrid: mRID for this object
        :param name: Any free human readable and possibly non unique text naming the object.
        :param equipment: The :class:`zepben.model.Equipment` associated with this UsagePoint.
        :param location: :class:`zepben.model.Location` of this resource.
        :param end_devices: The :class:`EndDevice`'s (Meter's) associated with this UsagePoint.
        :param diag_objs: An ordered list of :class:`zepben.model.DiagramObject`'s.
        """
        super().__init__(mrid, name, diag_objs)
        self.__equipment = equipment if equipment is not None else []
        for equip in self.equipment:
            equip.add_usage_point(self)
        self.usage_point_location = location
        self.__end_devices = end_devices if end_devices is not None else []

    @property
    def equipment(self):
        return self.__equipment

    @property
    def end_devices(self):
        return self.__end_devices

    def add_end_device(self, end_device):
        self.end_devices.append(end_device)

    def is_metered(self):
        """
        Check whether this `UsagePoint` is metered. A `UsagePoint` is metered if it's associated with at
        least one  :class:`zepben.model.EndDevice`.
        :return: True if this UsagePoint has an EndDevice, False otherwise.
        """
        return len(self.end_devices) > 0

    def to_pb(self):
        args = self._pb_args()
        equip_ids = [equip.mrid for equip in self.equipment]
        args['equipmentMRIDs'] = equip_ids
        return PBUsagePoint(**args)

    @staticmethod
    def from_pb(pb_up, network, **kwargs):
        """
        Convert a :class:`zepben.cim.iec61968.metering.UsagePoint` to a UsagePoint. We accept a UsagePoint with no
        equipmentMRIDs set.
        :param pb_up: The protobuf UsagePoint
        :param network: An EquipmentContainer to query for equipment related to this UsagePoint
        :return: A UsagePoint
        """
        equipment = []
        for e in pb_up.equipmentMRIDs:
            try:
                equipment.append(network[e])
            except KeyError as k:
                logger.debug(f"Network was missing equipment {e} for UsagePoint {pb_up.mRID}")
                continue

        return UsagePoint(mrid=pb_up.mRID, name=pb_up.name, equipment=equipment,
                          location=Location.from_pb(pb_up.usagePointLocation),
                          diag_objs=DiagramObject.from_pbs(pb_up.diagramObjects))


class Meter(EndDevice):
    """
    Physical asset that performs the metering role of the usage point.
    Used for measuring consumption and detection of events.

    Attributes:
        usage_points: The :class:`UsagePoints` this Meter is associated with.
    """
    def __init__(self, mrid: str, usage_points: List[UsagePoint], name: str = "", customer: Customer = None,
                 location: Location = None, diag_objs: List[DiagramObject] = None):
        """
        Every UsagePoint associated with this Meter will have a back-reference to the meter added via
        `UsagePoint.add_end_device`
        :param mrid: mRID for this object
        :param name: Any free human readable and possibly non unique text naming the object.
        :param location: :class:`zepben.model.Location` of this resource.
        :param diag_objs: An ordered list of :class:`zepben.model.DiagramObject`'s.
        """
        super().__init__(mrid, name, customer, location, diag_objs)
        self.usage_points = usage_points
        for point in self.usage_points:
            point.add_end_device(self)

    def to_pb(self):
        usage_points = [up.mrid for up in self.usage_points]
        return PBMeter(mRID=self.mrid, name=self.name, usagePointMRIDs=usage_points)

    @staticmethod
    def from_pb(pb_m, network):
        """
        Create a meter from a protobuf Meter
        A meter requires all specified usagePointMRIDs to already exist in the network.
        Customer, serviceLocation, and diagramObjects are optional.
        :param pb_m: A protobuf Meter
        :param network: EquipmentContainer to be used for fetching UsagePoint's and Customer's
        :raises: NoUsagePointException if no UsagePoint has been added to the network.
        :return: a Meter
        """
        usage_points = [network.get_usage_point(p) for p in pb_m.usagePointMRIDs]

        if pb_m.customerMRID:
            try:
                customer = network.get_customer(pb_m.customerMRID)
            except NoCustomerException:
                logger.debug(f"Network was missing customer {pb_m.customerMRID} for meter {pb_m.mRID}")
                customer = None
        else:
            customer = None

        return Meter(mrid=pb_m.mRID, usage_points=usage_points, name=pb_m.name, customer=customer,
                     location=Location.from_pb(pb_m.serviceLocation), diag_objs=DiagramObject.from_pbs(pb_m.diagramObjects))


class MeterReading(IdentifiedObject):
    """
    A set of values (Readings) obtained from a meter.

    Do not use a MeterReading if you are not tying the readings to a Meter. You should instead be using a list of
    Reading's, if all you need is the Reading data.

    Attributes:
        meter : The :class:`Meter` associated with this MeterReading, OR a string of the Meter's MRID.
        readings : A list of (subclass) :class:`Reading`'s acquired from the associated meter.
    """
    def __init__(self, meter: Union[str, Meter], mrid: str = "", name: str = "", readings: List[Reading] = None):
        """
        Create a MeterReading
        :param meter: The :class:`Meter` associated with this MeterReading, OR a string of the Meter's MRID.
        :param mrid: mRID for this object. Optional and not typically used.
        :param name: Any free human readable and possibly non unique text naming the object.
        :param readings: A list of :class:`Reading`'s acquired from the associated meter.
        """
        super().__init__(mrid, name)
        self.meter = meter
        self._readings = readings
        self._sort_readings()
        self.__is_sorted = False

    @property
    def readings(self):
        """
        We sort lazily to optimise insertion times. We expect that there will only ever be a negligible number
        of readings as they should always be bucketed upstream.
        TODO: Check later if sorting lazily is a terrible idea. Might just always make sense to add readings
          in batches and sort at insertion time - depends on if we have access to insert in batches
        :return:
        """
        if not self.__is_sorted:
            self._sort_readings()
            self.__is_sorted = True
        return self._readings

    @property
    def meter_mrid(self):
        """
        Meter could just be an mRID or a Meter (if one exists)
        :return: The mRID of the meter
        """
        if isinstance(self.meter, Meter):
            return self.meter.mrid
        else:
            return self.meter

    def _sort_readings(self):
        """TODO: Acquire lock"""
        self._readings.sort(key=lambda x: x.timestamp)

    def add_reading(self, reading):
        self._readings.append(reading)
        self.__is_sorted = False

    def add_readings(self, readings: Iterable[Reading]):
        self._readings.extend(readings)
        self.__is_sorted = False

    def to_pb(self):
        readings = [r.to_pb() for r in self.readings]
        return PBMeterReading(mRID=self.mrid, name=self.name, meterMRID=self.meter_mrid, readings=readings)

    @staticmethod
    def from_pb(pb_mr, network=None, **kwargs):
        """
        :param pb_mr: The protobuf MeterReading
        :param network: Network to query for the meter. If None we will still return a MeterReading as long as
                        meterMRID is not empty.
        :param kwargs: To be passed through to `Reading.from_pb`
        :return:
        """
        readings = [Reading.from_pb(r, **kwargs) for r in pb_mr.readings]
        if pb_mr.meterMRID:
            if network is not None:
                try:
                    meter = network.get_meter(pb_mr.meterMRID)
                except NoMeterException:
                    meter = pb_mr.meterMRID
            else:
                meter = pb_mr.meterMRID
        else:
            raise NoMeterException("Meter for MeterReading {pb_mr.mrid} was not specified. Please specify a meter")

        return MeterReading(meter=meter, mrid=pb_mr.mRID, name=pb_mr.name, readings=readings)

