#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

import itertools
import logging
from enum import Enum
from typing import TYPE_CHECKING, Dict, List, Union, Iterable

from zepben.evolve.model.cim.iec61970.base.core.phase_code import PhaseCode

from zepben.evolve.model.cim.iec61970.base.core.connectivity_node import ConnectivityNode
from zepben.evolve.services.common.base_service import BaseService
from zepben.evolve.services.network.tracing.connectivity.terminal_connectivity_connected import TerminalConnectivityConnected
from pathlib import Path
if TYPE_CHECKING:
    from zepben.evolve import Terminal, SinglePhaseKind, ConnectivityResult, Measurement, ConductingEquipment

__all__ = ["connect", "connected_terminals", "connected_equipment", "NetworkService"]
logger = logging.getLogger(__name__)
TRACED_NETWORK_FILE = str(Path.home().joinpath(Path("traced.json")))


class ProcessStatus(Enum):
    PROCESSED = 0
    INVALID = 1
    SKIPPED = 2


def connect(terminal: Terminal, connectivity_node: ConnectivityNode):
    """
    Connect a `Terminal`` to a `ConnectivityNode`
    `terminal` The `Terminal` to connect.
    `connectivity_node` The `ConnectivityNode` to connect ``Terminal` to.
    """
    terminal.connect(connectivity_node)
    connectivity_node.add_terminal(terminal)


def connected_terminals(terminal: Terminal, phases: Union[None, PhaseCode, Iterable[SinglePhaseKind]] = None) -> List[ConnectivityResult]:
    """
    Find the connected `Terminal`s for the specified `terminal` using only the phases of the specified `phaseCode`.

    @param terminal: The `Terminal` to process.
    @param phases: Which phases should be used for the connectivity check. If omitted, the phases of `terminal` will be used.
    @return: A list of `ConnectivityResult` specifying the connections between `terminal` and the connected `Terminal`s
    """
    phases = phases or terminal.phases
    if isinstance(phases, PhaseCode):
        phases = phases.single_phases

    return TerminalConnectivityConnected().connected_terminals(terminal, phases)


def connected_equipment(conducting_equipment: ConductingEquipment,
                        phases: Union[None, PhaseCode, Iterable[SinglePhaseKind]] = None) -> List[ConnectivityResult]:
    """
    Find the connected `ConductingEquipment` for each `Terminal` of `conductingEquipment` using only the specified `phases`.

    @param conducting_equipment: The `ConductingEquipment` to process.
    @param phases: Which phases should be used for the connectivity check. If omitted,
                  all valid phases will be used.
    @return: A list of `ConnectivityResult` specifying the connections between `conductingEquipment` and the connected `ConductingEquipment`
    """
    if isinstance(phases, PhaseCode):
        phases = phases.single_phases

    return list(itertools.chain(*(connected_terminals(term, phases) for term in conducting_equipment.terminals)))


def _attempt_to_reuse_connection(terminal1: Terminal, terminal2: Terminal) -> ProcessStatus:
    """
    Attempt to connect two `Terminal`s.
    Returns `ProcessStatus` reflecting whether the connection was reused. PROCESSED if a connection was
    established, INVALID if it couldn't be, and SKIPPED if neither terminal had an existing `ConnectivityNode`.
    """
    cn1 = terminal1.connectivity_node
    cn2 = terminal2.connectivity_node

    if cn1 is not None:
        if cn2 is not None:
            if cn1 is cn2:
                return ProcessStatus.PROCESSED
        elif connect(terminal2, cn1):
            return ProcessStatus.PROCESSED
        return ProcessStatus.INVALID
    elif cn2 is not None:
        return ProcessStatus.PROCESSED if connect(terminal1, cn2) else ProcessStatus.INVALID
    return ProcessStatus.SKIPPED


