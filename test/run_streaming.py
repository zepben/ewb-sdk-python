#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.evolve import connect, NetworkService

from zepben.evolve.streaming.get.network_consumer import SyncNetworkConsumerClient
import cProfile


def run_retrieve():
    with connect() as channel:
        client = SyncNetworkConsumerClient(channel=channel)
        result = client.retrieve_network()
        result.throw_on_error()
        network = result.result.network_service
        print(len(network._unresolved_references))
        print(network.len_of())


def run_feeder():
    with connect() as channel:
        service = NetworkService()
        client = SyncNetworkConsumerClient(channel=channel)
        result = client.get_feeder(service, "PBH3A")
        network = result.result
        print(len(service._unresolved_references))
        print(service.len_of())


if __name__ == "__main__":
    cProfile.run("run_retrieve()")
    cProfile.run("run_feeder()")
