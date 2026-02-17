from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.autor import Autor
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    person: str | Unset = UNSET,
    fach: str | Unset = UNSET,
    org: str | Unset = UNSET,
    page: int | Unset = 1,
    per_page: int | Unset = 32,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["person"] = person

    params["fach"] = fach

    params["org"] = org

    params["page"] = page

    params["per_page"] = per_page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v2/autoren",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | list[Autor] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Autor.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | list[Autor]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    person: str | Unset = UNSET,
    fach: str | Unset = UNSET,
    org: str | Unset = UNSET,
    page: int | Unset = 1,
    per_page: int | Unset = 32,
) -> Response[Any | list[Autor]]:
    """Retrieves a list of authors filtered by optional parameters. Returns authors matching the specified
    criteria including name fragments, professional field, and organization.

    Args:
        person (str | Unset):
        fach (str | Unset):
        org (str | Unset):
        page (int | Unset):  Default: 1.
        per_page (int | Unset):  Default: 32.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | list[Autor]]
    """

    kwargs = _get_kwargs(
        person=person,
        fach=fach,
        org=org,
        page=page,
        per_page=per_page,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    person: str | Unset = UNSET,
    fach: str | Unset = UNSET,
    org: str | Unset = UNSET,
    page: int | Unset = 1,
    per_page: int | Unset = 32,
) -> Any | list[Autor] | None:
    """Retrieves a list of authors filtered by optional parameters. Returns authors matching the specified
    criteria including name fragments, professional field, and organization.

    Args:
        person (str | Unset):
        fach (str | Unset):
        org (str | Unset):
        page (int | Unset):  Default: 1.
        per_page (int | Unset):  Default: 32.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | list[Autor]
    """

    return sync_detailed(
        client=client,
        person=person,
        fach=fach,
        org=org,
        page=page,
        per_page=per_page,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    person: str | Unset = UNSET,
    fach: str | Unset = UNSET,
    org: str | Unset = UNSET,
    page: int | Unset = 1,
    per_page: int | Unset = 32,
) -> Response[Any | list[Autor]]:
    """Retrieves a list of authors filtered by optional parameters. Returns authors matching the specified
    criteria including name fragments, professional field, and organization.

    Args:
        person (str | Unset):
        fach (str | Unset):
        org (str | Unset):
        page (int | Unset):  Default: 1.
        per_page (int | Unset):  Default: 32.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | list[Autor]]
    """

    kwargs = _get_kwargs(
        person=person,
        fach=fach,
        org=org,
        page=page,
        per_page=per_page,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    person: str | Unset = UNSET,
    fach: str | Unset = UNSET,
    org: str | Unset = UNSET,
    page: int | Unset = 1,
    per_page: int | Unset = 32,
) -> Any | list[Autor] | None:
    """Retrieves a list of authors filtered by optional parameters. Returns authors matching the specified
    criteria including name fragments, professional field, and organization.

    Args:
        person (str | Unset):
        fach (str | Unset):
        org (str | Unset):
        page (int | Unset):  Default: 1.
        per_page (int | Unset):  Default: 32.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | list[Autor]
    """

    return (
        await asyncio_detailed(
            client=client,
            person=person,
            fach=fach,
            org=org,
            page=page,
            per_page=per_page,
        )
    ).parsed
