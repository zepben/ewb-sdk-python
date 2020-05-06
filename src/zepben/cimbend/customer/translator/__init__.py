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


from zepben.protobuf.cim.iec61968.common.Agreement_pb2 import Agreement
from zepben.protobuf.cim.iec61968.customers.CustomerAgreement_pb2 import CustomerAgreement
from zepben.protobuf.cim.iec61968.customers.Customer_pb2 import Customer
from zepben.protobuf.cim.iec61968.customers.PricingStructure_pb2 import PricingStructure
from zepben.cimbend.customer.translator.customer_proto2cim import *
import zepben.cimbend.common

__all__ = ["customer_proto2cim.py"]

Customer.mrid = lambda self: getattr(self, 'or').mrid()
CustomerAgreement.mrid = lambda self: self.agr.mrid()
Agreement.mrid = lambda self: self.doc.mrid()
PricingStructure.mrid = lambda self: self.doc.mrid()

CustomerAgreement.name_and_mrid = lambda self: self.agr.name_and_mrid()
Agreement.name_and_mrid = lambda self: self.doc.name_and_mrid()
