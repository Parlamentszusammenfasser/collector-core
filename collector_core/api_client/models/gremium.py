from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.parlament import Parlament
from ..types import UNSET, Unset

T = TypeVar("T", bound="Gremium")


@_attrs_define
class Gremium:
    """Ein Gremium in dem Entscheidungen getroffen werden können. z.B: Ausschüsse, Plenum, Kabinett, Volk, ...

    Attributes:
        parlament (Parlament): Enumeration der Parlamentsähnlichen Entscheidungscorpi in Deutschland
        wahlperiode (int):
        name (str): Name des betreffenden Gremiums. 'plenum', 'regierung', 'volk' sind reservierte namen Example:
            Ausschuss für Inneres und Gemüseauflauf.
        link (str | Unset):
    """

    parlament: Parlament
    wahlperiode: int
    name: str
    link: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        parlament = self.parlament.value

        wahlperiode = self.wahlperiode

        name = self.name

        link = self.link

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "parlament": parlament,
                "wahlperiode": wahlperiode,
                "name": name,
            }
        )
        if link is not UNSET:
            field_dict["link"] = link

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        parlament = Parlament(d.pop("parlament"))

        wahlperiode = d.pop("wahlperiode")

        name = d.pop("name")

        link = d.pop("link", UNSET)

        gremium = cls(
            parlament=parlament,
            wahlperiode=wahlperiode,
            name=name,
            link=link,
        )

        gremium.additional_properties = d
        return gremium

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
