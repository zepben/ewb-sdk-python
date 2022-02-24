#  Copyright 2020 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.


class MissingReferenceException(Exception):
    TYPE = 'UNKNOWN'

    def __init__(self, referenced_mrid: str, referrer=None, **kwargs):
        self.referenced_mrid = referenced_mrid
        self.referrer = referrer

        super().__init__(kwargs)

    @property
    def info(self):
        if self.referrer is not None:
            if hasattr(self.referrer, 'DESCRIPTOR'):
                self.referrer_type = self.referrer.DESCRIPTOR.name
                self.referrer_mrid = self.referrer.mRID
            else:
                self.referrer_type = type(self.referrer).__name__
                self.referrer_mrid = self.referrer.mrid
        return f"{self.TYPE} {self.referenced_mrid} was not found in the network. It must be created before {self.referrer_type}[{self.referrer_mrid}] can reference it."


class NetworkException(Exception):
    pass


class AlreadyExistsException(Exception):
    pass


class ReadingException(Exception):
    pass


class PhaseException(Exception):
    pass


class NominalPhaseException(Exception):
    pass


class WiringException(Exception):
    pass


class TracingException(Exception):
    pass
