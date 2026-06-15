/*
 * Copyright 2025 Zeppelin Bend Pty Ltd
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 *
 * _tracing_c.c — C-accelerated network tracing engine.
 */

#include <Python.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

typedef enum {
    SPK_A = 0, SPK_B = 1, SPK_C = 2, SPK_N = 3,
    SPK_AB = 4, SPK_BC = 5, SPK_AC = 6, SPK_ABC = 7, SPK_NONE = 8
} SinglePhaseKind;

typedef struct {
    PyObject* terminal;
    SinglePhaseKind* phases;
    int phase_count;
    bool occupied;
} VisitedEntry;

typedef struct {
    VisitedEntry* entries;
    int capacity;
    int size;
} VisitedTracker;

typedef struct CStep {
    PyObject* terminal;
    PyObject* data;
    int num_terminal_steps;
    int num_equipment_steps;
    struct CStep* next;
} CStep;

typedef struct {
    CStep* head;
    CStep* tail;
    int size;
} CQueue;

/* ------------------------------------------------------------------ */
/*  VisitedTracker functions                                          */
/* ------------------------------------------------------------------ */

static unsigned long _visited_hash(PyObject* terminal,
                                    const SinglePhaseKind* phases,
                                    int phase_count) {
    long h = PyObject_Hash(terminal);
    if (h == -1) h = (long)(uintptr_t)terminal;
    unsigned long hash = (unsigned long)h;
    if (phases && phase_count > 0) {
        /* Hash the phase VALUES, not the array address, so that
           (terminal, [0]) always hashes to the same bucket regardless
           of where the phases array lives in memory. */
        for (int i = 0; i < phase_count; i++) {
            hash ^= (unsigned long)phases[i];
            hash *= 0x9e3779b97f4a7c15UL;
        }
    }
    return hash;
}

static int _visited_index(unsigned long hash, int capacity) {
    return (int)(hash & (unsigned long)(capacity - 1));
}

static int _visited_resize(VisitedTracker* tracker) {
    int old_cap = tracker->capacity;
    VisitedEntry* old_entries = tracker->entries;
    int new_cap = old_cap * 2;
    tracker->entries = (VisitedEntry*)calloc((size_t)new_cap, sizeof(VisitedEntry));
    if (!tracker->entries) {
        tracker->entries = old_entries;
        return -1;
    }
    tracker->capacity = new_cap;
    tracker->size = 0;
    for (int i = 0; i < old_cap; i++) {
        if (old_entries[i].occupied) {
            VisitedEntry* src = &old_entries[i];
            unsigned long hash = _visited_hash(src->terminal, src->phases, src->phase_count);
            int idx = _visited_index(hash, new_cap);
            /* Linear probe with safety limit to avoid infinite loops */
            int probes = 0;
            while (tracker->entries[idx].occupied && probes < new_cap) {
                idx = (idx + 1) & (new_cap - 1);
                probes++;
            }
            /* Allocate new phases array for the new entry */
            SinglePhaseKind* new_phases = NULL;
            if (src->phases && src->phase_count > 0) {
                new_phases = (SinglePhaseKind*)malloc(
                    (size_t)src->phase_count * sizeof(SinglePhaseKind));
                if (new_phases) {
                    memcpy(new_phases, src->phases,
                           (size_t)src->phase_count * sizeof(SinglePhaseKind));
                }
            }
            tracker->entries[idx].terminal = src->terminal;
            tracker->entries[idx].phases = new_phases;
            tracker->entries[idx].phase_count = src->phase_count;
            tracker->entries[idx].occupied = true;
            tracker->size++;
        }
    }
    /* Free old entries' phases pointers and the old array */
    for (int i = 0; i < old_cap; i++) {
        if (old_entries[i].occupied && old_entries[i].phases) {
            free(old_entries[i].phases);
        }
    }
    free(old_entries);
    return 0;
}

