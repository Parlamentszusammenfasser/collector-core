from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.api_key_status_scope import ApiKeyStatusScope

T = TypeVar("T", bound="ApiKeyStatus")


@_attrs_define
class ApiKeyStatus:
    """Status information about the API key used in the current request

    Attributes:
        scope (ApiKeyStatusScope):
        expires_at (datetime.datetime): When this key will expire. If is_being_rotated is true, this is the date the
            rotation is complete.
        is_being_rotated (bool): Whether this key is currently in a transition process
    """

    scope: ApiKeyStatusScope
    expires_at: datetime.datetime
    is_being_rotated: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scope = self.scope.value

        expires_at = self.expires_at.isoformat()

        is_being_rotated = self.is_being_rotated

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scope": scope,
                "expires_at": expires_at,
                "is_being_rotated": is_being_rotated,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        scope = ApiKeyStatusScope(d.pop("scope"))

        expires_at = isoparse(d.pop("expires_at"))

        is_being_rotated = d.pop("is_being_rotated")

        api_key_status = cls(
            scope=scope,
            expires_at=expires_at,
            is_being_rotated=is_being_rotated,
        )

        api_key_status.additional_properties = d
        return api_key_status

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
