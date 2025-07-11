#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from logging import Logger
from typing import Optional, Callable, List, Union, Type, TypeVar, Protocol

from zepben.ewb import (ConductingEquipment, NetworkService, PhaseCode, EnergySource, AcLineSegment, Breaker, Terminal, LvFeeder,
                        PowerTransformer, EnergyConsumer, PowerElectronicsConnection, Clamp, Cut)
from zepben.ewb.model.cim.extensions.iec61970.base.core.site import Site
from zepben.ewb.model.cim.iec61970.base.core.feeder import Feeder
from zepben.ewb.model.cim.iec61970.base.wires.busbar_section import BusbarSection
from zepben.ewb.model.cim.iec61970.base.wires.junction import Junction
from zepben.ewb.model.cim.iec61970.base.wires.power_transformer_end import PowerTransformerEnd
from zepben.ewb.services.network.tracing.networktrace.operators.network_state_operators import NetworkStateOperators
from zepben.ewb.services.network.tracing.networktrace.tracing import Tracing

SubclassesConductingEquipment = TypeVar('SubclassesConductingEquipment', bound=ConductingEquipment)


def null_action(_):
    """
    An action that does nothing.

    :param _: Any item that will be ignored
    """


class OtherCreator(Protocol):
    """Type hint class"""

    def __call__(self, mrid: str, *args, **kwargs) -> ConductingEquipment: ...


