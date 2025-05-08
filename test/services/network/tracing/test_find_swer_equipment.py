#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Callable, Awaitable
from unittest.mock import call, patch

import pytest

from zepben.evolve import FindSwerEquipment, TestNetworkBuilder, PhaseCode, BaseVoltage, \
    ConductingEquipment, verify_stop_conditions, step_on_when_run, step_on_when_run_with_is_stopping, NetworkStateOperators


class TestFindSwerEquipment:

    # pylint: disable=attribute-defined-outside-init
    # noinspection PyArgumentList
    def setup_method(self):
        self.state_operators = NetworkStateOperators.NORMAL

        self.find_swer_equipment = FindSwerEquipment()

    # pylint: enable=attribute-defined-outside-init

    @pytest.mark.asyncio
    async def test_processes_all_feeders_in_a_network(self):
        ns = (await TestNetworkBuilder()
              .from_power_transformer([PhaseCode.AB, PhaseCode.A]) # tx0
              .from_power_transformer([PhaseCode.AB, PhaseCode.A]) # tx1
              .add_feeder('tx0') # fdr2
              .add_feeder('tx1') # fdr3
              .build())

        pass

        with patch.object(self.find_swer_equipment, 'find_on_feeder') as find_on_feeder:
            await self.find_swer_equipment.find(ns, self.state_operators)

            for feeder in ['fdr2', 'fdr3']:
                find_on_feeder.assert_has_calls([call(ns[feeder], self.state_operators)])

    @pytest.mark.asyncio
    async def test_only_runs_trace_from_swer_transformers_and_only_runs_non_swer_from_lv(self):
        ns = (await TestNetworkBuilder()
              .from_breaker()  # b0
              .to_power_transformer()  # tx1
              .to_acls()  # c2
              .to_power_transformer([PhaseCode.AB, PhaseCode.A])  # tx3
              .to_acls(PhaseCode.A)  # c4
              .to_acls(PhaseCode.A)  # c5
              .to_power_transformer([PhaseCode.A, PhaseCode.AN, PhaseCode.AN])  # tx6
              .to_acls(PhaseCode.AN, action=self._make_lv)  # c7
              .to_breaker(PhaseCode.AN, action=self._make_lv)  # b8
              .branch_from('tx6', 2)
              .to_acls(PhaseCode.AN, action=self._make_hv)  # c9
              .add_feeder("b0")  # fdr8
              .build())

        results = await self.find_swer_equipment.find(ns['fdr10'])

        assert results

        for n in ('tx3', 'c4', 'c5', 'tx6', 'c7', 'b8'):
            assert ns[n] in results


    @pytest.mark.asyncio
    async def test_does_not_run_from_SWER_regulators(self):
        ns = (
            await TestNetworkBuilder
            .from_breaker(PhaseCode.A)  # b0
            .to_power_transformer([PhaseCode.A, PhaseCode.A])  # tx1
            .to_acls(PhaseCode.A)  # c2
            .add_feeder('b0')  # fdr3
            .build()
        )

        assert len(self.find_swer_equipment.find(ns['fdr3'], self.state_operators)) == 0

    @pytest.mark.asyncio
    async def test_does_not_run_through_other_transformers_that_will_be_traced(self):
        ns = (
            await TestNetworkBuilder()
            .from_acls(PhaseCode.AN)  # c9
            .to_power_transformer([PhaseCode.AN, PhaseCode.A])  #tx1
            .to_acls(PhaseCode.A)  # c2
            .to_power_transformer([PhaseCode.A, PhaseCode.A])  # tx3
            .to_acls(PhaseCode.A)  # c4
            .to_power_transformer([PhaseCode.A, PhaseCode.AN])  # tx5
            .to_acls(PhaseCode.AN)  # c6
            .add_feeder("c0")  # fdr7
            .build())

        results = await self.find_swer_equipment.find(ns, self.state_operators)

        for n in ['tx1', 'c2', 'tx3', 'c4', 'tx5']:
            assert ns[n] in results


    @pytest.mark.asyncio
    async def test_SWER_includes_open_switches_and_stops_at_them(self):
        ns = (
            await TestNetworkBuilder()
            .from_power_transformer([PhaseCode.AN, PhaseCode.A])  # tx0
            .to_breaker(is_normally_open=True)  # b1
            .to_acls()  # c2
            .add_feeder('tx0')  # fdr3
            .build()
        )

        results = await self.find_swer_equipment.find(ns['fdr3'], self.state_operators)
        for n in ('tx0', 'b1'):
            assert ns[n] in results

        assert self.state_operators.is_open(ns['b1'])

    @pytest.mark.asyncio
    async def test_LV_includes_open_switches_and_stops_at_them(self):
        ns = (
            await TestNetworkBuilder()
            .from_power_transformer([PhaseCode.A, PhaseCode.AN])  # tx0
            .to_acls(PhaseCode.AN, action=self._make_lv)  # c1
            .to_breaker(PhaseCode.AN, is_normally_open=True, action=self._make_lv)  # b2
            .to_acls(PhaseCode.AN, action=self._make_lv)  # c3
            .add_feeder('tx0')  # fdr4
            .build()
        )
        results = await self.find_swer_equipment.find(ns['fdr4'], self.state_operators)

        for n in ('tx0', 'c1', 'b2'):
            assert ns[n] in results

        assert self.state_operators.is_open(ns['b2'])

    @pytest.mark.asyncio
    async def test_runs_off_multiple_terminals(self):
        ns = (await TestNetworkBuilder()
              .from_power_transformer([PhaseCode.A, PhaseCode.A, PhaseCode.AN, PhaseCode.AN])  # tx0
              .to_acls(PhaseCode.AN, action=self._make_lv)  # c1
              .branch_from("tx0", 1)
              .to_acls(PhaseCode.A)  # c2
              .branch_from("tx0", 2)
              .to_acls(PhaseCode.A)  # c3
              .branch_from("tx0", 3)
              .to_acls(PhaseCode.AN, action=self._make_lv)  # c4
              .add_feeder("tx0")  # fdr5
              .build())

        results = await self.find_swer_equipment.find(ns["fdr5"], self.state_operators)

        for n in ('tx0', 'c1', 'c2', 'c3', 'c4'):
            assert ns[n] in results

    @pytest.mark.asyncio
    async def test_does_not_loop_back_out_of_swer_from_lv(self):
        ns = (await TestNetworkBuilder()
              .from_junction(num_terminals=1)  # j0
              .to_acls()  # c1
              .to_acls(PhaseCode.A)  # c2
              .to_power_transformer([PhaseCode.A, PhaseCode.AN])  # tx3
              .to_acls(PhaseCode.AN, action=self._make_lv)  # c4
              .to_power_transformer([PhaseCode.AN, PhaseCode.A])  # tx5
              .to_acls(PhaseCode.A)  # c6
              .connect("c6", "c1", 2, 1)
              .add_feeder("j0")  # fdr7
              .build())

        results = await self.find_swer_equipment.find(ns, self.state_operators)

        for n in ('c2', 'tx3', 'c4', 'tx5', 'c6'):
            assert ns[n] in results


    @staticmethod
    def _make_bv(ce: ConductingEquipment, volts: int):
        bv = BaseVoltage()
        bv.nominal_voltage = volts
        ce.base_voltage = bv

    def _make_lv(self, ce: ConductingEquipment):
        self._make_bv(ce, 415)

    def _make_hv(self, ce: ConductingEquipment):
        self._make_bv(ce, 11000)