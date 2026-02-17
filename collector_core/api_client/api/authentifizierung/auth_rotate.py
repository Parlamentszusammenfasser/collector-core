from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.rotation_response import RotationResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v2/auth/rotate",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | RotationResponse | None:
    if response.status_code == 201:
        response_201 = RotationResponse.from_dict(response.json())

        return response_201

    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | RotationResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Any | RotationResponse]:
    """Key rotation endpoint for creating a new API key while maintaining the existing one for a transition
    period of one day. The old key remains valid until the specified rotation_complete_date, after which
    it is automatically revoked. Rotates only the own key if it is not invalid.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | RotationResponse]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Any | RotationResponse | None:
    """Key rotation endpoint for creating a new API key while maintaining the existing one for a transition
    period of one day. The old key remains valid until the specified rotation_complete_date, after which
    it is automatically revoked. Rotates only the own key if it is not invalid.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | RotationResponse
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Any | RotationResponse]:
    """Key rotation endpoint for creating a new API key while maintaining the existing one for a transition
    period of one day. The old key remains valid until the specified rotation_complete_date, after which
    it is automatically revoked. Rotates only the own key if it is not invalid.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | RotationResponse]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Any | RotationResponse | None:
    """Key rotation endpoint for creating a new API key while maintaining the existing one for a transition
    period of one day. The old key remains valid until the specified rotation_complete_date, after which
    it is automatically revoked. Rotates only the own key if it is not invalid.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | RotationResponse
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
