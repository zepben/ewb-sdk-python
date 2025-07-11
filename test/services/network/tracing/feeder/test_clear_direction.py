#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import pytest

from services.network.tracing.feeder.test_set_direction import DOWNSTREAM, UPSTREAM, BOTH, NONE
from zepben.ewb import TestNetworkBuilder, NetworkStateOperators, NetworkService, Terminal, ConductingEquipment, FeederDirection, Tracing
from zepben.ewb.model.cim.iec61970.base.wires.busbar_section import BusbarSection
from zepben.ewb.services.network.tracing.feeder.clear_direction import ClearDirection


class TestClearDirection:
    clear_direction = ClearDirection()
    state_operators = NetworkStateOperators.NORMAL

    @pytest.mark.asyncio
    async def test_clear_direction(self):
        #
        #            1--c2--2
        # b0 11--c1--2
        #            1--c3--2
        #
        n = await (
            TestNetworkBuilder()
            .from_breaker()  # b0
            .to_acls()  # c1
            .to_acls()  # c2
            .from_acls()  # c3
            .connect('c1', 'c3', 2, 1)
            .add_feeder('b0')
            .build()
        )
        term = _get_t(n, 'b0', 2)
        head_terminals = await self.clear_direction.run(term, self.state_operators)
        assert term in head_terminals

        _check_expected_direction(_get_t(n, 'b0', 1), FeederDirection.NONE)
        _check_expected_direction(_get_t(n, 'b0', 2), FeederDirection.NONE)
        _check_expected_direction(_get_t(n, 'c1', 1), FeederDirection.NONE)
        _check_expected_direction(_get_t(n, 'c1', 2), FeederDirection.NONE)
        _check_expected_direction(_get_t(n, 'c2', 1), FeederDirection.NONE)
        _check_expected_direction(_get_t(n, 'c2', 2), FeederDirection.NONE)
        _check_expected_direction(_get_t(n, 'c3', 1), FeederDirection.NONE)
        _check_expected_direction(_get_t(n, 'c3', 2), FeederDirection.NONE)

    @pytest.mark.asyncio
    async def test_only_clears_given_state(self):
        #
        #
        # b0 11--c1--2
        #
        #
        n = await(
            TestNetworkBuilder()
            .from_breaker()  # b0
            .to_acls()  # c1
            .add_feeder('b0')
            .build()
        )
        term = _get_t(n, 'b0', 2)
        head_terminals = await self.clear_direction.run(term, NetworkStateOperators.NORMAL)
        assert term in head_terminals

        _check_expected_direction(_get_t(n, 'b0', 2), NONE, expected_current=DOWNSTREAM)
        _check_expected_direction(_get_t(n, 'c1', 1), NONE, expected_current=UPSTREAM)
        _check_expected_direction(_get_t(n, 'c1', 2), NONE, expected_current=DOWNSTREAM)

    @pytest.mark.asyncio
    async def test_can_clear_from_any_terminal_and_only_steps_externally(self):
        #
        #            1--c2--2
        # b0 11--c1--2
        #            1--c3--2
        #
        n = await(
            TestNetworkBuilder()
            .from_breaker()  # b0
            .to_acls()  # c1
            .to_acls()  # c2
            .from_acls()  # c3
            .connect('c1', 'c3', 2, 1)
            .add_feeder('b0')
            .build()
        )

        head_terminals = await self.clear_direction.run(_get_t(n, 'c1', 2), self.state_operators)
        assert not head_terminals

        _check_expected_direction(_get_t(n, 'b0', 1), NONE)
        _check_expected_direction(_get_t(n, 'b0', 2), DOWNSTREAM)
        _check_expected_direction(_get_t(n, 'c1', 1), UPSTREAM)
        _check_expected_direction(_get_t(n, 'c1', 2), NONE)
        _check_expected_direction(_get_t(n, 'c2', 1), NONE)
        _check_expected_direction(_get_t(n, 'c2', 2), NONE)
        _check_expected_direction(_get_t(n, 'c3', 1), NONE)
        _check_expected_direction(_get_t(n, 'c3', 2), NONE)

    @pytest.mark.asyncio
    async def test_clears_loops(self):
        #
        #            1--c2--2
        # b0 11--c1--2      1--c3--2
        #            1--c4--2
        #
        n = await(
            TestNetworkBuilder()
            .from_breaker()  # b0
            .to_acls()  # c1
            .to_acls()  # c2
            .from_acls()  # c3
            .from_acls()  # c4
            .connect('c4', 'c1', 1, 2)
            .connect('c4', 'c3', 2, 1)
            .add_feeder('b0')
            .build()
        )
        term = _get_t(n, 'b0', 2)
        head_terminals = await self.clear_direction.run(term, self.state_operators)
        assert term in head_terminals

        _check_expected_direction(_get_t(n, 'b0', 1), NONE)
        _check_expected_direction(_get_t(n, 'b0', 2), NONE)
        _check_expected_direction(_get_t(n, 'c1', 1), NONE)
        _check_expected_direction(_get_t(n, 'c1', 2), NONE)
        _check_expected_direction(_get_t(n, 'c2', 1), NONE)
        _check_expected_direction(_get_t(n, 'c2', 2), NONE)
        _check_expected_direction(_get_t(n, 'c3', 1), NONE)
        _check_expected_direction(_get_t(n, 'c3', 2), NONE)
        _check_expected_direction(_get_t(n, 'c4', 1), NONE)
        _check_expected_direction(_get_t(n, 'c4', 2), NONE)

    @pytest.mark.asyncio
    async def test_stops_at_open_points(self):
        #
        # b0 11--c1--21 b2 21--c3--21 b4 2
        #
        n = await(
            TestNetworkBuilder()
            .from_breaker()  # b0
            .to_acls()  # c1
            .to_breaker(is_normally_open=True)  # b2
            .to_acls()  # c3
            .to_breaker()  # c4
            .add_feeder('b0')
            .add_feeder('b4', 1)
            .build()
        )
        term = _get_t(n, 'b0', 2)
        head_terminals = await self.clear_direction.run(term, self.state_operators)
        assert term in head_terminals

        _check_expected_direction(_get_t(n, 'b0', 1), NONE)
        _check_expected_direction(_get_t(n, 'b0', 2), NONE)
        _check_expected_direction(_get_t(n, 'c1', 1), NONE)
        _check_expected_direction(_get_t(n, 'c1', 2), NONE)
        _check_expected_direction(_get_t(n, 'b2', 1), NONE)
        _check_expected_direction(_get_t(n, 'b2', 2), UPSTREAM)
        _check_expected_direction(_get_t(n, 'c3', 1), DOWNSTREAM)
        _check_expected_direction(_get_t(n, 'c3', 2), UPSTREAM)
        _check_expected_direction(_get_t(n, 'b4', 1), DOWNSTREAM)
        _check_expected_direction(_get_t(n, 'b4', 2), NONE)

    @pytest.mark.asyncio
    async def test_returns_all_encountered_feeder_head_terminals(self):
        #
        # b0 11--c1--21 b2 21--c3--21 b4 2
        #
        n = await(
            TestNetworkBuilder()
            .from_breaker()  # b0
            .to_acls()  # c1
            .to_breaker()  # b2
            .to_acls()  # c3
            .to_breaker()  # b4
            .add_feeder('b0')
            .add_feeder('b4', 1)
            .build()
        )
        term = _get_t(n, 'b0', 2)
        head_terminals = await self.clear_direction.run(term, self.state_operators)
        for ht in (term, _get_t(n, 'b4', 1)):
            assert ht in head_terminals

        _check_expected_direction(_get_t(n, 'b0', 1), NONE)
        _check_expected_direction(_get_t(n, 'b0', 2), NONE)
        _check_expected_direction(_get_t(n, 'c1', 1), NONE)
        _check_expected_direction(_get_t(n, 'c1', 2), NONE)
        _check_expected_direction(_get_t(n, 'b2', 1), NONE)
        _check_expected_direction(_get_t(n, 'b2', 2), NONE)
        _check_expected_direction(_get_t(n, 'c3', 1), NONE)
        _check_expected_direction(_get_t(n, 'c3', 2), NONE)
        _check_expected_direction(_get_t(n, 'b4', 1), NONE)
        _check_expected_direction(_get_t(n, 'b4', 2), NONE)

    @pytest.mark.asyncio
    async def test_supports_clearing_with_busbar_section(self):
        #
        #      1--c3--2
        # b0 1 1 o1
        #      1--c2--2
        #
        n = await(
            TestNetworkBuilder()
            .from_breaker()  # b0
            .to_other(BusbarSection, num_terminals=1)  # 01
            .to_acls()  # c2
            .from_acls()  # c3
            .connect('o1', 'c3', 1, 1)
            .add_feeder('b0')
            .build()
        )
        term = _get_t(n, 'b0', 2)
        head_terminals = await self.clear_direction.run(term, self.state_operators)
        assert term in head_terminals

        _check_expected_direction(_get_t(n, 'b0', 1), NONE)
        _check_expected_direction(_get_t(n, 'b0', 2), NONE)
        _check_expected_direction(_get_t(n, 'o1', 1), NONE)
        _check_expected_direction(_get_t(n, 'c2', 1), NONE)
        _check_expected_direction(_get_t(n, 'c2', 2), NONE)
        _check_expected_direction(_get_t(n, 'c3', 1), NONE)
        _check_expected_direction(_get_t(n, 'c3', 2), NONE)

    @pytest.mark.asyncio
    async def test_clears_loops(self):
        #
        #            1--c2--2
        # b0 11--c1--2      1--c3--21 b4
        #            1--c5--2
        #
        n = await(
            TestNetworkBuilder()
            .from_breaker()  # b0
            .to_acls()  # c1
            .to_acls()  # c2
            .to_acls()  # c3
            .to_breaker()  # b4
            .from_acls()  # c5
            .connect('c5', 'c1', 1, 2)
            .connect('c5', 'c3', 2, 1)
            .add_feeder('b0')
            .add_feeder('b4', 1)
            .build()
        )
        breaker = n.get('b4')
        self.state_operators.set_open(breaker, True)

        term = _get_t(n, 'b4', 1)
        head_terminals = await self.clear_direction.run(term, self.state_operators)
        assert term in head_terminals

        for term in head_terminals:
            if not self.state_operators.is_open(term.conducting_equipment):
                await Tracing.set_direction().run_terminal(term, self.state_operators)

        _check_expected_direction(_get_t(n, 'b0', 1), NONE)
        _check_expected_direction(_get_t(n, 'b0', 2), DOWNSTREAM)
        _check_expected_direction(_get_t(n, 'c1', 1), UPSTREAM)
        _check_expected_direction(_get_t(n, 'c1', 2), DOWNSTREAM)
        _check_expected_direction(_get_t(n, 'c2', 1), BOTH)
        _check_expected_direction(_get_t(n, 'c2', 2), BOTH)
        _check_expected_direction(_get_t(n, 'c3', 1), UPSTREAM)
        _check_expected_direction(_get_t(n, 'c3', 2), DOWNSTREAM)
        _check_expected_direction(_get_t(n, 'b4', 1), UPSTREAM)
        _check_expected_direction(_get_t(n, 'b4', 2), NONE)
        _check_expected_direction(_get_t(n, 'c5', 1), BOTH)
        _check_expected_direction(_get_t(n, 'c5', 2), BOTH)

def _get_t(network: NetworkService, mrid: str, sequence_number: int) -> Terminal:
    return network.get(mrid, ConductingEquipment).get_terminal_by_sn(sequence_number)

def _check_expected_direction(t: Terminal, expected_normal: FeederDirection, expected_current: FeederDirection = None):
    assert t.normal_feeder_direction == expected_normal
    assert t.current_feeder_direction == expected_current or expected_normal
