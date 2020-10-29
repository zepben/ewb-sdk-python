#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.cimbend.cim.iec61968.metering import MeterReading, ReactivePowerReading, RealPowerReading, VoltageReading
from zepben.cimbend.measurement.metrics_store import MetricsStore


class TestMetricsStore(object):

    def test_iteration(self):
        store = MetricsStore()
        r1 = RealPowerReading(1, 1.0)
        r2 = ReactivePowerReading(2, 1.0)
        r3 = VoltageReading(3, 1.0)
        mr = MeterReading(meter="10", readings=[r1, r2, r3])
        store.store_meter_reading(mr)


