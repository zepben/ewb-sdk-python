#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import datetime

import zepben.protobuf.metadata.metadata_data_pb2
from zepben.protobuf.metadata.metadata_responses_pb2 import GetMetadataResponse
from google.protobuf.timestamp_pb2 import Timestamp as PBTimestamp

from zepben.evolve import Metadata, DataSource


def create_metadata() -> Metadata:
    return Metadata(
        "title",
        "version",
        {
            "source one": DataSource(
                "source one",
                "source version one",
                datetime.datetime.now()
            ),
            "source two": DataSource(
                "source two",
                "source version two",
                datetime.datetime.now()
            )
        }
    )


def _create_metadata_response(expected_metadata: Metadata) -> GetMetadataResponse:
    return GetMetadataResponse(
        title=expected_metadata.title,
        version=expected_metadata.version,
        dataSources=[data_source_to_pb(it) for it in expected_metadata.data_sources.values()]
    )


def data_source_to_pb(data_source: DataSource) -> zepben.protobuf.metadata.metadata_data_pb2.DataSource:
    ts = PBTimestamp()
    ts.FromDatetime(data_source.timestamp)
    return zepben.protobuf.metadata.metadata_data_pb2.DataSource(
        source=data_source.source,
        version=data_source.version,
        timestamp=ts
    )
