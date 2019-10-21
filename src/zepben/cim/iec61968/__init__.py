"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""

from zepben.cim.iec61968.assetinfo.AssetInfo_pb2 import *
from zepben.cim.iec61968.assetinfo.AssetInfo_pb2_grpc import *
from zepben.cim.iec61968.assetinfo.CableInfo_pb2 import *
from zepben.cim.iec61968.assetinfo.CableInfo_pb2_grpc import *
from zepben.cim.iec61968.assetinfo.OverheadWireInfo_pb2 import *
from zepben.cim.iec61968.assetinfo.OverheadWireInfo_pb2_grpc import *
from zepben.cim.iec61968.assetinfo.TransformerEndInfo_pb2 import *
from zepben.cim.iec61968.assetinfo.TransformerEndInfo_pb2_grpc import *
from zepben.cim.iec61968.assetinfo.WireMaterialKind_pb2 import *
from zepben.cim.iec61968.assetinfo.WireMaterialKind_pb2_grpc import *
from zepben.cim.iec61968.assets.AssetOwner_pb2 import *
from zepben.cim.iec61968.assets.AssetOwner_pb2_grpc import *
from zepben.cim.iec61968.common.Location_pb2 import *
from zepben.cim.iec61968.common.Location_pb2_grpc import *
from zepben.cim.iec61968.common.Organisation_pb2 import *
from zepben.cim.iec61968.common.Organisation_pb2_grpc import *
from zepben.cim.iec61968.common.PositionPoint_pb2 import *
from zepben.cim.iec61968.common.PositionPoint_pb2_grpc import *
from zepben.cim.iec61968.common.StreetAddress_pb2 import *
from zepben.cim.iec61968.common.StreetAddress_pb2_grpc import *
from zepben.cim.iec61968.common.TownDetail_pb2 import *
from zepben.cim.iec61968.common.TownDetail_pb2_grpc import *
from zepben.cim.iec61968.customers.Customer_pb2 import *
from zepben.cim.iec61968.customers.Customer_pb2_grpc import *
from zepben.cim.iec61968.customers.CustomerAgreement_pb2 import *
from zepben.cim.iec61968.customers.CustomerAgreement_pb2_grpc import *
from zepben.cim.iec61968.customers.CustomerKind_pb2 import *
from zepben.cim.iec61968.customers.CustomerKind_pb2_grpc import *
from zepben.cim.iec61968.customers.PricingStructure_pb2 import *
from zepben.cim.iec61968.customers.PricingStructure_pb2_grpc import *
from zepben.cim.iec61968.customers.Tariff_pb2 import *
from zepben.cim.iec61968.customers.Tariff_pb2_grpc import *
from zepben.cim.iec61968.metering.Meter_pb2 import *
from zepben.cim.iec61968.metering.Meter_pb2_grpc import *
from zepben.cim.iec61968.metering.MeterReading_pb2 import *
from zepben.cim.iec61968.metering.MeterReading_pb2_grpc import *
from zepben.cim.iec61968.metering.Reading_pb2 import *
from zepben.cim.iec61968.metering.Reading_pb2_grpc import *
from zepben.cim.iec61968.metering.UsagePoint_pb2 import *
from zepben.cim.iec61968.metering.UsagePoint_pb2_grpc import *
