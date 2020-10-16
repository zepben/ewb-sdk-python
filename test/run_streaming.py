
import zepben.cimbend.streaming.streaming as streaming
import asyncio
import grpc


channel = grpc.insecure_channel('localhost:50051')
network = asyncio.run(streaming.retrieve_network(channel))
print(len(network._unresolved_references))
print(len([obj for obj in network.objects()]))