static VisitedTracker* _visited_tracker_create(int initial_capacity) {
    int cap = 512;
    while (cap < initial_capacity) cap *= 2;
    VisitedTracker* tracker = (VisitedTracker*)malloc(sizeof(VisitedTracker));
    if (!tracker) return NULL;
    tracker->entries = (VisitedEntry*)calloc((size_t)cap, sizeof(VisitedEntry));
    if (!tracker->entries) { free(tracker); return NULL; }
    tracker->capacity = cap;
    tracker->size = 0;
    return tracker;
}

static void _visited_tracker_destroy(VisitedTracker* tracker) {
    if (!tracker) return;
    if (tracker->entries) {
        for (int i = 0; i < tracker->capacity; i++) {
            if (tracker->entries[i].occupied) {
                if (tracker->entries[i].phases) free(tracker->entries[i].phases);
            }
        }
        free(tracker->entries);
    }
    free(tracker);
}

static int _visited_tracker_has_visited(VisitedTracker* tracker, PyObject* terminal,
                                         const SinglePhaseKind* phases, int phase_count) {
    if (!tracker || !terminal) return -1;
    unsigned long hash = _visited_hash(terminal, phases, phase_count);
    int idx = _visited_index(hash, tracker->capacity);
    while (tracker->entries[idx].occupied) {
        VisitedEntry* e = &tracker->entries[idx];
        if (e->terminal == terminal) {
            /* Phase key must match: NULL vs non-NULL, or exact phase values */
            if (!e->phases && !phases) return 1;
            if (e->phases && phases && e->phase_count == phase_count) {
                bool match = true;
                for (int i = 0; i < phase_count; i++) {
                    if (e->phases[i] != phases[i]) { match = false; break; }
                }
                if (match) return 1;
            }
        }
        idx = (idx + 1) & (tracker->capacity - 1);
    }
    return 0;
}

static int _visited_tracker_visit(VisitedTracker* tracker, PyObject* terminal,
                                   const SinglePhaseKind* phases, int phase_count) {
    if (!tracker || !terminal) return -1;
    unsigned long hash = _visited_hash(terminal, phases, phase_count);
    int idx = _visited_index(hash, tracker->capacity);
    while (tracker->entries[idx].occupied) {
        VisitedEntry* e = &tracker->entries[idx];
        if (e->terminal == terminal) {
            /* Phase key must match: NULL vs non-NULL, or exact phase values */
            if (!e->phases && !phases) return 0;
            if (e->phases && phases && e->phase_count == phase_count) {
                bool match = true;
                for (int i = 0; i < phase_count; i++) {
                    if (e->phases[i] != phases[i]) { match = false; break; }
                }
                if (match) return 0;
            }
        }
        idx = (idx + 1) & (tracker->capacity - 1);
    }
    if (tracker->size >= tracker->capacity * 3 / 4) {
        if (_visited_resize(tracker) < 0) return -1;
        hash = _visited_hash(terminal, phases, phase_count);
        idx = _visited_index(hash, tracker->capacity);
    }
    VisitedEntry* e = &tracker->entries[idx];
    e->terminal = terminal;
    if (phases && phase_count > 0) {
        e->phases = (SinglePhaseKind*)malloc((size_t)phase_count * sizeof(SinglePhaseKind));
        if (!e->phases) return -1;
        memcpy(e->phases, phases, (size_t)phase_count * sizeof(SinglePhaseKind));
        e->phase_count = phase_count;
    } else {
        e->phases = NULL;
        e->phase_count = 0;
    }
    e->occupied = true;
    tracker->size++;
    return 1;
}

static void _visited_tracker_clear(VisitedTracker* tracker) {
    if (!tracker) return;
    for (int i = 0; i < tracker->capacity; i++) {
        if (tracker->entries[i].occupied) {
            if (tracker->entries[i].phases) {
                free(tracker->entries[i].phases);
                tracker->entries[i].phases = NULL;
            }
            tracker->entries[i].terminal = NULL;
        }
        tracker->entries[i].occupied = false;
    }
    tracker->size = 0;
}

/* ------------------------------------------------------------------ */
/*  Queue functions                                                   */
/* ------------------------------------------------------------------ */

static CQueue* _cqueue_create(void) {
    CQueue* queue = (CQueue*)malloc(sizeof(CQueue));
    if (!queue) return NULL;
    queue->head = NULL;
    queue->tail = NULL;
    queue->size = 0;
    return queue;
}

