

#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum

__all__ = ["CustomerKind"]


class CustomerKind(Enum):
    UNKNOWN = 0
    """ Default """

    commercialIndustrial = 1
    """ Commercial industrial customer. """

    energyServiceScheduler = 2
    """ Customer as energy service scheduler. """

    energyServiceSupplier = 3
    """ Customer as energy service supplier. """

    enterprise = 4
    """ --- Missing form CIM --- """

    internalUse = 5
    """ Internal use customer. """

    other = 6
    """ Other kind of customer. """

    pumpingLoad = 7
    """ Pumping load customer. """

    regionalOperator = 8
    """ --- Missing form CIM --- """

    residential = 9
    """ Residential customer. """

    residentialAndCommercial = 10
    """ Residential and commercial customer. """

    residentialAndStreetlight = 11
    """ Residential and streetlight customer. """

    residentialFarmService = 12
    """ Residential farm service customer. """

    residentialStreetlightOthers = 13
    """ Residential streetlight or other related customer. """

    subsidiary = 14
    """ --- Missing form CIM --- """

    windMachine = 15
    """ Wind machine customer. """

    @property
    def short_name(self):
        return str(self)[13:]
