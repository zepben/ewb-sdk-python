#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TapChanger"]

from typing import Optional, TYPE_CHECKING

from zepben.ewb.model.cim.iec61970.base.core.power_system_resource import PowerSystemResource
from zepben.ewb.util import require

if TYPE_CHECKING:
    from zepben.ewb.model.cim.iec61970.base.wires.tap_changer_control import TapChangerControl


class TapChanger(PowerSystemResource):
    """
    Mechanism for changing transformer winding tap positions.
    """

    control_enabled: Optional[bool] = None
    """Specifies the regulation status of the equipment.  True is regulating, false is not regulating."""

    neutral_u: Optional[int] = None
    """Voltage at which the winding operates at the neutral tap setting."""

    tap_changer_control: Optional['TapChangerControl'] = None
    """The regulating control scheme in which this tap changer participates."""

    _high_step: Optional[int] = None
    _low_step: Optional[int] = None
    _neutral_step: Optional[int] = None
    _normal_step: Optional[int] = None
    _step: Optional[float] = None

    def __init__(self, high_step: int = None, low_step: int = None, neutral_step: int = None, normal_step: int = None, step: float = None, **kwargs):
        super(TapChanger, self).__init__(**kwargs)
        if high_step is not None:
            self._high_step = high_step
        if low_step is not None:
            self._low_step = low_step
        if neutral_step is not None:
            self._neutral_step = neutral_step
        if normal_step is not None:
            self._normal_step = normal_step
        if step is not None:
            self._step = step
        self._validate_steps()

    @property
    def high_step(self):
        """
        Highest possible tap step position, advance from neutral. The attribute shall be greater than lowStep. This tap position results in the
        maximum voltage boost on secondary winding(s).
        """
        return self._high_step

    @high_step.setter
    def high_step(self, val):
        require((val is None) or (self._low_step is None) or (val > self._low_step),
                lambda: f"High step [{val}] must be greater than low step [{self._low_step}]")
        self._check_steps(self.low_step, val)
        self._high_step = val

    @property
    def low_step(self):
        """Lowest possible tap step position, retard from neutral. This tap position results in the maximum voltage buck on secondary winding(s)."""
        return self._low_step

    @low_step.setter
    def low_step(self, val):
        require((val is None) or (self._high_step is None) or (val < self._high_step),
                lambda: f"Low step [{val}] must be less than high step [{self._high_step}]")
        self._check_steps(val, self.high_step)
        self._low_step = val

    @property
    def neutral_step(self):
        """The neutral tap step position for this winding. The attribute shall be equal or greater than lowStep and equal or less than highStep."""
        return self._neutral_step

    @neutral_step.setter
    def neutral_step(self, val):
        require(self._is_in_range(val), lambda: f"Neutral step [{val}] must be between high step [{self._high_step}] and low step [{self._low_step}]")
        self._neutral_step = val

    @property
    def normal_step(self):
        """
        The tap step position used in "normal" network operation for this winding. For a "Fixed" tap changer indicates the current physical tap setting.
        The attribute shall be equal or greater than lowStep and equal or less than highStep.
        """
        return self._normal_step

    @normal_step.setter
    def normal_step(self, val):
        require(self._is_in_range(val), lambda: f"Normal step [{val}] must be between high step [{self._high_step}] and low step [{self._low_step}]")
        self._normal_step = val

    @property
    def step(self):
        """
        Tap changer position. Starting step for a steady state solution. Non integer values are allowed to support continuous tap variables.
        The reasons for continuous value are to support study cases where no discrete tap changers has yet been designed, a solutions where a narrow voltage
        band force the tap step to oscillate or accommodate for a continuous solution as input.
        The attribute shall be equal or greater than lowStep and equal or less than highStep.
        """
        return self._step

    @step.setter
    def step(self, val):
        require(self._is_in_range(val), lambda: f"Step [{val}] must be between high step [{self._high_step}] and low step [{self._low_step}]")
        self._step = val

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
        require((self._high_step is None) or (self._low_step is None) or (self._high_step > self._low_step),
                lambda: f"High step [{self._high_step}] must be greater than low step [{self._low_step}]")
        require(self._is_in_range(self._neutral_step),
                lambda: f"Neutral step [{self.neutral_step}] must be between high step [{self._high_step}] and low step [{self._low_step}]")
        require(self._is_in_range(self._normal_step),
                lambda: f"Normal step [{self.normal_step}] must be between high step [{self._high_step}] and low step [{self._low_step}]")
        require(self._is_in_range(self._step), lambda: f"Step [{self._step}] must be between high step [{self._high_step}] and low step [{self._low_step}]")

    def _is_in_range(self, val) -> bool:
        if val is None:
            return True

        if self._low_step is not None:
            if val < self._low_step:
                return False

        if self._high_step is not None:
            if val > self._high_step:
                return False

        return True