static void _cqueue_destroy(CQueue* queue) {
    if (!queue) return;
    CStep* current = queue->head;
    while (current) {
        CStep* next = current->next;
        free(current);
        current = next;
    }
    free(queue);
}

static void _cqueue_push(CQueue* queue, PyObject* terminal, PyObject* data,
                 int num_terminal_steps, int num_equipment_steps) {
    if (!queue || !terminal) return;
    CStep* step = (CStep*)malloc(sizeof(CStep));
    if (!step) return;
    step->terminal = terminal;
    step->data = data;
    step->num_terminal_steps = num_terminal_steps;
    step->num_equipment_steps = num_equipment_steps;
    step->next = NULL;
    if (!queue->tail) {
        queue->head = step;
        queue->tail = step;
    } else {
        queue->tail->next = step;
        queue->tail = step;
    }
    queue->size++;
}

static PyObject* _cqueue_pop(CQueue* queue) {
    if (!queue || !queue->head) {
        Py_INCREF(Py_None);
        return Py_None;
    }
    CStep* step = queue->head;
    queue->head = step->next;
    if (!queue->head) queue->tail = NULL;
    PyObject* terminal = step->terminal;
    PyObject* data = step->data;
    int num_terminal_steps = step->num_terminal_steps;
    int num_equipment_steps = step->num_equipment_steps;
    PyObject* result = Py_BuildValue("(OOii)", terminal, data,
                                      num_terminal_steps, num_equipment_steps);
    free(step);
    queue->size--;
    return result;
}

static int _cqueue_is_empty(CQueue* queue) {
    return queue ? queue->head == NULL : 1;
}

static void _cqueue_clear(CQueue* queue) {
    if (!queue) return;
    CStep* current = queue->head;
    while (current) {
        CStep* next = current->next;
        free(current);
        current = next;
    }
    queue->head = NULL;
    queue->tail = NULL;
    queue->size = 0;
}

/* ------------------------------------------------------------------ */
/*  Traversal functions                                               */
/* ------------------------------------------------------------------ */

static int g_step_count = 0;

