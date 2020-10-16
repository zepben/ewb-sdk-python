

import zepben.cimbend.streaming.streaming as streaming
import asyncio
import grpc 


class TestStreaming(object):

    def test_retrieve_network(self):
        """Test retrieve_network"""
        channel = grpc.insecure_channel('localhost:50051')
        network = asyncio.run(streaming.retrieve_network(channel))
        print(len(network._unresolved_references))