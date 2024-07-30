#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import cProfile
import platform
from time import perf_counter, process_time
from typing import Callable

from zepben.evolve import connect, Feeder
from zepben.evolve.streaming.get.network_consumer import SyncNetworkConsumerClient

rpc_port = 9001
indent_level = 0
indent = 3
profile = False


def run_streaming():
    print(platform.architecture())
    _time("get object", run_get_object)
    _time("get feeder", run_feeder)
    # Depending on the database you have loaded this can take substantial time (minutes), so it is disabled by default.
    # _time("retrieve network", run_retrieve)
    _time("retrieve network hierarchy", run_network_hierarchy)


def run_retrieve():
    with connect(rpc_port=rpc_port) as channel:
        client = SyncNetworkConsumerClient(channel=channel)

        client.retrieve_network().throw_on_error()

        _log(f"Num unresolved: {client.service.num_unresolved_references()}")
        _log(f"Num objects: {client.service.len_of()}")


def run_get_object():
    with connect(rpc_port=rpc_port) as channel:
        client = SyncNetworkConsumerClient(channel=channel)

        client.get_identified_object("21527151-6fce-423d-84e5-8254a00b05b1").throw_on_error()

        _log(f"Num unresolved: {client.service.num_unresolved_references()}")
        _log(f"Num objects: {client.service.len_of()}")


def run_feeder():
    with connect(rpc_port=rpc_port) as channel:
        client = SyncNetworkConsumerClient(channel=channel)

        client.get_equipment_container("CTN005", Feeder).throw_on_error()

        _log(f"Num unresolved: {client.service.num_unresolved_references()}")
        _log(f"Num objects: {client.service.len_of()}")


def run_network_hierarchy():
    with connect(rpc_port=rpc_port) as channel:
        client = SyncNetworkConsumerClient(channel=channel)

        network_hierarchy = client.get_network_hierarchy().throw_on_error().value

        _log(f"Num geographical regions: {len(network_hierarchy.geographical_regions)}")
        _log(f"Num sub geographical regions: {len(network_hierarchy.sub_geographical_regions)}")
        _log(f"Num substations: {len(network_hierarchy.substations)}")
        _log(f"Num feeders: {len(network_hierarchy.feeders)}")
        _log(f"Num circuits: {len(network_hierarchy.circuits)}")
        _log(f"Num loops: {len(network_hierarchy.loops)}")


def _time(desc: str, run: Callable[[], None]):
    start_perf = perf_counter()
    start_proc = process_time()

    _log(f"Running {desc}...")
    global indent_level
    indent_level += 1
    try:
        run()
    except Exception as e:
        _log(f"Exception caught: {type(e).__name__} - {str(e)}")

    indent_level -= 1

    duration_perf = int(perf_counter() - start_perf)
    duration_proc = int(process_time() - start_proc)
    _log(f"{desc} took perf={int(duration_perf / 60)}:{duration_perf % 60:02}, proc={int(duration_proc / 60)}:{duration_proc % 60:02}")


def _log(msg: str):
    c = " "
    print(f"{c * (indent * indent_level)}{msg}")


if __name__ == "__main__":
    if profile:
        cProfile.run("_time(\"streaming\", run_streaming)")
    else:
        _time("streaming", run_streaming)
