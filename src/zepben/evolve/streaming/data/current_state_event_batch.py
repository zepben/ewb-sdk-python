#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
__all__ = ["CurrentStateEventBatch"]

from dataclasses import dataclass
from typing import Iterable

from zepben.evolve.streaming.data.current_state_event import CurrentStateEvent


@dataclass
class CurrentStateEventBatch:
    """
    A collection of events that should be operated on as a batch.

    Attributes:
        batch_id: A unique identifier for the batch of events being processed. This allows tracking or grouping multiple events under a single batch.
        events: A list of `CurrentStateEvent` objects representing the state changes or events that are being submitted in the current batch.
    """

    batch_id: int
    events: Iterable[CurrentStateEvent]
