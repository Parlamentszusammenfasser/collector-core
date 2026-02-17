from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="EnumPutBodyReplacingItem")


@_attrs_define
class EnumPutBodyReplacingItem:
    """
    Attributes:
        values (list[str]):
        replaced_by (int): This value is replaced by the object with index {} in the 'objects' list above. 0-Based
            indexing.
    """

    values: list[str]
    replaced_by: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        values = self.values

        replaced_by = self.replaced_by

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "values": values,
                "replaced_by": replaced_by,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        values = cast(list[str], d.pop("values"))

        replaced_by = d.pop("replaced_by")

        enum_put_body_replacing_item = cls(
            values=values,
            replaced_by=replaced_by,
        )

        enum_put_body_replacing_item.additional_properties = d
        return enum_put_body_replacing_item

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
