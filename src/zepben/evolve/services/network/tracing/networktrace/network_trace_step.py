#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Set, Generic, TypeVar, TYPE_CHECKING, Optional, List, FrozenSet

from zepben.evolve.services.network.tracing.connectivity.nominal_phase_path import NominalPhasePath

if TYPE_CHECKING:
    from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
    from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
    from zepben.evolve.model.cim.iec61970.base.wires.aclinesegment import AcLineSegment
    from zepben.evolve.model.cim.iec61970.base.wires.single_phase_kind import SinglePhaseKind

T = TypeVar('T')

class NetworkTraceStep(Generic[T]):
    """
    Represents a single step in a network trace, containing information about the path taken and associated data.

    `T` The type of additional data associated with the trace step.
    :param path: The path representing the transition from one terminal to another.
    :param num_terminal_steps: The count of terminals stepped on along this path.
    :param num_equipment_steps: The count of equipment stepped on along this path.
    :param data: Additional data associated with this step in the trace.
    """

    @dataclass
    class Path:
        """
        Represents the path taken in a network trace step, detailing the transition from one terminal to another.

        A limitation of the network trace is that all terminals must have associated conducting equipment. This means that if the `from_terminal`
        or `to_terminal` have `None` conducting equipment an [IllegalStateException] will be thrown.

        No validation is done on the `traversed_ac_line_segment` against the `from_terminal` and `to_terminal`. It assumes the creator knows what they are doing
        and thus avoids the overhead of validation as this class will have lots if instances created as part of a [NetworkTrace].

        :param from_terminal: The terminal that was stepped from.
        :param to_terminal: The terminal that was stepped to.
        :param traversed_ac_line_segment: If the from_terminal and to_terminal path was via an `AcLineSegment`, this is the segment that was traversed
        :param nominal_phase_paths: A list of nominal phase paths traced in this step. If this is empty, phases have been ignored.
        """
        from_terminal: Terminal
        to_terminal: Terminal
        traversed_ac_line_segment: Optional[AcLineSegment] = field(default=None)
        nominal_phase_paths: Optional[Set[NominalPhasePath]] = field(default_factory=set)

        def to_phases_set(self) -> FrozenSet[SinglePhaseKind]:
            if len(self.nominal_phase_paths) == 0:
                return frozenset()
            return frozenset(map(lambda it: it.to_phase, self.nominal_phase_paths))

        @property
        def from_equipment(self) -> ConductingEquipment:
            """
            The conducting equipment associated with `self.from_terminal`.
            """
            ce = self.from_terminal.conducting_equipment
            if not ce:
                raise AttributeError("Network trace does not support terminals that do not have conducting equipment")
            return ce

        @property
        def to_equipment(self) -> ConductingEquipment:
            """
            The conducting equipment associated with `self.to_terminal`.
            """
            ce = self.to_terminal.conducting_equipment
            if not ce:
                raise AttributeError("Network trace does not support terminals that do not have conducting equipment")
            return ce

        @property
        def traced_internally(self) -> bool:
            """
            `True` if the from and to terminals belong to the same equipment; `False` otherwise.
            """
            return self.from_equipment == self.to_equipment

        @property
        def traced_externally(self) -> bool:
            """
            `True` if the from and to terminals belong to different equipment; `False` otherwise.
            """
            return not self.traced_internally

        @property
        def did_traverse_ac_line_segment(self) -> bool:
            return self.traversed_ac_line_segment is not None

        def next_num_equipment_steps(self, current_num: int) -> int:
            return current_num + 1 if self.traced_externally else current_num


    Type = Enum('Type', ('ALL', 'INTERNAL', 'EXTERNAL'))

    def __init__(self, path: Path, num_terminal_steps: int, num_equipment_steps: int, data: T):
        self.path = path
        self.num_terminal_steps = num_terminal_steps
        self.num_equipment_steps = num_equipment_steps
        self.data = data

    def type(self) -> Type:
        """
        Returns the [Type] of the step. This will be [Type.INTERNAL] if [Path.tracedInternally] is true, [Type.EXTERNAL] when [Path.tracedExternally] is true
        and will never be [Type.ALL] which is used in other NetworkTrace functionality to determine if all steps should be used for that particular function.

        Returns [Type.INTERNAL] with [Path.tracedInternally] is true, [Type.EXTERNAL] when [Path.tracedExternally] is true
        """
        return self.Type.INTERNAL if self.path.traced_internally else self.Type.EXTERNAL

    def next_num_terminal_steps(self):
        return self.num_terminal_steps + 1
