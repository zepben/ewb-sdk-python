#  Copyright 2023 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from zepben.evolve.services.common.meta.service_info import service_info
from zepben.protobuf.metadata.metadata_responses_pb2 import GetMetadataResponse as PBGetMetadataResponse, GetMetadataResponse

from zepben.evolve import DataSource

from google.protobuf.timestamp_pb2 import Timestamp as PBTimestamp
from zepben.protobuf.metadata.metadata_data_pb2 import DataSource as PBDataSource


def data_source_to_pb(ds: DataSource) -> PBDataSource:
    ts = PBTimestamp()
    ts.FromDatetime(ds.timestamp)
    return PBDataSource(
        source=ds.source,
        version=ds.version,
        timestamp=ts
    )


def data_source_from_pb(pb: PBDataSource) -> DataSource:
    # noinspection PyArgumentList
    return DataSource(
        source=pb.source,
        version=pb.version,
        timestamp=pb.timestamp.ToDatetime() if pb.timestamp != PBTimestamp() else None
    )


def service_info_to_pb(si: service_info) -> GetMetadataResponse:
    return GetMetadataResponse(
        title=si.title,
        version=si.version,
        dataSources=[data_source_to_pb(it) for it in si.data_sources]
    )


def service_info_from_pb(pb: PBGetMetadataResponse) -> service_info:
    data_sources = list()
    for ds in pb.dataSources:
        # noinspection PyArgumentList
        data_sources.append(data_source_from_pb(ds))
    # noinspection PyArgumentList
    return service_info(
        title=pb.title,
        version=pb.version,
        data_sources=data_sources
    )
