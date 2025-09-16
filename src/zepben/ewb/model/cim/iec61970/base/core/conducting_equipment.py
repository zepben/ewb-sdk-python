#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

__all__ = ['ConductingEquipment']

import sys
from typing import List, TYPE_CHECKING, Union
from warnings import deprecated

from zepben.ewb.collections.autoslot import dataslot, BackingValue
from zepben.ewb.collections.boilerplate import MRIDListAccessor
from zepben.ewb.model.cim.iec61970.base.core.equipment import Equipment
from zepben.ewb.util import require

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.base_voltage import BaseVoltage
    from zepben.ewb.model.cim.iec61970.base.core.terminal import Terminal


@dataslot
class ConductingEquipment(Equipment):
    """
    Abstract class, should only be used through subclasses.
    The parts of the AC power system that are designed to carry current or that are conductively connected through
    terminals.

    ConductingEquipment are connected by `Terminal`'s which are in turn associated with
    `ConnectivityNode`'s. Each `Terminal` is associated with
    _exactly one_ `ConnectivityNode`, and through that `ConnectivityNode` can be linked with many other `Terminals` and `ConductingEquipment`.
    """

    base_voltage: BaseVoltage | None = None
    """
    `BaseVoltage` of this `ConductingEquipment`. Use only when there is no voltage level container used and only one base voltage applies. For example, not
    used for transformers.
    """

    _terminals: List[Terminal] | None = BackingValue()
    terminals: List[Terminal] | None = MRIDListAccessor()
    max_terminals = int(sys.maxsize)

    # pylint: disable=unused-argument
    def get_base_voltage(self, terminal: Terminal = None):
        """
        Get the `BaseVoltage` of this `ConductingEquipment`.
        Note `terminal` is not used here, but this method can be overridden in child classes (e.g PowerTransformer).

        `terminal` The `Terminal` to get the voltage at.
        Returns thee BaseVoltage of this `ConductingEquipment` at `terminal`
        """
        return self.base_voltage

    @property
    def base_voltage_value(self) -> int:
        """
        :return: The value of the nominal voltage for the base voltage if there is one, otherwise 0.
        """
        return self.base_voltage.nominal_voltage if self.base_voltage and self.base_voltage.nominal_voltage else 0

    @deprecated("Use len(items) instead.")
    def num_items(self) -> int: ...

    def get_terminal(self, identifier: Union[int, str]):
        """
        Get the `Terminal` for this `ConductingEquipment` identified by `mrid` or `sequence_number`

        :param identifier: the mRID of the required `Terminal`, or the `sequence_number` of the terminal in relation
            to this `ConductingEquipment`
        :return: The `Terminal` with the specified `mrid` if it exists

        Raises `KeyError` if `mrid` wasn't present.
        Raises `TypeError` if the identifier wasn't a recognised type
        """
        if isinstance(identifier, str):
            return self.get_terminal_by_mrid(identifier)
        elif isinstance(identifier, int):
            return self.get_terminal_by_sn(identifier)
        raise TypeError(f'Attempting to access MRID list with identifier ' +
                        f'of type {type(identifier)}.')

    @deprecated("Use terminals[mrid] instead.")
    def get_terminal_by_mrid(self, mrid: str) -> Terminal: ...

    def get_terminal_by_sn(self, sequence_number: int):
        """
        Get the `Terminal` on this `ConductingEquipment` by its `sequence_number`.

        :param sequence_number: The `sequence_number` of the `Terminal` in relation to this `ConductingEquipment`.

        :return: The `Terminal` on this `ConductingEquipment` with sequence number `sequence_number`

        Raises IndexError if no `Terminal` was found with sequence_number `sequence_number`.
        """
        term = self._terminals[sequence_number-1] # Correct for one-indexed lists in UML
        if term.sequence_number != sequence_number:
            raise IndexError(f"No Terminal with sequence_number {sequence_number} " +
                             f"was found in ConductingEquipment {str(self)}")
        return term

    def __getitem__(self, item: int):
        return self.get_terminal_by_sn(item)

    def add_terminal(self, terminal: Terminal) -> ConductingEquipment:
        """
        Associate `terminal` with this `ConductingEquipment`. If `terminal.sequence_number` == 0, the terminal will be assigned a sequence_number of
        `self.num_terminals() + 1`.

        `terminal` The `Terminal` to associate with this `ConductingEquipment`.
        Returns A reference to this `ConductingEquipment` to allow fluent use.
        Raises `ValueError` if another `Terminal` with the same `mrid` already exists for this `ConductingEquipment`.
        Raises `ValueError` if `max_terminals` has already been reached.
        """
        # TODO: Remove this filth
        if self._validate_terminal(terminal):
            return self
        self._terminals.append(terminal)
        return self

    @deprecated("Use terminals.remove() instead.")
    def remove_terminal(self, terminal: Terminal) -> ConductingEquipment:
        ...

    @deprecated("Use terminals.clear() instead.")
    def clear_terminals(self) -> ConductingEquipment: ...

    def __repr__(self):
        return (f"{super(ConductingEquipment, self).__repr__()}, in_service={self.in_service}, "
                f"normally_in_service={self.normally_in_service}, location={self.location}"
                )

    def _validate_terminal(self, terminal: Terminal) -> bool:
        """
        Validate a terminal against this `ConductingEquipment`'s `Terminal`s.

        `terminal` The `Terminal` to validate.
        Returns True if `Terminal`` is already associated with this `ConductingEquipment`, otherwise False.
        Raises `ValueError` if `Terminal`s `conducting_equipment` is not this `ConductingEquipment`,
        or if this `ConductingEquipment` has a different `Terminal` with the same mRID.
        """
        if self._validate_reference(terminal, self.get_terminal_by_mrid, "A Terminal"):
            return True

        if self._validate_reference_by_field(terminal, terminal.sequence_number, self.get_terminal_by_sn, "sequence_number"):
            return True

        require(terminal.conducting_equipment is self,
                lambda: f"Terminal {terminal} references another piece of conducting equipment {terminal.conducting_equipment}, expected {str(self)}.")
        return False
