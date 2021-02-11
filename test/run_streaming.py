#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import connect, NetworkService

from zepben.evolve.streaming.get.network_consumer import SyncNetworkConsumerClient
import cProfile


def run_retrieve():
    with connect(rpc_port=50052) as channel:
        client = SyncNetworkConsumerClient(channel=channel)
        result = client.retrieve_network()
        result.throw_on_error()
        service = result.result.network_service
        print(f"Num unresolved: {service.num_unresolved_references()}")
        print(f"Num objects: {service.len_of()}")


def run_feeder():
    with connect(rpc_port=50052) as channel:
        service = NetworkService()
        client = SyncNetworkConsumerClient(channel=channel)
        result = client.get_feeder(service, "PBH3A")
        network = result.result
        print(f"Num unresolved: {service.num_unresolved_references()}")
        print(f"Num objects: {service.len_of()}")


if __name__ == "__main__":
    print("running get feeder")
    # cProfile.run("run_feeder()")
    run_feeder()
    print("running retrieve network")
    # cProfile.run("run_retrieve()")
    run_retrieve()
