#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.protobuf.cim.iec61968.common.Agreement_pb2 import Agreement
from zepben.protobuf.cim.iec61968.customers.CustomerAgreement_pb2 import CustomerAgreement
from zepben.protobuf.cim.iec61968.customers.Customer_pb2 import Customer
from zepben.protobuf.cim.iec61968.customers.PricingStructure_pb2 import PricingStructure
from zepben.protobuf.cim.iec61968.customers.Tariff_pb2 import Tariff

__all__ = []

Customer.mrid = lambda self: getattr(self, 'or').mrid()
CustomerAgreement.mrid = lambda self: self.agr.mrid()
Agreement.mrid = lambda self: self.doc.mrid()
PricingStructure.mrid = lambda self: self.doc.mrid()
Tariff.mrid = lambda self: self.doc.mrid()

CustomerAgreement.name_and_mrid = lambda self: self.agr.name_and_mrid()
Agreement.name_and_mrid = lambda self: self.doc.name_and_mrid()
