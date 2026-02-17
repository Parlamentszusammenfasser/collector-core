from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="RotationResponse")


@_attrs_define
class RotationResponse:
    """Response from a successful key rotation request

    Attributes:
        new_api_key (str): The newly created API key (shown only once)
        rotation_complete_date (datetime.datetime): Confirmed date when the old key will be invalidated
    """

    new_api_key: str
    rotation_complete_date: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        new_api_key = self.new_api_key

        rotation_complete_date = self.rotation_complete_date.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "new_api_key": new_api_key,
                "rotation_complete_date": rotation_complete_date,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        new_api_key = d.pop("new_api_key")

        rotation_complete_date = isoparse(d.pop("rotation_complete_date"))

        rotation_response = cls(
            new_api_key=new_api_key,
            rotation_complete_date=rotation_complete_date,
        )

        rotation_response.additional_properties = d
        return rotation_response

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
