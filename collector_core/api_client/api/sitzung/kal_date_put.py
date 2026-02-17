import datetime
from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.parlament import Parlament
from ...models.sitzung import Sitzung
from ...types import Response


def _get_kwargs(
    parlament: Parlament,
    datum: datetime.date,
    *,
    body: list[Sitzung],
    x_scraper_id: UUID,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["X-Scraper-Id"] = x_scraper_id

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/v2/kalender/{parlament}/{datum}".format(
            parlament=quote(str(parlament), safe=""),
            datum=quote(str(datum), safe=""),
        ),
    }

    _kwargs["json"] = []
    for body_item_data in body:
        body_item = body_item_data.to_dict()
        _kwargs["json"].append(body_item)

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | None:
    if response.status_code == 201:
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
    parlament: Parlament,
    datum: datetime.date,
    *,
    client: AuthenticatedClient,
    body: list[Sitzung],
    x_scraper_id: UUID,
) -> Response[Any]:
    """Collector interface for adding or updating sessions for a specific date and parliament. Completely
    replaces all sessions for the given date, with restrictions based on how far in the past the date
    is. Admin API keys can override the time restriction.

    Args:
        parlament (Parlament): Enumeration der Parlamentsähnlichen Entscheidungscorpi in
            Deutschland
        datum (datetime.date):
        x_scraper_id (UUID):
        body (list[Sitzung]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        parlament=parlament,
        datum=datum,
        body=body,
        x_scraper_id=x_scraper_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    parlament: Parlament,
    datum: datetime.date,
    *,
    client: AuthenticatedClient,
    body: list[Sitzung],
    x_scraper_id: UUID,
) -> Response[Any]:
    """Collector interface for adding or updating sessions for a specific date and parliament. Completely
    replaces all sessions for the given date, with restrictions based on how far in the past the date
    is. Admin API keys can override the time restriction.

    Args:
        parlament (Parlament): Enumeration der Parlamentsähnlichen Entscheidungscorpi in
            Deutschland
        datum (datetime.date):
        x_scraper_id (UUID):
        body (list[Sitzung]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        parlament=parlament,
        datum=datum,
        body=body,
        x_scraper_id=x_scraper_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
