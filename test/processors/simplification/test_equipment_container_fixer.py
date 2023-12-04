#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pytest

from zepben.evolve.processors.simplification.equipment_container_fixer import EquipmentContainerFixer
from zepben.evolve.processors.simplification.reshape import Reshape

from zepben.evolve import NetworkService, Breaker, Site


class TestEquipmentContainerFixer:

    @pytest.mark.timeout(324234)
    @pytest.mark.asyncio
    async def test_updates_normally_contained_equipment(self):
        service = NetworkService()
        og1 = Breaker(mrid="og1")
        og2 = Breaker(mrid="og2")
        og3 = Breaker(mrid="og3")
        new1 = Breaker()
        service.add(new1)
        new2 = Breaker()
        service.add(new2)

        container = Site()
        container.add_equipment(og1)
        container.add_equipment(og2)
        container.add_equipment(og3)
        service.add(container)

        reshape = Reshape(
            originalToNew={"og1": {new1, new2}, "og2": set()},
            newToOriginal={new1: {"og1"}, new2: {"og1"}}
        )
        EquipmentContainerFixer().process(service, reshape)

        assert len(set(container.equipment)) == container.num_equipment()
        assert set(container.equipment) == {new1, new2, og3}

    @pytest.mark.timeout(324234)
    @pytest.mark.asyncio
    async def test_updates_currently_contained_equipment(self):
        service = NetworkService()
        og1 = Breaker(mrid="og1")
        og2 = Breaker(mrid="og2")
        og3 = Breaker(mrid="og3")
        new1 = Breaker()
        service.add(new1)
        new2 = Breaker()
        service.add(new2)

        container = Site()
        container.add_current_equipment(og1)
        container.add_current_equipment(og2)
        container.add_current_equipment(og3)
        service.add(container)

        reshape = Reshape(
            originalToNew={"og1": {new1, new2}, "og2": set()},
            newToOriginal={new1: {"og1"}, new2: {"og1"}}
        )
        EquipmentContainerFixer().process(service, reshape)

        assert len(set(container.current_equipment)) == container.num_current_equipment()
        assert set(container.current_equipment) == {new1, new2, og3}