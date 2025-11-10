#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from zepben.ewb import CimConsumerClient


@pytest.mark.asyncio
async def test_abstract_coverage():
    # We should not be able to instantiate an abstract class to begin with
    with pytest.raises(TypeError):
        _ = CimConsumerClient()

    # with pytest.raises(NotImplementedError):
    #     (await client.service).throw_on_error()
    #
    # with pytest.raises(NotImplementedError):
    #     (await client.get_identified_object("id")).throw_on_error()
    #
    # with pytest.raises(NotImplementedError):
    #     (await client.get_identified_objects(["id"])).throw_on_error()
    #
    # with pytest.raises(NotImplementedError):
    #     (await client.get_metadata()).throw_on_error()
