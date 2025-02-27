#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from enum import Enum
from dataclasses import dataclass
from typing import TypeVar

from zepben.evolve import Terminal, NominalPhasePath, ConductingEquipment

T = TypeVar('T')


class NetworkTraceStep[T]:
    """
    Represents a single step in a network trace, containing information about the path taken and associated data.

    `T` The type of additional data associated with the trace step.
    `path` The path representing the transition from one terminal to another.
    `numTerminalSteps` The count of terminals stepped on along this path.
    `numEquipmentSteps` The count of equipment stepped on along this path.
    `data` Additional data associated with this step in the trace.
    `type` The [Type] of this step.
    """
    @dataclass
    class Path:
        """
        Represents the path taken in a network trace step, detailing the transition from one terminal to another.

        A limitation of the network trace is that all terminals must have associated conducting equipment. This means that if the [fromTerminal]
        or [toTerminal] have `null` conducting equipment an [IllegalStateException] will be thrown.

        `fromTerminal` The terminal that was stepped from.
        `toTerminal` The terminal that was stepped to.
        `nominalPhasePaths` A list of nominal phase paths traced in this step. If this is empty, phases have been ignored.
        `fromEquipment` The conducting equipment associated with the [fromTerminal].
        `toEquipment` The conducting equipment associated with the [toTerminal].
        `tracedInternally` `true` if the from and to terminals belong to the same equipment; `false` otherwise.
        `tracedExternally` `true` if the from and to terminals belong to different equipment; `false` otherwise.
        """
        from_terminal: Terminal
        to_terminal: Terminal
        nominal_phase_paths: list[NominalPhasePath]

        @property
        def from_equipment(self) -> ConductingEquipment:
            return self.from_terminal.conducting_equipment  # TODO error("Network trace does not support terminals that do not have conducting equipment")

        @property
        def to_equipment(self) -> ConductingEquipment:
            return self.to_terminal.conducting_equipment  # TODO error("Network trace does not support terminals that do not have conducting equipment")

        @property
        def traced_internally(self) -> bool:
            return self.from_equipment == self.to_equipment

        @property
        def traced_externally(self) -> bool:
            return not self.traced_internally

    path: Path
    Type = Enum('ALL', 'INTERNAL', 'EXTERNAL')
    num_terminal_steps: int
    num_equipment_steps: int
    data: T

    def type(self) -> Path:
        """
        Returns the [Type] of the step. This will be [Type.INTERNAL] if [Path.tracedInternally] is true, [Type.EXTERNAL] when [Path.tracedExternally] is true
        and will never be [Type.ALL] which is used in other NetworkTrace functionality to determine if all steps should be used for that particular function.

        Returns [Type.INTERNAL] with [Path.tracedInternally] is true, [Type.EXTERNAL] when [Path.tracedExternally] is true
        """
        if self.path.traced_internally():
            return self.Type.INTERNAL
        else:
            return self.Type.EXTERNAL

