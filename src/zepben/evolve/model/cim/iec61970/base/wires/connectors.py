#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment

__all__ = ["Connector", "Junction", "BusbarSection"]


class Connector(ConductingEquipment):
    """
    A conductor, or group of conductors, with negligible impedance, that serve to connect other conducting equipment
    within a single substation and are modelled with a single logical terminal.
    """
    pass


class Junction(Connector):
    """
    A point where one or more conducting equipments are connected with zero resistance.
    """
    pass


class BusbarSection(Connector):
    """
    A conductor, or group of conductors, with negligible impedance, that serve to connect other conducting equipment within a single substation.
                                                                                                                                            
    Voltage measurements are typically obtained from voltage transformers that are connected to busbar sections. A bus bar section may have many
    physical terminals but for analysis is modelled with exactly one logical terminal.
    """
    pass
