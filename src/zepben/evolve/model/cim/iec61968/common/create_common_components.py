#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

from zepben.evolve import *


def create_location(main_address: StreetAddress = None, position_points: List[PositionPoint] = None) -> Location:
    """
    Location()
    Location: main_address, position_points
    """
    args = locals()
    # noinspection PyArgumentList
    return Location(**args)


def create_organisation(mrid: str = None, name: str = '', description: str = "", names: List[Name] = None) -> Organisation:
    """
    Organisation(IdentifiedObject)
    IdentifiedObject: mrid, name, description, names
    Organisation:
    """
    args = locals()
    return Organisation(**args)


def create_position_point(x_position: float, y_position: float) -> PositionPoint:
    """
    PositionPoint()
    PositionPoint: x_position, y_position
    """
    args = locals()
    # noinspection PyArgumentList
    return PositionPoint(**args)


def create_street_address(postal_code: str = "", town_detail: TownDetail = None) -> StreetAddress:
    """
    StreetAddress()
    StreetAddress: postal_code, town_detail
    """
    args = locals()
    # noinspection PyArgumentList
    return StreetAddress(**args)


def create_town_detail(name: str = "", state_or_province: str = "") -> TownDetail:
    """
    TownDetail()
    TownDetail: name, state_or_province
    """
    args = locals()
    # noinspection PyArgumentList
    return TownDetail(**args)
