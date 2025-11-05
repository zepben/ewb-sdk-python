#  Copyright 2025 Zeppelin Bend Pty Ltd
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["TelephoneNumber"]

from dataclasses import field, dataclass


@dataclass
class TelephoneNumber:
    """
    Telephone number.
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
    """Phone number according to ITU E.164. Will return `null` if a valid"""  # TODO: lulwut? also jvmsdk
    partial_itu_phone: str | None = field(default=None)
    """As much of the phone number according to ITU E.164 that could be formatted based on the given fields."""
    local_number: str | None = None
    """Main (local) part of this telephone number."""
    is_primary: str | None = None
    """[ZBEX] Is this telephone number the primary number."""
    description: str | None = None
    """[ZBEX] Description for this phone number, e.g: home, work, mobile."""

    def __post_init__(self):
        if self.country_code is not None and len(it := self.maybe_itu_formatted_phone()) <= 15:
            self.itu_phone = it
        self.partial_itu_phone = self.maybe_itu_formatted_phone() if self.itu_phone is None else None

    def maybe_itu_formatted_phone(self) -> str | None:
        return f"{self.country_code or ''}{self.area_code or ''}{self.city_code or ''}{self.local_number or ''}" or None

    def __str__(self):
        def inner():
            yield self.dial_out
            yield f"{self.international_prefix or ''}{self.maybe_itu_formatted_phone()}"
            if self.extension is not None:
                yield f'ext {self.extension}'

        return f"{self.description}: {' '.join(inner())} [primary: {self.is_primary}]"
