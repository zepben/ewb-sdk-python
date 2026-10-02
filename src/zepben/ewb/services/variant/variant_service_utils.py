#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0.

from __future__ import annotations

__all__ = ["when_variant_identified_object"]

from typing import Callable, Any, TypeVar

from zepben.ewb.model.cim.iec61970.base.core.identifiable import Identifiable
from zepben.ewb.model.cim.extensions.iec61970.infiec61970.infpart303.networkmodelprojects.network_model_project import NetworkModelProject
from zepben.ewb.model.cim.iec61970.infiec61970.infpart303.networkmodelprojects.annotated_project_dependency import AnnotatedProjectDependency
from zepben.ewb.model.cim.iec61970.infiec61970.infpart303.networkmodelprojects.network_model_project_stage import NetworkModelProjectStage
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.change_set import ChangeSet
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_creation import ObjectCreation
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_deletion import ObjectDeletion
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_modification import ObjectModification

R = TypeVar("R")


def _default_is_other(obj: Any) -> R:
    raise IllegalArgumentException(
        f"Identified object type {type(obj).__name__} is not supported by the network model project service")


def when_variant_identified_object(
    identifiable: Identifiable,
    is_network_model_project: Callable[[NetworkModelProject], R],
    is_network_model_project_stage: Callable[[NetworkModelProjectStage], R],
    is_annotated_project_dependency: Callable[[AnnotatedProjectDependency], R],
    is_change_set: Callable[[ChangeSet], R],
    is_object_creation: Callable[[ObjectCreation], R],
    is_object_deletion: Callable[[ObjectDeletion], R],
    is_object_modification: Callable[[ObjectModification], R],
    is_other: Callable[[Any], R] = _default_is_other,
) -> R:
    """
    A function that provides an exhaustive `when` style statement for all `Identifiable` leaf types supported by
    the `VariantService`. If the provided `identifiable` is not supported by the service the `is_other` handler
    is invoked which by default will throw an `IllegalArgumentException`.

    By using this function, you acknowledge that if any new types are added to the variant service, and thus this
    function, it will cause an error when updating to the new version. This should reduce errors due to missed
    handling of new types introduced to the model. As this is intended behaviour it generally will not be
    considered a breaking change in terms of semantic versioning of this library.

    If it is not critical that all types within the service are always handled, it is recommended to use a typical
    if-else branch and update new cases as required without breaking your code.

    :param identifiable: The identified object to handle.
    """
    if isinstance(identifiable, NetworkModelProject):
        return is_network_model_project(identifiable)
    if isinstance(identifiable, NetworkModelProjectStage):
        return is_network_model_project_stage(identifiable)
    if isinstance(identifiable, AnnotatedProjectDependency):
        return is_annotated_project_dependency(identifiable)
    if isinstance(identifiable, ChangeSet):
        return is_change_set(identifiable)
    if isinstance(identifiable, ObjectCreation):
        return is_object_creation(identifiable)
    if isinstance(identifiable, ObjectDeletion):
        return is_object_deletion(identifiable)
    if isinstance(identifiable, ObjectModification):
        return is_object_modification(identifiable)
    return is_other(identifiable)


class IllegalArgumentException(Exception):
    """Mirrors Kotlin's `IllegalArgumentException` used by the default `is_other` handler."""
