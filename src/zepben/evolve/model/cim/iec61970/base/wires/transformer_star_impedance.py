#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import Optional, Callable, TYPE_CHECKING

from dataclassy import dataclass

if TYPE_CHECKING:
    from zepben.evolve.model.cim.iec61968.assetinfo.transformer_end_info import TransformerEndInfo

from zepben.evolve.model.cim.iec61970.base.core.identified_object import IdentifiedObject

__all__ = ["TransformerStarImpedance", "ResistanceReactance"]


@dataclass(slots=True)
class ResistanceReactance(object):
    r: Optional[float] = None
    r0: Optional[float] = None
    x: Optional[float] = None
    x0: Optional[float] = None

    def is_complete(self) -> bool:
        return self.r is not None and self.r0 is not None and self.x is not None and self.x0 is not None

    def merge_if_incomplete(self, to_merge: Callable[[], Optional[ResistanceReactance]]) -> ResistanceReactance:
        if self.is_complete():
            return self
        else:
            rr = to_merge()
            if rr is not None:
                return ResistanceReactance(self.r if self.r is not None else rr.r,
                                           self.r0 if self.r0 is not None else rr.r0,
                                           self.x if self.x is not None else rr.x,
                                           self.x0 if self.x0 is not None else rr.x0)
            else:
                return self


class TransformerStarImpedance(IdentifiedObject):
    """
    Transformer star impedance (Pi-model) that accurately reflects impedance for transformers with 2 or 3 windings. For transformers with 4 or more windings,
    TransformerMeshImpedance class shall be used.
    For transmission networks use PowerTransformerEnd impedances (r, r0, x, x0, b, b0, g and g0).
    """

    r: Optional[float] = 0.0
    """ r : Resistance of the transformer end. Unit: Ohms  """

    r0: Optional[float] = 0.0
    """ r0 : Zero sequence series resistance of the transformer end. Unit: Ohms"""

    x: Optional[float] = 0.0
    """ x : Positive sequence series reactance  of the transformer end. Unit: Ohms"""

    x0: Optional[float] = 0.0
    """ x0 : Zero sequence series reactance of the transformer end. Unit: Ohms"""

    transformer_end_info: Optional[TransformerEndInfo] = None
    """Transformer end datasheet used to calculate this transformer star impedance."""

    def resistance_reactance(self) -> ResistanceReactance:
        """
        Get the `ResistanceReactance` for this `TransformerStarImpedance`. If any values are missing
        attempt to calculate them from the `TransformerEndInfo` tests.
        Returns the `ResistanceReactance` for this `TransformerStarImpedance`
        """
        return ResistanceReactance(self.r, self.r0, self.x, self.x0).merge_if_incomplete(
            lambda: self.transformer_end_info.calculate_resistance_reactance_from_tests() if self.transformer_end_info is not None else None
        )
