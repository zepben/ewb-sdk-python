"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations

from dataclasses import dataclass, field, InitVar
from typing import Set, Optional
from weakref import ref, ReferenceType

from zepben.cimbend.cim.iec61970.base.core.identified_object import IdentifiedObject
from zepben.cimbend.cim.iec61970.base.core.phase_code import PhaseCode
from zepben.cimbend.cores import from_count
from zepben.cimbend.phases import TracedPhases, cores_from_phases
from zepben.cimbend.tracing.connectivity import ConnectivityResult
from zepben.cimbend.tracing.phase_status import current_phases as ps_current_phases, normal_phases as ps_normal_phases

__all__ = ["AcDcTerminal", "Terminal"]

# This is False to allow us to ref() it below. It's expected that users will always check existence via ``if x.connectivity_node:``
NO_CONNECTIVITY_NODE = False


class AcDcTerminal(IdentifiedObject):
    """
    An electrical connection point (AC or DC) to a piece of conducting equipment. Terminals are connected at physical
    connection points called connectivity nodes.
    """
    pass


@dataclass
class Terminal(AcDcTerminal):
    """
    A terminal is a connection point on a piece of ConductingEquipment. Terminals are connected at physical connection points called connectivity nodes.
    All ConductingEquipment must have terminals and all terminals must have an associated piece of ConductingEquipment.

    Note: If you are extending this class you must ensure you always safely access the linked equipment (i.e, check it is
    not None)

    Attributes -
        - conducting_equipment : A reference back to the equipment this Terminal belongs to. Conducting equipment have
                                terminals that may be connected to other conducting equipment terminals via connectivity
                                nodes or topological nodes.
                                Note: The Terminal will *not* be added to the ``conducting_equipment`` as part of construction.
                                You must explicitly add the ``Terminal`` to its ``ConductingEquipment`` via ``add_terminal()``.
        - phases : A :class:`zepben.cimbend.phases.PhaseCode` representing the normal network phasing condition of this
                   Terminal.
        - connectivity_node: The :class:`zepben.cimbend.iec61970.base.core.connectivity_node.ConnectivityNode` that this
                             ``Terminal`` is connected to.
        - traced_phases: The :class:`zepben.cimbend.phases.TracedPhases` representing the traced phases in both the
                         normal and current network. If properly configured you would expect the normal state phases to
                         match those in ``phases``
    """
    conducting_equipment: Optional[ConductingEquipment] = None
    phases: PhaseCode = PhaseCode.ABC
    traced_phases: TracedPhases = field(default_factory=TracedPhases)
    connectivitynode: InitVar[ConnectivityNode] = NO_CONNECTIVITY_NODE
    _cn: ReferenceType = field(init=False)

    def __post_init__(self, connectivitynode):
        super().__post_init__()
        self.connectivity_node = connectivitynode

    @property
    def connectivity_node(self):
        return self._cn()

    @connectivity_node.setter
    def connectivity_node(self, cn):
        self._cn = ref(cn)

    @property
    def connected(self) -> bool:
        return self.connectivity_node

    def __lt__(self, other):
        """
        TODO: fix
        This definition should only be used for sorting within a :class:`zepben.cimbend.tracing.queue.PriorityQueue`
        :param other: Another Terminal to compare against
        :return: True if self has more cores than other, False otherwise.
        """
        return cores_from_phases(self.phases) > cores_from_phases(other.phases)

    def normal_phases(self, nominal_phase: SinglePhaseKind):
        return ps_normal_phases(self, nominal_phase)

    def current_phases(self, nominal_phase: SinglePhaseKind):
        return ps_current_phases(self, nominal_phase)

    def get_pos_point(self):
        return self.conducting_equipment.pos_point(self.get_sequence_number())

    def get_sequence_number(self):
        return self.conducting_equipment.terminal_sequence_number(self)

    def get_switch(self):
        """
        Get any associated switch for this Terminal
        :return: Switch if present in this terminals ConnectivityNode, else None
        """
        return self.connectivity_node.get_switch()

    def get_nominal_voltage(self):
        return self.conducting_equipment.get_nominal_voltage(self)

    def get_other_terminals(self):
        return [t for t in self.conducting_equipment.terminals if t is not self]

    def get_connectivity(self, cores: Set[int] = None, exclude=None):
        """
        Get the connectivity between this terminal and all other terminals in its `ConnectivityNode`.
        :param cores: Core paths to trace between the terminals. Defaults to all cores.
        :param exclude: `Terminal`'s to exclude from the result. Will be skipped if encountered.
        :return: List of :class:`ConnectivityResult`'s for this terminal.
        """
        if exclude is None:
            exclude = set()
        if cores is None:
            cores = from_count(self.num_cores)
        results = []
        for terminal in self.connectivity_node:
            if self != terminal and terminal not in exclude:  # Don't include ourselves.
                cr = ConnectivityResult(self, terminal)
                for core in cores:
                    connected_core = terminal.external_to_internal_wiring(self.internal_to_external_wiring(core))
                    if connected_core != -1:
                        cr.add_core_path(core, connected_core)
                if cr.from_cores:
                    # Only return CR's that are physically wired together.
                    results.append(cr)
        return results

    def connect(self, connectivity_node: ConnectivityNode):
        self.connectivity_node = ref(connectivity_node)

    def disconnect(self):
        self.connectivity_node = NO_CONNECTIVITY_NODE

