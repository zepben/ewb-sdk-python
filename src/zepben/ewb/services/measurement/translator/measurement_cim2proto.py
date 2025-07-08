#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["analog_value_to_pb", "accumulator_value_to_pb", "discrete_value_to_pb", "measurement_value_to_pb"]

# noinspection PyPackageRequirements,PyUnresolvedReferences
from google.protobuf.timestamp_pb2 import Timestamp
from zepben.protobuf.cim.iec61970.base.meas.AccumulatorValue_pb2 import AccumulatorValue as PBAccumulatorValue
from zepben.protobuf.cim.iec61970.base.meas.AnalogValue_pb2 import AnalogValue as PBAnalogValue
from zepben.protobuf.cim.iec61970.base.meas.DiscreteValue_pb2 import DiscreteValue as PBDiscreteValue
from zepben.protobuf.cim.iec61970.base.meas.MeasurementValue_pb2 import MeasurementValue as PBMeasurementValue

from zepben.ewb.model.cim.iec61970.base.meas.accumulator_value import AccumulatorValue
from zepben.ewb.model.cim.iec61970.base.meas.analog_value import AnalogValue
from zepben.ewb.model.cim.iec61970.base.meas.discrete_value import DiscreteValue
from zepben.ewb.model.cim.iec61970.base.meas.measurement_value import MeasurementValue


def analog_value_to_pb(cim: AnalogValue) -> PBAnalogValue:
    return PBAnalogValue(mv=measurement_value_to_pb(cim), analogMRID=cim.analog_mrid, value=cim.value)


def accumulator_value_to_pb(cim: AccumulatorValue) -> PBAccumulatorValue:
    return PBAccumulatorValue(mv=measurement_value_to_pb(cim), accumulatorMRID=cim.accumulator_mrid, value=cim.value)


def discrete_value_to_pb(cim: DiscreteValue) -> PBDiscreteValue:
    return PBDiscreteValue(mv=measurement_value_to_pb(cim), discreteMRID=cim.discrete_mrid, value=cim.value)


def measurement_value_to_pb(cim: MeasurementValue) -> PBMeasurementValue:
    ts = Timestamp()
    ts.FromDatetime(cim.time_stamp)
    return PBMeasurementValue(timeStamp=ts)


AnalogValue.to_pb = analog_value_to_pb
AccumulatorValue.to_pb = accumulator_value_to_pb
DiscreteValue.to_pb = discrete_value_to_pb
MeasurementValue.to_pb = measurement_value_to_pb