static int _traversal_run(PyObject* start_steps_list, int can_stop_on_start,
                  PyObject* get_next_paths_fn,
                  PyObject* is_in_service_fn,
                  PyObject* check_queue_cond_fn,
                  PyObject* check_stop_cond_fn,
                  PyObject* apply_action_fn) {
    if (!start_steps_list || !get_next_paths_fn) {
        PyErr_SetString(PyExc_ValueError, "NULL start_steps or get_next_paths_fn");
        return -1;
    }
    VisitedTracker* visited = _visited_tracker_create(512);
    if (!visited) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create visited tracker");
        return -1;
    }
    CQueue* queue = _cqueue_create();
    if (!queue) {
        _visited_tracker_destroy(visited);
        PyErr_SetString(PyExc_MemoryError, "Failed to create queue");
        return -1;
    }
    g_step_count = 0;
    Py_ssize_t nstart = PyList_Size(start_steps_list);
    for (Py_ssize_t i = 0; i < nstart; i++) {
        PyObject* step_tuple = PyList_GetItem(start_steps_list, i);
        if (!PyTuple_Check(step_tuple) || PyTuple_Size(step_tuple) < 4) continue;
        PyObject* terminal = PyTuple_GetItem(step_tuple, 0);
        PyObject* data = PyTuple_GetItem(step_tuple, 1);
        int num_terminal_steps = (int)PyLong_AsLong(PyTuple_GetItem(step_tuple, 2));
        int num_equipment_steps = (int)PyLong_AsLong(PyTuple_GetItem(step_tuple, 3));
        _visited_tracker_visit(visited, terminal, NULL, 0);
        _cqueue_push(queue, terminal, data, num_terminal_steps, num_equipment_steps);
    }
    while (!_cqueue_is_empty(queue)) {
        PyObject* step_result = _cqueue_pop(queue);
        if (!step_result) break;
        PyObject* current_terminal = NULL;
        PyObject* current_data = NULL;
        int num_terminal_steps = 0;
        int num_equipment_steps = 0;
        if (!PyArg_ParseTuple(step_result, "OOii", &current_terminal, &current_data,
                               &num_terminal_steps, &num_equipment_steps)) {
            PyErr_Clear();
            Py_DECREF(step_result);
            continue;
        }
        Py_DECREF(step_result);
        g_step_count++;
        if (apply_action_fn) {
            PyObject* result = PyObject_CallOneArg(apply_action_fn, current_data);
            if (result) Py_DECREF(result);
            else PyErr_Clear();
        }
        PyObject* next_paths_list = PyObject_CallOneArg(get_next_paths_fn, current_terminal);
        if (!next_paths_list) {
            PyErr_Clear();
            continue;
        }
        Py_ssize_t npaths = PyList_Size(next_paths_list);
        for (Py_ssize_t p = 0; p < npaths; p++) {
            PyObject* path_tuple = PyList_GetItem(next_paths_list, p);
            if (!PyTuple_Check(path_tuple)) continue;
            Py_ssize_t nitems = PyTuple_Size(path_tuple);
            if (nitems < 5) continue;
            PyObject* next_terminal = PyTuple_GetItem(path_tuple, 0);
            PyObject* data = PyTuple_GetItem(path_tuple, 1);
            int num_terminal_steps = (int)PyLong_AsLong(PyTuple_GetItem(path_tuple, 2));
            int num_equipment_steps = (int)PyLong_AsLong(PyTuple_GetItem(path_tuple, 3));
            PyObject* phases_tuple = PyTuple_GetItem(path_tuple, 4);
            if (phases_tuple && PyList_Check(phases_tuple)) {
                int phase_count = (int)PyList_Size(phases_tuple);
                if (phase_count > 0) {
                    SinglePhaseKind* phases = (SinglePhaseKind*)malloc(
                        (size_t)phase_count * sizeof(SinglePhaseKind));
                    if (phases) {
                        for (int i = 0; i < phase_count; i++) {
                            phases[i] = (SinglePhaseKind)PyLong_AsLong(
                                PyList_GetItem(phases_tuple, i));
                        }
                        if (_visited_tracker_has_visited(visited, next_terminal, phases, phase_count) == 1) {
                            free(phases);
                            continue;
                        }
                        _visited_tracker_visit(visited, next_terminal, phases, phase_count);
                        free(phases);
                    }
                }
            } else {
                if (_visited_tracker_has_visited(visited, next_terminal, NULL, 0) == 1) {
                    continue;
                }
                _visited_tracker_visit(visited, next_terminal, NULL, 0);
            }
            _cqueue_push(queue, next_terminal, data, num_terminal_steps, num_equipment_steps);
        }
        Py_DECREF(next_paths_list);
    }
    _cqueue_destroy(queue);
    _visited_tracker_destroy(visited);
    return 0;
}

static void _traversal_reset(void) { g_step_count = 0; }
static int _traversal_step_count(void) { return g_step_count; }

/* ------------------------------------------------------------------ */
/*  Python C API wrapper functions                                    */
/* ------------------------------------------------------------------ */

static PyObject* py_visited_tracker_create(PyObject* self, PyObject* args) {
    int initial_capacity = 512;
    if (!PyArg_ParseTuple(args, "|i", &initial_capacity)) return NULL;
    VisitedTracker* tracker = _visited_tracker_create(initial_capacity);
    if (!tracker) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create visited tracker");
        return NULL;
    }
    return PyLong_FromVoidPtr(tracker);
}

static PyObject* py_visited_tracker_destroy(PyObject* self, PyObject* args) {
    unsigned long ptr;
    if (!PyArg_ParseTuple(args, "k", &ptr)) return NULL;
    _visited_tracker_destroy((VisitedTracker*)(uintptr_t)ptr);
    Py_RETURN_NONE;
}

