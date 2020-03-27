# Streaming #
Sending and receiving of data can be achieved through the streaming module, which provides connection facilities and streaming of `Network`s. This module is the preferred way of sending data between systems utilising the CIM model.

The connection module provides both an asyncio and synchronous interface. The synchronous interface will work **ONLY** if you are **NOT** using asyncio.

To connect to an HTTPS server with auth token and client auth:

    from zepben.model.streaming import connect
    
    ca = cert = key = None
    with open('path/to/key', 'rb') as f:
        key = f.read()
    with open('path/to/ca', 'rb') as f:
        ca = f.read()
    with open('path/to/cert', 'rb') as f:
        cert = f.read()
    with connect(host="grpc.example.com", conf_port=8080, client_id="id", client_secret="secret", pkey=key, cert=cert, ca=ca) as conn:
        # do stuff with conn
        network = conn.get_whole_network(...)
       
Using async is the same interface:

    from zepben.model.streaming import connect_async
    
    ... 
    
    async with connect_async(host="grpc.example.com", conf_port=8080, client_id="id", client_secret="secret", pkey=key, cert=cert, ca=ca) as conn:
        # do stuff with conn
        network = await conn.get_whole_network(...)


