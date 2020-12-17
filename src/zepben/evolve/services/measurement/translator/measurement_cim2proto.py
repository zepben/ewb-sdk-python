#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.protobuf.cim.iec61970.base.meas.MeasurementValue_pb2 import MeasurementValue as PBMeasurementValue
from zepben.protobuf.cim.iec61970.base.meas.AccumulatorValue_pb2 import AccumulatorValue as PBAccumulatorValue
from zepben.protobuf.cim.iec61970.base.meas.AnalogValue_pb2 import AnalogValue as PBAnalogValue
from zepben.protobuf.cim.iec61970.base.meas.DiscreteValue_pb2 import DiscreteValue as PBDiscreteValue
from zepben.evolve.model.cim.iec61970.base.meas.value import AnalogValue, AccumulatorValue, DiscreteValue, MeasurementValue
from google.protobuf.timestamp_pb2 import Timestamp

__all__ = ["analogvalue_to_pb", "accumulatorvalue_to_pb", "discretevalue_to_pb", "measurementvalue_to_pb"]


def analogvalue_to_pb(cim: AnalogValue) -> PBAnalogValue:
    return PBAnalogValue(mv=measurementvalue_to_pb(cim), analogMRID=cim.analog_mrid, value=cim.value)


def accumulatorvalue_to_pb(cim: AccumulatorValue) -> PBAccumulatorValue:
    return PBAccumulatorValue(mv=measurementvalue_to_pb(cim), accumulatorMRID=cim.accumulator_mrid, value=cim.value)


def discretevalue_to_pb(cim: DiscreteValue) -> PBDiscreteValue:
    return PBDiscreteValue(mv=measurementvalue_to_pb(cim), discreteMRID=cim.discrete_mrid, value=cim.value)


def measurementvalue_to_pb(cim: MeasurementValue) -> PBMeasurementValue:
    ts = Timestamp()
    ts.FromDatetime(cim.time_stamp)
    return PBMeasurementValue(timeStamp=ts)


AnalogValue.to_pb = analogvalue_to_pb
AccumulatorValue.to_pb = accumulatorvalue_to_pb
DiscreteValue.to_pb = discretevalue_to_pb
MeasurementValue.to_pb = measurementvalue_to_pb