static PyObject* py_visited_tracker_has_visited(PyObject* self, PyObject* args) {
    unsigned long ptr;
    PyObject* terminal;
    PyObject* phases_obj = Py_None;
    if (!PyArg_ParseTuple(args, "kO|O", &ptr, &terminal, &phases_obj)) return NULL;
    VisitedTracker* tracker = (VisitedTracker*)(uintptr_t)ptr;
    SinglePhaseKind* phases = NULL;
    int phase_count = 0;
    if (phases_obj != Py_None) {
        if (!PyList_Check(phases_obj) && !PyTuple_Check(phases_obj)) {
            PyErr_SetString(PyExc_TypeError, "phases must be a list or tuple");
            return NULL;
        }
        phase_count = (int)PySequence_Size(phases_obj);
        if (phase_count > 0) {
            phases = (SinglePhaseKind*)malloc((size_t)phase_count * sizeof(SinglePhaseKind));
            if (!phases) { PyErr_SetString(PyExc_MemoryError, "OOM"); return NULL; }
            for (int i = 0; i < phase_count; i++) {
                PyObject* item = PySequence_GetItem(phases_obj, i);
                if (!item) { free(phases); return NULL; }
                phases[i] = (SinglePhaseKind)PyLong_AsLong(item);
                Py_DECREF(item);
            }
        }
    }
    int result = _visited_tracker_has_visited(tracker, terminal, phases, phase_count);
    if (phases) free(phases);
    return PyLong_FromLong(result);
}

static PyObject* py_visited_tracker_visit(PyObject* self, PyObject* args) {
    unsigned long ptr;
    PyObject* terminal;
    PyObject* phases_obj = Py_None;
    if (!PyArg_ParseTuple(args, "kO|O", &ptr, &terminal, &phases_obj)) return NULL;
    VisitedTracker* tracker = (VisitedTracker*)(uintptr_t)ptr;
    SinglePhaseKind* phases = NULL;
    int phase_count = 0;
    if (phases_obj != Py_None) {
        if (!PyList_Check(phases_obj) && !PyTuple_Check(phases_obj)) {
            PyErr_SetString(PyExc_TypeError, "phases must be a list or tuple");
            return NULL;
        }
        phase_count = (int)PySequence_Size(phases_obj);
        if (phase_count > 0) {
            phases = (SinglePhaseKind*)malloc((size_t)phase_count * sizeof(SinglePhaseKind));
            if (!phases) { PyErr_SetString(PyExc_MemoryError, "OOM"); return NULL; }
            for (int i = 0; i < phase_count; i++) {
                PyObject* item = PySequence_GetItem(phases_obj, i);
                if (!item) { free(phases); return NULL; }
                phases[i] = (SinglePhaseKind)PyLong_AsLong(item);
                Py_DECREF(item);
            }
        }
    }
    int result = _visited_tracker_visit(tracker, terminal, phases, phase_count);
    if (phases) free(phases);
    return PyLong_FromLong(result);
}

static PyObject* py_visited_tracker_clear(PyObject* self, PyObject* args) {
    unsigned long ptr;
    if (!PyArg_ParseTuple(args, "k", &ptr)) return NULL;
    _visited_tracker_clear((VisitedTracker*)(uintptr_t)ptr);
    Py_RETURN_NONE;
}

static PyObject* py_cqueue_create(PyObject* self, PyObject* args) {
    CQueue* queue = _cqueue_create();
    if (!queue) { PyErr_SetString(PyExc_MemoryError, "Failed to create queue"); return NULL; }
    return PyLong_FromVoidPtr(queue);
}

static PyObject* py_cqueue_destroy(PyObject* self, PyObject* args) {
    unsigned long ptr;
    if (!PyArg_ParseTuple(args, "k", &ptr)) return NULL;
    _cqueue_destroy((CQueue*)(uintptr_t)ptr);
    Py_RETURN_NONE;
}

static PyObject* py_cqueue_push(PyObject* self, PyObject* args) {
    unsigned long ptr;
    PyObject* terminal;
    PyObject* data = Py_None;
    int num_terminal_steps = 0;
    int num_equipment_steps = 0;
    if (!PyArg_ParseTuple(args, "kO|Oii", &ptr, &terminal, &data,
                           &num_terminal_steps, &num_equipment_steps)) return NULL;
    _cqueue_push((CQueue*)(uintptr_t)ptr, terminal, data, num_terminal_steps, num_equipment_steps);
    Py_RETURN_NONE;
}

