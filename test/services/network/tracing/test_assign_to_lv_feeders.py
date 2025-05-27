#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Iterable

import pytest
from zepben.evolve import Equipment, TestNetworkBuilder, Feeder, BaseVoltage, LvFeeder, NetworkStateOperators, CurrentTransformer, FaultIndicator, \
    ProtectedSwitch, CurrentRelay, ProtectionRelayScheme, ProtectionRelaySystem, PhotoVoltaicUnit, PowerElectronicsConnection, ConductingEquipment, Breaker
from zepben.evolve.services.network.tracing.networktrace.tracing import Tracing


def validate_equipment(equipment: Iterable[Equipment], *expected_mrids: str):
    equip_mrids = tuple(e.mrid for e in equipment)
    assert equip_mrids == expected_mrids
    for mrid in expected_mrids:
        assert mrid in equip_mrids


class TestAssignToLvFeeders:

    bv_hv = BaseVoltage(nominal_voltage=11000)
    bv_lv = BaseVoltage(nominal_voltage=400)

    @staticmethod
    def base_voltage(ce: ConductingEquipment, voltage: BaseVoltage):
        ce.base_voltage = voltage

    def _make_hv(self, ce: ConductingEquipment):
        return self.base_voltage(ce, self.bv_hv)

    def _make_lv(self, ce: ConductingEquipment):
        return self.base_voltage(ce, self.bv_lv)

    @pytest.mark.asyncio
    @pytest.mark.parametrize('feeder_start_point_between_conductors_network', [(True,)], indirect=True)
    async def test_applies_to_equipment_on_head_terminal_side(self, feeder_start_point_between_conductors_network):
        lv_feeder = feeder_start_point_between_conductors_network.get("f")
        await Tracing.assign_equipment_to_lv_feeders().run(feeder_start_point_between_conductors_network)
        validate_equipment(lv_feeder.equipment, "fsp", "c2")

    @pytest.mark.asyncio
    @pytest.mark.parametrize('feeder_start_point_to_open_point_network', [(True, False, True)], indirect=True)
    async def test_stops_at_normally_open_points(self, feeder_start_point_to_open_point_network):
        lv_feeder = feeder_start_point_to_open_point_network.get("f")
        await Tracing.assign_equipment_to_lv_feeders().run(feeder_start_point_to_open_point_network, NetworkStateOperators.NORMAL)
        await Tracing.assign_equipment_to_lv_feeders().run(feeder_start_point_to_open_point_network, NetworkStateOperators.CURRENT)
        validate_equipment(lv_feeder.equipment, "fsp", "c1", "op")
        validate_equipment(lv_feeder.current_equipment, "fsp", "c1", "op", "c2")

    @pytest.mark.asyncio
    @pytest.mark.parametrize('loop_under_feeder_head_network', [(True,)], indirect=True)
    async def test_assigns_equipment_to_feeders_with_loops(self, caplog, loop_under_feeder_head_network):
        await Tracing.assign_equipment_to_lv_feeders().run(loop_under_feeder_head_network)

        lv_feeder = loop_under_feeder_head_network.get("f", LvFeeder)
        validate_equipment(lv_feeder.equipment, "s0", "c1", "c3", "c4", "c2")

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

        await Tracing.assign_equipment_to_lv_feeders().run(network_service)
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

        await Tracing.assign_equipment_to_lv_feeders().run(network_service)
        validate_equipment(lv_feeder.equipment, "b0", "c1", "tx2")

    @pytest.mark.asyncio
    async def test_only_powered_via_head_equipment(self):
        bv_hv = BaseVoltage(nominal_voltage=11000)
        bv_lv = BaseVoltage(nominal_voltage=400)

        # noinspection PyArgumentList
        network_service = (TestNetworkBuilder()
                           .from_breaker(action=lambda ce: setattr(ce, "base_voltage", bv_hv))
                           .to_acls(action=lambda ce: setattr(ce, "base_voltage", bv_hv))
                           .from_breaker(action=lambda ce: setattr(ce, "base_voltage", bv_lv))
                           .to_acls(action=lambda ce: setattr(ce, "base_voltage", bv_lv))
                           .connect("c1", "c3", 2, 2)
                           .add_feeder("b0")
                           .add_lv_feeder("b2")
                           .network)

        network_service.add(bv_hv)
        network_service.add(bv_lv)

        feeder = network_service.get("fdr4", Feeder)
        lv_feeder = network_service.get("lvf5", LvFeeder)

        await Tracing.assign_equipment_to_feeders().run(network_service)
        await Tracing.assign_equipment_to_lv_feeders().run(network_service)

        assert set(feeder.normal_energized_lv_feeders) == set()
        assert set(lv_feeder.normal_energizing_feeders) == set()

    @pytest.mark.asyncio
    async def test_single_feeder_powers_multiple_lv_feeders(self):
        network_service = (TestNetworkBuilder()
                           .from_breaker()
                           .add_feeder("b0")
                           .add_lv_feeder("b0")
                           .add_lv_feeder("b0")
                           .network)

        feeder = network_service.get("fdr1", Feeder)
        lv_feeder1 = network_service.get("lvf2", LvFeeder)
        lv_feeder2 = network_service.get("lvf3", LvFeeder)

        await Tracing.assign_equipment_to_feeders().run(network_service)
        await Tracing.assign_equipment_to_lv_feeders().run(network_service)

        assert set(feeder.normal_energized_lv_feeders) == {lv_feeder1, lv_feeder2}
        assert set(lv_feeder1.normal_energizing_feeders) == {feeder}
        assert set(lv_feeder2.normal_energizing_feeders) == {feeder}

    @pytest.mark.asyncio
    async def test_multiple_feeders_power_single_lv_feeder(self):
        network_service = (TestNetworkBuilder()
                           .from_breaker()
                           .add_feeder("b0")
                           .add_feeder("b0")
                           .add_lv_feeder("b0")
                           .network)

        feeder1 = network_service.get("fdr1", Feeder)
        feeder2 = network_service.get("fdr2", Feeder)
        lv_feeder = network_service.get("lvf3", LvFeeder)

        await Tracing.assign_equipment_to_feeders().run(network_service)
        await Tracing.assign_equipment_to_lv_feeders().run(network_service)

        assert set(feeder1.normal_energized_lv_feeders) == {lv_feeder}
        assert set(feeder2.normal_energized_lv_feeders) == {lv_feeder}
        assert set(lv_feeder.normal_energizing_feeders) == {feeder1, feeder2}

    @pytest.mark.asyncio
    async def test_assigns_auxiliary_equipment_to_lv_feeder(self):
        network = (TestNetworkBuilder()
                   .from_breaker()  # b0
                   .to_acls()  # c1
                   .add_lv_feeder('b0')
                   ).network
        
        a1 = CurrentTransformer(mrid='a1')
        a1.terminal = network.get('c1-t1')
        network.add(a1)

        a2 = FaultIndicator(mrid='a2')
        a2.terminal = network.get('c1-t1')
        network.add(a2)

        lv_feeder = network['lvf2']

        await Tracing.assign_equipment_to_lv_feeders().run(network, NetworkStateOperators.NORMAL)
        validate_equipment(lv_feeder.equipment, 'b0', 'c1', 'a1', 'a2')

    @pytest.mark.asyncio
    async def test_assigns_protection_equipment_to_feeder(self):
        network = (TestNetworkBuilder()
                   .from_breaker()  # b0
                   .add_lv_feeder('b0')
                   ).network

        ps = network.get('b0', ProtectedSwitch)
        cr = CurrentRelay(mrid='cr1')
        ps.add_relay_function(cr)
        cr.add_protected_switch(ps)

        prs = ProtectionRelayScheme(mrid='psr2')
        cr.add_scheme(prs)
        prs.add_function(cr)

        prsys = ProtectionRelaySystem(mrid='prsys3')
        prs.system = prsys
        prsys.add_scheme(prs)

        network.add(cr)
        network.add(prs)
        network.add(prsys)

        lv_feeder = network['lvf1']

        await Tracing.assign_equipment_to_lv_feeders().run(network, NetworkStateOperators.NORMAL)

        validate_equipment(lv_feeder.equipment, 'b0', 'prsys3')

    @pytest.mark.asyncio
    async def test_assigns_power_electronic_units_to_feeder(self):
        peu1 = PhotoVoltaicUnit(mrid='peu1')

        def pec_action(this: PowerElectronicsConnection):
            this.add_unit(peu1)
            peu1.power_electronics_connection = this

        network = (TestNetworkBuilder()
                   .from_breaker()  # b0
                   .to_power_electronics_connection(action=pec_action)  # pec1
                   .add_lv_feeder('b0')
                   ).network

        network.add(peu1)

        lv_feeder = network['lvf2']

        await Tracing.assign_equipment_to_lv_feeders().run(network, NetworkStateOperators.NORMAL)

        validate_equipment(lv_feeder.equipment, 'b0', 'pec1', 'peu1')

    @pytest.mark.asyncio
    async def lv_feeders_detect_back_feeds_for_energizing_feeders(self):
        # 1 b0 21 tx1 21--c2--21--c3--21 tx4 21 b5 2
        #
        # NOTE: Transformer is deliberately set to use the hv voltage as their base voltage to ensure they are still processed.
        #
        network = (TestNetworkBuilder()
                  .from_breaker(action=self._make_hv)  # b0
                  .to_power_transformer(action=self._make_hv)  # tx1
                  .to_acls(action=self._make_lv)  # c2
                  .to_acls(action=self._make_lv)  # c3
                  .to_power_transformer(action=self._make_hv)  # tx4
                  .to_breaker(action=self._make_hv)
                  .add_feeder("b0")
                  .add_lv_feeder("tx1")
                  .add_lv_feeder("tx4", 1)
                  .add_feeder("b5", 1)
                  ).network

        feeder6: Feeder = network["fdr6"]
        feeder9: Feeder = network["fdr9"]
        lv_feeder7: LvFeeder = network["lvf7"]
        lv_feeder8: LvFeeder = network["lvf8"]

        await Tracing.assign_equipment_to_feeders().run(network, NetworkStateOperators.NORMAL)
        await Tracing.assign_equipment_to_lv_feeders().run(network, NetworkStateOperators.NORMAL)

        assert feeder6.normal_energized_lv_feeders == [lv_feeder7, lv_feeder8]
        assert feeder9.normal_energized_lv_feeders == [lv_feeder7, lv_feeder8]
        assert lv_feeder7.normal_energizing_feeders == [feeder6, feeder9]
        assert lv_feeder8.normal_energizing_feeders == [feeder6, feeder9]

    @pytest.mark.asyncio
    async def test_lv_feeders_detect_back_feeds_for_dist_substation_sites(self):
        #
        #                1--c2--21 b3 2
        # 1 tx0 21--c1--2
        #                1--c4--21 b5 21--c6--21 b7 2
        #
        network = (TestNetworkBuilder()
                   .from_power_transformer(end_actions=[lambda t: setattr(t, 'rated_u', self.bv_hv.nominal_voltage), lambda t: setattr(t, 'rated_u', self.bv_lv.nominal_voltage)])  # tx0
                   .to_acls(action=self._make_lv)  # c1
                   .to_acls(action=self._make_lv)  # c2
                   .to_breaker(action=self._make_lv)  # b3
                   .from_acls(action=self._make_lv)  # c4
                   .to_breaker(action=self._make_lv)  # b5
                   .to_acls(action=self._make_lv)  # c6
                   .to_breaker(action=self._make_lv)  # b7
                   .connect('c1', 'c4', 2, 1)
                   .add_lv_feeder('tx0')  # lvf8
                   .add_lv_feeder('b3')  # lvf9
                   .add_lv_feeder('b5')  # lvf10
                   .add_lv_feeder('b7', 1)  # lvf11
                   .add_site(['tx0', 'c1', 'c2', 'b3', 'c4', 'b5'])  # site12
                   ).network

        operators = NetworkStateOperators.NORMAL
        b7: Breaker = network['b7']

        feeder = Feeder()
        lv_feeder8 = network['lvf8']
        operators.associate_energizing_feeder(feeder, lv_feeder8)
        lv_feeder9 = network['lvf9']
        operators.associate_energizing_feeder(feeder, lv_feeder9)
        lv_feeder10 = network['lvf10']
        operators.associate_energizing_feeder(feeder, lv_feeder10)
        
        # We create an LV feeder to assign from b7 with its associated energizing feeder, which we will test is assigned to all LV feeders
        # in the dist substation site, not just the one on b5.
        back_feed = Feeder()
        lv_feeder = LvFeeder()
        operators.associate_energizing_feeder(back_feed, lv_feeder)

        await Tracing.assign_equipment_to_lv_feeders().run(
            b7.get_terminal_by_sn(1),
            network.lv_feeder_start_points,
            {},
            [lv_feeder],
            operators
        )

        # Make sure the LV feeder trace stopped at the first LV feeder head.
        assert [it.mrid for it in lv_feeder.equipment] == ['b7', 'c6', 'b5']

        # Make sure both feeders are now considered to be energizing all LV feeders.
        assert list(feeder.normal_energized_lv_feeders) == [lv_feeder8, lv_feeder9, lv_feeder10, lv_feeder]
        assert list(back_feed.normal_energized_lv_feeders) == [lv_feeder, lv_feeder8, lv_feeder9, lv_feeder10]

        # Make sure all LV feeders are now considered to be energized by both feeders.
        assert list(lv_feeder.normal_energizing_feeders) == [back_feed, feeder]
        assert list(lv_feeder8.normal_energizing_feeders) == [feeder, back_feed]
        assert list(lv_feeder9.normal_energizing_feeders) == [feeder, back_feed]
        assert list(lv_feeder10.normal_energizing_feeders) == [feeder, back_feed]

    @pytest.mark.asyncio
    async def test_assigns_normal_and_current_energising_feeders_based_on_state(self):
        network = (TestNetworkBuilder()
                   .from_breaker()  # b0
                   .add_lv_feeder('b0')  # lvf1
                   ).network

        normal_feeder = Feeder()
        current_feeder = Feeder()
        breaker = network['b0']
        lv_feeder = network['lvf1']

        breaker.add_container(normal_feeder)
        breaker.add_current_container(current_feeder)

        await Tracing.assign_equipment_to_lv_feeders().run(network, NetworkStateOperators.NORMAL)
        await Tracing.assign_equipment_to_lv_feeders().run(network, NetworkStateOperators.CURRENT)

        assert list(normal_feeder.normal_energized_lv_feeders) == [lv_feeder]
        assert list(lv_feeder.normal_energizing_feeders) == [normal_feeder]

        assert list(current_feeder.current_energized_lv_feeders) == [lv_feeder]
        assert list(lv_feeder.current_energizing_feeders) == [current_feeder]

    @pytest.mark.asyncio
    async def test_does_not_trace_out_from_terminal_belonging_to_open_switch(self):
        #
        # 1 b0 21--c1--2
        #
        network = (TestNetworkBuilder()
                   .from_breaker(is_normally_open=True)  # b0
                   .to_acls()  # c1
                   .add_lv_feeder('b0')  # lvf2
                   ).network

        await Tracing.assign_equipment_to_lv_feeders().run(network, NetworkStateOperators.NORMAL, network['b0'][2])

        feeder = network['lvf2']
        validate_equipment(feeder.equipment, 'b0')
    