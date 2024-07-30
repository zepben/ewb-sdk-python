#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Iterable

import pytest
from zepben.evolve import assign_equipment_to_feeders, Equipment, TestNetworkBuilder, Feeder, BaseVoltage


def validate_equipment(equipment: Iterable[Equipment], *expected_mrids: str):
    equip_mrids = [e.mrid for e in equipment]
    for mrid in expected_mrids:
        assert mrid in equip_mrids


class TestAssignToFeeders:

    @pytest.mark.asyncio
    @pytest.mark.parametrize('feeder_start_point_between_conductors_network', [(False,)], indirect=True)
    async def test_applies_to_equipment_on_head_terminal_side(self, feeder_start_point_between_conductors_network):
        feeder = feeder_start_point_between_conductors_network.get("f")
        await assign_equipment_to_feeders().run(feeder_start_point_between_conductors_network)
        validate_equipment(feeder.equipment, "fsp", "c2")

    @pytest.mark.asyncio
    @pytest.mark.parametrize('feeder_start_point_to_open_point_network', [(True, False, False)], indirect=True)
    async def test_stops_at_normally_open_points(self, feeder_start_point_to_open_point_network):
        feeder = feeder_start_point_to_open_point_network.get("f")
        await assign_equipment_to_feeders().run(feeder_start_point_to_open_point_network)
        validate_equipment(feeder.equipment, "fsp", "c1", "op")
        validate_equipment(feeder.current_equipment, "fsp", "c1", "op", "c2")

    @pytest.mark.asyncio
    @pytest.mark.parametrize('loop_under_feeder_head_network', [(False,)], indirect=True)
    async def test_assigns_equipment_to_feeders_with_loops(self, caplog, loop_under_feeder_head_network):
        """
        # s0 1 * 1--c1--2 * 1--c2--2 * 1--c4--2
        #                 2----c3----1
        """
        await assign_equipment_to_feeders().run(loop_under_feeder_head_network)

        feeder = loop_under_feeder_head_network.get("f", Feeder)
        validate_equipment(feeder.equipment, "s0", "c1", "c2", "c3", "c4")

    @pytest.mark.asyncio
    async def test_stops_at_lv_equipment(self):
        bv_hv = BaseVoltage(nominal_voltage=11000)
        bv_lv = BaseVoltage(nominal_voltage=400)

        # noinspection PyArgumentList
        network_service = (TestNetworkBuilder()
                           .from_breaker(action=lambda ce: setattr(ce, "base_voltage", bv_hv))
                           .to_acls(action=lambda ce: setattr(ce, "base_voltage", bv_hv))
                           .to_acls(action=lambda ce: setattr(ce, "base_voltage", bv_lv))
                           .add_feeder("b0")
                           .network)

        network_service.add(bv_hv)
        network_service.add(bv_lv)

        feeder = network_service.get("fdr3")

        await assign_equipment_to_feeders().run(network_service)
        validate_equipment(feeder.equipment, "b0", "c1")

    @pytest.mark.asyncio
    async def test_includes_transformers(self):
        bv_hv = BaseVoltage(nominal_voltage=11000)
        bv_lv = BaseVoltage(nominal_voltage=400)

        # noinspection PyArgumentList
        network_service = (TestNetworkBuilder()
                           .from_breaker(action=lambda ce: setattr(ce, "base_voltage", bv_hv))
                           .to_acls(action=lambda ce: setattr(ce, "base_voltage", bv_hv))
                           .to_power_transformer(end_actions=[lambda ce: setattr(ce, "base_voltage", bv_hv), lambda ce: setattr(ce, "base_voltage", bv_lv)])
                           .to_acls(action=lambda ce: setattr(ce, "base_voltage", bv_lv))
                           .add_feeder("b0")
                           .network)

        network_service.add(bv_hv)
        network_service.add(bv_lv)

        feeder = network_service.get("fdr4", Feeder)

        await assign_equipment_to_feeders().run(network_service)
        validate_equipment(feeder.equipment, "b0", "c1", "tx2")
