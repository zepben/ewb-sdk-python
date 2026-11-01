#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["DatedVariantPathComponents"]

from dataclasses import dataclass
from datetime import date

from zepben.ewb.database.paths.database_type import DatabaseType, VariantContents


@dataclass
class DatedVariantPathComponents:
    """
    The components extracted from a dated variant path (the inverse of `EwbDataFilePaths.get_dated_variant_path`).
    """

    type: DatabaseType
    date: date
    variant: str
    variant_contents: VariantContents
