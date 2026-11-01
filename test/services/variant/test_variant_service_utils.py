#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0.
#
# Ported from `com.zepben.ewb.services.variant.VariantServiceUtilsTest`.
#
# The JVM test uses `verifyWhenServiceFunctionSupportsAllServiceTypes`, a reflection helper that:
#   1. asserts the set of `Identifiable` leaf classes used as handler-parameter types by the `when`
#      function is exactly the set of supported types, and
#   2. for each supported type, feeds an instance and asserts exactly the matching handler is invoked,
#      plus an unknown object invokes the `isOther` error handler.
#
# In Python the equivalent of the JVM's Kotlin-type reflection is `typing.get_type_hints` over the
# `when_variant_identified_object` signature.
import inspect
import re
import typing

from zepben.ewb.model.cim.iec61970.base.core.identifiable import Identifiable
from zepben.ewb.services.variant.variant_service import VariantService
from zepben.ewb.services.variant.variant_service_utils import when_variant_identified_object

HANDLER_NAMES = (
    "is_network_model_project",
    "is_network_model_project_stage",
    "is_annotated_project_dependency",
    "is_change_set",
    "is_object_creation",
    "is_object_deletion",
    "is_object_modification",
    "is_other",
)


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


def _construct(cls) -> Identifiable:
    """Construct an instance of `cls` (mRID-constructible types get `id-<Name>`, members are no-arg)."""
    if _positional_param_count(cls) == 1:
        return cls(f"id-{cls.__name__}")
    return cls()


def _callback_param_types() -> set:
    """
    The set of `Identifiable` leaf classes used as handler-parameter types by
    `when_variant_identified_object` (mirrors the JVM collecting `whenFunction.parameters` types).
    """
    hints = typing.get_type_hints(when_variant_identified_object)
    types = set()
    for name, hint in hints.items():
        if name in ("identifiable", "is_other", "return"):
            continue
        args = typing.get_args(hint)  # Callable[[X], R] -> (list-of-X, R)
        param_types = args[0]
        if isinstance(param_types, (list, tuple)) and param_types:
            types.add(param_types[0])
    return types


def _expected_callback_name(cls_name: str) -> str:
    """Kotlin `is${SimpleName}` -> Python `is_<snake_case_name>`."""
    snake = re.sub(r"(?<!^)(?=[A-Z])", "_", cls_name).lower()
    return f"is_{snake}"


class TestVariantServiceUtils(object):

    def test_supports_all_variant_service_types(self):
        # 1. The handler parameter types must exactly match the supported types.
        assert _callback_param_types() == VariantService().supported_types

        # 2. Each supported type dispatches to exactly its matching handler.
        for cls in VariantService().supported_types:
            called = {}
            handlers = {name: self._make_handler(called, name) for name in HANDLER_NAMES}
            obj = _construct(cls)
            when_variant_identified_object(obj, **handlers)
            expected = _expected_callback_name(cls.__name__)
            assert list(called) == [expected], (cls.__name__, called)
            assert called[expected] is obj

        # 3. An unknown `Identifiable` dispatches to the `is_other` handler.
        called = {}
        handlers = {name: self._make_handler(called, name) for name in HANDLER_NAMES}
        unknown = _UnknownIdentifiable("unknown-id")
        when_variant_identified_object(unknown, **handlers)
        assert list(called) == ["is_other"], called
        assert called["is_other"] is unknown

    @staticmethod
    def _make_handler(called, name):
        def handler(obj):
            called[name] = obj
            return "ok"
        return handler


class _UnknownIdentifiable(Identifiable):
    """A stand-in for an `Identifiable` type that is not supported by the variant service."""
