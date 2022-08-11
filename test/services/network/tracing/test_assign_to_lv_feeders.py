#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Iterable

import pytest
from zepben.evolve import assign_equipment_to_feeders, Equipment, TestNetworkBuilder, Feeder, BaseVoltage, LvFeeder
from zepben.evolve.services.network.tracing.tracing import assign_equipment_to_lv_feeders


def validate_equipment(equipment: Iterable[Equipment], *expected_mrids: str):
    equip_mrids = [e.mrid for e in equipment]
    for mrid in expected_mrids:
        assert mrid in equip_mrids


class TestAssignToLvFeeders:

    @pytest.mark.asyncio
    @pytest.mark.parametrize('feeder_start_point_between_conductors_network', [(True,)], indirect=True)
    async def test_applies_to_equipment_on_head_terminal_side(self, feeder_start_point_between_conductors_network):
        lv_feeder = feeder_start_point_between_conductors_network.get("f")
        await assign_equipment_to_lv_feeders().run(feeder_start_point_between_conductors_network)
        validate_equipment(lv_feeder.equipment, "fsp", "c2")

    @pytest.mark.asyncio
    @pytest.mark.parametrize('feeder_start_point_to_open_point_network', [(True, False, True)], indirect=True)
    async def test_stops_at_normally_open_points(self, feeder_start_point_to_open_point_network):
        lv_feeder = feeder_start_point_to_open_point_network.get("f")
        await assign_equipment_to_lv_feeders().run(feeder_start_point_to_open_point_network)
        validate_equipment(lv_feeder.equipment, "fsp", "c1", "op")
        validate_equipment(lv_feeder.current_equipment, "fsp", "c1", "op", "c2")

    @pytest.mark.asyncio
    @pytest.mark.parametrize('loop_under_feeder_head_network', [(True,)], indirect=True)
    async def test_assigns_equipment_to_feeders_with_loops(self, caplog, loop_under_feeder_head_network):
        await assign_equipment_to_lv_feeders().run(loop_under_feeder_head_network)

        lv_feeder = loop_under_feeder_head_network.get("f", LvFeeder)
        validate_equipment(lv_feeder.equipment, "s0", "c1", "c2", "c3", "c4")

    @pytest.mark.asyncio
    async def test_stops_at_hv_equipment(self):
        bv_hv = BaseVoltage(nominal_voltage=11000)
        bv_lv = BaseVoltage(nominal_voltage=400)

        # noinspection PyArgumentList
        network_service = (TestNetworkBuilder()
                           .from_breaker(action=lambda ce: setattr(ce, "base_voltage", bv_lv))
                           .to_acls(action=lambda ce: setattr(ce, "base_voltage", bv_lv))
                           .to_acls(action=lambda ce: setattr(ce, "base_voltage", bv_hv))
                           .add_lv_feeder("b0")
                           .network)

        network_service.add(bv_hv)
        network_service.add(bv_lv)

        lv_feeder = network_service.get("lvf3")

        await assign_equipment_to_lv_feeders().run(network_service)
        validate_equipment(lv_feeder.equipment, "b0", "c1")

    @pytest.mark.asyncio
    async def test_includes_transformers(self):
        bv_hv = BaseVoltage(nominal_voltage=11000)
        bv_lv = BaseVoltage(nominal_voltage=400)

        # noinspection PyArgumentList
        network_service = (TestNetworkBuilder()
                           .from_breaker(action=lambda ce: setattr(ce, "base_voltage", bv_lv))
                           .to_acls(action=lambda ce: setattr(ce, "base_voltage", bv_lv))
                           .to_power_transformer(end_actions=[lambda ce: setattr(ce, "base_voltage", bv_lv), lambda ce: setattr(ce, "base_voltage", bv_hv)])
                           .to_acls(action=lambda ce: setattr(ce, "base_voltage", bv_hv))
                           .add_lv_feeder("b0")
                           .network)

        network_service.add(bv_hv)
        network_service.add(bv_lv)

        lv_feeder = network_service.get("lvf4", LvFeeder)

        await assign_equipment_to_lv_feeders().run(network_service)
        validate_equipment(lv_feeder.equipment, "b0", "c1", "tx2")
