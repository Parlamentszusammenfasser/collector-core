from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AuthListingKeytagResponse200")


@_attrs_define
class AuthListingKeytagResponse200:
    """
    Attributes:
        dokumente (list[str] | Unset):
        sitzungen (list[str] | Unset):
        vorgaenge (list[str] | Unset):
        stationen (list[str] | Unset):
    """

    dokumente: list[str] | Unset = UNSET
    sitzungen: list[str] | Unset = UNSET
    vorgaenge: list[str] | Unset = UNSET
    stationen: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dokumente: list[str] | Unset = UNSET
        if not isinstance(self.dokumente, Unset):
            dokumente = self.dokumente

        sitzungen: list[str] | Unset = UNSET
        if not isinstance(self.sitzungen, Unset):
            sitzungen = self.sitzungen

        vorgaenge: list[str] | Unset = UNSET
        if not isinstance(self.vorgaenge, Unset):
            vorgaenge = self.vorgaenge

        stationen: list[str] | Unset = UNSET
        if not isinstance(self.stationen, Unset):
            stationen = self.stationen

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if dokumente is not UNSET:
            field_dict["dokumente"] = dokumente
        if sitzungen is not UNSET:
            field_dict["sitzungen"] = sitzungen
        if vorgaenge is not UNSET:
            field_dict["vorgaenge"] = vorgaenge
        if stationen is not UNSET:
            field_dict["stationen"] = stationen

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        dokumente = cast(list[str], d.pop("dokumente", UNSET))

        sitzungen = cast(list[str], d.pop("sitzungen", UNSET))

        vorgaenge = cast(list[str], d.pop("vorgaenge", UNSET))

        stationen = cast(list[str], d.pop("stationen", UNSET))

        auth_listing_keytag_response_200 = cls(
            dokumente=dokumente,
            sitzungen=sitzungen,
            vorgaenge=vorgaenge,
            stationen=stationen,
        )

        auth_listing_keytag_response_200.additional_properties = d
        return auth_listing_keytag_response_200

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
