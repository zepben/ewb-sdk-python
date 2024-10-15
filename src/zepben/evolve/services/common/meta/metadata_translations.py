#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

# noinspection PyPackageRequirements,PyUnresolvedReferences
from google.protobuf.timestamp_pb2 import Timestamp as PBTimestamp
from zepben.protobuf.metadata.metadata_data_pb2 import DataSource as PBDataSource
from zepben.protobuf.metadata.metadata_data_pb2 import ServiceInfo as PBServiceInfo

from zepben.evolve import DataSource, ServiceInfo


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


def service_info_to_pb(si: ServiceInfo) -> PBServiceInfo:
    return PBServiceInfo(
        title=si.title,
        version=si.version,
        dataSources=[data_source_to_pb(ds) for ds in si.data_sources]
    )


def service_info_from_pb(pb: PBServiceInfo) -> ServiceInfo:
    # noinspection PyArgumentList
    return ServiceInfo(
        title=pb.title,
        version=pb.version,
        data_sources=[data_source_from_pb(ds_pb) for ds_pb in pb.dataSources]
    )