static PyObject* py_cqueue_pop(PyObject* self, PyObject* args) {
    unsigned long ptr;
    if (!PyArg_ParseTuple(args, "k", &ptr)) return NULL;
    PyObject* result = _cqueue_pop((CQueue*)(uintptr_t)ptr);
    return result;
}

static PyObject* py_cqueue_is_empty(PyObject* self, PyObject* args) {
    unsigned long ptr;
    if (!PyArg_ParseTuple(args, "k", &ptr)) return NULL;
    return PyBool_FromLong((long)_cqueue_is_empty((CQueue*)(uintptr_t)ptr));
}

static PyObject* py_cqueue_clear(PyObject* self, PyObject* args) {
    unsigned long ptr;
    if (!PyArg_ParseTuple(args, "k", &ptr)) return NULL;
    _cqueue_clear((CQueue*)(uintptr_t)ptr);
    Py_RETURN_NONE;
}

static PyObject* py_traversal_run(PyObject* self, PyObject* args) {
    PyObject* start_steps_list;
    int can_stop_on_start;
    PyObject* get_next_paths_fn;
    PyObject* is_in_service_fn = Py_None;
    PyObject* check_queue_cond_fn = Py_None;
    PyObject* check_stop_cond_fn = Py_None;
    PyObject* apply_action_fn = Py_None;
    if (!PyArg_ParseTuple(args, "OpOOOOO", &start_steps_list, &can_stop_on_start,
                           &get_next_paths_fn, &is_in_service_fn,
                           &check_queue_cond_fn, &check_stop_cond_fn,
                           &apply_action_fn)) return NULL;
    int result = _traversal_run(start_steps_list, can_stop_on_start,
                                 get_next_paths_fn, is_in_service_fn,
                                 check_queue_cond_fn, check_stop_cond_fn,
                                 apply_action_fn);
    return PyLong_FromLong(result);
}

static PyObject* py_traversal_reset(PyObject* self, PyObject* args) {
    _traversal_reset();
    Py_RETURN_NONE;
}

static PyObject* py_traversal_step_count(PyObject* self, PyObject* args) {
    return PyLong_FromLong((long)_traversal_step_count());
}

/* ------------------------------------------------------------------ */
/*  Module initialization                                             */
/* ------------------------------------------------------------------ */

static PyMethodDef _tracing_c_functions[] = {
    {"visited_tracker_create", py_visited_tracker_create, METH_VARARGS, NULL},
    {"visited_tracker_destroy", py_visited_tracker_destroy, METH_VARARGS, NULL},
    {"visited_tracker_has_visited", py_visited_tracker_has_visited, METH_VARARGS, NULL},
    {"visited_tracker_visit", py_visited_tracker_visit, METH_VARARGS, NULL},
    {"visited_tracker_clear", py_visited_tracker_clear, METH_VARARGS, NULL},
    {"cqueue_create", py_cqueue_create, METH_VARARGS, NULL},
    {"cqueue_destroy", py_cqueue_destroy, METH_VARARGS, NULL},
    {"cqueue_push", py_cqueue_push, METH_VARARGS, NULL},
    {"cqueue_pop", py_cqueue_pop, METH_VARARGS, NULL},
    {"cqueue_is_empty", py_cqueue_is_empty, METH_VARARGS, NULL},
    {"cqueue_clear", py_cqueue_clear, METH_VARARGS, NULL},
    {"traversal_run", py_traversal_run, METH_VARARGS, NULL},
    {"traversal_reset", py_traversal_reset, METH_VARARGS, NULL},
    {"traversal_step_count", py_traversal_step_count, METH_VARARGS, NULL},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef tracing_c_module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "_tracing_c",
    .m_doc = "C-accelerated network tracing engine",
    .m_size = -1,
    .m_methods = _tracing_c_functions,
};

PyMODINIT_FUNC
PyInit__tracing_c(void) {
    return PyModule_Create(&tracing_c_module);
}
