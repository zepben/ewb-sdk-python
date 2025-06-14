#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import asyncio
import json

from zepben.evolve import connect_with_token, NetworkConsumerClient, NetworkTrace
from zepben.evolve.services.network.tracing.networktrace.maxql.parser import MaxQLRunner

# TODO: THIS IS A LIVE TEST FILE, IF YOU SEE THIS IN A PR, IT SHOULD BE DELETED!
tests = [
"with RW1255 select where is PowerTransformer",
"with RW1255 select where name like 086TRF",
"with RW1255 select where length < 10",
"with RW1255 trace downstream from 82810990",
"with RW1255 trace upstream from 82810990",
"with RW1255 trace from 82810990 stopping at is switch",
"with RW1255 trace downstream from 82810990 stopping at is switch",
]

async def main():
    with open("config.json") as f:
        c = json.loads(f.read())

    channel = connect_with_token(
        host=c["host"],
        access_token=c["access_token"],
        rpc_port=c["rpc_port"],
        ca_filename=c['ca_path']
    )

    client = NetworkConsumerClient(channel)

    for text in tests:
        result = await MaxQLRunner(client).run(text)
        if isinstance(result, NetworkTrace):
            await result.add_step_action(lambda step, ctx: print(step.path.to_equipment)).run()
        else:
            print([type(r) for r in result])
        input('continue...')

if __name__ == '__main__':
    asyncio.run(main())