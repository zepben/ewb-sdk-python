#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
C-accelerated network tracing extension.

This module provides a ctypes-based bridge to the C implementation of
the hot-path data structures (visited tracker, queue) used in network
traversal. When the C extension is available, it is used transparently
to speed up the traversal loop.

Build:
    gcc -shared -fPIC -O2 -Wall -std=c11 \
      -I$(python3-config --includes | grep -oP '(?<=-I)[^ ]+') \
      src/zepben/ewb/services/network/tracing/_tracing_c.c \
      -o src/zepben/ewb/services/network/tracing/_tracing_c_ext/_tracing_c.cpython-313-x86_64-linux-gnu.so

Usage:
    from zepben.ewb.services.network.tracing._tracing_c import (
        use_c_extension, is_c_extension_available, create_visited_tracker, create_queue
    )
    use_c_extension(True)  # Enable C extension
"""

__all__ = [
    'use_c_extension', 'is_c_extension_available',
    'create_visited_tracker', 'create_queue',
    # C-level functions (for testing / direct use)
    'visited_tracker_create', 'visited_tracker_destroy',
    'visited_tracker_visit', 'visited_tracker_has_visited', 'visited_tracker_clear',
    'cqueue_create', 'cqueue_destroy', 'cqueue_push', 'cqueue_pop',
    'cqueue_is_empty', 'cqueue_clear',
    'traversal_run', 'traversal_reset', 'traversal_step_count',
]

import os
from typing import Optional, Tuple

# ---------------------------------------------------------------------------
# Try to import the native C extension from the subpackage
# ---------------------------------------------------------------------------

_C_AVAILABLE = False
_C_LIB = None

try:
    from _tracing_c_ext import _tracing_c as _C_LIB  # type: ignore
    _C_AVAILABLE = True
except ImportError:
    pass


def is_c_extension_available() -> bool:
    """Return True if the C extension compiled and loaded successfully."""
    return _C_AVAILABLE


def use_c_extension(enabled: Optional[bool] = None) -> bool:
    """
    Enable or disable the C extension for tracing.

    * enabled=True  – force use (raises if unavailable)
    * enabled=False – force pure-Python
    * enabled=None  – auto-detect (default: use C if available)

    Returns the effective state after the call.
    """
    global _C_AVAILABLE
    if enabled is None:
        return _C_AVAILABLE
    if enabled and not _C_AVAILABLE:
        raise RuntimeError(
            "C tracing extension not available. "
            "Compile with: gcc -shared -fPIC -O2 -Wall -std=c11 "
            "-I$(python3-config --includes | grep -oP '(?<=-I)[^ ]+') "
            "src/zepben/ewb/services/network/tracing/_tracing_c.c "
            "-o src/zepben/ewb/services/network/tracing/_tracing_c_ext/_tracing_c.cpython-313-x86_64-linux-gnu.so"
        )
    _C_AVAILABLE = bool(enabled)
    return _C_AVAILABLE


# ---------------------------------------------------------------------------
# C-level function wrappers (for testing / direct use)
# ---------------------------------------------------------------------------

def visited_tracker_create(capacity: int = 512) -> int:
    """Create a C-accelerated visited tracker. Returns opaque handle."""
    if not _C_AVAILABLE or _C_LIB is None:
        raise RuntimeError("C extension not available")
    return _C_LIB.visited_tracker_create(capacity)


def visited_tracker_destroy(handle: int) -> None:
    _C_LIB.visited_tracker_destroy(handle)


def visited_tracker_visit(handle: int, terminal: object, phases: Optional[Tuple] = None) -> bool:
    result = _C_LIB.visited_tracker_visit(handle, terminal, phases)
    return result == 1


def visited_tracker_has_visited(handle: int, terminal: object, phases: Optional[Tuple] = None) -> bool:
    result = _C_LIB.visited_tracker_has_visited(handle, terminal, phases)
    return result == 1


def visited_tracker_clear(handle: int) -> None:
    _C_LIB.visited_tracker_clear(handle)


def cqueue_create() -> int:
    return _C_LIB.cqueue_create()


def cqueue_destroy(handle: int) -> None:
    _C_LIB.cqueue_destroy(handle)


def cqueue_push(handle: int, item: object, data: object = None,
                num_terminal_steps: int = 0, num_equipment_steps: int = 0) -> None:
    _C_LIB.cqueue_push(handle, item, data, num_terminal_steps, num_equipment_steps)


def cqueue_pop(handle: int):
    return _C_LIB.cqueue_pop(handle)


def cqueue_is_empty(handle: int) -> bool:
    return _C_LIB.cqueue_is_empty(handle) == 1


def cqueue_clear(handle: int) -> None:
    _C_LIB.cqueue_clear(handle)


def traversal_run(start_steps, can_stop_on_start, get_next_paths_fn,
                  is_in_service_fn=None, check_queue_cond_fn=None,
                  check_stop_cond_fn=None, apply_action_fn=None) -> int:
    return _C_LIB.traversal_run(
        start_steps, can_stop_on_start, get_next_paths_fn,
        is_in_service_fn, check_queue_cond_fn,
        check_stop_cond_fn, apply_action_fn,
    )


def traversal_reset() -> None:
    _C_LIB.traversal_reset()


def traversal_step_count() -> int:
    return _C_LIB.traversal_step_count()


# ---------------------------------------------------------------------------
# Python-side wrappers (high-level)
# ---------------------------------------------------------------------------

class _VisitedTracker:
    """C-accelerated visited tracker."""

    __slots__ = ('_handle',)

    def __init__(self, capacity: int = 512):
        self._handle = visited_tracker_create(capacity)

    def has_visited(self, terminal: object, phases: Optional[Tuple] = None) -> bool:
        return visited_tracker_has_visited(self._handle, terminal, phases)

    def visit(self, terminal: object, phases: Optional[Tuple] = None) -> bool:
        return visited_tracker_visit(self._handle, terminal, phases)

    def clear(self):
        visited_tracker_clear(self._handle)

    def __del__(self):
        if hasattr(self, '_handle') and self._handle:
            visited_tracker_destroy(self._handle)
            self._handle = None


class _CQueue:
    """C-accelerated FIFO queue."""

    __slots__ = ('_handle',)

    def __init__(self):
        self._handle = cqueue_create()

    def push(self, item: object, data: object = None,
             num_terminal_steps: int = 0, num_equipment_steps: int = 0):
        cqueue_push(self._handle, item, data, num_terminal_steps, num_equipment_steps)

    def pop(self):
        return cqueue_pop(self._handle)

    def is_empty(self) -> bool:
        return cqueue_is_empty(self._handle)

    def clear(self):
        cqueue_clear(self._handle)

    def __del__(self):
        if hasattr(self, '_handle') and self._handle:
            cqueue_destroy(self._handle)
            self._handle = None


# ---------------------------------------------------------------------------
# Pure-Python fallbacks
# ---------------------------------------------------------------------------

class _PythonVisitedTracker:
    """Pure-Python fallback for visited tracker."""

    __slots__ = ('_visited',)

    def __init__(self, capacity: int = 512):
        self._visited = set()

    def has_visited(self, terminal: object, phases: Optional[Tuple] = None) -> bool:
        key = (id(terminal), phases) if phases else id(terminal)
        return key in self._visited

    def visit(self, terminal: object, phases: Optional[Tuple] = None) -> bool:
        key = (id(terminal), phases) if phases else id(terminal)
        if key not in self._visited:
            self._visited.add(key)
            return True
        return False

    def clear(self):
        self._visited.clear()


class _PythonQueue:
    """Pure-Python fallback for FIFO queue."""

    __slots__ = ('_queue',)

    def __init__(self):
        from collections import deque
        self._queue = deque()

    def push(self, item: object, data: object = None,
             num_terminal_steps: int = 0, num_equipment_steps: int = 0):
        self._queue.append((item, data, num_terminal_steps, num_equipment_steps))

    def pop(self):
        if self._queue:
            return self._queue.popleft()
        return None

    def is_empty(self) -> bool:
        return len(self._queue) == 0

    def clear(self):
        self._queue.clear()


# ---------------------------------------------------------------------------
# Public factory functions
# ---------------------------------------------------------------------------

def create_visited_tracker(capacity: int = 512):
    """Create a C-accelerated visited tracker, or pure-Python fallback."""
    if _C_AVAILABLE and _C_LIB is not None:
        return _VisitedTracker(capacity)
    return _PythonVisitedTracker(capacity)


def create_queue():
    """Create a C-accelerated FIFO queue, or pure-Python fallback."""
    if _C_AVAILABLE and _C_LIB is not None:
        return _CQueue()
    return _PythonQueue()
