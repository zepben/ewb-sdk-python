#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ['DatabaseType', 'VariantContents']

from enum import Enum
from typing import Set


class DatabaseType(Enum):
    CUSTOMER = (0, True, "customers")
    DIAGRAM = (1, True, "diagrams")
    MEASUREMENT = (2, True, "measurements")
    NETWORK_MODEL = (3, True, "network-model")
    VARIANT = (4, True, "variants")
    TILE_CACHE = (5, True, "tile-cache")
    ENERGY_READING = (6, True, "load-readings")

    ENERGY_READINGS_INDEX = (7, False, "load-readings-index")
    LOAD_AGGREGATOR_METERS_BY_DATE = (8, False, "load-aggregator-mbd")
    WEATHER_READING = (9, False, "weather-readings")
    RESULTS_CACHE = (10, False, "results-cache")

    @property
    def short_name(self):
        return str(self)[15:]

    @property
    def per_date(self):
        return self.value[1]

    @property
    def file_descriptor(self):
        return self.value[2]


class VariantContents(Enum):
    """
    The contents contained within the variant.

    :var DELETIONS_REVERSEMODIFICATIONS: Contains the target of `ObjectDeletion`s and `ObjectReverseModification`s. These are called 'original' because
        the target will be the original object from the base model that the ChangeSet was derived from.
    :var CREATIONS_MODIFICATIONS: Contains the target of `ObjectCreation`s and `ObjectModification`s. These are called 'new' as the targets contain
        only updates or additions to the base model.
    :var CHANGESET: Contains the ChangeSet and its ChangeSetMembers.
    """
    DELETIONS_REVERSEMODIFICATIONS = ("original", frozenset({DatabaseType.NETWORK_MODEL, DatabaseType.CUSTOMER, DatabaseType.DIAGRAM, DatabaseType.MEASUREMENT}))
    CREATIONS_MODIFICATIONS = ("new", frozenset({DatabaseType.NETWORK_MODEL, DatabaseType.CUSTOMER, DatabaseType.DIAGRAM, DatabaseType.MEASUREMENT}))
    CHANGESET = ("", frozenset({DatabaseType.VARIANT}))

    @property
    def short_name(self):
        return str(self)[16:]

    @property
    def sub_directory(self) -> str:
        return self.value[0]

    @property
    def types(self) -> Set[DatabaseType]:
        return set(self.value[1])
