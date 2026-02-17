from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.autor import Autor


T = TypeVar("T", bound="AutorenPutBodyReplacingItem")


@_attrs_define
class AutorenPutBodyReplacingItem:
    """
    Attributes:
        values (list[Autor]):
        replaced_by (int): This object is replaced by the object with index {} in the 'objects' list above. 0-Based
            indexing.
    """

    values: list[Autor]
    replaced_by: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        values = []
        for values_item_data in self.values:
            values_item = values_item_data.to_dict()
            values.append(values_item)

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
        from ..models.autor import Autor

        d = dict(src_dict)
        values = []
        _values = d.pop("values")
        for values_item_data in _values:
            values_item = Autor.from_dict(values_item_data)

            values.append(values_item)

        replaced_by = d.pop("replaced_by")

        autoren_put_body_replacing_item = cls(
            values=values,
            replaced_by=replaced_by,
        )

        autoren_put_body_replacing_item.additional_properties = d
        return autoren_put_body_replacing_item

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
