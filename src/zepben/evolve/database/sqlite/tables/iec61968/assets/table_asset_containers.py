#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from abc import ABC

from zepben.evolve.database.sqlite.tables.iec61968.assets.table_assets import TableAssets

__all__ = ["TableAssetContainers"]


class TableAssetContainers(TableAssets, ABC):
    pass
