from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.auth_listing_keytag_response_200 import AuthListingKeytagResponse200
from ...types import Response


def _get_kwargs(
    keytag: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v2/auth/keys/{keytag}".format(
            keytag=quote(str(keytag), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | AuthListingKeytagResponse200 | None:
    if response.status_code == 200:
        response_200 = AuthListingKeytagResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | AuthListingKeytagResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    keytag: str,
    *,
    client: AuthenticatedClient,
) -> Response[Any | AuthListingKeytagResponse200]:
    """Retrieve a detailed overview of the objects changed by this key

    Args:
        keytag (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AuthListingKeytagResponse200]
    """

    kwargs = _get_kwargs(
        keytag=keytag,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    keytag: str,
    *,
    client: AuthenticatedClient,
) -> Any | AuthListingKeytagResponse200 | None:
    """Retrieve a detailed overview of the objects changed by this key

    Args:
        keytag (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | AuthListingKeytagResponse200
    """

    return sync_detailed(
        keytag=keytag,
        client=client,
    ).parsed


async def asyncio_detailed(
    keytag: str,
    *,
    client: AuthenticatedClient,
) -> Response[Any | AuthListingKeytagResponse200]:
    """Retrieve a detailed overview of the objects changed by this key

    Args:
        keytag (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AuthListingKeytagResponse200]
    """

    kwargs = _get_kwargs(
        keytag=keytag,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    keytag: str,
    *,
    client: AuthenticatedClient,
) -> Any | AuthListingKeytagResponse200 | None:
    """Retrieve a detailed overview of the objects changed by this key

    Args:
        keytag (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | AuthListingKeytagResponse200
    """

    return (
        await asyncio_detailed(
            keytag=keytag,
            client=client,
        )
    ).parsed
