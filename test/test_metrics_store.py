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


