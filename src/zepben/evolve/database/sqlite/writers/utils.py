#  Copyright 2021 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging
from sqlite3 import Cursor
from typing import Optional, Callable, Any

from zepben.evolve import PreparedStatement

logger = logging.getLogger("metadata_entry_writer")


def validate_save(it, saver: Callable[[Any], bool], on_save_failure: Callable[[Exception], None]) -> bool:
    try:
        return saver(it)
    except Exception as e:
        on_save_failure(e)
        return False


def try_execute_single_update(query: PreparedStatement, cursor: Cursor, description: str, on_error: Optional[Callable[[], None]] = None) -> bool:
    """
    Execute an update on the database with the given `query`.
    Failures will be logged as warnings.
    `query` The PreparedStatement to execute.
    `id` The mRID of the relevant object that is being saved
    `description` A description of the type of object (e.g AcLineSegment)
    Returns True if the execute was successful, False otherwise.
    """
    try:
        query.execute(cursor)
        return True
    except Exception as de:
        if on_error:
            on_error()
        logger.warning(f"Failed to save {description}. Error was: {de}\n  SQL: {query}\n  Fields: {query.parameters}")
        return False
