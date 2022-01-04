#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve import *

__all__ = ["create_location", "create_organisation", "create_position_point", "create_street_address", "create_town_detail"]


def create_location(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None, main_address: StreetAddress = None,
                    position_points: List[PositionPoint] = None) -> Location:
    """
    Location(IdentifiedObject)
    IdentifiedObject: mrid, name, description, names
    Location: main_address, position_points
    """
    # noinspection PyArgumentList
    return Location(**locals())


def create_organisation(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None) -> Organisation:
    """
    Organisation(IdentifiedObject)
    IdentifiedObject: mrid, name, description, names
    Organisation:
    """
    return Organisation(**locals())


def create_position_point(x_position: float, y_position: float) -> PositionPoint:
    """
    PositionPoint()
    PositionPoint: x_position, y_position
    """
    # noinspection PyArgumentList
    return PositionPoint(**locals())


def create_street_address(postal_code: str = "", town_detail: TownDetail = None, po_box: str = "", street_detail: List[StreetDetail] = None
                          ) -> StreetAddress:
    """
    StreetAddress()
    StreetAddress: postal_code, town_detail
    """
    # noinspection PyArgumentList
    return StreetAddress(**locals())


def create_town_detail(name: str = None, state_or_province: str = None) -> TownDetail:
    """
    TownDetail()
    TownDetail: name, state_or_province
    """
    # noinspection PyArgumentList
    return TownDetail(**locals())
