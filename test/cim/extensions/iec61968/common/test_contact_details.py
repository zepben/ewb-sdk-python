#  Copyright 2026 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
from hypothesis import given
from hypothesis.strategies import builds, text, sampled_from, booleans

from cim.cim_creators import ALPHANUM
from cim.private_collection_validator import validate_unordered_other, DuplicateBehaviour
from streaming.get.pb_creators import lists
from zepben.ewb import ContactMethodType, TelephoneNumber, ElectronicAddress, ContactDetails


contact_details_kwargs = {
    "id": text(alphabet=ALPHANUM),
    "contact_address": text(alphabet=ALPHANUM),
    "contact_type": text(alphabet=ALPHANUM),
    "first_name": text(alphabet=ALPHANUM),
    "last_name": text(alphabet=ALPHANUM),
    "preferred_contact_method": sampled_from(ContactMethodType),
    "is_primary": booleans(),
    "business_name": text(alphabet=ALPHANUM),
    "phone_numbers": lists(builds(TelephoneNumber)),
    "electronic_addresses": lists(builds(ElectronicAddress)),
}


contact_details_args = [
    text(alphabet=ALPHANUM),
    text(alphabet=ALPHANUM),
    text(alphabet=ALPHANUM),
    text(alphabet=ALPHANUM),
    text(alphabet=ALPHANUM),
    sampled_from(ContactMethodType),
    booleans(),
    text(alphabet=ALPHANUM),
    [TelephoneNumber()],
    [ElectronicAddress()],
]


def test_contact_details_constructor_default():
    c = ContactDetails(id="test")

    assert c.contact_address is None
    assert c.contact_type is None
    assert c.first_name is None
    assert c.last_name is None
    assert c.preferred_contact_method == ContactMethodType.UNKNOWN
    assert c.is_primary is None
    assert c.business_name is None
    assert not list(c.phone_numbers)
    assert not list(c.electronic_addresses)


@given(**contact_details_kwargs)
def test_contact_details_constructor_kwargs(
    id,
    contact_address,
    contact_type,
    first_name,
    last_name,
    preferred_contact_method,
    is_primary,
    business_name,
    phone_numbers,
    electronic_addresses
):
    c = ContactDetails(
        id=id,
        contact_address=contact_address,
        contact_type=contact_type,
        first_name=first_name,
        last_name=last_name,
        preferred_contact_method=preferred_contact_method,
        is_primary=is_primary,
        business_name=business_name,
        phone_numbers=phone_numbers,
        electronic_addresses=electronic_addresses
    )

    assert c.contact_address == contact_address
    assert c.contact_type == contact_type
    assert c.first_name == first_name
    assert c.last_name == last_name
    assert c.preferred_contact_method == preferred_contact_method
    assert c.is_primary == is_primary
    assert c.business_name == business_name
    assert list(c.phone_numbers) == phone_numbers
    assert list(c.electronic_addresses) == electronic_addresses


def test_contact_details_constructor_args():
    c = ContactDetails(*contact_details_args)

    assert c.id == contact_details_args[-10]
    assert c.contact_address == contact_details_args[-9]
    assert c.contact_type == contact_details_args[-8]
    assert c.first_name == contact_details_args[-7]
    assert c.last_name == contact_details_args[-6]
    assert c.preferred_contact_method == contact_details_args[-5]
    assert c.is_primary == contact_details_args[-4]
    assert c.business_name == contact_details_args[-3]
    assert list(c.phone_numbers) == contact_details_args[-2]
    assert list(c.electronic_addresses) == contact_details_args[-1]

def test_phone_number_collection():
    def get_phone_number(it: ContactDetails, number: str):
        for tn in it.phone_numbers:
            if tn.local_number == number:
                return tn
        raise KeyError(number)

    validate_unordered_other(
        ContactDetails,
        lambda it: TelephoneNumber(local_number=it),
        ContactDetails.phone_numbers,
        ContactDetails.num_phone_numbers,
        get_phone_number,
        ContactDetails.add_phone_number,
        ContactDetails.remove_phone_number,
        ContactDetails.clear_phone_numbers,
        lambda it: it.local_number,
        duplicate_behaviour=DuplicateBehaviour.SUPPORTED
    )

def test_electronic_address_collection():
    def get_electronic_address(it: ContactDetails, number: str):
        for tn in it.electronic_addresses:
            if tn.email1 == number:
                return tn
        raise KeyError(number)

    validate_unordered_other(
        ContactDetails,
        lambda it: ElectronicAddress(email1=it),
        ContactDetails.electronic_addresses,
        ContactDetails.num_electronic_addresses,
        get_electronic_address,
        ContactDetails.add_electronic_address,
        ContactDetails.remove_electronic_address,
        ContactDetails.clear_electronic_addresses,
        lambda it: it.email1,
        duplicate_behaviour=DuplicateBehaviour.SUPPORTED
    )