class TestNetworkBuilder:
    """
    A class for building simple test networks, often used for unit testing.
    """

    __test__ = False

    def __init__(self):
        self.network: NetworkService = NetworkService()
        """
        The network where objects are created for this `TestNetworkBuilder`. You should not be readily required to access the network via this property,
        but should instead access it via `build` to ensure the correct tracing is applied before use.
        """

        self._count = 0
        self._current: Optional[ConductingEquipment] = None
        self._current_terminal: Optional[int] = None

    def from_source(
        self,
        nominal_phases: PhaseCode = PhaseCode.ABC,
        mrid: Optional[str] = None,
        action: Callable[[EnergySource], None] = null_action
    ) -> 'TestNetworkBuilder':
        """
        Start a new network island from an `EnergySource`, updating the network pointer to the new `EnergySource`.

        :param nominal_phases: The `PhaseCode` for the new `EnergySource`, used as both the nominal and energising phases. Must be a subset of `PhaseCode.ABCN`.
        :param mrid: Optional mRID for the new source.
        :param action: An action that accepts the new `EnergySource` to allow for additional initialisation.

        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        it = self._create_external_source(mrid, nominal_phases)
        action(it)
        self._current = it
        return self

    def to_source(
        self,
        nominal_phases: PhaseCode = PhaseCode.ABC,
        mrid: Optional[str] = None,
        connectivity_node_mrid: Optional[str] = None,
        action: Callable[[EnergySource], None] = null_action
    ) -> 'TestNetworkBuilder':
        """
        Add a new `EnergySource` to the network and connect it to the current network pointer, updating the network pointer to the new `EnergySource`.

        :param nominal_phases: The `PhaseCode` for the new `EnergySource`, used as both the nominal and energising phases. Must be a subset of `PhaseCode.ABCN`.
        :param mrid: Optional mRID for the new source.
        :param connectivity_node_mrid: Optional id of the connectivity node used to connect this `EnergySource` to the previous item. Will only be used if the
         previous item is not already connected.
        :param action: An action that accepts the new `EnergySource` to allow for additional initialisation.

        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        it = self._create_external_source(mrid, nominal_phases)
        self._connect(self._current, it, connectivity_node_mrid)
        action(it)
        self._current = it
        return self

    def from_acls(
        self,
        nominal_phases: PhaseCode = PhaseCode.ABC,
        mrid: Optional[str] = None,
        action: Callable[[AcLineSegment], None] = null_action
    ) -> 'TestNetworkBuilder':
        """
        Start a new network island from an `AcLineSegment`, updating the network pointer to the new `AcLineSegment`.

        :param nominal_phases: The nominal phases for the new `AcLineSegment`.
        :param mrid: Optional mRID for the new `AcLineSegment`.
        :param action: An action that accepts the new `AcLineSegment` to allow for additional initialisation.

        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        it = self._create_acls(mrid, nominal_phases)
        action(it)
        self._current = it
        return self

    def to_acls(
        self,
        nominal_phases: PhaseCode = PhaseCode.ABC,
        mrid: Optional[str] = None,
        connectivity_node_mrid: Optional[str] = None,
        action: Callable[[AcLineSegment], None] = null_action
    ) -> 'TestNetworkBuilder':
        """
        Add a new `AcLineSegment` to the network and connect it to the current network pointer, updating the network pointer to the new `AcLineSegment`.

        :param nominal_phases: The nominal phases for the new `AcLineSegment`.
        :param mrid: Optional mRID for the new `AcLineSegment`.
        :param connectivity_node_mrid: Optional id of the connectivity node used to connect this `AcLineSegment` to the previous item. Will only be used if the
         previous item is not already connected.
        :param action: An action that accepts the new `AcLineSegment` to allow for additional initialisation.

        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        acls = self._create_acls(mrid, nominal_phases)
        self._connect(self._current, acls, connectivity_node_mrid)
        action(acls)
        self._current = acls
        return self

    def from_breaker(
        self,
        nominal_phases: PhaseCode = PhaseCode.ABC,
        is_normally_open: bool = False,
        is_open: Optional[bool] = None,
        mrid: Optional[str] = None,
        action: Callable[[Breaker], None] = null_action
    ) -> 'TestNetworkBuilder':
        """
        Start a new network island from a `Breaker`, updating the network pointer to the new `Breaker`.

        :param nominal_phases: The nominal phases for the new `Breaker`.
        :param is_normally_open: The normal state of the switch. Defaults to False.
        :param is_open: The current state of the switch. Defaults to `is_normally_open`.
        :param mrid: Optional mRID for the new `Breaker`.
        :param action: An action that accepts the new `Breaker` to allow for additional initialisation.

        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        it = self._create_breaker(mrid, nominal_phases, is_normally_open=is_normally_open, is_open=is_open if is_open is not None else is_normally_open)
        action(it)
        self._current = it
        return self

    def to_breaker(
        self,
        nominal_phases: PhaseCode = PhaseCode.ABC,
        is_normally_open: bool = False,
        is_open: Optional[bool] = None,
        mrid: Optional[str] = None,
        connectivity_node_mrid: Optional[str] = None,
        action: Callable[[Breaker], None] = null_action
    ) -> 'TestNetworkBuilder':
        """
        Add a new `Breaker` to the network and connect it to the current network pointer, updating the network pointer to the new `Breaker`.

        :param nominal_phases: The nominal phases for the new `Breaker`.
        :param is_normally_open: The normal state of the switch. Defaults to False.
        :param is_open: The current state of the switch. Defaults to `is_normally_open`.
        :param mrid: Optional mRID for the new `Breaker`.
        :param connectivity_node_mrid: Optional id of the connectivity node used to connect this `Breaker` to the previous item. Will only be used if the
         previous item is not already connected.
        :param action: An action that accepts the new `Breaker` to allow for additional initialisation.

        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        it = self._create_breaker(mrid, nominal_phases, is_normally_open=is_normally_open, is_open=is_open if is_open is not None else is_normally_open)
        self._connect(self._current, it, connectivity_node_mrid)
        action(it)
        self._current = it
        return self

    def from_junction(
        self,
        nominal_phases: PhaseCode = PhaseCode.ABC,
        num_terminals: Optional[int] = None,
        mrid: Optional[str] = None,
        action: Callable[[Junction], None] = null_action
    ) -> 'TestNetworkBuilder':
        """
        Start a new network island from a `Junction`, updating the network pointer to the new `Junction`.

        :param nominal_phases: The nominal phases for the new `Junction`.
        :param num_terminals: The number of terminals to create on the new `Junction`. Defaults to 2.
        :param mrid: Optional mRID for the new `Junction`.
        :param action: An action that accepts the new `Junction` to allow for additional initialisation.

        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        it = self._create_junction(mrid, nominal_phases, num_terminals)
        action(it)
        self._current = it
        return self

    def to_junction(
        self,
        nominal_phases: PhaseCode = PhaseCode.ABC,
        num_terminals: Optional[int] = None,
        mrid: Optional[str] = None,
        connectivity_node_mrid: Optional[str] = None,
        action: Callable[[Junction], None] = null_action
    ) -> 'TestNetworkBuilder':
        """
        Add a new `Junction` to the network and connect it to the current network pointer, updating the network pointer to the new `Junction`.

        :param nominal_phases: The nominal phases for the new `Junction`.
        :param num_terminals: The number of terminals to create on the new `Junction`. Defaults to 2.
        :param mrid: Optional mRID for the new `Junction`.
        :param connectivity_node_mrid: Optional id of the connectivity node used to connect this `Junction` to the previous item. Will only be used if the
         previous item is not already connected.
        :param action: An action that accepts the new `Junction` to allow for additional initialisation.

        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        it = self._create_junction(mrid, nominal_phases, num_terminals)
        self._connect(self._current, it, connectivity_node_mrid)
        action(it)
        self._current = it
        return self

    def to_power_electronics_connection(
        self,
        nominal_phases: PhaseCode = PhaseCode.ABC,
        num_terminals: Optional[int] = None,
        mrid: Optional[str] = None,
        connectivity_node_mrid: Optional[str] = None,
        action: Callable[[PowerElectronicsConnection], None] = null_action
    ) -> 'TestNetworkBuilder':
        """
        Add a new `PowerElectronicsConnection` to the network and connect it to the current network pointer, updating the network pointer to the new
        `PowerElectronicsConnection`.

        :param nominal_phases: The nominal phases for the new `PowerElectronicsConnection`.
        :param num_terminals: The number of terminals to create on the new `PowerElectronicsConnection`. Defaults to 2.
        :param mrid: Optional mRID for the new `PowerElectronicsConnection`.
        :param connectivity_node_mrid: Optional id of the connectivity node used to connect this `PowerElectronicsConnection` to the previous item. Will only be
         used if the previous item is not already connected.
        :param action: An action that accepts the new `PowerElectronicsConnection` to allow for additional initialisation.

        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        it = self._create_power_electronics_connection(mrid, nominal_phases, num_terminals)
        self._connect(self._current, it, connectivity_node_mrid)
        action(it)
        self._current = it
        return self

    def from_power_transformer(
        self,
        nominal_phases: Optional[List[PhaseCode]] = None,
        end_actions: Optional[List[Callable[[PowerTransformerEnd], None]]] = None,
        mrid: Optional[str] = None,
        action: Callable[[PowerTransformer], None] = null_action
    ) -> 'TestNetworkBuilder':
        """
        Start a new network island from a `PowerTransformer`, updating the network pointer to the new `PowerTransformer`.

        :param nominal_phases: The nominal phases for each end of the new `PowerTransformer`. Defaults to two `PhaseCode.ABC` ends.
        :param end_actions: Actions that accepts the new `PowerTransformerEnd` to allow for additional initialisation.
        :param action: An action that accepts the new `PowerTransformer` to allow for additional initialisation.
        :param mrid: Optional mRID for the new `PowerTransformer`.
        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        it = self._create_power_transformer(mrid, nominal_phases or [PhaseCode.ABC, PhaseCode.ABC])
        if end_actions:
            for i in range(0, it.num_ends()):
                end_actions[i](it.get_end_by_num(i + 1))

        action(it)
        self._current = it
        return self

    def to_power_transformer(
        self,
        nominal_phases: Optional[List[PhaseCode]] = None,
        end_actions: Optional[List[Callable[[PowerTransformerEnd], None]]] = None,
        mrid: Optional[str] = None,
        connectivity_node_mrid: Optional[str] = None,
        action: Callable[[PowerTransformer], None] = null_action
    ) -> 'TestNetworkBuilder':
        """
        Add a new `PowerTransformer` to the network and connect it to the current network pointer, updating the network pointer to the new `PowerTransformer`.

        :param nominal_phases: The nominal phases for each end of the new `PowerTransformer`. Defaults to two `PhaseCode.ABC` ends.
        :param end_actions: Actions that accepts the new `PowerTransformerEnd` to allow for additional initialisation.
        :param action: An action that accepts the new `PowerTransformer` to allow for additional initialisation.
        :param mrid: Optional mRID for the new `PowerTransformer`.
        :param connectivity_node_mrid: Optional id of the connectivity node used to connect this `PowerTransformer` to the previous item. Will only be used if
         the previous item is not already connected.
        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        it = self._create_power_transformer(mrid, nominal_phases or [PhaseCode.ABC, PhaseCode.ABC])
        self._connect(self._current, it, connectivity_node_mrid)

        if end_actions:
            for i in range(0, it.num_ends()):
                end_actions[i](it.get_end_by_num(i + 1))

        action(it)
        self._current = it
        return self

    def to_energy_consumer(
        self,
        nominal_phases: PhaseCode = PhaseCode.ABC,
        mrid: Optional[str] = None,
        connectivity_node_mrid: Optional[str] = None,
        action: Callable[[EnergyConsumer], None] = null_action
    ) -> 'TestNetworkBuilder':
        """
        Add a new `EnergyConsumer` to the network and connect it to the current network pointer, updating the network pointer to the new
        `EnergyConsumer`.

        :param nominal_phases: The nominal phases for the new `EnergyConsumer`.
        :param mrid: Optional mRID for the new `EnergyConsumer`.
        :param connectivity_node_mrid: Optional id of the connectivity node used to connect this `EnergyConsumer` to the previous item. Will only be used if the
         previous item is not already connected.
        :param action: An action that accepts the new `EnergyConsumer` to allow for additional initialisation.

        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        it = self._create_energy_consumer(mrid, nominal_phases)
        self._connect(self._current, it, connectivity_node_mrid)
        action(it)
        self._current = it
        return self

    def from_busbar_section(
        self,
        nominal_phases: PhaseCode = PhaseCode.ABC,
        mrid: str = None,
        action: Callable[[BusbarSection], None] = null_action
    ) -> 'TestNetworkBuilder':
        """
        Start a new network island from a `BusbarSection`, updating the network pointer to the new `BusbarSection`.

        :param nominal_phases: The nominal phases for the new `BusbarSection`.
        :param mrid: Optional mRID for the new `BusbarSection`.
        :param action: An action that accepts the new `BusbarSection` to allow for additional initialisation.

        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        it = self._create_busbar_section(mrid, nominal_phases)
        action(it)
        self._current = it
        return self

    def to_busbar_section(
        self,
        nominal_phases: PhaseCode = PhaseCode.ABC,
        mrid: str = None,
        connectivity_node_mrid: Optional[str] = None,
        action: Callable[[BusbarSection], None] = null_action
    ) -> 'TestNetworkBuilder':
        """

        Add a new `BusbarSection` to the network and connect it to the current network pointer, updating the network pointer to the new `BusbarSection`.

        :param nominal_phases: The nominal phases for the new `BusbarSection`.
        :param mrid: Optional mRID for the new `BusbarSection`.
        :param connectivity_node_mrid: Optional id of the connectivity node used to connect this `BusbarSection` to the previous item. Will only be used
         if the previous item is not already connected.
        :param action: An action that accepts the new `BusbarSection` to allow for additional initialisation.

        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        it = self._create_busbar_section(mrid, nominal_phases)
        self._connect(self._current, it, connectivity_node_mrid)
        action(it)
        self._current = it
        return self

    def from_other(
        self,
        creator: Union[OtherCreator, Type[SubclassesConductingEquipment]],
        nominal_phases: PhaseCode = PhaseCode.ABC,
        num_terminals: Optional[int] = None,
        mrid: Optional[str] = None,
        action: Callable[[SubclassesConductingEquipment], None] = null_action,
        default_mrid_prefix: Optional[str] = None
    ) -> 'TestNetworkBuilder':
        """
        Start a new network island from a `ConductingEquipment` created by `creator`, updating the network pointer to the new `ConductingEquipment`.

        :param creator: A callable function used to create the new `ConductingEquipment`. It will be passed the generated mRID for the new
              `ConductingEquipment`.
        :param nominal_phases: The nominal phases for the new `ConductingEquipment`.
        :param num_terminals: The number of terminals to create on the new `ConductingEquipment`. Defaults to 2.
        :param mrid: Optional mRID for the new `ConductingEquipment`.
        :param action: An action that accepts the new `ConductingEquipment` to allow for additional initialisation.
        :param default_mrid_prefix:  mRID prefix to use for the new `ConductingEquipment`

        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        if mrid and default_mrid_prefix:
            raise ValueError('cant specify both mrid and default_mrid_prefix as your intention is unclear')
        it = self._create_other(mrid, creator, nominal_phases, num_terminals, default_mrid_prefix=default_mrid_prefix)
        action(it)
        self._current = it
        return self

    def to_other(
        self,
        creator: Union[OtherCreator, Type[SubclassesConductingEquipment]],
        nominal_phases: PhaseCode = PhaseCode.ABC,
        num_terminals: Optional[int] = None,
        mrid: Optional[str] = None,
        connectivity_node_mrid: Optional[str] = None,
        action: Callable[[SubclassesConductingEquipment], None] = null_action,
        default_mrid_prefix: Optional[str] = None
    ) -> 'TestNetworkBuilder':
        """
        Add a new `ConductingEquipment` to the network and connect it to the current network pointer, updating the network pointer to the new
        `ConductingEquipment`.

        :param creator: A callable function used to create the new `ConductingEquipment`. It will be passed the generated mRID for the new
              `ConductingEquipment`.
        :param nominal_phases: The nominal phases for the new `ConductingEquipment`.
        :param num_terminals: The number of terminals to create on the new `ConductingEquipment`. Defaults to 2.
        :param mrid: Optional mRID for the new `ConductingEquipment`.
        :param connectivity_node_mrid: Optional id of the connectivity node used to connect this `ConductingEquipment` to the previous item. Will only be used
         if the previous item is not already connected.
        :param action: An action that accepts the new `ConductingEquipment` to allow for additional initialisation.
        :param default_mrid_prefix:  mRID prefix to use for the new `ConductingEquipment`

        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        if mrid and default_mrid_prefix:
            raise ValueError('cant specify both mrid and default_mrid_prefix as your intention is unclear')
        it = self._create_other(mrid, creator, nominal_phases, num_terminals, default_mrid_prefix=default_mrid_prefix)
        self._connect(self._current, it, connectivity_node_mrid)
        action(it)
        self._current = it
        return self

    def with_clamp(
        self,
        mrid: Optional[str] = None,
        length_from_terminal_1: float = None,
        nominal_phases: PhaseCode = PhaseCode.ABC,
        action: Callable[[Clamp], None] = null_action
    ) -> 'TestNetworkBuilder':
        """
        Create a clamp on the current network pointer (must be an `AcLineSegment`) without moving the current network pointer.

        :param mrid: Optional mRID for the new `Clamp`
        :param length_from_terminal_1: The length from terminal 1 of the `AcLineSegment` being clamped
        :param nominal_phases: The nominal phases for the new `BusbarSection`.
        :param action: An action that accepts the new `Clamp` to allow for additional initialisation.

        :return: This `TestNetworkBuilder` to allow for fluent use
        """
        acls = self._current
        if not isinstance(acls, AcLineSegment):
            raise ValueError("`with_clamp` can only be called when the last added item was an AcLineSegment")

        clamp = Clamp(mrid=mrid or f'{acls.mrid}-clamp{acls.num_clamps() + 1}', length_from_terminal_1=length_from_terminal_1)
        self._add_terminal(clamp, 1, nominal_phases)

        acls.add_clamp(clamp)
        action(clamp)
        self.network.add(clamp)
        return self

    def with_cut(
        self,
        mrid: Optional[str] = None,
        length_from_terminal_1: Optional[float] = None,
        is_normally_open: bool = True,
        is_open: bool = None,
        nominal_phases: PhaseCode = PhaseCode.ABC,
        action: Callable[[Cut], None] = null_action
    ) -> 'TestNetworkBuilder':
        """
        Create a cut on the current network pointer (must be an `AcLineSegment`) without moving the current network pointer.

        :param mrid: Optional mRID for the new `Cut`
        :param length_from_terminal_1: The length from terminal 1 of the `AcLineSegment` being cut
        :param is_normally_open: The normal state of the cut, defaults to True
        :param is_open: The current state of the cut. Defaults to `is_normally_open`
        :param nominal_phases: The nominal phases for the new `BusbarSection`.
        :param action: An action that accepts the new `Cut` to allow for additional initialisation.

        :return: This `TestNetworkBuilder` to allow for fluent use
        """
        acls = self._current
        if not isinstance(acls, AcLineSegment):
            raise ValueError("`with_cut` can only be called when the last added item was an AcLineSegment")

        cut = Cut(mrid=mrid or f'{acls.mrid}-cut{acls.num_cuts() + 1}', length_from_terminal_1=length_from_terminal_1)
        for i in [1, 2]:
            self._add_terminal(cut, i, nominal_phases)

        cut.set_normally_open(is_normally_open)
        if is_open is None:
            cut.set_open(is_normally_open)
        else:
            cut.set_open(is_open)

        acls.add_cut(cut)
        action(cut)
        self.network.add(cut)
        return self

    def branch_from(self, from_: str, terminal: Optional[int] = None) -> 'TestNetworkBuilder':
        """
        Move the current network pointer to the specified `from` allowing branching of the network. This has the effect of changing the current network pointer.

        :param from_: The mRID of the `ConductingEquipment` to split from.
        :param terminal: The terminal to split from. Defaults to last terminal.

        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        self._current = self.network.get(from_, ConductingEquipment)
        self._current_terminal = terminal
        return self

    def connect_to(
        self,
        to: str,
        to_terminal: int = None,
        from_terminal: int = None,
        connectivity_node_mrid: Optional[str] = None
    ) -> 'TestNetworkBuilder':
        """
        Connect to current network pointer to the specified `to` without moving the current network pointer.

        :param to: The mRID of the second `ConductingEquipment` to be connected.
        :param to_terminal: The sequence number or terminal on `to` which will be connected.
        :param from_terminal: Optional sequence number of the terminal on current network pointer which will be connected.
        :param connectivity_node_mrid: Optional id of the connectivity node used to connect the terminals. Will only be used if both terminals are not already
         connected.
        :return: This `TestNetworkBuilder` to allow for fluent use.
        """

        self._connect(
            self._current,
            self.network.get(to, ConductingEquipment),
            connectivity_node_mrid,
            from_terminal,
            to_terminal
        )
        return self

    def connect(
        self,
        from_: str,
        to: str,
        from_terminal: int,
        to_terminal: int,
        connectivity_node_mrid: Optional[str] = None
    ) -> 'TestNetworkBuilder':
        """
        Connect the specified `from` and `to` without moving the current network pointer.

        :param from_: The mRID of the first `ConductingEquipment` to be connected.
        :param to: The mRID of the second `ConductingEquipment` to be connected.
        :param from_terminal: The sequence number of the terminal on `from` which will be connected.
        :param to_terminal: The sequence number of the terminal on `to` which will be connected.
        :param connectivity_node_mrid: Optional id of the connectivity node used to connect the terminals. Will only be used if both terminals are not already
         connected.

        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        self._connect(
            self.network.get(from_, ConductingEquipment),
            self.network.get(to, ConductingEquipment),
            connectivity_node_mrid,
            from_terminal,
            to_terminal
        )
        return self

    def add_feeder(self, head_mrid: str, sequence_number: Optional[int] = None, mrid: Optional[str] = None) -> 'TestNetworkBuilder':
        """
        Create a new feeder with the specified terminal as the head terminal.

        :param head_mrid: The mRID of the head `ConductingEquipment`.
        :param sequence_number: The `Terminal` sequence number of the head terminal. Defaults to last terminal.
        :param mrid: Optional mRID for the new `Feeder`.

        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        self._create_feeder(mrid, self.network.get(head_mrid, ConductingEquipment), sequence_number)
        return self

    def add_lv_feeder(self, head_mrid: str, sequence_number: Optional[int] = None, mrid: Optional[str] = None) -> 'TestNetworkBuilder':
        """
        Create a new LV feeder with the specified terminal as the head terminal.

        :param head_mrid: The mRID of the head `ConductingEquipment`.
        :param sequence_number: The `Terminal` sequence number of the head terminal. Defaults to last terminal.
        :param mrid: Optional mRID for the new `LvFeeder`.

        :return: This `TestNetworkBuilder` to allow for fluent use.
        """
        self._create_lv_feeder(mrid, self.network.get(head_mrid, ConductingEquipment), sequence_number)
        return self

    def add_site(self, equipment_mrids: List[str], mrid: Optional[str] = None) -> 'TestNetworkBuilder':
        """
        Create a new Site containing the specified equipment.

        :param equipment_mrids: The mRID's of the equipment to add to the site
        :param mrid: Optional mRID for the new `Site`.
        :return: This [TestNetworkBuilder] to allow for fluent use.
        """

        site = Site(mrid=self._next_id(mrid, 'site'))

        for _id in equipment_mrids:
            ce = self.network[_id]
            site.add_equipment(ce)
            ce.add_container(site)
        self.network.add(site)

        return self

    async def build(self, apply_directions_from_sources: bool = True, debug_logger: Logger = None) -> NetworkService:
        """
        Get the `NetworkService` after apply traced phasing and feeder directions.

        Does not infer phasing.

        :return: The `NetworkService` created by this `TestNetworkBuilder`
        """
        await Tracing.set_direction(debug_logger=debug_logger).run(self.network, network_state_operators=NetworkStateOperators.NORMAL)
        await Tracing.set_direction(debug_logger=debug_logger).run(self.network, network_state_operators=NetworkStateOperators.CURRENT)
        await Tracing.set_phases(debug_logger=debug_logger).run(self.network, network_state_operators=NetworkStateOperators.NORMAL)
        await Tracing.set_phases(debug_logger=debug_logger).run(self.network, network_state_operators=NetworkStateOperators.CURRENT)

        if apply_directions_from_sources:
            for es in self.network.objects(EnergySource):
                for terminal in es.terminals:
                    await Tracing.set_direction(debug_logger=debug_logger).run_terminal(terminal, network_state_operators=NetworkStateOperators.NORMAL)
                    await Tracing.set_direction(debug_logger=debug_logger).run_terminal(terminal, network_state_operators=NetworkStateOperators.CURRENT)

        await Tracing.assign_equipment_to_feeders(debug_logger=debug_logger).run(self.network, network_state_operators=NetworkStateOperators.NORMAL)
        await Tracing.assign_equipment_to_lv_feeders(debug_logger=debug_logger).run(self.network, network_state_operators=NetworkStateOperators.NORMAL)
        await Tracing.assign_equipment_to_feeders(debug_logger=debug_logger).run(self.network, network_state_operators=NetworkStateOperators.CURRENT)
        await Tracing.assign_equipment_to_lv_feeders(debug_logger=debug_logger).run(self.network, network_state_operators=NetworkStateOperators.CURRENT)

        return self.network

    def _next_id(self, mrid: Optional[str], type_: str) -> str:
        if mrid:
            return mrid

        id_ = f"{type_}{self._count}"
        self._count += 1
        return id_

    def _connect(
        self,
        from_: ConductingEquipment,
        to: ConductingEquipment,
        connectivity_node_mrid: Optional[str] = None,
        from_terminal: Optional[int] = None,
        to_terminal: Optional[int] = None
    ):
        from_term = from_.get_terminal_by_sn(from_terminal if from_terminal else self._current_terminal if self._current_terminal else from_.num_terminals())
        to_term = to.get_terminal_by_sn(to_terminal if to_terminal else 1)
        if (connectivity_node_mrid is None) or from_term.connected or to_term.connected:
            self.network.connect_terminals(from_term, to_term)
        else:
            self.network.connect_by_mrid(from_term, connectivity_node_mrid)
            self.network.connect_by_mrid(to_term, connectivity_node_mrid)
        self._current_terminal = None

    def _create_external_source(self, mrid: Optional[str], nominal_phases: PhaseCode) -> EnergySource:
        if any(it not in PhaseCode.ABCN for it in nominal_phases.single_phases):
            raise ValueError("EnergySource phases must be a subset of ABCN")

        es = EnergySource(mrid=self._next_id(mrid, "s"), is_external_grid=True)
        self._add_terminal(es, 1, nominal_phases)

        self.network.add(es)
        return es

    def _create_acls(self, mrid: Optional[str], nominal_phases: PhaseCode) -> AcLineSegment:
        acls = AcLineSegment(mrid=self._next_id(mrid, "c"))
        self._add_terminal(acls, 1, nominal_phases)
        self._add_terminal(acls, 2, nominal_phases)

        self.network.add(acls)
        return acls

    def _create_breaker(self, mrid: Optional[str], nominal_phases: PhaseCode, is_normally_open: bool, is_open: bool) -> Breaker:
        b = Breaker(mrid=self._next_id(mrid, "b"))
        b.set_normally_open(is_normally_open)
        b.set_open(is_open)

        self._add_terminal(b, 1, nominal_phases)
        self._add_terminal(b, 2, nominal_phases)

        self.network.add(b)
        return b

    def _create_junction(self, mrid: Optional[str], nominal_phases: PhaseCode, num_terminals: Optional[int]) -> Junction:
        j = Junction(mrid=self._next_id(mrid, "j"))
        for i in range(1, (num_terminals if num_terminals is not None else 2) + 1):
            self._add_terminal(j, i, nominal_phases)

        self.network.add(j)
        return j

    def _create_busbar_section(self, mrid: Optional[str], nominal_phases: PhaseCode) -> BusbarSection:
        b = BusbarSection(mrid=self._next_id(mrid, 'bbs'))
        self._add_terminal(b, 1, nominal_phases)

        self.network.add(b)
        return b

    def _create_power_electronics_connection(self, mrid: Optional[str], nominal_phases: PhaseCode, num_terminals: Optional[int]) -> PowerElectronicsConnection:
        pec = PowerElectronicsConnection(mrid=self._next_id(mrid, "pec"))
        for i in range(1, (num_terminals if num_terminals is not None else 2) + 1):
            self._add_terminal(pec, i, nominal_phases)

        self.network.add(pec)
        return pec

    def _create_power_transformer(self, mrid: Optional[str], nominal_phases: List[PhaseCode]):
        tx = PowerTransformer(mrid=self._next_id(mrid, "tx"))

        i = 1
        for phase_code in nominal_phases:
            t = Terminal(mrid=f"{tx.mrid}-t{i}")
            t.phases = phase_code
            self.network.add(t)

            tx.add_terminal(t)

            end = PowerTransformerEnd(mrid=f"{tx.mrid}-e{i}")
            end.terminal = t
            self.network.add(end)
            tx.add_end(end)

            i += 1

        self.network.add(tx)
        return tx

    def _create_energy_consumer(self, mrid: Optional[str], nominal_phases: PhaseCode) -> EnergyConsumer:
        ec = EnergyConsumer(mrid=self._next_id(mrid, "ec"))
        self._add_terminal(ec, 1, nominal_phases)

        self.network.add(ec)
        return ec

    def _create_other(
        self,
        mrid: Optional[str],
        creator: Union[OtherCreator, Type[SubclassesConductingEquipment]],
        nominal_phases: PhaseCode,
        num_terminals: Optional[int],
        default_mrid_prefix: Optional[str] = None
    ) -> SubclassesConductingEquipment:
        o = creator(mrid=self._next_id(mrid, default_mrid_prefix or "o"))
        for i in range(1, (num_terminals if num_terminals is not None else 2) + 1):
            self._add_terminal(o, i, nominal_phases)

        self.network.add(o)
        return o

    def _create_feeder(self, mrid: Optional[str], head_equipment: ConductingEquipment, sequence_number: Optional[int] = None) -> Feeder:
        f = Feeder(
            mrid=self._next_id(mrid, "fdr"),
            normal_head_terminal=head_equipment.get_terminal_by_sn(sequence_number if sequence_number else head_equipment.num_terminals())
        )

        f.add_equipment(head_equipment)
        f.add_current_equipment(head_equipment)
        head_equipment.add_container(f)
        head_equipment.add_current_container(f)

        self.network.add(f)
        return f

    def _create_lv_feeder(self, mrid: Optional[str], head_equipment: ConductingEquipment, sequence_number: Optional[int] = None) -> LvFeeder:
        lvf = LvFeeder(
            mrid=self._next_id(mrid, "lvf"),
            normal_head_terminal=head_equipment.get_terminal_by_sn(sequence_number if sequence_number else head_equipment.num_terminals())
        )

        lvf.add_equipment(head_equipment)
        lvf.add_current_equipment(head_equipment)
        head_equipment.add_container(lvf)
        head_equipment.add_current_container(lvf)

        self.network.add(lvf)
        return lvf

    def _add_terminal(self, ce: ConductingEquipment, sn: int, nominal_phases: PhaseCode):
        terminal = Terminal(mrid=f"{ce.mrid}-t{sn}", phases=nominal_phases)
        ce.add_terminal(terminal)
        self.network.add(terminal)