class NetworkService(BaseService):
    """
    A full representation of the power network.
    Contains a map of equipment (string ID's -> Equipment/Nodes/etc)
    **All** `IdentifiedObject's` submitted to this Network **MUST** have unique mRID's!

    Attributes -
        metrics_store : Storage for meter measurement data associated with this network.
    """

    name: str = "network"
    _connectivity_nodes: Dict[str, ConnectivityNode] = dict()
    _auto_cn_index: int = 0
    _measurements: Dict[str, List[Measurement]] = []

    def __init__(self):
        self._objects_by_type[ConnectivityNode] = self._connectivity_nodes

    def get_measurements(self, mrid: str, t: type) -> List[Measurement]:
        """
        Get all measurements of type `t` associated with the given `mrid`.
                                                                                                              
        The `mrid` should be either a `PowerSystemResource` or a
        `Terminal` MRID that is assigned to the corresponding fields on the measurements.
        Returns all `Measurement`s indexed by `mrid` in this service.
        Raises `KeyError` if `mrid` isn't present in this service.
        """
        # noinspection PyTypeChecker
        return [meas for meas in self._measurements[mrid] if isinstance(meas, t)]

    def add_measurement(self, measurement: Measurement) -> bool:
        """
        Add a `Measurement` to this `NetworkService`

        `measurement` The `Measurement` to add.
        Returns `True` if `measurement` was added, `False` otherwise
        """
        return self._index_measurement(measurement, measurement.mrid) and self.add(measurement)

    def remove_measurement(self, measurement) -> bool:
        """
        Remove a `Measurement` from this `NetworkService`

        `measurement` The `Measurement` to remove.
        Returns `True` if `measurement` was removed, `False` otherwise
        """
        self._remove_measurement_index(measurement)
        return self.remove(measurement)

    def connect_by_mrid(self, terminal: Terminal, connectivity_node_mrid: str) -> bool:
        """
        Connect a `Terminal` to the `ConnectivityNode` with mRID `connectivity_node_mrid`
        `terminal` The `Terminal` to connect.
        `connectivity_node_mrid` The mRID of the `ConnectivityNode`. Will be created in the `Network` if it
        doesn't already exist.
        Returns True if the connection was made or already existed, False if `Terminal` was already connected to a
        different `ConnectivityNode`
        """
        if not connectivity_node_mrid:
            return False

        if terminal.connectivity_node:
            return connectivity_node_mrid == terminal.connectivity_node.mrid

        cn = self.add_connectivity_node(connectivity_node_mrid)
        connect(terminal, cn)
        return True

    def connect_terminals(self, terminal1: Terminal, terminal2: Terminal) -> bool:
        """
        Connect two `Terminal`s
        Returns True if the `Terminal`s could be connected, False otherwise.
        """
        status = _attempt_to_reuse_connection(terminal1, terminal2)
        if status == ProcessStatus.PROCESSED:
            return True
        elif status == ProcessStatus.INVALID:
            return False

        cn = self.add_connectivity_node(self._generate_cn_mrid())
        connect(terminal2, cn)
        connect(terminal1, cn)

        return True

    def _generate_cn_mrid(self):
        mrid = f"generated_cn_{self._auto_cn_index}"
        while mrid in self._connectivity_nodes:
            self._auto_cn_index += 1
            mrid = f"generated_cn_{self._auto_cn_index}"
        return mrid

    def disconnect(self, terminal: Terminal):
        """
        Disconnect a `Terminal`` from its `ConnectivityNode`. Will also remove the `ConnectivityNode` from this
        `Network` if it no longer has any terminals.
        `terminal` The `Terminal` to disconnect.
        """
        cn = terminal.connectivity_node
        if cn is None:
            return
        cn.remove_terminal(terminal)
        terminal.disconnect()
        if cn.num_terminals() == 0:
            del self._connectivity_nodes[cn.mrid]

    def disconnect_by_mrid(self, connectivity_node_mrid: str):
        """
        Disconnect a `ConnectivityNode` from this `Network`. Will disconnect all ``Terminal`s from the
        `ConnectivityNode`
        `connectivity_node_mrid` The mRID of the `ConnectivityNode` to disconnect.
        Raises `KeyError` if there is no `ConnectivityNode` for `connectivity_node_mrid`
        """
        cn = self._connectivity_nodes[connectivity_node_mrid]
        if cn is not None:
            for term in cn.terminals:
                term.disconnect()
            cn.clear_terminals()
            del self._connectivity_nodes[connectivity_node_mrid]

    def get_primary_sources(self):
        """
        Get the primary source for this network. All directions are applied relative to this EnergySource
        Returns The primary EnergySource
        """
        # noinspection PyUnresolvedReferences
        return [source for source in self._objects_by_type[EnergySource].values() if source.is_external_grid]

    def add_connectivity_node(self, mrid: str):
        """
        Add a connectivity node to the network.
        `mrid` mRID of the ConnectivityNode
        Returns A new ConnectivityNode with `mrid` if it doesn't already exist, otherwise the existing
                 ConnectivityNode represented by `mrid`
        """
        if mrid not in self._connectivity_nodes:
            self._connectivity_nodes[mrid] = ConnectivityNode(mrid=mrid)
            return self._connectivity_nodes[mrid]
        else:
            return self._connectivity_nodes[mrid]

    def _index_measurement(self, measurement: Measurement, mrid: str) -> bool:
        if not mrid:
            return False

        if mrid in self._measurements:
            for meas in self._measurements[mrid]:
                if meas.mrid == measurement.mrid:
                    return False
            else:
                self._measurements[mrid].append(measurement)
                return True
        else:
            self._measurements[mrid] = [measurement]
            return True

    def _remove_measurement_index(self, measurement: Measurement):
        try:
            self._measurements[measurement.terminal_mrid].remove(measurement)
        except KeyError:
            pass
        try:
            self._measurements[measurement.power_system_resource_mrid].remove(measurement)
        except KeyError:
            pass
