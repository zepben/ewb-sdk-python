


__all__ = ["MetricsStore"]


#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

class MetricsStore(object):
    """
    We store buckets of time (5 minute intervals), which map to meters which map to Reading types (see metering.py)
    to ordered lists of readings of that type.
    If a meter doesn't report for a bucket, that meter did not report any metrics for that time period
    """
    def __init__(self, bucket_duration: int = 5000):
        self.store = dict()
        self.bucket_duration = bucket_duration
        self._ordered_buckets = []
        self._bucket_times = set()

    def _get_bucket(self, timestamp):
        """
        Return the timestamp defining each bucket. These will start from 0 and be in intervals of `self.bucket_duration`
        """
        return timestamp - (timestamp % self.bucket_duration)


    def __next__(self):
        for r in self.ascending_iteration():
            yield r

        raise StopIteration()

    @property
    def buckets(self):
        """
        Time buckets in this metrics store.
        Returns List of present time buckets in ascending order
        """
        # We lazy sort because we don't want to slow down write times. This will probably disappear in the long run
        # TODO: Revisit this after first stable version, potentially when a timeseries DB is implemented

        ordered_buckets = sorted(self._bucket_times)
        return ordered_buckets

    def ascending_iteration(self):
        """

        Returns Mapping of meter IDs to Meter's by bucket time in ascending order
        """
        for bucket_time in self.buckets:
            for meter in self.store[bucket_time].values():
                yield meter

    def store_meter_reading(self, meter_reading, reading_type):
        """
        Stores a given meter reading. If the meter already has readings in the bucket it will append
        the readings to the existing meter, based on the type of the reading.


        Note that a MeterReadings mRID is not used as part of this function. For the purposes of storing readings,
        only the associated meter mRID is considered.
        `meter_reading`
        Returns
        """
        for reading in meter_reading.readings:
            bucket_time = self._get_bucket(reading.timestamp)
            bucket = self.store.get(bucket_time, {})
            self._bucket_times.add(bucket_time)
            reading_types = bucket.get(meter_reading.meter_mrid, {})
            readings = reading_types.get(reading_type, [])
            readings.append(reading)
            reading_types[reading_type] = readings
            bucket[meter_reading.meter_mrid] = reading_types
            self.store[bucket_time] = bucket
