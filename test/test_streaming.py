#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import zepben.cimbend.streaming.streaming as streaming
import asyncio
import grpc 


class TestStreaming(object):

    def test_retrieve_network(self):
        """Test retrieve_network"""
        channel = grpc.insecure_channel('localhost:50051')
        network = asyncio.run(streaming.retrieve_network(channel))
        print(len(network._unresolved_references))