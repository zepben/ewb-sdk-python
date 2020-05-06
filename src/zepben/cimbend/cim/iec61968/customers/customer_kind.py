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

from enum import Enum

__all__ = ["CustomerKind"]


class CustomerKind(Enum):
    """ Default """
    UNKNOWN = 0

    """ Commercial industrial customer. """
    commercialIndustrial = 1

    """ Customer as energy service scheduler. """
    energyServiceScheduler = 2

    """ Customer as energy service supplier. """
    energyServiceSupplier = 3

    """ --- Missing form CIM --- """
    enterprise = 4

    """ Internal use customer. """
    internalUse = 5

    """ Other kind of customer. """
    other = 6

    """ Pumping load customer. """
    pumpingLoad = 7

    """ --- Missing form CIM --- """
    regionalOperator = 8

    """ Residential customer. """
    residential = 9

    """ Residential and commercial customer. """
    residentialAndCommercial = 10

    """ Residential and streetlight customer. """
    residentialAndStreetlight = 11

    """ Residential farm service customer. """
    residentialFarmService = 12

    """ Residential streetlight or other related customer. """
    residentialStreetlightOthers = 13

    """ --- Missing form CIM --- """
    subsidiary = 14

    """ Wind machine customer. """
    windMachine = 15

    @property
    def short_name(self):
        return str(self)[16:]
