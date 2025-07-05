#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["Site"]

from typing import Iterable, Type, Generator

#todo import from explicit package
from zepben.evolve import EquipmentContainer, ConductingEquipment, NetworkStateOperators
from zepben.evolve.model.cim.extensions.iec61970.base.feeder.lv_feeder import LvFeeder
from zepben.evolve.model.cim.extensions.zbex import zbex


@zbex
class Site(EquipmentContainer):
    """
    [ZBEX]
    A collection of equipment for organizational purposes, used for grouping distribution resources located at a site.
    Note this is not a CIM concept - however represents an `EquipmentContainer` in CIM. This is to avoid the use of `EquipmentContainer` as a concrete class.
    """

    def find_lv_feeders(
        self,
        lv_feeder_start_points: Iterable[ConductingEquipment],
        state_operators: Type[NetworkStateOperators]
    ) -> Generator[LvFeeder, None, None]:
        from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
        for ce in state_operators.get_equipment(self):
            if isinstance(ce, ConductingEquipment):
                if ce in lv_feeder_start_points:
                    if not state_operators.is_open(ce):  # Exclude any open switch that might be energised by a different feeder on the other side
                        for lv_feeder in ce.lv_feeders(state_operators):
                            yield lv_feeder
