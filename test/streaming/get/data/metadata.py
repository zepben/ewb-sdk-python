#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import datetime

from zepben.evolve.services.common.meta.metadata_translations import data_source_to_pb
from zepben.protobuf.metadata.metadata_responses_pb2 import GetMetadataResponse

from zepben.evolve import service_info, DataSource


def create_metadata() -> service_info:
    # noinspection PyArgumentList
    return service_info(
        "title",
        "version",
        [
            DataSource(
                "source one",
                "source version one",
                datetime.datetime.now()
            ),
            DataSource(
                "source two",
                "source version two",
                datetime.datetime.now()
            )
        ]
    )


def create_metadata_response(expected_metadata: service_info) -> GetMetadataResponse:
    return GetMetadataResponse(
        title=expected_metadata.title,
        version=expected_metadata.version,
        dataSources=[data_source_to_pb(it) for it in expected_metadata.data_sources]
    )



