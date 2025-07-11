#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["measurement_value_to_cim", "analog_value_to_cim", "accumulator_value_to_cim", "discrete_value_to_cim"]

from zepben.protobuf.cim.iec61970.base.meas.AccumulatorValue_pb2 import AccumulatorValue as PBAccumulatorValue
from zepben.protobuf.cim.iec61970.base.meas.AnalogValue_pb2 import AnalogValue as PBAnalogValue
from zepben.protobuf.cim.iec61970.base.meas.DiscreteValue_pb2 import DiscreteValue as PBDiscreteValue
from zepben.protobuf.cim.iec61970.base.meas.MeasurementValue_pb2 import MeasurementValue as PBMeasurementValue

from zepben.ewb.model.cim.iec61970.base.meas.accumulator_value import AccumulatorValue
from zepben.ewb.model.cim.iec61970.base.meas.analog_value import AnalogValue
from zepben.ewb.model.cim.iec61970.base.meas.discrete_value import DiscreteValue
from zepben.ewb.model.cim.iec61970.base.meas.measurement_value import MeasurementValue
from zepben.ewb.services.measurement.measurements import MeasurementService


######################
# IEC61970 Base Meas #
######################

def accumulator_value_to_cim(pb: PBAccumulatorValue, service: MeasurementService):
    # noinspection PyArgumentList
    cim = AccumulatorValue(accumulator_mrid=pb.accumulatorMRID, value=pb.value)
    measurement_value_to_cim(pb.mv, cim)
    service.add(cim)


def analog_value_to_cim(pb: PBAnalogValue, service: MeasurementService):
    # noinspection PyArgumentList
    cim = AnalogValue(analog_mrid=pb.analogMRID, value=pb.value)
    measurement_value_to_cim(pb.mv, cim)
    service.add(cim)


def discrete_value_to_cim(pb: PBDiscreteValue, service: MeasurementService):
    # noinspection PyArgumentList
    cim = DiscreteValue(discrete_mrid=pb.discreteMRID, value=pb.value)
    measurement_value_to_cim(pb.mv, cim)
    service.add(cim)


def measurement_value_to_cim(pb: PBMeasurementValue, cim: MeasurementValue):
    cim.time_stamp = pb.timeStamp.ToDatetime()


PBAccumulatorValue.to_cim = accumulator_value_to_cim
PBAnalogValue.to_cim = analog_value_to_cim
PBDiscreteValue.to_cim = discrete_value_to_cim
PBMeasurementValue.to_cim = measurement_value_to_cim
