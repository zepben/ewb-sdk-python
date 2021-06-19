#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

import math
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from zepben.evolve import TransformerTankInfo, NoLoadTest, OpenCircuitTest, ShortCircuitTest
from zepben.evolve.model.cim.iec61968.assets.asset_info import AssetInfo
from zepben.evolve.model.cim.iec61970.base.wires.transformer_star_impedance import TransformerStarImpedance, ResistanceReactance
from zepben.evolve.model.cim.iec61970.base.wires.winding_connection import WindingConnection

__all__ = ["TransformerEndInfo"]


class TransformerEndInfo(AssetInfo):
    """Transformer end data."""

    connection_kind: WindingConnection = WindingConnection.UNKNOWN_WINDING
    """Kind of connection."""

    emergency_s: Optional[int] = None
    """Apparent power that the winding can carry under emergency conditions (also called long-term emergency power). Unit: VA"""

    end_number: int = 0
    """Number for this transformer end, corresponding to the end's order in the PowerTransformer.vectorGroup attribute. Highest voltage winding
         should be 1."""

    insulation_u: Optional[int] = None
    """Basic insulation level voltage rating. Unit: Volts"""

    phase_angle_clock: Optional[int] = None
    """Winding phase angle where 360 degrees are represented with clock hours, so the valid values are {0, ..., 11}. For example,
         to express the second winding in code 'Dyn11', set attributes as follows: 'endNumber'=2, 'connectionKind' = Yn and 'phaseAngleClock' = 11."""

    r: Optional[float] = None
    """DC resistance. Unit: Ohms"""

    rated_s: Optional[int] = None
    """Normal apparent power rating. Unit: VA"""

    rated_u: Optional[int] = None
    """Rated voltage: phase-phase for three-phase windings, and either phase-phase or phase-neutral for single-phase windings. Unit: Volts"""

    short_term_s: Optional[int] = None
    """Apparent power that this winding can carry for a short period of time (in emergency). Unit: VA"""

    transformer_tank_info: Optional[TransformerTankInfo] = None
    """Transformer tank data that this end description is part of."""

    transformer_star_impedance: Optional[TransformerStarImpedance] = None
    """Transformer star impedance calculated from this transformer end datasheet."""

    energised_end_no_load_tests: Optional[NoLoadTest] = None
    """
    All no-load test measurements in which this transformer end was energised.
    """

    energised_end_short_circuit_tests: Optional[ShortCircuitTest] = None
    """
    All short-circuit test measurements in which this transformer end was short-circuited.
    """

    grounded_end_short_circuit_tests: Optional[ShortCircuitTest] = None
    """
    All short-circuit test measurements in which this transformer end was energised.
    """

    open_end_open_circuit_tests: Optional[OpenCircuitTest] = None
    """
    All open-circuit test measurements in which this transformer end was not excited.
    """

    energised_end_open_circuit_tests: Optional[OpenCircuitTest] = None
    """
    All open-circuit test measurements in which this transformer end was excited.
    """

    def resistance_reactance(self) -> Optional[ResistanceReactance]:
        """
        Get the `ResistanceReactance` for this `TransformerEndInfo` from either the pre-calculated `transformer_star_impedance` or
        calculated from the associated test data.

        Returns the `ResistanceReactance` for this `TransformerEndInfo` or None if it could not be calculated
        """
        if self.transformer_star_impedance is not None:
            return self.transformer_star_impedance.resistance_reactance().merge_if_incomplete(lambda: self.calculate_resistance_reactance_from_tests())
        else:
            return self.calculate_resistance_reactance_from_tests()

    def calculate_resistance_reactance_from_tests(self) -> Optional[ResistanceReactance]:
        """
        Get the `ResistanceReactance` for this `TransformerEndInfo` calculated from the associated test data.

        Returns the `ResistanceReactance` for this `TransformerEndInfo` or None if it could not be calculated
        """

        def calculate_r_x(voltage: float, r: float, rated_u: int, rated_s: int):
            if not any(elem is None for elem in [voltage, r, rated_u, rated_s]):
                x = round(math.sqrt(((voltage / 100) * rated_u ** 2 / rated_s) ** 2 - r ** 2), 2)
                return [r, x]
            else:
                return None

        def calculate_r_x_from_test(short_circuit_test: ShortCircuitTest, rated_u: int, rated_s: int) -> Optional[float, float]:
            if short_circuit_test is not None:
                if short_circuit_test.voltage_ohmic_part is not None:
                    r = round((short_circuit_test.voltage_ohmic_part * rated_u ** 2) / (rated_s*100),2)
                    return calculate_r_x(short_circuit_test.voltage, r, rated_u, rated_s)
                elif short_circuit_test.loss is not None:
                    r = round(short_circuit_test.loss * (rated_u / rated_s) ** 2, 2)
                    return calculate_r_x(short_circuit_test.voltage, r, rated_u, rated_s)
                else:
                    return None
            else:
                return None

        if self.rated_u and self.rated_s:
            if calculate_r_x_from_test(self.energised_end_short_circuit_tests, self.rated_u, self.rated_s) is not None:
                rr = ResistanceReactance()
                [rr.r, rr.x] = calculate_r_x_from_test(self.energised_end_short_circuit_tests, self.rated_u, self.rated_s)
                return rr
            elif calculate_r_x_from_test(self.grounded_end_short_circuit_tests, self.rated_u, self.rated_s) is not None:
                rr = ResistanceReactance()
                [rr.r0, rr.x0] = calculate_r_x_from_test(self.grounded_end_short_circuit_tests, self.rated_u, self.rated_s)
                return rr
            else:
                return None
        else:
            return None
