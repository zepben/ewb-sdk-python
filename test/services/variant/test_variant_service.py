#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0.
#
# Ported from `com.zepben.ewb.services.variant.VariantServiceTest`.
#
# The JVM iterates `supportedKClasses` and filters on the primary constructor having a single
# parameter (which selects the "simple" mRID-constructible types, excluding the
# `ChangeSetMember` types that have no-arg constructors). In Python the equivalent of
# `primaryConstructor.parameters.size` is the number of positional (non-kwonly, non *args)
# parameters on `__init__`.
import inspect

from zepben.ewb.services.variant.variant_service import VariantService


def _positional_param_count(cls) -> int:
    """
    Number of positional constructor parameters on `cls` (excluding `self`, `*args`, `**kwargs`,
    and keyword-only params). Mirrors the JVM `primaryConstructor.parameters.size` used to
    distinguish "simple" (mRID-constructible) variant types from the no-arg `ChangeSetMember`s.
    """
    count = 0
    for name, param in inspect.signature(cls.__init__).parameters.items():
        if name == "self":
            continue
        if param.kind in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
            inspect.Parameter.KEYWORD_ONLY,
        ):
            continue
        count += 1
    return count


class TestVariantService(object):
    service = VariantService()

    # TODO: do this test for object creation/deletion/mod
    def test_can_add_and_remove_supported_types(self):
        # Filters out object creation/deletion/modification (the `ChangeSetMember` types, which
        # have no-arg constructors) and keeps the mRID-constructible variant types.
        for cls in sorted(self.service.supported_types, key=lambda c: c.__name__):
            if _positional_param_count(cls) != 1:
                continue
            obj = cls(f"id-{cls.__name__}")
            assert self.service.try_add(obj), "Initial tryAdd should return true"
            assert self.service.get(obj.mrid, default=None) is obj
            assert self.service.remove(obj), "remove should return true for a previously-added object"
            assert self.service.get(obj.mrid, default=None) is None
