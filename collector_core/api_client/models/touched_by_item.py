from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TouchedByItem")


@_attrs_define
class TouchedByItem:
    """
    Attributes:
        scraper_id (UUID | Unset): uuid of the scraper that touched this object
        key (str | Unset): Key hash of the scraper that touched the object
    """

    scraper_id: UUID | Unset = UNSET
    key: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scraper_id: str | Unset = UNSET
        if not isinstance(self.scraper_id, Unset):
            scraper_id = str(self.scraper_id)

        key = self.key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if scraper_id is not UNSET:
            field_dict["scraper_id"] = scraper_id
        if key is not UNSET:
            field_dict["key"] = key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _scraper_id = d.pop("scraper_id", UNSET)
        scraper_id: UUID | Unset
        if isinstance(_scraper_id, Unset):
            scraper_id = UNSET
        else:
            scraper_id = UUID(_scraper_id)

        key = d.pop("key", UNSET)

        touched_by_item = cls(
            scraper_id=scraper_id,
            key=key,
        )

        touched_by_item.additional_properties = d
        return touched_by_item

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
