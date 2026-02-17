from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.vg_ident_typ import VgIdentTyp

T = TypeVar("T", bound="VgIdent")


@_attrs_define
class VgIdent:
    """Eindeutiger Identifikator für einen Vorgang innerhalb eines Parlaments+Wahlperiode. Kann z.B. eine
    Initiativdrucksache oder eine Vorgansnummer im Parlament sein.

        Example:
            {'id': '20/12345', 'typ': 'initdrucks'}

        Attributes:
            id (str):  Example: 123e4567-e.
            typ (VgIdentTyp): Typ von Identifikatoren für einen gesamten Vorgang
    """

    id: str
    typ: VgIdentTyp
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        typ = self.typ.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "typ": typ,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        typ = VgIdentTyp(d.pop("typ"))

        vg_ident = cls(
            id=id,
            typ=typ,
        )

        vg_ident.additional_properties = d
        return vg_ident

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
