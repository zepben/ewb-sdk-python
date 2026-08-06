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
    """A list of ``PowerTransformerEnd`` objects for a transformer."""

    def get_by_num(self, end_number: int) -> PowerTransformerEnd:
        """Return a transformer end by its end number.

        :param end_number: The number of the required transformer end.
        :raises IndexError: If no transformer end has the requested number.
        """
        end = next((it for it in self if it.end_number == end_number), None)
        if end:
            return end
        raise IndexError(f"No TransformerEnd with end_number {end_number} was found in PowerTransformer {str(self._instance)}")

    def get_by_terminal(self, terminal: Terminal) -> PowerTransformerEnd:
        """Return a transformer end by its terminal.

        :param terminal: The terminal of the required transformer end.
        :raises IndexError: If no transformer end uses ``terminal``.
        """

        end = next((it for it in self if it.terminal == terminal), None)
        if end:
            return end
        raise IndexError(f"No TransformerEnd with terminal {terminal} was found in PowerTransformer {str(self._instance)}")
