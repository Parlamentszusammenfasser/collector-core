from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Autor")


@_attrs_define
class Autor:
    """Eine Person oder Organisation, die eine bestimmte Funktion übernommen hat. Z.B: Autor einer Stellungnahme, Experte
    bei einer Anhörung, Initiator eines Vorgangs.

        Example:
            {'person': 'Prof. Dr. Susanne Meyer', 'organisation': 'Universität Heidelberg', 'fachgebiet':
                'Verfassungsrecht', 'lobbyregister': 'https://www.lobbyregister.bundestag.de/suche/experte/12345'}

        Attributes:
            organisation (str):
            person (str | Unset):
            fachgebiet (str | Unset):
            lobbyregister (str | Unset):
    """

    organisation: str
    person: str | Unset = UNSET
    fachgebiet: str | Unset = UNSET
    lobbyregister: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        organisation = self.organisation

        person = self.person

        fachgebiet = self.fachgebiet

        lobbyregister = self.lobbyregister

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "organisation": organisation,
            }
        )
        if person is not UNSET:
            field_dict["person"] = person
        if fachgebiet is not UNSET:
            field_dict["fachgebiet"] = fachgebiet
        if lobbyregister is not UNSET:
            field_dict["lobbyregister"] = lobbyregister

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        organisation = d.pop("organisation")

        person = d.pop("person", UNSET)

        fachgebiet = d.pop("fachgebiet", UNSET)

        lobbyregister = d.pop("lobbyregister", UNSET)

        autor = cls(
            organisation=organisation,
            person=person,
            fachgebiet=fachgebiet,
            lobbyregister=lobbyregister,
        )

        autor.additional_properties = d
        return autor

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
