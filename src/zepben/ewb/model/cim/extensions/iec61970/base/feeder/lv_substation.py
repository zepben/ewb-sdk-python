#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Generator, TYPE_CHECKING

__all__ = ['LvSubstation']

from zepben.ewb import ngen, nlen, safe_remove_by_id, get_by_mrid
from zepben.ewb.model.cim.extensions.zbex import zbex
from zepben.ewb.model.cim.iec61970.base.core.equipment_container import EquipmentContainer
from zepben.ewb.model.cim.extensions.iec61970.base.feeder.lv_feeder import LvFeeder

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.core.feeder import Feeder


@zbex
class LvSubstation(EquipmentContainer):
    """
    [ZBEX] a collection of equipment for purposes other than generation or utilization, through which electric energy in bulk is passed for the distribution of energy to low voltage network.
    @property normal_energizing_feeders [ZBEX] the feeders that nominally energize the substation. also used for naming purposes.
    @property normal_energized_lv_feeders [ZBEX] the lv_feeders that are nominally energized by this lv_substation. also used for naming purposes.
    @property current_energizing_feeders [ZBEX] the feeders that currently energize the substation. also used for naming purposes.
    """

    _normal_energizing_feeders_by_id: dict[str | None, 'Feeder'] | None = None
    _current_energizing_feeders_by_id: dict[str | None, 'Feeder'] | None = None
    _normal_energized_lv_feeders_by_id: dict[str | None, LvFeeder] | None = None

    @zbex
    @property
    def normal_energizing_feeders(self) -> Generator["Feeder", None, None]:
        """[ZBEX] The HV/MV feeders that normally energize this ``LvSubstation``. The returned collection is read only."""
        return ngen((self._normal_energizing_feeders_by_id or {}).values())

    def num_normal_energizing_feeders(self) -> int:
        """Get the number of entries in the normal ``Feeder`` collection."""
        return nlen(self._normal_energizing_feeders_by_id or {})

    def get_normal_energizing_feeder(self, mrid: str) -> 'Feeder | None':
        """
        Energizing feeder using the normal state of the network.

        :param mrid: the mRID of the required normal ``Feeder``
        :returns: The ``Feeder`` with the specified ``mrid`` if it exists, otherwise null
        """
        return get_by_mrid(self._normal_energizing_feeders_by_id, mrid)

    def add_normal_energizing_feeder(self, feeder: 'Feeder') -> "LvSubstation":
        """
        Associate this ``LvSubstation`` with a ``Feeder`` in the normal state of the network.

        :param feeder: the HV/MV feeder to associate with this ``LvSubstation`` in the normal state of the network.
        :returns: This ``LvSubstation`` for fluent use.
        """
        if self._validate_reference(feeder, self.get_normal_energizing_feeder, "A Feeder"):
            return self

        if self._normal_energizing_feeders_by_id is None:
            self._normal_energizing_feeders_by_id = dict()
        self._normal_energizing_feeders_by_id[feeder.mrid] = feeder
        return self

    def remove_normal_energizing_feeder(self, feeder: 'Feeder') -> "LvSubstation":
        """
        Disassociate this ``LvSubstation`` from a ``Feeder`` in the normal state of the network.

        :param feeder: the HV/MV feeder to disassociate from this ``LvSubstation`` in the normal state of the network.
        :returns: true if a matching feeder is removed from the collection.
        """
        self._normal_energizing_feeders_by_id = safe_remove_by_id(self._normal_energizing_feeders_by_id, feeder)
        return self

    def clear_normal_energizing_feeders(self) -> "LvSubstation":
        """
        Clear all ``Feeder``'s associated with this ``LvSubstation`` in the normal state of the network.

        :returns: This ``LvSubstation`` for fluent use.
        """
        self._normal_energizing_feeders_by_id = None
        return self

    @zbex
    @property
    def normal_energized_lv_feeders(self) -> Generator[LvFeeder, None, None]:
        return ngen((self._normal_energized_lv_feeders_by_id or {}).values())

    def num_normal_energized_lv_feeders(self) -> int:
        """Get the number of entries in the normal ``LvFeeder`` collection."""
        return nlen(self._normal_energized_lv_feeders_by_id or {})

    def get_normal_energized_lv_feeder(self, mrid: str) -> LvFeeder | None:
        """
        Retrieve an energized ``LvFeeder`` using the normal state of the network.

        :param mrid: the mRID of the required normal ``LvFeeder``
        :returns: The ``LvFeeder`` with the specified ``mRID`` if it exists, otherwise null
        """
        return get_by_mrid(self._normal_energized_lv_feeders_by_id, mrid)

    def add_normal_energized_lv_feeder(self, lv_feeder: LvFeeder) -> "LvSubstation":
        """
        :param lv_feeder: the ``LvFeeder`` to associate with this feeder in the normal state of the network.
        """
        if self._validate_reference(lv_feeder, self.get_normal_energized_lv_feeder, "An LvFeeder"):
            return self

        if self._normal_energized_lv_feeders_by_id is None:
            self._normal_energized_lv_feeders_by_id = dict()
        self._normal_energized_lv_feeders_by_id[lv_feeder.mrid] = lv_feeder
        return self

    def remove_normal_energized_lv_feeder(self, lv_feeder: LvFeeder) -> "LvSubstation":
        """ 
        :param lv_feeder: the ``LvFeeder`` to disassociate from this HV/MV feeder in the normal state of the network.
        """
        self._normal_energized_lv_feeders_by_id = safe_remove_by_id(self._normal_energized_lv_feeders_by_id, lv_feeder)
        return self

    def clear_normal_energized_lv_feeders(self) -> "LvSubstation":
        """
        Clear all ``LvFeeder``'s associated with this ``LvSubstation`` in the normal state of the network.

        :returns: This ``LvSubstation`` for fluent use.
        """
        self._normal_energized_lv_feeders_by_id = None
        return self

    @zbex
    @property
    def current_energizing_feeders(self) -> Generator['Feeder', None, None]:
        """
        [ZBEX] The HV/MV feeders that currently energize this LV substation. The returned collection is read only.
        """
        return ngen((self._current_energizing_feeders_by_id or {}).values())

    def num_current_energizing_feeders(self) -> int:
        """
        Get the number of entries in the current ``Feeder`` collection.
        """
        return nlen(self._current_energizing_feeders_by_id or {})

    def get_current_energizing_feeder(self, mrid: str) -> 'Feeder | None':
        """
        Retrieve an energizing feeder using the current state of the network.

        :param mrid: the mRID of the required current ``Feeder``
        :returns: The ``Feeder`` with the specified ``mRID`` if it exists, otherwise null
        """
        return get_by_mrid(self._current_energizing_feeders_by_id, mrid)

    def add_current_energizing_feeder(self, feeder: 'Feeder') -> "LvSubstation":
        """
        Associate this ``LvSubstation`` with a ``Feeder`` in the current state of the network.

        :param feeder: the HV/MV feeder to associate with this ``LvSubstation`` in the current state of the network.
        :returns: This ``LvSubstation`` for fluent use.
        """
        if self._validate_reference(feeder, self.get_current_energizing_feeder, "A Feeder"):
            return self
        if self._current_energizing_feeders_by_id is None:
            self._current_energizing_feeders_by_id = dict()
        self._current_energizing_feeders_by_id[feeder.mrid] = feeder
        return self

    def remove_current_energizing_feeder(self, feeder: 'Feeder') -> "LvSubstation":
        """
        Disassociate this ``LvSubstation`` from a ``Feeder`` in the current state of the network.

        :param feeder: the HV/MV feeder to disassociate from this LvSubstation the current state of the network.
        :returns: true if a matching feeder is removed from the collection.
        """
        self._current_energizing_feeders_by_id = safe_remove_by_id(self._current_energizing_feeders_by_id, feeder)
        return self

    def clear_current_energizing_feeders(self) -> "LvSubstation":
        """
        Clear all ``Feeder``'s associated with this ``LvSubstation`` in the current state of the network.

        :returns: This ``LvSubstation`` for fluent use.
        """
        self._current_energizing_feeders_by_id = None
        return self

    def normal_energized_lv_switch_feeders(self) -> Generator[LvFeeder, None, None]:
        """
        Retrieves all normally energized LvFeeders that represent low voltage network connected below a switch on the edge of this LvSubstation. This is all LvFeeders in the normalEnergizedLvFeeders that has a normalHeadTerminal attached to a Switch.
        """
        # NOTE: import exists here due to a circular import problem
        from zepben.ewb.model.cim.iec61970.base.wires.switch import Switch

        for lv_feeder in self.normal_energized_lv_feeders:
            if (it := lv_feeder.normal_head_terminal) is not None and isinstance(it.conducting_equipment, Switch):
                yield lv_feeder
