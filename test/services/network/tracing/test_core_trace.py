#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import dataclass
from collections import Counter
from typing import List

import pytest

from services.network.test_data.phase_swap_loop_network import create_phase_swap_loop_network
from zepben.ewb import ConductingEquipment, PhaseCode, SinglePhaseKind, NetworkService, Tracing, NetworkStateOperators, stop_at_open, downstream, upstream, \
    NetworkTrace


@dataclass(frozen=True)
class TrackedPhases:
    equipment: ConductingEquipment
    phases: frozenset[SinglePhaseKind]


class TestCoreTrace:

    @pytest.mark.asyncio
    async def test_trace_cores(self):
        n = await self._get_network()

        # Trace all cores, we should visit everything
        start = n.get("node0", ConductingEquipment)
        visited = await self._current_non_directional_trace(start, PhaseCode.ABCN)
        assert len(visited) == 22

        # Trace from J9 on phase Y. Expect to visit J6 twice, once on Y and once on X. ac10 and j8 should never be visited.
        start = n["node9"]
        visited = await self._current_non_directional_trace(start, PhaseCode.Y)
        assert len(visited) == 21
        assert TrackedPhases(n["ac_line_segment11"], frozenset({SinglePhaseKind.Y})) in visited
        assert TrackedPhases(n["node5"], frozenset({SinglePhaseKind.Y})) in visited
        assert TrackedPhases(n["node0"], frozenset({SinglePhaseKind.B})) in visited
        assert TrackedPhases(n["node6"], frozenset({SinglePhaseKind.X})) in visited
        assert TrackedPhases(n["node6"], frozenset({SinglePhaseKind.Y})) in visited
        assert TrackedPhases(n["node7"], frozenset({SinglePhaseKind.B})) in visited

        visited_mrids = self._visited_mrids(visited)
        assert "ac10" not in visited_mrids
        assert "node8" not in visited_mrids

    @pytest.mark.asyncio
    async def test_trace_single_cores_downstream(self):
        n = await self._get_network()

        # Test from the "source" of the network downstream
        start = n.get("node0", ConductingEquipment)
        visited = await self._current_downstream_trace(start, PhaseCode.A)

        # j7, j9, acLineSegment8, acLineSegment9 and acLineSegment11 should not be traced.
        assert Counter(visited) == Counter([
            TrackedPhases(n["node0"], frozenset({SinglePhaseKind.A})),
            TrackedPhases(n["node1"], frozenset({SinglePhaseKind.A})),
            TrackedPhases(n["node2"], frozenset({SinglePhaseKind.A})),
            TrackedPhases(n["node3"], frozenset({SinglePhaseKind.A})),
            TrackedPhases(n["node4"], frozenset({SinglePhaseKind.X})),
            TrackedPhases(n["node5"], frozenset({SinglePhaseKind.X})),
            TrackedPhases(n["node6"], frozenset({SinglePhaseKind.X})),
            TrackedPhases(n["node8"], frozenset({SinglePhaseKind.X})),
            TrackedPhases(n["ac_line_segment0"], frozenset({SinglePhaseKind.A})),
            TrackedPhases(n["ac_line_segment1"], frozenset({SinglePhaseKind.A})),
            TrackedPhases(n["ac_line_segment2"], frozenset({SinglePhaseKind.A})),
            TrackedPhases(n["ac_line_segment3"], frozenset({SinglePhaseKind.A})),
            TrackedPhases(n["ac_line_segment4"], frozenset({SinglePhaseKind.A})),
            TrackedPhases(n["ac_line_segment5"], frozenset({SinglePhaseKind.X})),
            TrackedPhases(n["ac_line_segment6"], frozenset({SinglePhaseKind.X})),
            TrackedPhases(n["ac_line_segment7"], frozenset({SinglePhaseKind.X})),
            TrackedPhases(n["ac_line_segment10"], frozenset({SinglePhaseKind.X})),
        ])

        # Test from partway downstream to make sure we don't go upstream
        start = n["node1"]
        visited = await self._normal_downstream_trace(start, PhaseCode.A)
        visited_mrids = self._visited_mrids(visited)

        assert len(visited) == 4
        assert TrackedPhases(n["node1"], frozenset({SinglePhaseKind.A})) in visited
        assert TrackedPhases(n["node2"], frozenset({SinglePhaseKind.A})) in visited
        assert "ac_line_segment1" not in visited_mrids

        # Test on a core that splits onto different cores on different branches
        start = n["node0"]
        visited = await self._normal_downstream_trace(start, PhaseCode.C)
        assert len(visited) == 11
        assert TrackedPhases(n["node1"], frozenset({SinglePhaseKind.C})) in visited
        assert TrackedPhases(n["node2"], frozenset({SinglePhaseKind.C})) in visited
        assert TrackedPhases(n["node7"], frozenset({SinglePhaseKind.C})) in visited
        assert TrackedPhases(n["node6"], frozenset({SinglePhaseKind.Y})) in visited

        assert "node3" not in visited_mrids

    @pytest.mark.asyncio
    async def test_trace_multiple_cores_downstream(self):
        n = await self._get_network()

        # Test from the "source" of the network downstream
        start = n.get("node0", ConductingEquipment)
        visited = await self._normal_downstream_trace(start, PhaseCode.BC)

        # j8 and acLineSegment10 should not be traced.
        assert Counter(visited) == Counter([
            TrackedPhases(n["node0"], frozenset({SinglePhaseKind.B, SinglePhaseKind.C})),
            TrackedPhases(n["node1"], frozenset({SinglePhaseKind.B, SinglePhaseKind.C})),
            TrackedPhases(n["node2"], frozenset({SinglePhaseKind.B, SinglePhaseKind.C})),
            TrackedPhases(n["node3"], frozenset({SinglePhaseKind.B})),
            TrackedPhases(n["node4"], frozenset({SinglePhaseKind.Y})),
            TrackedPhases(n["node5"], frozenset({SinglePhaseKind.Y})),
            TrackedPhases(n["node6"], frozenset({SinglePhaseKind.X, SinglePhaseKind.Y})),
            TrackedPhases(n["node6"], frozenset({SinglePhaseKind.Y})),
            TrackedPhases(n["node7"], frozenset({SinglePhaseKind.B, SinglePhaseKind.C})),
            TrackedPhases(n["node9"], frozenset({SinglePhaseKind.Y})),
            TrackedPhases(n["ac_line_segment0"], frozenset({SinglePhaseKind.B, SinglePhaseKind.C})),
            TrackedPhases(n["ac_line_segment1"], frozenset({SinglePhaseKind.B, SinglePhaseKind.C})),
            TrackedPhases(n["ac_line_segment2"], frozenset({SinglePhaseKind.B, SinglePhaseKind.C})),
            TrackedPhases(n["ac_line_segment3"], frozenset({SinglePhaseKind.B, SinglePhaseKind.C})),
            TrackedPhases(n["ac_line_segment4"], frozenset({SinglePhaseKind.B})),
            TrackedPhases(n["ac_line_segment5"], frozenset({SinglePhaseKind.Y})),
            TrackedPhases(n["ac_line_segment6"], frozenset({SinglePhaseKind.Y})),
            TrackedPhases(n["ac_line_segment7"], frozenset({SinglePhaseKind.Y})),
            TrackedPhases(n["ac_line_segment8"], frozenset({SinglePhaseKind.X, SinglePhaseKind.Y})),
            TrackedPhases(n["ac_line_segment9"], frozenset({SinglePhaseKind.B, SinglePhaseKind.C})),
            TrackedPhases(n["ac_line_segment11"], frozenset({SinglePhaseKind.Y})),
        ])

    @pytest.mark.asyncio
    async def test_trace_single_cores_upstream(self):
        n = await self._get_network()
        start = n.get("ac_line_segment11", ConductingEquipment)
        visited = await self._normal_upstream_trace(start, PhaseCode.Y)

        assert len(visited) == 9
        assert Counter(visited) == Counter([
            TrackedPhases(n["ac_line_segment11"], frozenset({SinglePhaseKind.Y})),
            TrackedPhases(n["node5"], frozenset({SinglePhaseKind.Y})),
            TrackedPhases(n["ac_line_segment6"], frozenset({SinglePhaseKind.Y})),
            TrackedPhases(n["node4"], frozenset({SinglePhaseKind.Y})),
            TrackedPhases(n["ac_line_segment5"], frozenset({SinglePhaseKind.Y})),
            TrackedPhases(n["node3"], frozenset({SinglePhaseKind.B})),
            TrackedPhases(n["ac_line_segment4"], frozenset({SinglePhaseKind.B})),
            TrackedPhases(n["ac_line_segment0"], frozenset({SinglePhaseKind.B})),
            TrackedPhases(n["node0"], frozenset({SinglePhaseKind.B})),
        ])

    @pytest.mark.asyncio
    async def test_trace_multiple_cores_upstream(self):
        n = await self._get_network()
        start = n.get("ac_line_segment8", ConductingEquipment)
        visited = await self._normal_upstream_trace(start, PhaseCode.XY)

        assert Counter(visited) == Counter([
            TrackedPhases(n["ac_line_segment8"], frozenset({SinglePhaseKind.X, SinglePhaseKind.Y})),
            TrackedPhases(n["node7"], frozenset({SinglePhaseKind.B, SinglePhaseKind.C})),
            TrackedPhases(n["ac_line_segment9"], frozenset({SinglePhaseKind.B, SinglePhaseKind.C})),
            TrackedPhases(n["ac_line_segment2"], frozenset({SinglePhaseKind.B, SinglePhaseKind.C})),
            TrackedPhases(n["node1"], frozenset({SinglePhaseKind.B, SinglePhaseKind.C})),
            TrackedPhases(n["ac_line_segment1"], frozenset({SinglePhaseKind.B, SinglePhaseKind.C})),
            TrackedPhases(n["ac_line_segment0"], frozenset({SinglePhaseKind.B, SinglePhaseKind.C})),
            TrackedPhases(n["node0"], frozenset({SinglePhaseKind.B, SinglePhaseKind.C})),
        ])

    @staticmethod
    async def _get_network() -> NetworkService:
        n = create_phase_swap_loop_network()

        await Tracing.set_phases().run(n)
        await Tracing.set_phases().run(n, NetworkStateOperators.CURRENT)

        await Tracing.set_direction().run(n)
        await Tracing.set_direction().run(n, NetworkStateOperators.CURRENT)

        return n

    @staticmethod
    def _visited_mrids(visited) -> List[str]:
        return [it.equipment.mrid for it in visited]

    async def _current_non_directional_trace(self, start: ConductingEquipment, phases: PhaseCode) -> List[TrackedPhases]:
        return await self._run_trace(Tracing.network_trace(NetworkStateOperators.CURRENT).add_condition(stop_at_open()), start, phases)

    async def _normal_downstream_trace(self, start: ConductingEquipment, phases: PhaseCode) -> List[TrackedPhases]:
        return await self._run_trace(Tracing.network_trace(NetworkStateOperators.NORMAL).add_condition(downstream()), start, phases)

    async def _current_downstream_trace(self, start: ConductingEquipment, phases: PhaseCode) -> List[TrackedPhases]:
        return await self._run_trace(Tracing.network_trace(NetworkStateOperators.CURRENT).add_condition(downstream()), start, phases)

    async def _normal_upstream_trace(self, start: ConductingEquipment, phases: PhaseCode) -> List[TrackedPhases]:
        return await self._run_trace(Tracing.network_trace(NetworkStateOperators.NORMAL).add_condition(upstream()), start, phases)

    @staticmethod
    async def _run_trace(trace: NetworkTrace, start: ConductingEquipment, phases: PhaseCode) -> List[TrackedPhases]:
        visited = []

        await (
            trace.add_step_action(lambda step, ctx: print(f"{step.path} - isStopping:{ctx.is_stopping}"))
            .add_step_action(
                lambda step, stx: visited.append(TrackedPhases(step.path.to_equipment, frozenset({it.to_phase for it in step.path.nominal_phase_paths}))))
            .run(start, phases=phases)
        )

        return visited
