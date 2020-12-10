#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.cimbend import connect, NetworkConsumerClient, NetworkService

from zepben.cimbend.streaming.network_consumer import SyncNetworkConsumerClient
import cProfile


def run_retrieve():
    with connect() as channel:
        client = SyncNetworkConsumerClient(channel=channel)
        result = client.retrieve_network()
        network = result.result
        print(len(network._unresolved_references))
        print(len([obj for obj in network.objects()]))


def run_feeder():
    with connect() as channel:
        service = NetworkService()
        client = SyncNetworkConsumerClient(channel=channel)
        result = client.get_feeder(service, "PBH3A")
        network = result.result
        print(len(service._unresolved_references))
        print(len([obj for obj in service.objects()]))


if __name__ == "__main__":
    cProfile.run("run_retrieve()")
    cProfile.run("run_feeder()")
