from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.gremium import Gremium
from ...models.parlament import Parlament
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    gr: str | Unset = UNSET,
    p: Parlament | Unset = UNSET,
    wp: int | Unset = UNSET,
    page: int | Unset = 1,
    per_page: int | Unset = 32,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["gr"] = gr

    json_p: str | Unset = UNSET
    if not isinstance(p, Unset):
        json_p = p.value

    params["p"] = json_p

    params["wp"] = wp

    params["page"] = page

    params["per_page"] = per_page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v2/gremien",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | list[Gremium] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Gremium.from_dict(response_200_item_data)

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
) -> Response[Any | list[Gremium]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    gr: str | Unset = UNSET,
    p: Parlament | Unset = UNSET,
    wp: int | Unset = UNSET,
    page: int | Unset = 1,
    per_page: int | Unset = 32,
) -> Response[Any | list[Gremium]]:
    """Retrieves a list of committees filtered by optional parameters. Returns committees matching the
    specified criteria from parliament bodies and electoral periods.

    Args:
        gr (str | Unset):
        p (Parlament | Unset): Enumeration der Parlamentsähnlichen Entscheidungscorpi in
            Deutschland
        wp (int | Unset):
        page (int | Unset):  Default: 1.
        per_page (int | Unset):  Default: 32.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | list[Gremium]]
    """

    kwargs = _get_kwargs(
        gr=gr,
        p=p,
        wp=wp,
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
    gr: str | Unset = UNSET,
    p: Parlament | Unset = UNSET,
    wp: int | Unset = UNSET,
    page: int | Unset = 1,
    per_page: int | Unset = 32,
) -> Any | list[Gremium] | None:
    """Retrieves a list of committees filtered by optional parameters. Returns committees matching the
    specified criteria from parliament bodies and electoral periods.

    Args:
        gr (str | Unset):
        p (Parlament | Unset): Enumeration der Parlamentsähnlichen Entscheidungscorpi in
            Deutschland
        wp (int | Unset):
        page (int | Unset):  Default: 1.
        per_page (int | Unset):  Default: 32.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | list[Gremium]
    """

    return sync_detailed(
        client=client,
        gr=gr,
        p=p,
        wp=wp,
        page=page,
        per_page=per_page,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    gr: str | Unset = UNSET,
    p: Parlament | Unset = UNSET,
    wp: int | Unset = UNSET,
    page: int | Unset = 1,
    per_page: int | Unset = 32,
) -> Response[Any | list[Gremium]]:
    """Retrieves a list of committees filtered by optional parameters. Returns committees matching the
    specified criteria from parliament bodies and electoral periods.

    Args:
        gr (str | Unset):
        p (Parlament | Unset): Enumeration der Parlamentsähnlichen Entscheidungscorpi in
            Deutschland
        wp (int | Unset):
        page (int | Unset):  Default: 1.
        per_page (int | Unset):  Default: 32.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | list[Gremium]]
    """

    kwargs = _get_kwargs(
        gr=gr,
        p=p,
        wp=wp,
        page=page,
        per_page=per_page,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    gr: str | Unset = UNSET,
    p: Parlament | Unset = UNSET,
    wp: int | Unset = UNSET,
    page: int | Unset = 1,
    per_page: int | Unset = 32,
) -> Any | list[Gremium] | None:
    """Retrieves a list of committees filtered by optional parameters. Returns committees matching the
    specified criteria from parliament bodies and electoral periods.

    Args:
        gr (str | Unset):
        p (Parlament | Unset): Enumeration der Parlamentsähnlichen Entscheidungscorpi in
            Deutschland
        wp (int | Unset):
        page (int | Unset):  Default: 1.
        per_page (int | Unset):  Default: 32.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | list[Gremium]
    """

    return (
        await asyncio_detailed(
            client=client,
            gr=gr,
            p=p,
            wp=wp,
            page=page,
            per_page=per_page,
        )
    ).parsed
