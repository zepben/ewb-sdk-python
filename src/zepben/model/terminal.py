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


from zepben.cim.iec61970 import Terminal as PBTerminal
from zepben.model.cores import from_count
from zepben.model.identified_object import IdentifiedObject
from zepben.model.diagram_layout import DiagramObject
from zepben.model.phases import Phases, cores_from_phases
from zepben.model.wiring import IMPLICIT_WIRING, Wiring
from zepben.model.exceptions import NoEquipmentException, NoConnectivityNodeException, WiringException
from zepben.model.tracing.phase_status import current_phases as ps_current_phases, normal_phases as ps_normal_phases
from typing import List, Set
from weakref import ref
from zepben.model.tracing.connectivity import ConnectivityResult


class Terminal(IdentifiedObject):
    """
    A terminal is a connection point on a piece of ConductingEquipment. All ConductingEquipment must have terminals and
    all terminals must have an associated piece of ConductingEquipment.

    Note: If you are extending this class you must ensure you always safely access the linked equipment (i.e, check it is
    not None)

    Attributes:
        - equipment : A reference back to the equipment this Terminal belongs to. This reference will typically
                      be added in :class:`zepben.model.ConductingEquipment::__init__()`.
        - phases : A :class:`zepben.model.phases.PhaseCode` representing the normal network phasing condition of this
                   Terminal.
        - connected : The connected status is related to a bus-branch model and the topological node to terminal relation.
                      True implies the terminal is connected to the related topological node and false implies it is not.
                      In a bus-branch model, the connected status is used to tell if equipment is disconnected without having to change
                      the connectivity described by the topological node to terminal relation. A valid case is that conducting
                      equipment can be connected in one end and open in the other. In particular for an AC line segment,
                      where the reactive line charging can be significant, this is a relevant case.
    """

    def __init__(self, mrid: str, connectivity_node, phases: Phases = None, name: str = "",
                 diag_objs: List[DiagramObject] = None, equipment=None, connected: bool = True):
        """
        Create a Terminal.
        The provided connectivity_node will always be referenced weakly to ensure that a single Terminal reference
        can't indirectly keep an entire network alive via the ConnectivityNode.
        :param mrid: Master resource identifier for this Terminal.
        :param phases: A :class:`zepben.model.phases.PhaseCode` representing the normal network phasing condition of this
                       Terminal.
        :param connectivity_node: The :class:`zepben.model.ConnectivityNode` that this terminal is attached to.
        :param name: Any free human readable and possibly non unique text naming the object.
        :param diag_objs: An ordered list of :class:`zepben.model.DiagramObject`'s.
        :param connected: Whether this terminal is connected (potentially energised). See description in class definition.
        :param equipment: A reference to the equipment that owns this terminal. This can be set after instantiation as
                          to resolve chicken-and-egg issues between terminals and equipment (as both have references).
        """
        self.phases = phases if phases is not None else Phases()
        self.connected = connected
        self.__connectivity_node = ref(connectivity_node)
        self.__equipment = equipment
        self.__ext_int_wiring = [-1 for _ in range(self.num_cores)]
        self.__int_ext_wiring = [-1 for _ in range(self.num_cores)]
        super().__init__(mrid, name, diag_objs)

    @property
    def connectivity_node(self):
        return self.__connectivity_node()

    @connectivity_node.setter
    def connectivity_node(self, cn):
        self.__connectivity_node = ref(cn)

    @property
    def equipment(self):
        if self.__equipment is None:
            raise NoEquipmentException("Terminal was missing a reference to its connected piece of equipment, this should not happen.")
        return self.__equipment

    @equipment.setter
    def equipment(self, equip):
        self.__equipment = equip

    @property
    def num_cores(self):
        try:
            return self.equipment.num_cores
        except (AttributeError, NoEquipmentException):  # Equipment may not be set yet, but num_cores should always be the same.
            return cores_from_phases(self.phases.phase)

    def __lt__(self, other):
        """
        TODO: this will be used for priority. Implement this based on phasing (more phases = higher priority = less than)
              Need to check if heap queue sorts ascending or descending.
        :param other:
        :return:
        """
        return self.num_cores > other.num_cores

    def normal_phases(self, core):
        return ps_normal_phases(self, core)

    def current_phases(self, core):
        return ps_current_phases(self, core)

    def get_pos_point(self):
        return self.equipment.pos_point(self.get_sequence_number())

    def get_sequence_number(self):
        return self.equipment.terminal_sequence_number(self)

    def get_switch(self):
        """
        Get any associated switch for this Terminal
        :return: Switch if present in this terminals ConnectivityNode, else None
        """
        return self.connectivity_node.get_switch()

    def get_nominal_voltage(self):
        return self.equipment.get_nominal_voltage(self)

    def external_to_internal_wiring(self, external_wiring: int):
        """
        :param external_wiring: The external wiring of the connectivity node.
        :return: The core of the conducting equipment connected to the external wiring.
        """
        if external_wiring < 0 or external_wiring >= len(self.__ext_int_wiring):
            return -1
        return self.__ext_int_wiring[external_wiring]

    def internal_to_external_wiring(self, core: int):
        """
        :param core: the core of the conducting equipment.
        :return: The external wiring of the connectivity node connected to the core.
        """
        if core < 0 or core >= len(self.__int_ext_wiring):
            return -1
        return self.__int_ext_wiring[core]

    def get_other_terminals(self):
        return [t for t in self.equipment.terminals if t is not self]

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

    def connect(self, wiring: Wiring):
        """
        Connect this terminal's wiring to its `ConnectivityNode`
        :param wiring: The wiring to use to connect
        :raises: :class:`zepben.model.exceptions.WiringException` if `wiring` is incompatible with the `ConnectivityNode`
        """
        if wiring.num_cores != self.num_cores:
            raise WiringException(f"Wiring had {wiring.num_cores} and terminal had {self.num_cores}. They must have the same number of cores")
        # max_cores = -1
        # if not self.connectivity_node.terminals:
        #     max_cores = self.num_cores
        # else:
        #     for t in self.connectivity_node.terminals:
        #         max_cores = max(max_cores, t.num_cores)
        # TODO: Fix this. It currently enforces order on the connectivity model via loading of equipment.
        #       Probably this validation should be moved to a separate network validation step
        # if wiring.max_connectivity_node_wires >= max_cores:
        #    raise WiringException(f"Wiring ({wiring.max_connectivity_node_wires}) cores exceeds connectivity node ({max_cores}) cores")
        self.__int_ext_wiring = wiring.terminal_to_connectivity_node()
        self.__ext_int_wiring = wiring.connectivity_node_to_terminal()

    def to_pb(self):
        args = self._pb_args()
        args['connectivityNodeMRID'] = self.connectivity_node.mrid
        return PBTerminal(**args)

    @staticmethod
    def from_pb(pb_t, network, **kwargs):
        """
        Every terminal requires a connectivityNodeMRID to be specified.
        :param pb_t: A protobuf Terminal to convert to Terminal
        :param network: The EquipmentContainer that the terminal belongs to. Associated ConnectivityNode's will be
                        added to this network.
        :param wiring: Wiring for this Terminal. TODO: does this need to be part of Terminal.proto?
        :return: A zepben.model.Terminal
        :raises: NoConnectivityNodeException when connectivityNodeMRID is not set.
        """
        if not pb_t.connectivityNodeMRID:
            raise NoConnectivityNodeException(f"Terminal {pb_t.mRID} has no connectivity node declared.")
        conn_node = network.add_connectivitynode(pb_t.connectivityNodeMRID)
        term = Terminal(mrid=pb_t.mRID,
                        phases=Phases.from_pb(pb_t.phases),
                        connectivity_node=conn_node,
                        name=pb_t.name,
                        connected=pb_t.connected,
                        diag_objs=DiagramObject.from_pbs(pb_t.diagramObjects))
        term.connect(IMPLICIT_WIRING[term.num_cores])
        conn_node.add_terminal(term)
        return term

    def __str__(self):
        return f"{super().__str__()}, {self.phases}, cn: {self.connectivity_node.mrid}, conn: {self.connected}"

