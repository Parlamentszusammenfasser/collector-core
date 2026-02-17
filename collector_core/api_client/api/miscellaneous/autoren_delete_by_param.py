from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    person: str | Unset = UNSET,
    fach: str | Unset = UNSET,
    org: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["person"] = person

    params["fach"] = fach

    params["org"] = org

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/v2/autoren",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | None:
    if response.status_code == 204:
        return None

    if response.status_code == 403:
        return None

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    person: str | Unset = UNSET,
    fach: str | Unset = UNSET,
    org: str | Unset = UNSET,
) -> Response[Any]:
    """Administrative endpoint to delete authors matching the specified criteria. Removes all authors that
    match the filter parameters.

    Args:
        person (str | Unset):
        fach (str | Unset):
        org (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        person=person,
        fach=fach,
        org=org,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    person: str | Unset = UNSET,
    fach: str | Unset = UNSET,
    org: str | Unset = UNSET,
) -> Response[Any]:
    """Administrative endpoint to delete authors matching the specified criteria. Removes all authors that
    match the filter parameters.

    Args:
        person (str | Unset):
        fach (str | Unset):
        org (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        person=person,
        fach=fach,
        org=org,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
