#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import abc
from collections import Counter
from dataclasses import dataclass, field
from functools import reduce
from typing import Set, Tuple, FrozenSet, Dict, Callable, Union, TypeVar, Any, List, Generic, Optional, Iterable

from zepben.evolve import BasicTraversal, LifoQueue, Junction, BusbarSection, EquivalentBranch
from zepben.evolve.model.cim.iec61970.base.core.conducting_equipment import ConductingEquipment
from zepben.evolve.model.cim.iec61970.base.core.terminal import Terminal
from zepben.evolve.model.cim.iec61970.base.wires.aclinesegment import AcLineSegment
from zepben.evolve.model.cim.iec61970.base.wires.energy_consumer import EnergyConsumer
from zepben.evolve.model.cim.iec61970.base.wires.energy_source import EnergySource
from zepben.evolve.model.cim.iec61970.base.wires.power_electronics_connection import PowerElectronicsConnection
from zepben.evolve.model.cim.iec61970.base.wires.power_transformer import PowerTransformer, PowerTransformerEnd
from zepben.evolve.model.cim.iec61970.base.wires.switch import Switch
from zepben.evolve.services.network.network_service import NetworkService

__all__ = [
    "BusBranchNetworkCreationValidator",
    "BusBranchNetworkCreator",
    "BusBranchNetworkCreationMappings",
    "BusBranchNetworkCreationResult",
    "TerminalGrouping"
]

BBN = TypeVar('BBN')  # Bus-Branch Network
TN = TypeVar('TN')  # Topological Node
TB = TypeVar('TB')  # Topological Branch
EB = TypeVar('EB')  # Equivalent Branch
PT = TypeVar('PT')  # Power Transformer
ES = TypeVar('ES')  # Energy Source
EC = TypeVar('EC')  # Energy Consumer
PEC = TypeVar('PEC')  # Power Electronics Connection


class BusBranchNetworkCreationValidator(Generic[BBN, TN, TB, EB, PT, ES, EC, PEC], metaclass=abc.ABCMeta):
    """
    Validator used to determine if node-breaker network data is fit for the creation of a bus-branch network.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, "is_valid_network_data") and callable(subclass.is_valid_network_data)
                and hasattr(subclass, "is_valid_topological_node_data") and callable(subclass.is_valid_topological_node_data)
                and hasattr(subclass, "is_valid_topological_branch_data") and callable(subclass.is_valid_topological_branch_data)
                and hasattr(subclass, "is_valid_equivalent_branch_data") and callable(subclass.is_valid_topological_branch_data)
                and hasattr(subclass, "is_valid_power_transformer_data") and callable(subclass.is_valid_power_transformer_data)
                and hasattr(subclass, "is_valid_energy_source_data") and callable(subclass.is_valid_energy_source_data)
                and hasattr(subclass, "is_valid_energy_consumer_data") and callable(subclass.is_valid_energy_consumer_data)
                and hasattr(subclass, "is_valid_power_electronics_connection_data") and callable(subclass.is_valid_power_electronics_connection_data)
                or NotImplemented)

    @abc.abstractmethod
    def is_valid_network_data(self, node_breaker_network: NetworkService) -> bool:
        """
        Validates if provided data is fit for the creation of a bus-branch network.
        NOTE: Refer to class `BusBranchNetworkCreator` for parameter information.

        :return: Whether data is valid or not.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def is_valid_topological_node_data(
        self,
        bus_branch_network: BBN,
        base_voltage: Optional[int],
        collapsed_conducting_equipment: FrozenSet[ConductingEquipment],
        border_terminals: FrozenSet[Terminal],
        inner_terminals: FrozenSet[Terminal],
        node_breaker_network: NetworkService
    ) -> bool:
        """
        Validates if provided data is fit for the creation of a topological node.
        NOTE: Refer to class `BusBranchNetworkCreator` for parameter information.

        :return: Whether data is valid or not.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def is_valid_topological_branch_data(
        self,
        bus_branch_network: BBN,
        connected_topological_nodes: Tuple[TN, TN],
        length: Optional[float],
        collapsed_ac_line_segments: FrozenSet[AcLineSegment],
        border_terminals: FrozenSet[Terminal],
        inner_terminals: FrozenSet[Terminal],
        node_breaker_network: NetworkService
    ) -> bool:
        """
        Validates if provided data is fit for the creation of a topological branch.
        NOTE: Refer to class `BusBranchNetworkCreator` for parameter information.

        :return: Whether data is valid or not.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def is_valid_equivalent_branch_data(
        self,
        bus_branch_network: BBN,
        connected_topological_nodes: List[TN],
        equivalent_branch: EquivalentBranch,
        node_breaker_network: NetworkService
    ) -> bool:
        """
        Validates if provided data is fit for the creation of an equivalent branch.
        NOTE: Refer to class `BusBranchNetworkCreator` for parameter information.

        :return: Whether data is valid or not.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def is_valid_power_transformer_data(
        self,
        bus_branch_network: BBN,
        power_transformer: PowerTransformer,
        ends_to_topological_nodes: List[Tuple[PowerTransformerEnd, Optional[TN]]],
        node_breaker_network: NetworkService
    ) -> bool:
        """
        Validates if provided data is fit for the creation of a power transformer.
        NOTE: Refer to class `BusBranchNetworkCreator` for parameter information.

        :return: Whether data is valid or not.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def is_valid_energy_source_data(
        self,
        bus_branch_network: BBN,
        energy_source: EnergySource,
        connected_topological_node: TN,
        node_breaker_network: NetworkService
    ) -> bool:
        """
        Validates if provided data is fit for the creation of an energy source.
        NOTE: Refer to class `BusBranchNetworkCreator` for parameter information.

        :return: Whether data is valid or not.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def is_valid_energy_consumer_data(
        self,
        bus_branch_network: BBN,
        energy_consumer: EnergyConsumer,
        connected_topological_node: TN,
        node_breaker_network: NetworkService,
    ) -> bool:
        """
        Validates if provided data is fit for the creation of an energy consumer.
        NOTE: Refer to class `BusBranchNetworkCreator` for parameter information.

        :return: Whether data is valid or not.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def is_valid_power_electronics_connection_data(
        self,
        bus_branch_network: BBN,
        power_electronics_connection: PowerElectronicsConnection,
        connected_topological_node: TN,
        node_breaker_network: NetworkService
    ) -> bool:
        """
        Validates if provided data is fit for the creation of a power electronics connection.
        NOTE: Refer to class `BusBranchNetworkCreator` for parameter information.

        :return: Whether data is valid or not.
        """
        raise NotImplementedError


