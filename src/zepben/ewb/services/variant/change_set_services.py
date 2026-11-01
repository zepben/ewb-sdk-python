#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0.

from __future__ import annotations

__all__ = ["ChangeSetServices"]

from dataclasses import fields
from typing import Optional, Collection, Generator

from zepben.ewb import require
from zepben.ewb.model.cim.iec61968.common.organisation import Organisation
from zepben.ewb.model.cim.iec61970.base.core.identifiable import Identifiable
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.change_set import ChangeSet
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.change_set_member import ChangeSetMember
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_creation import ObjectCreation
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_deletion import ObjectDeletion
from zepben.ewb.model.cim.iec61970.infiec61970.part303.genericdataset.object_modification import ObjectModification
from zepben.ewb.services.common.base_service import BaseService
from zepben.ewb.services.common.exceptions import UnsupportedIdentifiableException, IllegalStateException
from zepben.ewb.services.customer.customers import CustomerService
from zepben.ewb.services.diagram.diagrams import DiagramService
from zepben.ewb.services.network.network_service import NetworkService
from zepben.ewb.services.variant.variant_service import VariantService


class ChangeSetServices:
    """
    Contains a set of network, diagram, and customer services representing the contents of all changesets contained
    within `variant_service`.

    Note change sets represented by this service must only be populated against one base model of the network.
    """

    def __init__(
        self,
        change_set: Optional[ChangeSet],
        new_network_service: Optional[NetworkService] = None,
        original_network_service: Optional[NetworkService] = None,
        new_diagram_service: Optional[DiagramService] = None,
        original_diagram_service: Optional[DiagramService] = None,
        new_customer_service: Optional[CustomerService] = None,
        original_customer_service: Optional[CustomerService] = None,
    ):
        self.change_set = change_set
        self.new_network_service = new_network_service or NetworkService()
        self.original_network_service = original_network_service or NetworkService()
        self.new_diagram_service = new_diagram_service or DiagramService()
        self.original_diagram_service = original_diagram_service or DiagramService()
        self.new_customer_service = new_customer_service or CustomerService()
        self.original_customer_service = original_customer_service or CustomerService()

    def __getitem__(self, change_set_member: ChangeSetMember) -> Identifiable:
        require(self.change_set is not None, lambda: "You must have a change set to access its members")
        require(self.change_set.get_member(change_set_member.target_object_mrid) is not None,
                lambda: f"{change_set_member.type_name_and_mrid()} must be present in {self.change_set.type_name_and_mrid()}")
        if isinstance(change_set_member, (ObjectCreation, ObjectModification)):
            return self._get_from_new(change_set_member.target_object_mrid)
        if isinstance(change_set_member, ObjectDeletion):
            return self._get_from_original(change_set_member.target_object_mrid)
        raise IllegalStateException(f"{change_set_member.type_name_and_mrid()} class is unhandled")

    def created(self, obj: Collection[ObjectCreation]) -> Generator[Identifiable, None, None]:
        """Fetch the created objects for a collection of `ObjectCreation`s."""
        for item in obj:
            yield self._get_from_new(item.target_object_mrid)

    def modified(self, obj: Collection[ObjectModification]) -> Generator[Identifiable, None, None]:
        """Fetch the modified objects for a collection of `ObjectModification`s."""
        for item in obj:
            yield self._get_from_new(item.target_object_mrid)

    def deleted(self, obj: Collection[ObjectDeletion]) -> Generator[Identifiable, None, None]:
        """Fetch the deleted objects for a collection of `ObjectDeletion`s."""
        for item in obj:
            yield self._get_from_original(item.target_object_mrid)

    def original(self, obj: Collection[ObjectModification]) -> Generator[Identifiable, None, None]:
        """Fetch the reverse modification for a collection of `ObjectModification`s."""
        for item in obj:
            yield self._get_from_original(item.target_object_mrid)

    def get_reverse_modification(self, object_modification: ObjectModification) -> Identifiable:
        """
        Get the reverse modification object for `object_modification`, which should be the object from the base model of the variant.
        """
        return self._get_from_original(object_modification.target_object_mrid)

    def _get_from_new(self, mrid: str) -> Identifiable:
        obj = (self.new_network_service.get(mrid, default=None)
               or self.new_diagram_service.get(mrid, default=None)
               or self.new_customer_service.get(mrid, default=None))
        if obj is None:
            raise IllegalStateException(f"{mrid} was not found in any new service - have you removed it or messed with the service?")
        return obj

    def _get_from_original(self, mrid: str) -> Identifiable:
        obj = (self.original_network_service.get(mrid, default=None)
               or self.original_diagram_service.get(mrid, default=None)
               or self.original_customer_service.get(mrid, default=None))
        if obj is None:
            raise IllegalStateException(f"{mrid} was not found in any new service - have you removed it or messed with the service?")
        return obj

    def add_creation(self, variant_service: VariantService, change_set: ChangeSet, new_object: Identifiable) -> bool:
        """
        Create and add a new `ObjectCreation` for the provided `new_object`.

        :param new_object: The object that has been added.
        """
        creation = ObjectCreation()
        creation.target_object_mrid = new_object.mrid
        creation.change_set = change_set
        change_set.add_member(creation)
        variant_service.add(creation)

        return self._add_to_new(new_object)

    def add_modification(self, variant_service: VariantService, change_set: ChangeSet,
                         new_object: Identifiable, original_object: Identifiable) -> bool:
        """
        Create and add a new `ObjectModification` with changes from `new_object`, and save the
        `original_object` as a reverse modification.

        :param new_object: The object that has been changed.
        :param original_object: The original object, before changes.
        """
        modification = ObjectModification()
        modification.target_object_mrid = new_object.mrid
        modification.change_set = change_set
        change_set.add_member(modification)
        variant_service.add(modification)

        self._add_modification_associations(original_object, self.original_network_service)  # TODO test this and logic may be bad...
        self._add_modification_associations(new_object, self.new_network_service)  # TODO test this
        self._add_to_original(original_object)  # ObjectReverseModification - we don't care about whether this succeeded as it should be false if the obj is already present.
        return self._add_to_new(new_object)

    def add_deletion(self, variant_service: VariantService, change_set: ChangeSet, original_object: Identifiable) -> bool:
        """
        Create and add a new `ObjectDeletion` for the provided `original_object`.

        :param original_object: The object to delete.
        """
        deletion = ObjectDeletion()
        deletion.target_object_mrid = original_object.mrid
        deletion.change_set = change_set
        change_set.add_member(deletion)
        variant_service.add(deletion)

        return self._add_to_original(original_object)

    def add_original(self, original_object: Identifiable) -> bool:
        """
        Add a base object that has no changes to the original service.
        This object may be needed as it is referenced by other objects
        that have been changed.

        :param original_object: The object to add, should be an object from the base model.
        """
        return self._add_to_original(original_object)

    def _add_to_original(self, identifiable: Identifiable) -> bool:
        """
        :return: true if the object was added to any service, false if the object already existed in one of the services and couldn't be added.
        :raises UnsupportedIdentifiableException: if `identifiable` is not supported by any service.
        """
        try:
            added = self.original_network_service.try_add(identifiable)
            if added:
                if isinstance(identifiable, Organisation):
                    self.original_customer_service.add(identifiable)  # TODO: double check this... does this make sense?
                return True
            return False
        except UnsupportedIdentifiableException:
            try:
                return self.original_diagram_service.try_add(identifiable)
            except UnsupportedIdentifiableException:
                return self.original_customer_service.try_add(identifiable)

    def _add_to_new(self, identifiable: Identifiable) -> bool:
        """
        :return: true if the object was added to any service, false if the object already existed in one of the services and couldn't be added.
        :raises UnsupportedIdentifiableException: if `identifiable` is not supported by any service.
        """
        try:
            added = self.new_network_service.try_add(identifiable)
            if added:
                if isinstance(identifiable, Organisation):
                    self.new_customer_service.add(identifiable)  # TODO: double check this... does this make sense?
                return True
            return False
        except UnsupportedIdentifiableException:
            try:
                return self.new_diagram_service.try_add(identifiable)
            except UnsupportedIdentifiableException:
                return self.new_customer_service.try_add(identifiable)

    def _add_modification_associations(self, io: Identifiable, service: BaseService):
        for field in fields(io):
            value = getattr(io, field.name, None)
            if value is None:
                continue
            if isinstance(value, Identifiable):
                service.try_add(value)
            elif isinstance(value, (list, tuple, set, frozenset)):
                for item in value:
                    if isinstance(item, Identifiable):
                        service.try_add(item)
