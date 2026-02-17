from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import Response


def _get_kwargs(
    *,
    api_key_delete: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["api-key-delete"] = api_key_delete

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/v2/auth",
    }

    _kwargs["headers"] = headers
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
    api_key_delete: str,
) -> Response[Any]:
    """Key adder interface for removing API keys from the system. Allows administrators and key management
    services to revoke access by deleting an existing API key.

    Args:
        api_key_delete (str): A uniquely identifying string that is generated from key data within
            the database

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        api_key_delete=api_key_delete,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    api_key_delete: str,
) -> Response[Any]:
    """Key adder interface for removing API keys from the system. Allows administrators and key management
    services to revoke access by deleting an existing API key.

    Args:
        api_key_delete (str): A uniquely identifying string that is generated from key data within
            the database

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        api_key_delete=api_key_delete,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
