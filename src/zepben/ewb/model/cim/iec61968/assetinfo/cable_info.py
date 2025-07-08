#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["CableInfo"]

from zepben.ewb.model.cim.iec61968.assetinfo.wire_info import WireInfo


class CableInfo(WireInfo):
    """
    Cable data. A cable is an underground conductor.
    """
    pass
