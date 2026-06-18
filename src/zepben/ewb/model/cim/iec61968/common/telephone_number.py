#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TelephoneNumber"]

from dataclasses import field, dataclass


@dataclass(slots=True)
class TelephoneNumber:
    """
    Telephone number.

    :var area_code: (if applicable) Area or region code.
    :var city_code: (if applicable) City code.
    :var country_code: Country code.
    :var dial_out: (if applicable) Dial out code, for instance to call outside an enterprise.
    :var extension: (if applicable) Extension for this telephone number.
    :var international_prefix: (if applicable) Prefix used when calling an international number.
    :var itu_phone: Phone number according to ITU E.164. Will return ``None`` if a valid number cannot be calculated
    :var partial_itu_phone: As much of the phone number according to ITU E.164 that could be formatted based on the given fields.
    :var local_number: Main (local) part of this telephone number.
    :var is_primary: [ZBEX] Is this telephone number the primary number.
    :var description: [ZBEX] Description for this phone number, e.g: home, work, mobile.
    """

    area_code: str | None = None
    """(if applicable) Area or region code."""

    city_code: str | None = None
    """(if applicable) City code."""

    country_code: str | None = None
    """Country code."""

    dial_out: str | None = None
    """(if applicable) Dial out code, for instance to call outside an enterprise."""

    extension: str | None = None
    """(if applicable) Extension for this telephone number."""

    international_prefix: str | None = None
    """(if applicable) Prefix used when calling an international number."""

    itu_phone: str | None = field(default=None)
    """Phone number according to ITU E.164. Will return ``None`` if a valid number cannot be calculated"""

    partial_itu_phone: str | None = field(default=None)
    """As much of the phone number according to ITU E.164 that could be formatted based on the given fields."""

    local_number: str | None = None
    """Main (local) part of this telephone number."""

    is_primary: str | None = None
    """[ZBEX] Is this telephone number the primary number."""

    description: str | None = None
    """[ZBEX] Description for this phone number, e.g: home, work, mobile."""

    def __post_init__(self):
        if self.country_code is not None and (it := self._maybe_itu_formatted_phone())is not None and len(it) <= 15:
            self.itu_phone = it
        self.partial_itu_phone = self._maybe_itu_formatted_phone() if self.itu_phone is None else None

    def _maybe_itu_formatted_phone(self) -> str | None:
        return f"{self.country_code or ''}{self.area_code or ''}{self.city_code or ''}{self.local_number or ''}" or None

    def __hash__(self):
        return hash((type(self), *(getattr(self, s ) for s in self.__slots__)))

    def __str__(self):
        def inner():
            yield self.dial_out
            yield f"{self.international_prefix or ''}{self._maybe_itu_formatted_phone()}"
            if self.extension is not None:
                yield f'ext {self.extension}'

        return f"{self.description}: {' '.join(inner())} [primary: {self.is_primary}]"
