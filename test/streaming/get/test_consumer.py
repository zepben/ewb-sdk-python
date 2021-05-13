#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from zepben.evolve import BaseService, CimConsumerClient


@pytest.mark.asyncio
async def test_abstract_coverage():
    service = BaseService('service')
    client = CimConsumerClient()
    try:
        await client.get_identified_object(service, "id")
        raise AssertionError("Should have thrown")
    except NotImplementedError:
        pass
    except Exception as e:
        raise e

    try:
        await client.get_identified_objects(service, ["id"])
        raise AssertionError("Should have thrown")
    except NotImplementedError:
        pass
    except Exception as e:
        raise e
