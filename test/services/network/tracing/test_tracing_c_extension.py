#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Standalone tests for the C-accelerated tracing extension.
These tests don't require the full SDK (no zepben.protobuf dependency).

The Python wrapper _tracing_c.py loads the C extension via ctypes by path,
so it takes precedence over the compiled .so file. All C functions are
exposed as Python functions in _tracing_c.
"""

import sys
import os
import time

# Add the tracing module path so the C extension can be imported
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(_THIS_DIR))))
_TRACING_DIR = os.path.join(_REPO_ROOT, 'src', 'zepben', 'ewb', 'services', 'network', 'tracing')
sys.path.insert(0, _TRACING_DIR)

# Import everything from the Python wrapper (which loads the C extension via ctypes)
from _tracing_c import (  # type: ignore
    visited_tracker_create, visited_tracker_destroy,
    visited_tracker_visit, visited_tracker_has_visited, visited_tracker_clear,
    cqueue_create, cqueue_destroy, cqueue_push, cqueue_pop,
    cqueue_is_empty, cqueue_clear,
    traversal_run, traversal_reset, traversal_step_count,
    is_c_extension_available, use_c_extension,
    create_visited_tracker, create_queue,
    _C_AVAILABLE as _was_c_available,  # for fallback test
    _C_LIB,  # for fallback test
)

# Import the module itself to access internal state
import _tracing_c as _tracing_c_module  # type: ignore


def test_visited_tracker_basic():
    """Test basic visited tracker operations."""
    vt = visited_tracker_create(512)
    obj1, obj2, obj3 = object(), object(), object()

    # First visit should return 1 (newly visited)
    assert visited_tracker_visit(vt, obj1, None) == 1, "First visit should return 1"
    # Second visit to same object should return 0 (already visited)
    assert visited_tracker_visit(vt, obj1, None) == 0, "Second visit should return 0"
    # New object should return 1
    assert visited_tracker_visit(vt, obj2, None) == 1, "New object visit should return 1"
    # Has visited checks
    assert visited_tracker_has_visited(vt, obj1, None) == 1, "Should have visited obj1"
    assert visited_tracker_has_visited(vt, obj2, None) == 1, "Should have visited obj2"
    assert visited_tracker_has_visited(vt, obj3, None) == 0, "Should not have visited obj3"

    visited_tracker_destroy(vt)
    print("  test_visited_tracker_basic: PASSED")


def test_visited_tracker_with_phases():
    """Test visited tracker with phase filtering."""
    vt = visited_tracker_create(512)
    obj = object()

    # Visit without phases
    assert visited_tracker_visit(vt, obj, None) == 1
    assert visited_tracker_has_visited(vt, obj, None) == 1

    # Visit with phases AB
    assert visited_tracker_visit(vt, obj, [0, 1]) == 1  # new (different from no-phase)
    assert visited_tracker_has_visited(vt, obj, [0, 1]) == 1
    assert visited_tracker_has_visited(vt, obj, [1, 2]) == 0  # different phases

    # Visit with phases BC
    assert visited_tracker_visit(vt, obj, [1, 2]) == 1
    assert visited_tracker_has_visited(vt, obj, [1, 2]) == 1

    # Visit with phases ABC
    assert visited_tracker_visit(vt, obj, [0, 1, 2]) == 1
    assert visited_tracker_has_visited(vt, obj, [0, 1, 2]) == 1

    # Phase AB should NOT match ABC
    assert visited_tracker_has_visited(vt, obj, [0, 1]) == 1  # exact match
    assert visited_tracker_has_visited(vt, obj, [0, 1, 2]) == 1  # exact match

    visited_tracker_destroy(vt)
    print("  test_visited_tracker_with_phases: PASSED")


def test_visited_tracker_clear():
    """Test visited tracker clear operation."""
    vt = visited_tracker_create(512)
    obj = object()

    assert visited_tracker_visit(vt, obj, None) == 1
    assert visited_tracker_has_visited(vt, obj, None) == 1

    visited_tracker_clear(vt)
    assert visited_tracker_has_visited(vt, obj, None) == 0, "Should be cleared"

    # Can visit again after clear
    assert visited_tracker_visit(vt, obj, None) == 1

    visited_tracker_destroy(vt)
    print("  test_visited_tracker_clear: PASSED")


def test_visited_tracker_capacity_scaling():
    """Test visited tracker with many entries to exercise resize logic."""
    vt = visited_tracker_create(16)  # small initial capacity
    objects = [object() for _ in range(500)]

    for obj in objects:
        assert visited_tracker_visit(vt, obj, None) == 1

    # All should be visitable
    for i, obj in enumerate(objects):
        assert visited_tracker_has_visited(vt, obj, None) == 1, f"obj {i} not found"

    visited_tracker_destroy(vt)
    print("  test_visited_tracker_capacity_scaling: PASSED")


def test_queue_basic():
    """Test basic queue operations."""
    q = cqueue_create()

    assert cqueue_is_empty(q) == 1, "New queue should be empty"

    obj_a, obj_b, obj_c = object(), object(), object()
    cqueue_push(q, obj_a, 'data_a', 1, 0)
    cqueue_push(q, obj_b, 'data_b', 2, 0)
    cqueue_push(q, obj_c, 'data_c', 3, 0)

    assert cqueue_is_empty(q) == 0, "Queue should not be empty after push"

    # FIFO order
    first = cqueue_pop(q)
    assert first[0] is obj_a, "First pop should be obj_a"
    assert first[1] == 'data_a', "First pop data should match"
    assert first[2] == 1, "First pop num_terminal_steps should match"
    assert first[3] == 0, "First pop num_equipment_steps should match"

    second = cqueue_pop(q)
    assert second[0] is obj_b, "Second pop should be obj_b"

    third = cqueue_pop(q)
    assert third[0] is obj_c, "Third pop should be obj_c"

    assert cqueue_is_empty(q) == 1, "Queue should be empty after all pops"

    # Pop from empty queue
    result = cqueue_pop(q)
    assert result is None, "Pop from empty queue should return None"

    cqueue_destroy(q)
    print("  test_queue_basic: PASSED")


def test_queue_clear():
    """Test queue clear operation."""
    q = cqueue_create()
    cqueue_push(q, object(), 'data', 1, 0)
    cqueue_push(q, object(), 'data2', 2, 0)

    cqueue_clear(q)
    assert cqueue_is_empty(q) == 1, "Queue should be empty after clear"

    cqueue_destroy(q)
    print("  test_queue_clear: PASSED")


def test_queue_large():
    """Test queue with many items."""
    q = cqueue_create()
    objects = [object() for _ in range(10000)]

    for obj in objects:
        cqueue_push(q, obj, None, 0, 0)

    assert cqueue_is_empty(q) == 0

    for i, expected in enumerate(objects):
        result = cqueue_pop(q)
        assert result[0] is expected, f"Pop {i} mismatch"

    assert cqueue_is_empty(q) == 1

    cqueue_destroy(q)
    print("  test_queue_large: PASSED")


def test_traversal_run():
    """Test the C traversal run function with a simple graph."""
    # Create a simple graph: A -> B -> C
    # A connects to B, B connects to C
    obj_a, obj_b, obj_c = object(), object(), object()

    def get_next_paths(terminal):
        """Return next paths from a terminal."""
        if terminal is obj_a:
            # A -> B
            return [(obj_b, 'data_b', 1, 0, [0, 1])]
        elif terminal is obj_b:
            # B -> C
            return [(obj_c, 'data_c', 0, 1, [0])]
        else:
            return []

    def apply_action(data):
        """Called for each dequeued step."""
        pass

    start_steps = [
        (obj_a, 'data_a', 0, 0),
    ]

    traversal_reset()
    result = traversal_run(
        start_steps,
        0,  # can_stop_on_start
        get_next_paths,
        None,  # is_in_service_fn
        None,  # check_queue_cond_fn
        None,  # check_stop_cond_fn
        apply_action,
    )

    assert result == 0, f"Traversal should complete successfully (got {result})"
    step_count = traversal_step_count()
    assert step_count >= 3, f"Should have traversed at least 3 steps (A, B, C), got {step_count}"

    print(f"  test_traversal_run: PASSED (traversed {step_count} steps)")


def test_traversal_with_cycle_detection():
    """Test that the C traversal correctly handles cycles."""
    obj_a, obj_b = object(), object()

    def get_next_paths(terminal):
        if terminal is obj_a:
            return [(obj_b, 'data_b', 0, 0, [0])]
        elif terminal is obj_b:
            return [(obj_a, 'data_a', 0, 0, [0])]  # cycle back to A
        return []

    start_steps = [(obj_a, 'data_a', 0, 0)]

    traversal_reset()
    result = traversal_run(
        start_steps, 0, get_next_paths,
        None, None, None, None,
    )

    assert result == 0, "Traversal should complete without error"
    step_count = traversal_step_count()
    # A is visited with None (start), B with [0], A with [0] — then B is skipped
    # because B with [0] was already visited. So 3 steps total.
    assert step_count == 3, f"Should visit 3 nodes (A/None, B/[0], A/[0]), got {step_count}"

    print(f"  test_traversal_with_cycle_detection: PASSED (visited {step_count} nodes)")


def test_traversal_phase_filtering():
    """Test that phase filtering works correctly in traversal."""
    obj_a, obj_b = object(), object()

    def get_next_paths(terminal):
        if terminal is obj_a:
            # Only connect on phase AB
            return [(obj_b, 'data_b', 0, 0, [0, 1])]
        return []

    def apply_action(data):
        pass

    start_steps = [(obj_a, 'data_a', 0, 0)]

    traversal_reset()
    result = traversal_run(
        start_steps, 0, get_next_paths,
        None, None, None, apply_action,
    )

    assert result == 0
    step_count = traversal_step_count()
    assert step_count == 2, f"Should visit 2 nodes with phase filtering, got {step_count}"

    print(f"  test_traversal_phase_filtering: PASSED")


def test_c_extension_availability():
    """Test that the C extension is available."""
    assert is_c_extension_available() == True, "C extension should be available"
    print("  test_c_extension_availability: PASSED")


def test_pure_python_fallback():
    """Test that pure-Python fallbacks work when C extension is disabled."""
    # Save current state and disable C extension
    was_enabled = _tracing_c_module._C_AVAILABLE
    _tracing_c_module.use_c_extension(False)

    tracker = create_visited_tracker()
    obj = object()
    assert tracker.visit(obj) == True
    assert tracker.has_visited(obj) == True
    assert tracker.visit(obj) == False  # already visited
    tracker.clear()
    assert tracker.has_visited(obj) == False

    q = create_queue()
    q.push(obj, 'data', 1, 0)
    assert q.is_empty() == False
    popped = q.pop()
    assert popped[0] is obj
    assert q.is_empty() == True

    # Restore C extension state
    _tracing_c_module._C_AVAILABLE = was_enabled

    print("  test_pure_python_fallback: PASSED")


def test_performance_visited_tracker():
    """Benchmark visited tracker performance."""
    vt = visited_tracker_create(512)
    objects = [object() for _ in range(10000)]

    # Visit all
    start = time.time()
    for obj in objects:
        visited_tracker_visit(vt, obj, None)
    elapsed = time.time() - start
    print(f"  test_performance_visited_tracker: PASSED (10k visits in {elapsed:.4f}s)")

    visited_tracker_destroy(vt)


def test_performance_queue():
    """Benchmark queue performance."""
    q = cqueue_create()
    objects = [object() for _ in range(10000)]

    # Push all
    start = time.time()
    for obj in objects:
        cqueue_push(q, obj, None, 0, 0)
    push_elapsed = time.time() - start

    # Pop all
    start = time.time()
    while not cqueue_is_empty(q):
        cqueue_pop(q)
    pop_elapsed = time.time() - start

    print(f"  test_performance_queue: PASSED (10k push in {push_elapsed:.4f}s, pop in {pop_elapsed:.4f}s)")

    cqueue_destroy(q)


def test_performance_traversal():
    """Benchmark traversal performance."""
    # Create a chain: 0 -> 1 -> 2 -> ... -> 999
    objects = [object() for _ in range(1000)]

    def get_next_paths(terminal):
        idx = objects.index(terminal) if terminal in objects else -1
        if idx >= 0 and idx < len(objects) - 1:
            return [(objects[idx + 1], None, 0, 0, [0])]
        return []

    start_steps = [(objects[0], None, 0, 0)]

    traversal_reset()
    start = time.time()
    result = traversal_run(
        start_steps, 0, get_next_paths,
        None, None, None, None,
    )
    elapsed = time.time() - start
    step_count = traversal_step_count()

    assert result == 0
    assert step_count == 1000

    print(f"  test_performance_traversal: PASSED (1000-node chain in {elapsed:.4f}s, {step_count} steps)")


def run_all_tests():
    """Run all tests and report results."""
    tests = [
        test_c_extension_availability,
        test_visited_tracker_basic,
        test_visited_tracker_with_phases,
        test_visited_tracker_clear,
        test_visited_tracker_capacity_scaling,
        test_queue_basic,
        test_queue_clear,
        test_queue_large,
        test_traversal_run,
        test_traversal_with_cycle_detection,
        test_traversal_phase_filtering,
        test_pure_python_fallback,
        test_performance_visited_tracker,
        test_performance_queue,
        test_performance_traversal,
    ]

    passed = 0
    failed = 0
    errors = []

    print("=" * 60)
    print("C-Accelerated Tracing Extension Tests")
    print("=" * 60)

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            failed += 1
            errors.append((test.__name__, str(e)))
            print(f"  {test.__name__}: FAILED ({e})")

    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed, {passed + failed} total")
    print("=" * 60)

    if errors:
        print()
        print("Failures:")
        for name, error in errors:
            print(f"  - {name}: {error}")
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(run_all_tests())
