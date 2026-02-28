#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.ewb import TableProtectionRelayFunctions
from zepben.ewb.database.sql.column import Type, Nullable, Column


class TableDirectionalCurrentRelays(TableProtectionRelayFunctions):
    """
    A class representing the DirectionalCurrentRelay columns required for the database table.

    :var directional_characteristic_angle: A column storing the characteristic angle (in degrees) that defines the boundary between the operate and restrain regions of the directional element, relative to the polarizing quantity. Often referred to as Maximum Torque Angle (MTA) or Relay Characteristic Angle (RCA).
    :var polarizing_quantity_type: A column storing the type of voltage to be used for polarization. This guides the selection/derivation of voltage from the VTs.
    :var relay_element_phase: A column storing the phase associated with this directional relay element. This helps in selecting the correct 'self-phase' or other phase-derived.
    :var minimum_pickup_current: A column storing the minimum current magnitude required for the directional element to operate reliably and determine direction. This might be different from the main pickupCurrent for the overcurrent function.
    :var current_limit_1: A column storing the current limit number 1 for inverse time pickup in amperes.
    :var inverse_time_flag: A column storing the true if the current relay has inverse time characteristic.
    :var time_delay_1: A column storing the inverse time delay number 1 for current limit number 1 in seconds.

    """
    def __init__(self):
        super().__init__()

        self.directional_characteristic_angle: Column = self._create_column("directional_characteristic_angle", Type.DOUBLE, Nullable.NULL)
        self.polarizing_quantity_type: Column = self._create_column("polarizing_quantity_type", Type.STRING, Nullable.NULL)
        self.relay_element_phase: Column = self._create_column("relay_element_phase", Type.STRING, Nullable.NULL)
        self.minimum_pickup_current: Column = self._create_column("minimum_pickup_current", Type.DOUBLE, Nullable.NULL)
        self.current_limit_1: Column = self._create_column("current_limit_1", Type.DOUBLE, Nullable.NULL)
        self.inverse_time_flag: Column = self._create_column("inverse_time_flag", Type.BOOLEAN, Nullable.NULL)
        self.time_delay_1: Column = self._create_column("time_delay_1", Type.DOUBLE, Nullable.NULL)

    @property
    def name(self) -> str:
        return 'directional_current_relays'
