#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment

__all__ = ["Ground"]


class Ground(ConductingEquipment):
    """
    A point where the system is grounded used for connecting conducting equipment to ground. The power system model can have any number of grounds.
    """
    pass
