#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import datetime

from zepben.protobuf.metadata.metadata_responses_pb2 import GetMetadataResponse
from zepben.protobuf.metadata.metadata_data_pb2 import ServiceInfo as PBServiceInfo

from zepben.evolve import ServiceInfo, DataSource, data_source_to_pb


def create_metadata() -> ServiceInfo:
    # noinspection PyArgumentList
    return ServiceInfo(
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


def create_metadata_response(expected_metadata: ServiceInfo) -> GetMetadataResponse:
    return GetMetadataResponse(
        serviceInfo=PBServiceInfo(
            title=expected_metadata.title,
            version=expected_metadata.version,
            dataSources=[data_source_to_pb(it) for it in expected_metadata.data_sources]
        )
    )
