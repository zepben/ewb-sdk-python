#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Iterable

import pytest
from zepben.ewb import Equipment, TestNetworkBuilder, BaseVoltage, Tracing, NetworkStateOperators, CurrentTransformer, ProtectedSwitch, CurrentRelay, \
    ProtectionRelayScheme, ProtectionRelaySystem, PhotoVoltaicUnit, PowerElectronicsConnection, \
    ConductingEquipment, generate_id
from zepben.ewb.model.cim.iec61970.base.wires.junction import Junction
from zepben.ewb.model.cim.iec61970.base.auxiliaryequipment.fault_indicator import FaultIndicator
from zepben.ewb.model.cim.iec61970.base.wires.power_transformer_end import PowerTransformerEnd
from zepben.ewb.model.cim.iec61970.base.core.feeder import Feeder


def validate_equipment(equipment: Iterable[Equipment], *expected_mrids: str):
    equip_mrids = [e.mrid for e in equipment]

    for mrid in expected_mrids:
        assert mrid in equip_mrids


class TestAssignToFeeders:

    bv_hv = BaseVoltage(mrid=generate_id(), nominal_voltage=11000)
    bv_lv = BaseVoltage(mrid=generate_id(), nominal_voltage=400)

    @staticmethod
    def base_voltage(ce: ConductingEquipment, voltage: BaseVoltage):
        ce.base_voltage = voltage

    def _make_hv(self, ce: ConductingEquipment):
        return self.base_voltage(ce, self.bv_hv)

    def _make_lv(self, ce: ConductingEquipment):
        return self.base_voltage(ce, self.bv_lv)

    @pytest.mark.asyncio
    @pytest.mark.parametrize('feeder_start_point_between_conductors_network', [(False,)], indirect=True)
    async def test_applies_to_equipment_on_head_terminal_side(self, feeder_start_point_between_conductors_network):
        feeder = feeder_start_point_between_conductors_network.get("f")
        await Tracing.assign_equipment_to_feeders().run(
            feeder_start_point_between_conductors_network,
            NetworkStateOperators.NORMAL
        )
        validate_equipment(feeder.equipment, "fsp", "c2")

    @pytest.mark.asyncio
    @pytest.mark.parametrize('feeder_start_point_to_open_point_network', [(True, False, False)], indirect=True)
    async def test_stops_at_normally_open_points(self, feeder_start_point_to_open_point_network):
        feeder = feeder_start_point_to_open_point_network.get("f")
        await Tracing.assign_equipment_to_feeders().run(feeder_start_point_to_open_point_network, NetworkStateOperators.NORMAL)
        validate_equipment(feeder.equipment, "fsp", "c1", "op")

        await Tracing.assign_equipment_to_feeders().run(feeder_start_point_to_open_point_network, NetworkStateOperators.CURRENT)
        validate_equipment(feeder.current_equipment, "fsp", "c1", "op", "c2")

    @pytest.mark.asyncio
    @pytest.mark.parametrize('loop_under_feeder_head_network', [(False,)], indirect=True)
    async def test_assigns_equipment_to_feeders_with_loops(self, caplog, loop_under_feeder_head_network):
        """
        # s0 1 * 1--c1--2 * 1--c2--2 * 1--c4--2
        #                 2----c3----1
        """
        await Tracing.assign_equipment_to_feeders().run(loop_under_feeder_head_network, NetworkStateOperators.NORMAL)

        feeder = loop_under_feeder_head_network.get("f", Feeder)
        validate_equipment(feeder.equipment, "s0", "c1", "c2", "c3", "c4")

    @pytest.mark.asyncio
    async def test_stops_at_lv_equipment(self):
        # noinspection PyArgumentList
        network_service = (TestNetworkBuilder()
                           .from_breaker(action=self._make_hv)
                           .to_acls(action=self._make_hv)
                           .to_acls(action=self._make_lv)
                           .add_feeder("b0")
                           .network)

        network_service.add(self.bv_hv)
        network_service.add(self.bv_lv)

        feeder = network_service.get("fdr3")

        await Tracing.assign_equipment_to_feeders().run(network_service, NetworkStateOperators.NORMAL)
        validate_equipment(feeder.equipment, "b0", "c1")

    @pytest.mark.asyncio
    async def test_includes_transformers(self):
        # noinspection PyArgumentList
        network_service = (TestNetworkBuilder()
                           .from_breaker(action=self._make_hv)
                           .to_acls(action=self._make_hv)
                           .to_power_transformer(end_actions=[self._make_hv, self._make_lv])
                           .to_acls(action=self._make_lv)
                           .add_feeder("b0")
                           .network)

        network_service.add(self.bv_hv)
        network_service.add(self.bv_lv)

        feeder = network_service.get("fdr4", Feeder)

        await Tracing.assign_equipment_to_feeders().run(network_service, NetworkStateOperators.NORMAL)
        validate_equipment(feeder.equipment, "b0", "c1", "tx2")

    @pytest.mark.asyncio
    async def test_assigns_auxilary_equipment_to_feeder(self):
        network = (TestNetworkBuilder()
                   .from_breaker()  # b0
                   .to_acls()  # c1
                   .add_feeder('b0')
                   ).network

        a1 = CurrentTransformer(mrid='a1')
        a1.terminal = network.get('c1-t1')
        network.add(a1)

        a2 = FaultIndicator(mrid='a2')
        a2.terminal = network.get('c1-t1')
        network.add(a2)

        feeder = network['fdr2']

        await Tracing.assign_equipment_to_feeders().run(network, NetworkStateOperators.NORMAL)
        validate_equipment(feeder.equipment, 'b0', 'c1', 'a1', 'a2')

    @pytest.mark.asyncio
    async def test_assigns_protection_equipment_to_feeder(self):
        network = (TestNetworkBuilder()
                   .from_breaker()  # b0
                   .add_feeder('b0')
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

        feeder = network['fdr1']

        await Tracing.assign_equipment_to_feeders().run(network, NetworkStateOperators.NORMAL)

        validate_equipment(feeder.equipment, 'b0', 'prsys3')

    @pytest.mark.asyncio
    async def test_assigns_power_electronic_units_to_feeder(self):
        peu1 = PhotoVoltaicUnit(mrid='peu1')

        def pec_action(this: PowerElectronicsConnection):
            this.add_unit(peu1)
            peu1.power_electronics_connection = this

        network = (TestNetworkBuilder()
                   .from_breaker()  # b0
                   .to_power_electronics_connection(action=pec_action)  # pec1
                   .add_feeder('b0')
                   ).network

        network.add(peu1)

        feeder = network['fdr2']

        await Tracing.assign_equipment_to_feeders().run(network, NetworkStateOperators.NORMAL)

        validate_equipment(feeder.equipment, 'b0', 'pec1', 'peu1')

    @pytest.mark.asyncio
    async def test_can_be_run_from_a_single_terminal(self):
        #
        # 1 b0 21--c1--2 j2 31--c3--21--c4--2
        #                2
        #                1
        #                |
        #                c5
        #                |
        #                21--c6--2
        #
        network = (TestNetworkBuilder()
                   .from_breaker()  # b0
                   .to_acls()  # c1
                   .to_junction(num_terminals=3)  # j2
                   .to_acls()  # c3
                   .to_acls()  # c4
                   .from_acls()  # c5
                   .to_acls()  # c6
                   .connect('j2', 'c5', 2, 1)
                   .add_feeder('b0')  # fdr7
                   ).network

        feeder = network['fdr7']
        junction = network['j2']

        feeder.add_equipment(junction)
        junction.add_container(feeder)

        await Tracing.assign_equipment_to_feeders().run(network, NetworkStateOperators.NORMAL)

        # b0 is included from the network builder.
        # j2 was added to allow us to test the terminal based assignment.
        # c3 and c4 should have been added via the trace.
        # c1, c5 and c6 shouldn't have been added if the assignment only went out t3 of j2.
        validate_equipment(feeder.equipment, 'b0', 'j2', 'c3', 'c4')

    @pytest.mark.asyncio
    async def test_energizes_all_lv_feeders_for_a_dist_tx_site_that_is_energized(self):
        #
        #                            1--c4--21 b5 2
        # 1 b0 21--c121 tx2 21--c3--2
        #                            1--c6--21 b7 2
        #
        network = (TestNetworkBuilder()
                   .from_breaker(action=self._make_hv)  # b0
                   .to_acls(action=self._make_hv)  # c1
                   .to_power_transformer(end_actions=[lambda t: setattr(t, 'rated_u', self.bv_hv.nominal_voltage), lambda t: setattr(t, 'rated_u', self.bv_lv.nominal_voltage)])  # tx2
                   .to_acls(action=self._make_lv)  # c3
                   .to_acls(action=self._make_lv)  # c4
                   .to_breaker(action=self._make_lv)  # b5
                   .from_acls(action=self._make_lv)  # c6
                   .to_breaker(action=self._make_lv)  # b7
                   .connect('c3', 'c6', 2, 1)
                   .add_feeder('b0')  # fdr8
                   .add_lv_feeder('tx2')  # lvf9
                   .add_lv_feeder('b5')  # lvf10
                   .add_lv_feeder('b7')  # lvf11
                   .add_site(['tx2', 'c3', 'c4', 'b5', 'c6', 'b7'])  # site12
                   ).network

        feeder = network['fdr8']
        
        await Tracing.assign_equipment_to_feeders().run(network, NetworkStateOperators.NORMAL)

        # We ensure the HV trace stopped at the transformer, but the additional LV feeders from b5 and b7 are still
        # marked as energized through the dist substation site.
        validate_equipment(feeder.equipment, 'b0', 'c1', 'tx2')
        assert [it.mrid for it in feeder.normal_energized_lv_feeders] == ['lvf9', 'lvf10', 'lvf11']

    @pytest.mark.asyncio
    async def test_does_not_trace_out_from_terminal_belonging_to_open_switch(self):
        network = (TestNetworkBuilder()
                   .from_breaker(is_normally_open=True)  # b0
                   .to_acls()  # c1
                   .add_feeder('b0')
                   ).network

        await Tracing.assign_equipment_to_feeders().run(network, NetworkStateOperators.NORMAL, network['b0'][2])

        feeder = network['fdr2']
        validate_equipment(feeder.equipment, 'b0')
