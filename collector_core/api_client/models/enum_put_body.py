from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.enum_put_body_replacing_item import EnumPutBodyReplacingItem


T = TypeVar("T", bound="EnumPutBody")


@_attrs_define
class EnumPutBody:
    """
    Attributes:
        objects (list[str]):
        replacing (list[EnumPutBodyReplacingItem] | Unset):
    """

    objects: list[str]
    replacing: list[EnumPutBodyReplacingItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        objects = self.objects

        replacing: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.replacing, Unset):
            replacing = []
            for replacing_item_data in self.replacing:
                replacing_item = replacing_item_data.to_dict()
                replacing.append(replacing_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "objects": objects,
            }
        )
        if replacing is not UNSET:
            field_dict["replacing"] = replacing

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.enum_put_body_replacing_item import EnumPutBodyReplacingItem

        d = dict(src_dict)
        objects = cast(list[str], d.pop("objects"))

        _replacing = d.pop("replacing", UNSET)
        replacing: list[EnumPutBodyReplacingItem] | Unset = UNSET
        if _replacing is not UNSET:
            replacing = []
            for replacing_item_data in _replacing:
                replacing_item = EnumPutBodyReplacingItem.from_dict(replacing_item_data)

                replacing.append(replacing_item)

        enum_put_body = cls(
            objects=objects,
            replacing=replacing,
        )

        enum_put_body.additional_properties = d
        return enum_put_body

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