BNV = TypeVar('BNV', bound=BusBranchNetworkCreationValidator)  # Subtype of BusBranchNetworkCreationValidator


class BusBranchNetworkCreator(Generic[BBN, TN, TB, EB, PT, ES, EC, PEC, BNV], metaclass=abc.ABCMeta):
    """Contains the logic needed to generate a target bus-branch network from a source `NetworkService`.

    NOTE: All bus-branch network elements returned from the creators must have a uuid (universally unique identifier). This is needed to prevent collisions
    when generating the mappings object between the source `NetworkService` and the target bus-branch network.

    Generic Types:
        - BBN := Type for the object used to represent the bus-branch network.
        - TN := Type for the object used to represent a topological node in the bus-branch network.
        - TB := Type for the object used to represent a topological branch in the bus-branch network.
        - EB := Type for the object used to represent an equivalent branch in the bus-branch network.
        - PT := Type for the object used to represent a power transformer in the bus-branch network.
        - ES := Type for the object used to represent an energy source in the bus-branch network.
        - EC := Type for the object used to represent an energy consumer in the bus-branch network.
        - PEC := Type for the object used to represent a power electronics connection in the bus-branch network.
        - BNV := Type for the validator instance used in the creation of the bus-branch network.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, "bus_branch_network_creator") and callable(subclass.bus_branch_network_creator)
                and hasattr(subclass, "topological_node_creator") and callable(subclass.topological_node_creator)
                and hasattr(subclass, "topological_branch_creator") and callable(subclass.topological_branch_creator)
                and hasattr(subclass, "equivalent_branch_creator") and callable(subclass.topological_branch_creator)
                and hasattr(subclass, "power_transformer_creator") and callable(subclass.power_transformer_creator)
                and hasattr(subclass, "energy_source_creator") and callable(subclass.energy_source_creator)
                and hasattr(subclass, "energy_consumer_creator") and callable(subclass.energy_consumer_creator)
                and hasattr(subclass, "power_electronics_connection_creator") and callable(subclass.power_electronics_connection_creator)
                and hasattr(subclass, "validator_creator") and callable(subclass.validator_creator)
                or NotImplemented)

    @abc.abstractmethod
    def bus_branch_network_creator(self, node_breaker_network: NetworkService) -> BBN:
        """
        Creates an empty target bus-branch network instance of type BBN.

        :param node_breaker_network: Instance of type `NetworkService` being used as a source node-breaker network.
        :return: Target bus-branch network of type BBN.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def topological_node_creator(
        self,
        bus_branch_network: BBN,
        base_voltage: Optional[int],
        collapsed_conducting_equipment: FrozenSet[ConductingEquipment],
        border_terminals: FrozenSet[Terminal],
        inner_terminals: FrozenSet[Terminal],
        node_breaker_network: NetworkService
    ) -> Tuple[Any, TN]:
        """
        Callback used to create a topological node instance of type TN.

        :param bus_branch_network: Instance of type BBN being used as a target bus-branch network.
        :param base_voltage: Base voltage value to be used for the topological node in Volts.
        :param collapsed_conducting_equipment: Set that contains all instances of `ConductingEquipment` being collapsed in this topological node.
        :param border_terminals: Set that contains all instances of `Terminal` that connect this topological node to other equipment.
        :param inner_terminals: Set that contains all instances of `Terminal` collapsed in this topological node.
        :param node_breaker_network: Instance of type `NetworkService` being used as a source node-breaker network.
        :return: A 2-tuple with the first element being an id for the topological node and the second element being an instance of type TN that represents a
                 topological node in the target bus-branch network. This instance will be passed into the appropriate bus-branch model element creators for
                 the elements that are connected to this topological node.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def topological_branch_creator(
        self,
        bus_branch_network: BBN,
        connected_topological_nodes: Tuple[TN, TN],
        length: Optional[float],
        collapsed_ac_line_segments: FrozenSet[AcLineSegment],
        border_terminals: FrozenSet[Terminal],
        inner_terminals: FrozenSet[Terminal],
        node_breaker_network: NetworkService
    ) -> Tuple[Any, TB]:
        """
        Callback used to create a topological branch instance in target bus-branch network.

        :param bus_branch_network: Instance of type BBN being used as a target bus-branch network.
        :param connected_topological_nodes: Instances of type TN connected to this topological branch sorted by `FeederDirection`.
        :param length: Length of the topological branch in meters.
        :param collapsed_ac_line_segments: Set that contains all instances of `AcLineSegment` being collapsed in this topological branch. e.g. connected lines
               with the same impedance values.
        :param border_terminals: Set that contains all instances of `Terminal` that connect this topological branch to other equipment.
        :param inner_terminals: Set that contains all instances of `Terminal` collapsed in this topological branch.
        :param node_breaker_network: Instance of type `NetworkService` being used as a source node-breaker network.
        :return: A 2-tuple with the first element being an id for the topological branch and the second element being an instance of type TB that represents a
                 topological branch in the target bus-branch network.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def equivalent_branch_creator(
        self,
        bus_branch_network: BBN,
        connected_topological_nodes: List[TN],
        equivalent_branch: EquivalentBranch,
        node_breaker_network: NetworkService
    ) -> Tuple[Any, EB]:
        """
        Callback used to create an equivalent branch instance in target bus-branch network.

        :param bus_branch_network: Instance of type BBN being used as a target bus-branch network.
        :param connected_topological_nodes: Instances of type TN connected to this topological branch sorted by `FeederDirection`.
        :param equivalent_branch: Instance of `EquivalentBranch` used to generate the equivalent branch in target bus-branch network.
        :param node_breaker_network: Instance of type `NetworkService` being used as a source node-breaker network.
        :return: A 2-tuple with the first element being an id for the topological branch and the second element being an instance of type TB that represents a
                 topological branch in the target bus-branch network.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def power_transformer_creator(
        self,
        bus_branch_network: BBN,
        power_transformer: PowerTransformer,
        ends_to_topological_nodes: List[Tuple[PowerTransformerEnd, Optional[TN]]],
        node_breaker_network: NetworkService
    ) -> Dict[Any, PT]:
        """
        Callback used to create a power transformer instance in target bus-branch network.

        :param bus_branch_network: Instance of type BBN being used as a target bus-branch network.
        :param power_transformer: Instance of `PowerTransformer` used to generate power transformer in target bus-branch network.
        :param ends_to_topological_nodes: List holding power transformer ends with the topological nodes they are connected to sorted by `FeederDirection`.
        :param node_breaker_network: Instance of type `NetworkService` being used as a source node-breaker network.
        :return: A dictionary with keys being uuids for the instance/s of type PT that represents a power transformer in the target bus-branch network.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def energy_source_creator(
        self,
        bus_branch_network: BBN,
        energy_source: EnergySource,
        connected_topological_node: TN,
        node_breaker_network: NetworkService
    ) -> Dict[Any, ES]:
        """
        Callback used to create an energy source instance in target bus-branch network.

        :param bus_branch_network: Instance of type BBN being used as a target bus-branch network.
        :param energy_source: Instance of `EnergySource` used to generate energy source in target bus-branch network.
        :param connected_topological_node: Topological node of type TN that is connected to this energy source.
        :param node_breaker_network: Instance of type `NetworkService` being used as a source node-breaker network.
        :return: A dictionary with keys being uuids for the instance/s of type ES that represents an energy source in the target bus-branch network.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def energy_consumer_creator(
        self,
        bus_branch_network: BBN,
        energy_consumer: EnergyConsumer,
        connected_topological_node: TN,
        node_breaker_network: NetworkService,
    ) -> Dict[Any, EC]:
        """
        Callback used to pass all the required values to generate an energy consumer object.

        :param bus_branch_network: Instance of type BBN being used as a target bus-branch network.
        :param energy_consumer: Instance of `EnergyConsumer` used to generate energy consumer in target bus-branch network.
        :param connected_topological_node: Topological node of type TN that is connected to this energy consumer.
        :param node_breaker_network: Instance of type `NetworkService` being used as a source node-breaker network.
        :return: A dictionary with keys being uuids for the instance/s of type EC that represents an energy consumer in the target bus-branch network.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def power_electronics_connection_creator(
        self,
        bus_branch_network: BBN,
        power_electronics_connection: PEC,
        connected_topological_node: TN,
        node_breaker_network: NetworkService
    ) -> Dict[Any, PEC]:
        """
        Callback used to pass all the required values to generate a power electronics connection object.

        :param bus_branch_network: Instance of type BBN being used as a target bus-branch network.
        :param power_electronics_connection: Instance of `PowerElectronicsConnection` used to generate power electronics connection in target bus-branch
               network.
        :param connected_topological_node: Topological node of type TN that is connected to this power electronics connection.
        :param node_breaker_network: Instance of type `NetworkService` being used as a source node-breaker network.
        :return: A dictionary with keys being uuids for the instance/s of type PEC that represents a power electronics connection in the target bus-branch
                 network.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def validator_creator(self) -> BNV:
        """
        Callback used to create 'BusBranchNetworkCreationValidator' instance used for validation while creating a bus-branch
        network.

        :return: Instance of type 'BusBranchNetworkCreationValidator'.
        """
        raise NotImplementedError

    # noinspection PyMethodMayBeStatic
    def has_negligible_impedance(self, ce: ConductingEquipment) -> bool:
        """
        Callback used to evaluate if an instance of `ConductingEquipment` has negligible impedance.

        :param ce: `ConductingEquipment` instance whose impedance is being evaluated.
        :return: True if 'ce' has negligible impedance, False otherwise.
        """
        if isinstance(ce, AcLineSegment):
            return ce.length == 0
        if isinstance(ce, Switch):
            return not ce.is_open()
        if isinstance(ce, Junction) or isinstance(ce, BusbarSection):
            return True
        if isinstance(ce, EquivalentBranch):
            return _is_no_impedance_branch(ce)
        return False

    async def create(self, node_breaker_network: NetworkService) -> 'BusBranchNetworkCreationResult[BBN, BNV]':
        return await _create_bus_branch_network(self, node_breaker_network)


CE = TypeVar("CE", bound=ConductingEquipment)


@dataclass()
class TerminalGrouping(Generic[CE]):
    border_terminals: Set[Terminal] = field(default_factory=set)
    inner_terminals: Set[Terminal] = field(default_factory=set)
    conducting_equipment_group: Set[CE] = field(default_factory=set)

    def terminals(self) -> Set[Terminal]:
        return {*self.border_terminals, *self.inner_terminals}


class BusBranchToNodeBreakerMappings:

    def __init__(self):
        self.topological_nodes: Dict[Any, TerminalGrouping[ConductingEquipment]] = {}
        self.topological_branches: Dict[Any, TerminalGrouping[AcLineSegment]] = {}
        self.equivalent_branches: Dict[Any, Set[EquivalentBranch]] = {}
        self.power_transformers: Dict[Any, Set[PowerTransformer]] = {}
        self.energy_sources: Dict[Any, Set[EnergySource]] = {}
        self.energy_consumers: Dict[Any, Set[EnergyConsumer]] = {}
        self.power_electronics_connections: Dict[Any, Set[PowerElectronicsConnection]] = {}


class NodeBreakerToBusBranchMappings:

    def __init__(self):
        self.objects: Dict[str, Set[Any]] = {}


class BusBranchNetworkCreationMappings:
    """
    Holds mappings between a bus-branch network (bbn) and a node-breaker network (nbn) of type `NetworkService`.
    """

    def __init__(self):
        self.to_nbn = BusBranchToNodeBreakerMappings()
        self.to_bbn = NodeBreakerToBusBranchMappings()


def _add_to_mapping(mapping: Dict[Any, Set[Any]], uuid: Any, obj_to_add: Any) -> None:
    if uuid not in mapping:
        mapping[uuid] = set()
    mapping[uuid].add(obj_to_add)


class BusBranchNetworkCreationResult(Generic[BBN, BNV]):
    """
    Represents the results of creating a bus-branch network from a node-breaker network.
    """

    def __init__(self, validator: BNV):
        self.validator: BNV = validator
        self.mappings: BusBranchNetworkCreationMappings = BusBranchNetworkCreationMappings()
        self.network: BBN = None
        self.was_successful: bool = False


async def _create_bus_branch_network(
    bus_branch_network_creator: BusBranchNetworkCreator[BBN, TN, TB, EB, PT, ES, EC, PEC, BNV],
    node_breaker_network: NetworkService
) -> BusBranchNetworkCreationResult[BBN, BNV]:
    """
    Creates bus-branch network.

    :param bus_branch_network_creator: Instance of type `BusBranchNetworkCreator` used to generate the target bus-branch network.
    :param node_breaker_network: Instance of type `NetworkService` being used as a source node-breaker network.
    :return: `CreationResult`
    """
    _validate_number_of_terminals(node_breaker_network)
    validator = bus_branch_network_creator.validator_creator()

    result: BusBranchNetworkCreationResult[BBN, BNV] = BusBranchNetworkCreationResult(validator)

    if not validator.is_valid_network_data(node_breaker_network):
        return result

    bus_branch_network = bus_branch_network_creator.bus_branch_network_creator(node_breaker_network)

    terminals_to_tns = {}
    # create topological branches
    tbs_creation_success = await _create_topological_branches(node_breaker_network, bus_branch_network,
                                                              bus_branch_network_creator, result,
                                                              terminals_to_tns, validator)
    if not tbs_creation_success:
        return result

    # create equivalent branches
    ebs_creation_success = await _create_equivalent_branches(node_breaker_network, bus_branch_network,
                                                             bus_branch_network_creator, result,
                                                             terminals_to_tns, validator)
    if not ebs_creation_success:
        return result

    # create power transformers
    pt_creation_success = await _create_power_transformers(node_breaker_network, bus_branch_network,
                                                           bus_branch_network_creator, result,
                                                           terminals_to_tns, validator)
    if not pt_creation_success:
        return result

    # create energy sources
    es_creation_success = await _create_energy_sources(node_breaker_network, bus_branch_network,
                                                       bus_branch_network_creator,
                                                       result, terminals_to_tns, validator)
    if not es_creation_success:
        return result

    # create energy consumers
    ec_creation_success = await _create_energy_consumers(node_breaker_network, bus_branch_network,
                                                         bus_branch_network_creator,
                                                         result, terminals_to_tns, validator)
    if not ec_creation_success:
        return result

    # create power electronics connections
    pec_creation_success = await _create_power_electronics_connections(node_breaker_network, bus_branch_network,
                                                                       bus_branch_network_creator,
                                                                       result, terminals_to_tns, validator)
    if not pec_creation_success:
        return result

    result.network = bus_branch_network
    result.was_successful = True
    return result


async def _get_or_create_topological_node(
    terminal: Terminal,
    terminals_to_tns: Dict[str, TN],
    node_breaker_network: NetworkService,
    bus_branch_network: BBN,
    bus_branch_network_creator: BusBranchNetworkCreator[BBN, TN, TB, EB, PT, ES, EC, PEC, BNV],
    result: BusBranchNetworkCreationResult[BBN, BNV],
    validator: BNV
) -> (bool, TN):
    cached_tn = terminals_to_tns.get(terminal.mrid)
    if cached_tn is not None:
        return True, cached_tn

    # group terminals connected by negligible impedance equipment
    terminals_grouping = await _group_negligible_impedance_terminals(terminal,
                                                                     bus_branch_network_creator.has_negligible_impedance)
    negligible_impedance_equipment = frozenset(terminals_grouping.conducting_equipment_group)
    inner_terms = frozenset(terminals_grouping.inner_terminals)
    border_terms = frozenset(terminals_grouping.border_terminals)

    rated_u = _get_base_voltage(border_terms)

    # create topological node
    if not validator.is_valid_topological_node_data(bus_branch_network,
                                                    rated_u,
                                                    negligible_impedance_equipment,
                                                    border_terms,
                                                    inner_terms,
                                                    node_breaker_network):
        return False, None

    tn_id, tn = bus_branch_network_creator.topological_node_creator(
        bus_branch_network,
        rated_u,
        negligible_impedance_equipment,
        border_terms,
        inner_terms,
        node_breaker_network
    )

    # populate result mappings
    result.mappings.to_nbn.topological_nodes[tn_id] = terminals_grouping

    for t in terminals_grouping.terminals():
        _add_to_mapping(result.mappings.to_bbn.objects, t.mrid, tn)
        if t.connectivity_node is not None:
            _add_to_mapping(result.mappings.to_bbn.objects, t.connectivity_node.mrid, tn)

    for ce in terminals_grouping.conducting_equipment_group:
        _add_to_mapping(result.mappings.to_bbn.objects, ce.mrid, tn)

    # map terminals to associated topological nodes for easy lookup when creating connected equipment
    for t in border_terms:
        terminals_to_tns[t.mrid] = tn
    for t in inner_terms:
        terminals_to_tns[t.mrid] = tn

    return True, tn


async def _create_topological_branches(
    node_breaker_network: NetworkService,
    bus_branch_network: BBN,
    bus_branch_network_creator: BusBranchNetworkCreator[BBN, TN, TB, EB, PT, ES, EC, PEC, BNV],
    result: BusBranchNetworkCreationResult[BBN, BNV],
    terminals_to_tns: Dict[str, TN],
    validator: BNV
) -> bool:
    processed_acls_ids = set()
    for acls in node_breaker_network.objects(AcLineSegment):
        if not (acls.mrid in processed_acls_ids or bus_branch_network_creator.has_negligible_impedance(acls)):
            lines_grouping = await _group_common_ac_line_segment_terminals(acls)
            border_terms = frozenset(lines_grouping.border_terminals)
            common_acls = frozenset(lines_grouping.conducting_equipment_group)
            inner_terms = frozenset(lines_grouping.inner_terminals)

            # get/create connected topological nodes
            acls_tns = []
            for t in _sort_terminals_by_feeder_direction(border_terms):
                tn_creation_success, tn = await _get_or_create_topological_node(t, terminals_to_tns,
                                                                                node_breaker_network,
                                                                                bus_branch_network,
                                                                                bus_branch_network_creator,
                                                                                result, validator)
                if not tn_creation_success:
                    return False
                acls_tns.append(tn)

            total_length = reduce(lambda s, l: l.length + s, (common_acl for common_acl in common_acls), 0.0)

            # create topological branch
            if not validator.is_valid_topological_branch_data(bus_branch_network,
                                                              (acls_tns[0], acls_tns[1]),
                                                              total_length,
                                                              common_acls,
                                                              border_terms,
                                                              inner_terms,
                                                              node_breaker_network):
                return False

            tb_id, tb = bus_branch_network_creator.topological_branch_creator(
                bus_branch_network,
                (acls_tns[0], acls_tns[1]),
                total_length,
                common_acls,
                border_terms,
                inner_terms,
                node_breaker_network
            )

            # populate result mappings
            result.mappings.to_nbn.topological_branches[tb_id] = lines_grouping

            for line in lines_grouping.conducting_equipment_group:
                _add_to_mapping(result.mappings.to_bbn.objects, line.mrid, tb)

            for t in lines_grouping.inner_terminals:
                _add_to_mapping(result.mappings.to_bbn.objects, t.mrid, tb)

                if t.connectivity_node is not None:
                    _add_to_mapping(result.mappings.to_bbn.objects, t.connectivity_node.mrid, tb)

            # flag processed ac-line-segments
            processed_acls_ids.update({acls.mrid for acls in common_acls})
    return True


async def _create_equivalent_branches(
    node_breaker_network: NetworkService,
    bus_branch_network: BBN,
    bus_branch_network_creator: BusBranchNetworkCreator[BBN, TN, TB, EB, PT, ES, EC, PEC, BNV],
    result: BusBranchNetworkCreationResult[BBN, BNV],
    terminals_to_tns: Dict[str, TN],
    validator: BNV
) -> bool:
    for eb in node_breaker_network.objects(EquivalentBranch):
        if eb.mrid in result.mappings.to_bbn.objects:
            # skip if already processed
            continue

        # get/create connected topological nodes
        eb_tns = []
        for t in _sort_terminals_by_feeder_direction(eb.terminals):
            tn_creation_success, tn = await _get_or_create_topological_node(t, terminals_to_tns,
                                                                            node_breaker_network,
                                                                            bus_branch_network,
                                                                            bus_branch_network_creator,
                                                                            result, validator)
            if not tn_creation_success:
                return False
            eb_tns.append(tn)

        if bus_branch_network_creator.has_negligible_impedance(eb):
            continue

        # create equivalent branch
        if not validator.is_valid_equivalent_branch_data(bus_branch_network, eb_tns, eb, node_breaker_network):
            return False

        teb_id, teb = bus_branch_network_creator.equivalent_branch_creator(bus_branch_network, eb_tns, eb, node_breaker_network)

        # populate result mappings
        _add_to_mapping(result.mappings.to_nbn.equivalent_branches, teb_id, eb)
        _add_to_mapping(result.mappings.to_bbn.objects, eb.mrid, teb)

    return True


async def _create_power_transformers(
    node_breaker_network: NetworkService,
    bus_branch_network: BBN,
    bus_branch_network_creator: BusBranchNetworkCreator[BBN, TN, TB, EB, PT, ES, EC, PEC, BNV],
    result: BusBranchNetworkCreationResult[BBN, BNV],
    terminals_to_tns: Dict[str, TN],
    validator: BNV
) -> bool:
    for pt in node_breaker_network.objects(PowerTransformer):
        # create list of ends with their connected topological nodes
        ends_to_topological_nodes = []
        for end in _sort_ends_by_feeder_direction(pt.ends):
            if end.terminal is not None:
                tn_creation_success, tn = await _get_or_create_topological_node(end.terminal, terminals_to_tns,
                                                                                node_breaker_network,
                                                                                bus_branch_network,
                                                                                bus_branch_network_creator, result,
                                                                                validator)
                if not tn_creation_success:
                    return False
                ends_to_topological_nodes.append((end, tn))
            else:
                ends_to_topological_nodes.append((end, None))

        # create power transformer
        if not validator.is_valid_power_transformer_data(bus_branch_network, pt, ends_to_topological_nodes,
                                                         node_breaker_network):
            return False

        txs = bus_branch_network_creator.power_transformer_creator(bus_branch_network, pt, ends_to_topological_nodes,
                                                                   node_breaker_network)

        # populate result mappings
        for tx_id, tx in txs.items():
            _add_to_mapping(result.mappings.to_nbn.power_transformers, tx_id, pt)
            _add_to_mapping(result.mappings.to_bbn.objects, pt.mrid, tx)

    return True


async def _create_energy_sources(
    node_breaker_network: NetworkService,
    bus_branch_network: BBN,
    bus_branch_network_creator: BusBranchNetworkCreator[BBN, TN, TB, EB, PT, ES, EC, PEC, BNV],
    result: BusBranchNetworkCreationResult[BBN, BNV],
    terminals_to_tns: Dict[str, TN],
    validator: BNV
) -> bool:
    for es in node_breaker_network.objects(EnergySource):
        es_terminal = next((t for t in es.terminals))
        tn_creation_success, tn = await _get_or_create_topological_node(es_terminal, terminals_to_tns,
                                                                        node_breaker_network,
                                                                        bus_branch_network, bus_branch_network_creator,
                                                                        result, validator)
        if not tn_creation_success:
            return False

        if not validator.is_valid_energy_source_data(bus_branch_network, es, tn, node_breaker_network):
            return False

        bb_ess = bus_branch_network_creator.energy_source_creator(bus_branch_network, es, tn, node_breaker_network)

        # populate result mappings
        for bb_es_id, bb_es in bb_ess.items():
            _add_to_mapping(result.mappings.to_nbn.energy_sources, bb_es_id, es)
            _add_to_mapping(result.mappings.to_bbn.objects, es.mrid, bb_es)

    return True


async def _create_energy_consumers(
    node_breaker_network: NetworkService,
    bus_branch_network: BBN,
    bus_branch_network_creator: BusBranchNetworkCreator[BBN, TN, TB, EB, PT, ES, EC, PEC, BNV],
    result: BusBranchNetworkCreationResult[BBN, BNV],
    terminals_to_tns: Dict[str, TN],
    validator: BNV
):
    for ec in node_breaker_network.objects(EnergyConsumer):
        ec_terminal = next((t for t in ec.terminals))
        tn_creation_success, tn = await _get_or_create_topological_node(ec_terminal, terminals_to_tns,
                                                                        node_breaker_network,
                                                                        bus_branch_network, bus_branch_network_creator,
                                                                        result, validator)
        if not tn_creation_success:
            return False

        if not validator.is_valid_energy_consumer_data(bus_branch_network, ec, tn, node_breaker_network):
            return False

        bb_ecs = bus_branch_network_creator.energy_consumer_creator(bus_branch_network, ec, tn,
                                                                    node_breaker_network)

        # populate result mappings
        for bb_ec_id, bb_ec in bb_ecs.items():
            _add_to_mapping(result.mappings.to_nbn.energy_consumers, bb_ec_id, ec)
            _add_to_mapping(result.mappings.to_bbn.objects, ec.mrid, bb_ec)

    return True


async def _create_power_electronics_connections(
    node_breaker_network: NetworkService,
    bus_branch_network: BBN,
    bus_branch_network_creator: BusBranchNetworkCreator[BBN, TN, TB, EB, PT, ES, EC, PEC, BNV],
    result: BusBranchNetworkCreationResult[BBN, BNV],
    terminals_to_tns: Dict[str, TN],
    validator: BNV
):
    for pec in node_breaker_network.objects(PowerElectronicsConnection):
        pec_terminal = next((t for t in pec.terminals))
        tn_creation_success, tn = await _get_or_create_topological_node(pec_terminal, terminals_to_tns,
                                                                        node_breaker_network,
                                                                        bus_branch_network, bus_branch_network_creator,
                                                                        result, validator)
        if not tn_creation_success:
            return False

        if not validator.is_valid_power_electronics_connection_data(bus_branch_network, pec, tn, node_breaker_network):
            return False

        bb_pecs = bus_branch_network_creator.power_electronics_connection_creator(bus_branch_network, pec, tn,
                                                                                  node_breaker_network)

        # populate result mappings
        for bb_pec_id, bb_pec in bb_pecs.items():
            _add_to_mapping(result.mappings.to_nbn.power_electronics_connections, bb_pec_id, pec)
            _add_to_mapping(result.mappings.to_bbn.objects, pec.mrid, bb_pec)

    return True


def _get_base_voltage(border_terminals: FrozenSet[Terminal]) -> Union[int, None]:
    voltages = set()
    for t in border_terminals:
        ce = t.conducting_equipment
        # Open switches may have a different voltage rating from the negligible-impedance equipment group due to the equipment on the other side of it.
        if isinstance(ce, Switch):
            continue
        if isinstance(ce, PowerTransformer):
            end_voltage = next((e.rated_u for e in ce.ends if e.terminal is t), None)
            if end_voltage is not None:
                voltages.add(end_voltage)
        else:
            if ce.base_voltage is not None:
                voltages.add(ce.base_voltage.nominal_voltage)
    return next(iter(voltages), None)


def _validate_number_of_terminals(network: NetworkService):
    illegal_acls = []
    for acl in network.objects(AcLineSegment):
        if acl.num_terminals() != 2:
            illegal_acls.append(acl.mrid)

    if len(illegal_acls) != 0:
        raise ValueError(
            f"NetworkService contains the following AcLineSegments with an invalid number of terminals: {illegal_acls}")

    illegal_es = []
    for es in network.objects(EnergySource):
        if es.num_terminals() != 1:
            illegal_es.append(es.mrid)

    if len(illegal_es) != 0:
        raise ValueError(
            f"NetworkService contains the following EnergySources with an invalid number of terminals: {illegal_es}")

    illegal_ec = []
    for ec in network.objects(EnergyConsumer):
        if ec.num_terminals() != 1:
            illegal_ec.append(ec.mrid)

    if len(illegal_ec) != 0:
        raise ValueError(
            f"NetworkService contains the following EnergyConsumers with an invalid number of terminals: {illegal_ec}")

    illegal_pec = []
    for pec in network.objects(PowerElectronicsConnection):
        if pec.num_terminals() != 1:
            illegal_pec.append(pec.mrid)

    if len(illegal_pec) != 0:
        raise ValueError(
            f"NetworkService contains the following PowerElectronicsConnections with an invalid number of terminals: {illegal_pec}")


async def _group_negligible_impedance_terminals(
    terminal: Terminal,
    has_negligible_impedance: Callable[[ConductingEquipment], bool]
) -> TerminalGrouping[ConductingEquipment]:
    tg = TerminalGrouping[ConductingEquipment]()
    # noinspection PyArgumentList
    trace = BasicTraversal(
        start_item=terminal,
        queue_next=_queue_terminals_across_negligible_impedance(has_negligible_impedance),
        step_actions=[_process_terminal(tg, has_negligible_impedance)]
    )
    await trace.run()
    return tg


def _process_terminal(
    tg: TerminalGrouping[ConductingEquipment],
    has_negligible_impedance: Callable[[ConductingEquipment], bool]
):
    async def add_to_group(t: Terminal, _):
        if has_negligible_impedance(t.conducting_equipment):
            tg.conducting_equipment_group.add(t.conducting_equipment)
            tg.inner_terminals.add(t)
        else:
            tg.border_terminals.add(t)

    return add_to_group


def _queue_terminals_across_negligible_impedance(
    has_negligible_impedance: Callable[[ConductingEquipment], bool]
):
    def queue_next(terminal: Terminal, traversal: BasicTraversal[Terminal]):
        if terminal.connectivity_node is not None:
            traversal.process_queue.extend(ot for ot in terminal.connectivity_node.terminals if ot != terminal)

        if has_negligible_impedance(terminal.conducting_equipment):
            traversal.process_queue.extend(ot for ot in terminal.conducting_equipment.terminals if ot != terminal)

    return queue_next


async def _group_common_ac_line_segment_terminals(acls: AcLineSegment) -> TerminalGrouping[AcLineSegment]:
    def has_common_impedance(line: AcLineSegment):
        return line.per_length_sequence_impedance.mrid == acls.per_length_sequence_impedance.mrid

    common_acls: TerminalGrouping[AcLineSegment] = TerminalGrouping()
    connectivity_node_counter = Counter()

    # noinspection PyArgumentList
    trace = BasicTraversal(
        start_item=acls,
        queue_next=_queue_common_impedance_lines(common_acls, has_common_impedance),
        step_actions=[_process_acls(common_acls, connectivity_node_counter)]
    )
    await trace.run()

    for t in (t for line in common_acls.conducting_equipment_group for t in line.terminals):
        if t.connectivity_node is None:
            common_acls.border_terminals.add(t)
            continue

        count = connectivity_node_counter.get(t.connectivity_node, 0)
        if count == 1:
            common_acls.border_terminals.add(t)
        else:
            common_acls.inner_terminals.add(t)

    return common_acls


def _process_acls(
    common_acls: TerminalGrouping[AcLineSegment],
    connectivity_node_counter: Counter
):
    async def add_to_group(acls: AcLineSegment, _):
        if acls in common_acls.conducting_equipment_group:
            return

        common_acls.conducting_equipment_group.add(acls)
        connectivity_node_counter.update(
            (t.connectivity_node for t in acls.terminals if t.connectivity_node is not None))

    return add_to_group


def _queue_common_impedance_lines(
    common_acls: TerminalGrouping[AcLineSegment],
    has_common_impedance: Callable[[AcLineSegment], bool]
):
    def queue_next(acls: AcLineSegment, traversal: BasicTraversal[AcLineSegment]):
        traversal.process_queue.extend(_next_common_acls(acls, has_common_impedance, common_acls))

    return queue_next


def _next_common_acls(
    acls: AcLineSegment,
    has_common_impedance: Callable[[AcLineSegment], bool],
    common_acls: TerminalGrouping[AcLineSegment]
) -> Set[AcLineSegment]:
    acls_terminals = {*acls.terminals}

    def can_process_ac_line(o: Terminal) -> bool:
        return o not in acls_terminals \
               and isinstance(o.conducting_equipment, AcLineSegment) \
               and has_common_impedance(o.conducting_equipment) \
               and o.conducting_equipment not in common_acls.conducting_equipment_group

    def is_non_forking_ac_line(t: Terminal) -> bool:
        return t.connectivity_node is not None and len(list(t.connectivity_node.terminals)) == 2

    return {
        o.conducting_equipment
        for t in acls.terminals if is_non_forking_ac_line(t)
        for o in t.connectivity_node.terminals if can_process_ac_line(o)
    }


def _is_no_impedance_branch(eb: EquivalentBranch):
    return eb.r is None or eb.x is None or eb.r == 0.0 or eb.x == 0.0


def _sort_ends_by_feeder_direction(ends: Iterable[PowerTransformerEnd]) -> List[PowerTransformerEnd]:
    return sorted(iter(ends), key=lambda pte: 999 if pte.terminal is None else pte.terminal.normal_feeder_direction.value)


def _sort_terminals_by_feeder_direction(terminals: Iterable[Terminal]) -> List[Terminal]:
    return sorted(iter(terminals), key=lambda ter: ter.normal_feeder_direction.value)
