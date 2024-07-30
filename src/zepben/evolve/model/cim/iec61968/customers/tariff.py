#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from zepben.evolve.model.cim.iec61968.common.document import Document

__all__ = ["Tariff"]


class Tariff(Document):
    """
    Document, approved by the responsible regulatory agency, listing the terms and conditions,
    including a schedule of prices, under which utility services will be provided. It has a
    unique number within the state or province. For rate schedules it is frequently allocated
    by the affiliated Public utilities commission (PUC).
    """
    pass
