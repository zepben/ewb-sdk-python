#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TapChanger"]

from typing import Optional, TYPE_CHECKING

from zepben.ewb.dataslot import dataslot, ValidatedDescriptor, validate
from zepben.ewb.model.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.ewb.util import require

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.wires.tap_changer_control import TapChangerControl


@dataslot
class TapChanger(PowerSystemResource):
    """
    Mechanism for changing transformer winding tap positions.
    """

    control_enabled: bool | None = None
    """Specifies the regulation status of the equipment.  True is regulating, false is not regulating."""

    neutral_u: int | None = None
    """Voltage at which the winding operates at the neutral tap setting."""

    tap_changer_control: Optional['TapChangerControl'] = None
    """The regulating control scheme in which this tap changer participates."""

    high_step: int | None = ValidatedDescriptor(None)
    low_step: int | None = ValidatedDescriptor(None)
    neutral_step: int | None = ValidatedDescriptor(None)
    normal_step: int | None = ValidatedDescriptor(None)
    step: float | None = ValidatedDescriptor(None)

    @validate(high_step)
    def _high_step_validate(self, val):
        require((val is None) or (self.low_step is None) or (val > self.low_step),
                lambda: f"High step [{val}] must be greater than low step [{self.low_step}]")
        self._check_steps(self.low_step, val)
        return val

    @validate(low_step)
    def _low_step_validate(self, val):
        require((val is None) or (self.high_step is None) or (val < self.high_step),
                lambda: f"Low step [{val}] must be less than high step [{self.high_step}]")
        self._check_steps(val, self.high_step)
        return val

    @validate(neutral_step)
    def _neutral_step_validate(self, val):
        require(self._is_in_range(val), lambda: f"Neutral step [{val}] must be between high step [{self.high_step}] and low step [{self.low_step}]")
        return val

    @validate(normal_step)
    def _normal_step_validate(self, val):
        require(self._is_in_range(val), lambda: f"Normal step [{val}] must be between high step [{self.high_step}] and low step [{self.low_step}]")
        return val

    @validate(step)
    def _step_validate(self, val):
        require(self._is_in_range(val), lambda: f"Step [{val}] must be between high step [{self.high_step}] and low step [{self.low_step}]")
        return val

    def _check_steps(self, low, high):
        if low is not None:
            require((self.step is None) or (low <= self.step), lambda: f"New value would invalidate current step of [{self.step}]")
            require((self.normal_step is None) or (low <= self.normal_step), lambda: f"New value would invalidate current normal_step of [{self.normal_step}]")
            require((self.neutral_step is None) or (low <= self.neutral_step),
                    lambda: f"New value would invalidate current neutral_step of [{self.neutral_step}]")

        if high is not None:
            require((self.step is None) or (self.step <= high), lambda: f"New value would invalidate current step of [{self.step}]")
            require((self.normal_step is None) or (self.normal_step <= high), lambda: f"New value would invalidate current normal_step of [{self.normal_step}]")
            require((self.neutral_step is None) or (self.neutral_step <= high),
                    lambda: f"New value would invalidate current neutral_step of [{self.neutral_step}]")

    def _validate_steps(self):
        require((self.high_step is None) or (self.low_step is None) or (self.high_step > self.low_step),
                lambda: f"High step [{self.high_step}] must be greater than low step [{self.low_step}]")
        require(self._is_in_range(self.neutral_step),
                lambda: f"Neutral step [{self.neutral_step}] must be between high step [{self.high_step}] and low step [{self.low_step}]")
        require(self._is_in_range(self.normal_step),
                lambda: f"Normal step [{self.normal_step}] must be between high step [{self.high_step}] and low step [{self.low_step}]")
        require(self._is_in_range(self.step), lambda: f"Step [{self.step}] must be between high step [{self.high_step}] and low step [{self.low_step}]")

    def _is_in_range(self, val) -> bool:
        if val is None:
            return True

        if self.low_step is not None:
            if val < self.low_step:
                return False

        if self.high_step is not None:
            if val > self.high_step:
                return False

        return True
