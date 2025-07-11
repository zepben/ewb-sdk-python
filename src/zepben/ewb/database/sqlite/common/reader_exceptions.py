#  Copyright 2024 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["MRIDLookupException", "NameTypeLookupException", "DuplicateMRIDException", "DuplicateNameTypeException"]


class MRIDLookupException(Exception):
    """
    An exception indicating that an mRID could not be found in a [BaseService].
    """


class NameTypeLookupException(Exception):
    """
    An exception indicating that a [NameType] could not be found in a [BaseService].
    """


class DuplicateMRIDException(Exception):
    """
    An exception indicating that an mRID has already been used by a different objects in a [BaseService].
    """


class DuplicateNameTypeException(Exception):
    """
    An exception indicating that n [NameType] has already been used in a [BaseService].
    """
