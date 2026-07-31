#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import TYPE_CHECKING

from zepben.ewb.boilerplate.collections.lazy_mrid_list import LazyMridList
if TYPE_CHECKING:
    from zepben.ewb import PowerTransformerEnd, Terminal


class PowerTransformerEndList(LazyMridList['PowerTransformerEnd']):

    def get_by_num(self, end_number: int) -> PowerTransformerEnd:
        """
        Get the `PowerTransformerEnd` on this `PowerTransformer` by its `end_number`.

        `end_number` The `end_number` of the `PowerTransformerEnd` in relation to this `PowerTransformer`s VectorGroup.
        Returns The `PowerTransformerEnd` referred to by `end_number`
        Raises IndexError if no `PowerTransformerEnd` was found with end_number `end_number`.
        """
        end = next((it for it in self if it.end_number == end_number), None)
        if end:
            return end
        raise IndexError(f"No TransformerEnd with end_number {end_number} was found in PowerTransformer {str(self._instance)}")

    def get_by_terminal(self, terminal: Terminal) -> PowerTransformerEnd:
        """
        Get the `PowerTransformerEnd` on this `PowerTransformer` by its `terminal`.

        `terminal` The `terminal` to find a `PowerTransformerEnd` for.
        Returns The `PowerTransformerEnd` connected to the specified `terminal`
        Raises IndexError if no `PowerTransformerEnd` connected to `terminal` was found on this `PowerTransformer`.
        """

        end = next((it for it in self if it.terminal == terminal), None)
        if end:
            return end
        raise IndexError(f"No TransformerEnd with terminal {terminal} was found in PowerTransformer {str(self._instance)}")
