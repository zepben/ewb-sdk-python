#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from zepben.evolve.model.cim.iec61968.assets.asset import AssetContainer

__all__ = ["Structure"]


class Structure(AssetContainer):
    """
    Construction holding assets such as conductors, transformers, switchgear, etc. Where applicable, number of conductors
    can be derived from the number of associated wire spacing instances.
    """
    pass
