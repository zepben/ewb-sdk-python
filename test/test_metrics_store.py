from zepben.model.metering import MeterReading, ReactivePowerReading, RealPowerReading, VoltageReading
from zepben.model.metrics_store import MetricsStore


class TestMetricsStore(object):

    def test_iteration(self):
        store = MetricsStore()
        r1 = RealPowerReading(1, 1.0)
        r2 = ReactivePowerReading(2, 1.0)
        r3 = VoltageReading(3, 1.0)
        mr = MeterReading(meter="10", readings=[r1, r2, r3])
        store.store_meter_reading(mr)


