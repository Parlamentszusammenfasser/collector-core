from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.enumeration_names import EnumerationNames
from ...types import UNSET, Response, Unset


def _get_kwargs(
    name: EnumerationNames,
    *,
    contains: str | Unset = UNSET,
    page: int | Unset = 1,
    per_page: int | Unset = 32,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["contains"] = contains

    params["page"] = page

    params["per_page"] = per_page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v2/enumeration/{name}".format(
            name=quote(str(name), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | list[str] | None:
    if response.status_code == 200:
        response_200 = cast(list[str], response.json())

        return response_200

    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | list[str]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    name: EnumerationNames,
    *,
    client: AuthenticatedClient | Client,
    contains: str | Unset = UNSET,
    page: int | Unset = 1,
    per_page: int | Unset = 32,
) -> Response[Any | list[str]]:
    """Retrieves values from a specified enumeration type. Returns a list of valid values that can be used
    in other API operations, optionally filtered by a substring.

    Args:
        name (EnumerationNames):
        contains (str | Unset):
        page (int | Unset):  Default: 1.
        per_page (int | Unset):  Default: 32.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | list[str]]
    """

    kwargs = _get_kwargs(
        name=name,
        contains=contains,
        page=page,
        per_page=per_page,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: EnumerationNames,
    *,
    client: AuthenticatedClient | Client,
    contains: str | Unset = UNSET,
    page: int | Unset = 1,
    per_page: int | Unset = 32,
) -> Any | list[str] | None:
    """Retrieves values from a specified enumeration type. Returns a list of valid values that can be used
    in other API operations, optionally filtered by a substring.

    Args:
        name (EnumerationNames):
        contains (str | Unset):
        page (int | Unset):  Default: 1.
        per_page (int | Unset):  Default: 32.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | list[str]
    """

    return sync_detailed(
        name=name,
        client=client,
        contains=contains,
        page=page,
        per_page=per_page,
    ).parsed


async def asyncio_detailed(
    name: EnumerationNames,
    *,
    client: AuthenticatedClient | Client,
    contains: str | Unset = UNSET,
    page: int | Unset = 1,
    per_page: int | Unset = 32,
) -> Response[Any | list[str]]:
    """Retrieves values from a specified enumeration type. Returns a list of valid values that can be used
    in other API operations, optionally filtered by a substring.

    Args:
        name (EnumerationNames):
        contains (str | Unset):
        page (int | Unset):  Default: 1.
        per_page (int | Unset):  Default: 32.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | list[str]]
    """

    kwargs = _get_kwargs(
        name=name,
        contains=contains,
        page=page,
        per_page=per_page,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: EnumerationNames,
    *,
    client: AuthenticatedClient | Client,
    contains: str | Unset = UNSET,
    page: int | Unset = 1,
    per_page: int | Unset = 32,
) -> Any | list[str] | None:
    """Retrieves values from a specified enumeration type. Returns a list of valid values that can be used
    in other API operations, optionally filtered by a substring.

    Args:
        name (EnumerationNames):
        contains (str | Unset):
        page (int | Unset):  Default: 1.
        per_page (int | Unset):  Default: 32.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | list[str]
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            contains=contains,
            page=page,
            per_page=per_page,
        )
    ).parsed
