#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from dataclassy import dataclass

__all__ = ["Ratio"]


@dataclass(slots=True, frozen=True)
class Ratio:
    """
    Fraction specified explicitly with a numerator and denominator, which can be used to calculate the quotient.
    """

    numerator: float
    """The part of a fraction that is below the line and that functions as the divisor of the numerator."""

    denominator: float
    """The part of a fraction that is above the line and signifies the number to be divided by the denominator."""

    @property
    def quotient(self) -> float:
        """
        The result of dividing the numerator by the denominator.

        :return: The quotient of this ``Ratio``.
        :raises AttributeError: If the denominator of this ``Ratio`` is zero.
        """
        if self.denominator == 0:
            raise AttributeError("Cannot calculate the quotient of a Ratio with a denominator of zero.")

        return self.numerator / self.denominator
