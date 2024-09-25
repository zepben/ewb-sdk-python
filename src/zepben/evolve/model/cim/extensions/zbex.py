#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

def zbex(thing):
    """
    Indicates that a member or class is a Zepben extension added to the CIM standard.

    All Zepben extensions should be annotated with @zbex, and have [ZBEX] linked into their docstring. Once this has been linked
    everywhere, you will be able to use "find usages" to see all of our extension attributes/classes.

    NOTE: Python doesn't let you decorate a member, so you will need to search for [ZBEX] to find those.
    """

    # We don't actually do anything with this decorator, it is just to mark that this is an extension.
    return thing
