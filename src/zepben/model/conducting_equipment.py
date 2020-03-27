from __future__ import annotations
from copy import copy
from zepben.model.equipment import Equipment
from zepben.model.cores import SUPPORTED_CORES
from zepben.model.phases import cores_from_phases
from zepben.model.base_voltage import BaseVoltage
from zepben.model.exceptions import NoEquipmentException
from typing import List, Set
__all__ = ['ConductingEquipment']


class ConductingEquipment(Equipment):
    """
    Abstract class, should only be used through subclasses.
    The parts of the AC power system that are designed to carry current or that are conductively connected through
    terminals.

    ConductingEquipment are connected by :class:`zepben.model.Terminal`'s which are in turn associated with
    :class:`zepben.model.ConnectivityNode`'s. Each `Terminal` is associated with _exactly one_ `ConnectivityNode`,
    and through that `ConnectivityNode` can be linked with many other `Terminals` and thus `ConductingEquipment`.

    Attributes:
        - base_voltage : A :class:`zepben.model.BaseVoltage`.
        - terminals : Conducting equipment have terminals that may be connected to other conducting equipment terminals
                      via connectivity nodes or topological nodes.
    """
    def __init__(self, mrid: str, base_voltage: BaseVoltage, terminals: List[Terminal], in_service: bool = True,
                 normally_in_service: bool = True, name: str = "", diag_objs: List[DiagramObject] = None,
                 location: Location = None, asset_info: AssetInfo = None, usage_points: List[UsagePoint] = None):
        """
        Create a ConductingEquipment
        :param mrid: mRID for this object
        :param in_service: If True, the equipment is in service.
        :param base_voltage: A :class:`zepben.model.BaseVoltage`.
        :param normally_in_service: If True, the equipment is _normally_ in service.
        :param name: Any free human readable and possibly non unique text naming the object.
        :param terminals: An ordered list of :class:`zepben.model.Terminal`'s. The order is important and the index of
                          each Terminal should reflect each Terminal's `sequenceNumber`.
        :param diag_objs: An ordered list of :class:`zepben.model.DiagramObject`'s.
        :param location: :class:`zepben.model.Location` of this resource.
        :param asset_info: A subclass of :class:`zepben.model.AssetInfo` providing information about the asset associated
                           with this PowerSystemResource.
        """
        self.base_voltage = base_voltage
        if terminals is None:
            self.terminals = list()
        else:
            self.terminals = copy(terminals)
        try:
            self.__num_cores = cores_from_phases(self.terminals[0].phases.phase)
        except IndexError:
            self.__num_cores = SUPPORTED_CORES  # Default to max cores when unknown.
        # We set a reference for each terminal back to its equipment to make iteration over a network easier
        for term in self.terminals:
            term.equipment = self
        super().__init__(mrid=mrid, in_service=in_service, normally_in_service=normally_in_service, name=name,
                         asset_info=asset_info, diag_objs=diag_objs, location=location, usage_points=usage_points)

    def __str__(self):
        return f"{super().__str__()} {self.base_voltage} in_serv: {self.in_service}, norm_in_serv: {self.normally_in_service} terms: {self.terminals}"

    def __repr__(self):
        return (f"{super().__repr__()}, num_cores={self.num_cores} in_service={self.in_service}, "
                f"normally_in_service={self.normally_in_service}, location={self.location}"
                )

    def __lt__(self, other):
        """
        This definition should only be used for sorting within a :class:`zepben.model.tracing.queue.PriorityQueue`
        :param other: Another Terminal to compare against
        :return: True if self has more cores than other, False otherwise.
        """
        return self.num_cores > other.num_cores

    @property
    def num_cores(self):
        return self.__num_cores

    @property
    def nominal_voltage(self):
        return self.base_voltage.nominal_voltage

    def is_metered(self):
        """
        Check whether this piece of equipment is metered. A piece of equipment is metered if it's associated with at
        least one :class:`zepben.model.UsagePoint` that has an :class:`zepben.model.EndDevice` attached to it.
        :return: True if this equipment has at least one `EndDevice` on one `UsagePoint`, False otherwise.
        """
        for up in self.usage_points:
            if up.is_metered():
                return True
        else:
            return False

    def add_terminal(self, terminal):
        self.terminals.append(terminal)

    def terminal_sequence_number(self, terminal):
        """
        Sequence number for terminals is stored as the index of the terminal in `self.terminals`
        :param terminal: The terminal to retrieve the sequence number for
        :return:
        """
        for i, term in enumerate(self.terminals):
            if term is terminal:
                return i
        raise NoEquipmentException("Terminal does not exist in this equipment")

    def get_terminal_for_node(self, node):
        for t in self.terminals:
            if t.connectivity_node.mrid == node.mrid:
                return t
        raise NoEquipmentException(f"Equipment {self.mrid} is not connected to node {node.mrid}")

    def get_terminal(self, seq_num):
        try:
            return self.terminals[seq_num]
        except (KeyError, IndexError):
            raise NoEquipmentException(f"Equipment {self.mrid} does not have a terminal {seq_num}")

    def get_nominal_voltage(self, terminal=None):
        """
        Get the nominal voltage for this piece of equipment.
        In cases where this equipment has multiple nominal voltages (i.e, transformers),
        this method should be overridden so providing a terminal will provide the voltage corresponding to that terminal

        :param terminal: Terminal to fetch voltage for
        """
        return self.nominal_voltage

    def get_connected_equipment(self, exclude: Set = None):
        """
        Get all :class:`ConductingEquipment` connected to this piece of equipment. An `Equipment` is connected if it has
        a `Terminal` associated with a `ConnectivityNode` that this `ConductingEquipment` is also associated with.

        :param exclude: Equipment to exclude from return.
        :return: A list of `ConductingEquipment` that are connected to this.
        """
        if exclude is None:
            exclude = []
        connected_equip = []
        for terminal in self.terminals:
            conn_node = terminal.connectivity_node
            for term in conn_node:
                if term.equipment in exclude:
                    continue
                if term != terminal:  # Don't include ourselves.
                    connected_equip.append(term.equipment)
        return connected_equip

    def _pb_args(self, exclude=None):
        args = super()._pb_args()
        if self.base_voltage:
            args['baseVoltageMRID'] = self.base_voltage.mrid
            del args['baseVoltage']
        return args

