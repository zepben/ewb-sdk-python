#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

import sys
from typing import Generator, Optional, Callable, Iterable, List, Union, Type, TYPE_CHECKING

from zepben.evolve.model.cim.iec61970.base.wires.clamp import Clamp
from zepben.evolve.model.cim.iec61970.base.wires.connectors import BusbarSection
from zepben.evolve.model.cim.iec61970.base.wires.cut import Cut
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.base.wires.aclinesegment import AcLineSegment
from zepben.evolve.services.network.tracing.connectivity.terminal_connectivity_connected import TerminalConnectivityConnected
from zepben.evolve.services.network.tracing.networktrace.network_trace_step import NetworkTraceStep

if TYPE_CHECKING:
    from zepben.evolve.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators

__all__ = ['NetworkTraceStepPathProvider']

PathFactory = Callable[[Terminal, AcLineSegment], Optional[NetworkTraceStep.Path]]


class NetworkTraceStepPathProvider:
    def __init__(
        self,
        state_operators: Type[NetworkStateOperators]
    ):
        self.state_operators = state_operators

    def next_paths(
        self,
        path: NetworkTraceStep.Path
    ) -> Generator[NetworkTraceStep.Path, None, None]:

        path_factory = (self._create_path_with_phases_factory(path) if path.nominal_phase_paths
                        else self._create_path_factory(path))

        def _get_next_paths():
            to_equipment = path.to_equipment
            if isinstance(to_equipment, AcLineSegment):
                return self._next_paths_from_ac_line_segment(to_equipment, path, path_factory)
            elif isinstance(to_equipment, BusbarSection):
                return self._next_paths_from_busbar(path, path_factory)
            elif isinstance(to_equipment, Clamp):
                return self._next_paths_from_clamp(to_equipment, path, path_factory)
            elif isinstance(to_equipment, Cut):
                return self._next_paths_from_cut(to_equipment, path, path_factory)

            elif path.traced_internally:
                return self._next_external_paths(path, path_factory)
            else:
                return seq_term_map_to_path(path.to_terminal.other_terminals(), path_factory)

        return (p for p in _get_next_paths() if p and self.state_operators.is_in_service(p.to_terminal.conducting_equipment))

    @staticmethod
    def _create_path_factory(
        path: NetworkTraceStep.Path
    ) -> PathFactory:

        def path_factory(next_terminal: Terminal, traversed: AcLineSegment) -> NetworkTraceStep.Path:
            return NetworkTraceStep.Path(path.to_terminal, next_terminal, traversed)
        return path_factory

    @staticmethod
    def _create_path_with_phases_factory(
        path: NetworkTraceStep.Path
    ) -> PathFactory:

        phase_paths = set(p.to_phase for p in path.nominal_phase_paths)
        next_from_terminal = path.to_terminal

        def path_factory(next_terminal: Terminal, traversed: AcLineSegment):
            next_paths = TerminalConnectivityConnected().terminal_connectivity(next_from_terminal, next_terminal, phase_paths)
            if next_paths.nominal_phase_paths:
                return NetworkTraceStep.Path(next_from_terminal, next_terminal, traversed, set(next_paths.nominal_phase_paths))
            else:
                return None

        return path_factory

    def _next_paths_from_ac_line_segment(
        self,
        segment: AcLineSegment,
        path: NetworkTraceStep.Path,
        path_factory: PathFactory
    ) -> Generator[NetworkTraceStep.Path, None, None]:

        # If the current path traversed the segment, we need to step externally from the segment terminal.
        # Otherwise, we traverse the segment
        if path.traced_internally or path.did_traverse_ac_line_segment:
            yield from self._next_external_paths(path, path_factory)
        else:
            if path.to_terminal.sequence_number == 1:
                yield from self._acls_traverse_from_terminal(
                    segment,
                    path.to_terminal,
                    length_from_t1=0.0,
                    towards_segment_t2=True,
                    can_stop_at_cut_at_same_position=True,
                    cut_at_same_position_from_terminal_number=1,
                    path_factory=path_factory)
            else:
                yield from self._acls_traverse_from_terminal(
                    segment,
                    path.to_terminal,
                    length_from_t1=acls_length_or_max(segment),
                    towards_segment_t2=False,
                    can_stop_at_cut_at_same_position=True,
                    cut_at_same_position_from_terminal_number=2,
                    path_factory=path_factory)

    @staticmethod
    def _next_paths_from_busbar(
        path: NetworkTraceStep.Path,
        path_factory: PathFactory
    ) -> Generator[NetworkTraceStep.Path, None, None]:

        yield from seq_term_map_to_path(
            (t for t in path.to_terminal.connected_terminals()
             # We don't go back to the terminal we came from as we already visited it to get to this busbar.
             if t != path.from_terminal
             # We don't step to terminals that are busbars as they would have been returned at the same time this busbar step was.
             and not isinstance(t.conducting_equipment, BusbarSection)
             ), path_factory
        )

    def _next_paths_from_clamp(
        self,
        clamp: Clamp,
        path: NetworkTraceStep.Path,
        path_factory: PathFactory
    ) -> Generator[NetworkTraceStep.Path, None, None]:

        # If the current path was from traversing an AcLineSegment, we need to step externally to other equipment.
        # Otherwise, we need to traverse the segment both ways.
        if path.did_traverse_ac_line_segment:
            yield from self._next_external_paths(path, path_factory)
            return

        elif path.traced_internally:
            yield from self._next_external_paths(path, path_factory)
        yield from self._traverse_ac_line_segment_from_clamp(clamp, path, path_factory)

    def _traverse_ac_line_segment_from_clamp(
        self,
        clamp: Clamp,
        path: NetworkTraceStep.Path,
        path_factory: PathFactory
    ) -> Generator[NetworkTraceStep.Path, None, None]:

        # Because we consider clamps at the same position as a cut on the terminal 1 side, we do not stop at cuts at the same position when
        # traversing towards t1, but we do when traversing towards t2.
        if not clamp.ac_line_segment:
            return

        _yielded_paths = set()

        def _mark(_path):
            _yielded_paths.add(_path.to_terminal)
            return _path

        yield from (
                _mark(path) for path in self._acls_traverse_from_terminal(
                clamp.ac_line_segment,
                path.to_terminal,
                length_from_t1=clamp.length_from_T1_or_0,
                towards_segment_t2=False,
                can_stop_at_cut_at_same_position=False,
                cut_at_same_position_from_terminal_number=1,
                path_factory=path_factory
            )
        )

        yield from (
                _mark(path) for path in self._acls_traverse_from_terminal(
                clamp.ac_line_segment,
                path.to_terminal,
                length_from_t1=clamp.length_from_T1_or_0,
                towards_segment_t2=True,
                can_stop_at_cut_at_same_position=True,
                cut_at_same_position_from_terminal_number=1,
                path_factory=path_factory
            ) if path.to_terminal not in _yielded_paths
        )

    def _next_paths_from_cut(
        self,
        cut: Cut,
        path: NetworkTraceStep.Path,
        path_factory: PathFactory
    ) -> Iterable[NetworkTraceStep.Path]:

        # If the current path was from traversing an AcLineSegment, we need to step externally to other equipment.
        if path.did_traverse_ac_line_segment:
            yield from self._next_external_paths(path, path_factory)
        # Else we need to traverse the segment.
        elif cut.ac_line_segment:
            yield from self._acls_traverse_from_terminal(
                cut.ac_line_segment,
                path.to_terminal,
                length_from_t1=cut.length_from_T1_or_0,
                towards_segment_t2=path.to_terminal.sequence_number != 1,
                can_stop_at_cut_at_same_position=False,
                cut_at_same_position_from_terminal_number=path.to_terminal.sequence_number,
                path_factory=path_factory
            )

        # If the current path traced internally, we need to also return the external terminals
        if path.traced_internally:
            # traversedAcLineSegment and tracedInternally should never both be true, so we should never get external terminals twice
            yield from self._next_external_paths(path, path_factory)
        # Else we need to step internally to the Cut's other terminal.
        else:
            other_terminal = cut.get_terminal_by_sn(2 if path.to_terminal.sequence_number == 1 else 1)
            yield from seq_term_map_to_path(other_terminal, path_factory)


    def _next_external_paths(
        self,
        path: NetworkTraceStep.Path,
        path_factory: PathFactory
    ) -> Generator[NetworkTraceStep.Path, None, None]:

        #Busbars are only modelled with a single terminal. So if we find any we need to step to them before the
        #other (non busbar) equipment connected to the same connectivity node. Once the busbar has been
        #visited we then step to the other non busbar terminals connected to the same connectivity node.
        #If there are no busbars we can just step to all other connected terminals.
        if isinstance(path.to_equipment, BusbarSection):
            yield from self._next_paths_from_busbar(path, path_factory)
        elif path.to_terminal.has_connected_busbars():
            yield from seq_term_map_to_path((t for t in path.to_terminal.connected_terminals() if isinstance(t.conducting_equipment, BusbarSection)), path_factory)
        else:
            yield from seq_term_map_to_path(path.to_terminal.connected_terminals(), path_factory)

    def _acls_traverse_from_terminal(
        self,
        acls: AcLineSegment,
        from_terminal: Terminal,
        length_from_t1: float,
        towards_segment_t2: bool,
        can_stop_at_cut_at_same_position: bool,
        cut_at_same_position_from_terminal_number: int,
        path_factory: PathFactory
    ) -> Generator[NetworkTraceStep.Path, None, None]:
        """
        This returns terminals found traversing along an AcLineSegment from any terminal "on" the segment. Terminals considered on the segment are any clamp
        or cut terminals that belong to the segment as well as the segment's own terminals. When traversing the segment, the traversal stops
        at and returns the next cut terminal found along the segment plus any clamp terminals it found between the fromTerminal and the cut terminal.
        If there are no cuts on the segment the terminal, the other end of the segment is returned along with all clamp terminals.
        To determine order of terminals on the segment, `lengthFromTerminal1` is used for cuts and clamps. When this property is null a default value of 0.0 is
        assumed, effectively placing it at the start of the segment. Terminal 1 on the segment is deemed at 0.0 and Terminal 2 is deemed at
        [AcLineSegment.length] or [Double.MAX_VALUE] if the length or the segment is `None`.

        This algorithm assumes AcLineSegments have exactly 2 terminals, cuts have exactly 2 terminals and clamps have exactly 1 terminal.

        If there is a cut and a clamp at the exact same length on the segment, it is assumed the clamp is on the terminal 1 side of the cut. This is so you do not
        get the clamp twice when traversing a segment from one end to the other. As a clamp can't technically be in the exact same spot as a cut, you should
        realistically model this either attaching the equipment attached by the clamp to the appropriate cut terminal, or, place a clamp at a length that is
        not exactly the same as the cut. This would yield more accurate and deterministic behaviour.

        :param from_terminal: The terminal on the segment to traverse from. This could either be a segment terminal, or a terminal from any cut or clamp on the segment.
        :param length_from_t1: The length from terminal 1 the fromTerminal is.
        :param towards_segment_t2: Use `true` if the segment should be traversed towards terminal 2, otherwise `False` to traverse towards terminal 1
        """

        cuts, clamps = list(acls.cuts), list(acls.clamps)

        # Can do a simple return if we don't need to do any special cuts/clamps processing
        if not any((cuts, clamps)):
            yield from seq_term_map_to_path(from_terminal.other_terminals(), path_factory, acls)
            return

        # We need to ignore cuts and clamps that are not "in service" because that means they do not exist!
        # We also make sure we filter out the cut or the clamp we are starting at, so we don't compare it in our checks
        filter_func = lambda it: it != from_terminal.conducting_equipment and self.state_operators.is_in_service(it)
        cuts: List[Cut] = list(filter(filter_func, cuts))
        clamps: List[Clamp] = list(filter(filter_func, clamps))

        cuts_at_same_position = [it for it in cuts if it.length_from_T1_or_0 == length_from_t1]
        stop_at_cuts_at_same_position = bool(can_stop_at_cut_at_same_position and cuts_at_same_position)

        def next_cut_length_from_terminal_1_func():
            if stop_at_cuts_at_same_position:
                return length_from_t1
            elif towards_segment_t2:
                return min((it.length_from_T1_or_0 for it in cuts if it.length_from_T1_or_0 > length_from_t1), default=None)
            else:
                return max((it.length_from_T1_or_0 for it in cuts if it.length_from_T1_or_0 < length_from_t1), default=None)

        next_cut_length_from_terminal_1 = next_cut_length_from_terminal_1_func()

        next_cuts = [it for it in cuts if it.length_from_T1_or_0 == next_cut_length_from_terminal_1] if next_cut_length_from_terminal_1 is not None else []

        def next_term_length_from_term_1_func():
            if next_cut_length_from_terminal_1 is not None:
                return next_cut_length_from_terminal_1
            elif towards_segment_t2:
                return acls_length_or_max(acls)
            else:
                return 0.0

        next_terminal_length_from_terminal_1 = next_term_length_from_term_1_func()

        def clamps_before_next_terminal_filter() -> Callable[[Clamp], bool]:
            if isinstance(from_terminal.conducting_equipment, AcLineSegment) and towards_segment_t2:
                return lambda it: length_from_t1 <= it.length_from_T1_or_0 <= next_terminal_length_from_terminal_1
            elif towards_segment_t2:
                return lambda it: length_from_t1 < it.length_from_T1_or_0 <= next_terminal_length_from_terminal_1
            elif (next_terminal_length_from_terminal_1 == 0.0) and len(next_cuts) == 0:
                return lambda it: next_terminal_length_from_terminal_1 <= it.length_from_T1_or_0 <= length_from_t1
            else:
                return lambda it: length_from_t1 >= it.length_from_T1_or_0 > next_terminal_length_from_terminal_1

        _filter = clamps_before_next_terminal_filter()

        clamps_before_next_terminal = (c for c in clamps if _filter(c))

        next_stop_terminals = [] if stop_at_cuts_at_same_position else (
                it.get_terminal(1 if towards_segment_t2 else 2) for it in next_cuts
        ) if next_cuts else [acls.get_terminal(2 if towards_segment_t2 else 1)]

        next_terminals = (
            (it.get_terminal(cut_at_same_position_from_terminal_number) for it in cuts_at_same_position),
            (it.get_terminal(1) for it in clamps_before_next_terminal),
            next_stop_terminals
        )

        for generator in next_terminals:
            yield from seq_term_map_to_path(generator, path_factory, acls)

def seq_term_map_to_path(
    terms: Union[Terminal, Iterable[Terminal]],
    path_factory: PathFactory,
    traversed_acls: AcLineSegment=None
) -> Generator[NetworkTraceStep.Path, None, None]:

    if isinstance(terms, Iterable):
        for terminal in terms:
            if terminal is not None:
                yield path_factory(terminal, traversed_acls)
    else:
        yield path_factory(terms, traversed_acls)

acls_length_or_max = lambda acls: acls.length or sys.float_info.max
