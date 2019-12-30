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


from zepben.model.equipment import Equipment


def normally_open(equip: Equipment, core=None):
    """
    Test if a given core on an equipment is normally open.
    :param equip: The equipment to test
    :param core: The core to test. If None tests all cores.
    :return: True if the equipment is open (de-energised), False otherwise
    """
    try:
        if core is None:
            ret = not equip.normally_in_service
            for core in range(0, equip.num_cores()):
                ret &= equip.normally_open(core)
            return ret
        else:
            return not equip.normally_in_service or equip.normally_open(core)
    except AttributeError:
        # This should only be reachable if equip is normally in service but didn't define normally_open, in which case
        # it's not normally open.
        return not equip.normally_in_service


def currently_open(equip: Equipment, core=None):
    """
    Test if a given core on an equipment is open.
    :param equip: The equipment to test
    :param core: The core to test. If None tests all cores.
    :return: True if the equipment is open (de-energised), False otherwise
    """
    try:
        if core is None:
            ret = not equip.in_service
            for core in range(0, equip.num_cores()):
                ret &= equip.is_open(core)
            return ret
        else:
            return not equip.in_service or equip.is_open(core)
    except AttributeError:
        # This should only be reachable if equip is normally in service but didn't define normally_open, in which case
        # it's not normally open.
        return not equip.in_service


def queue_next_equipment(item, exclude=None):
    return item.get_connected_equipment(exclude=exclude)


def queue_next_terminal(item, exclude=None):
    """
    Wrapper tracing queue function for queuing terminals via their connectivity
    TODO: Specify cores to trace based on the phasing of this "item".
    :param item:
    :param exclude:
    :return:
    """
    other_terms = item.get_other_terminals()
    if not other_terms:
        # If there are no other terminals we get connectivity for this one and return that. Note that this will
        # also return connections for EnergyConsumer's, but upstream will be covered by the exclude parameter and thus
        # should yield an empty list.
        return [cr.to_terminal for cr in item.get_connectivity(exclude=exclude)]

    crs = []
    for term in other_terms:
        crs.extend(term.get_connectivity(exclude=exclude))

    return [cr.to_terminal for cr in crs]
