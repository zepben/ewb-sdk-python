#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from enum import Enum

__all__ = ['DatabaseType']


class DatabaseType(Enum):
    CUSTOMER = (0, True, "customers")
    DIAGRAM = (1, True, "diagrams")
    MEASUREMENT = (2, True, "measurements")
    NETWORK_MODEL = (3, True, "network-model")
    TILE_CACHE = (4, True, "tile-cache")
    ENERGY_READING = (5, True, "load-readings")

    ENERGY_READINGS_INDEX = (6, False, "load-readings-index")
    LOAD_AGGREGATOR_METERS_BY_DATE = (7, False, "load-aggregator-mbd")
    WEATHER_READING = (8, False, "weather-readings")
    RESULTS_CACHE = (9, False, "results-cache")

    @property
    def short_name(self):
        return str(self)[27:]

    @property
    def per_date(self):
        return self.value[1]

    @property
    def file_descriptor(self):
        return self.value[2]
