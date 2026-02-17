from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.sitzung import Sitzung
from ...types import Response


def _get_kwargs(
    sid: UUID,
    *,
    body: Sitzung,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/v2/sitzung/{sid}".format(
            sid=quote(str(sid), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | None:
    if response.status_code == 201:
        return None

    if response.status_code == 304:
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
    sid: UUID,
    *,
    client: AuthenticatedClient,
    body: Sitzung,
) -> Response[Any]:
    r"""Administrative endpoint to directly set or replace a parliamentary session without merging or
    matching. Replaces the entire session data if it exists, or creates a new one if it doesn't.

    Args:
        sid (UUID):
        body (Sitzung): Sitzung oder Anhörung. Eine Anhörung wird es, wenn Experten geladen
            werden. Abstrahiert und kann daher sowohl Plenarsitzung als auch Ausschusssitzung sein.
            Example: {'api_id': 'b1a2c3d4-e5f6-7890-fedc-1234567890ab', 'titel': '143. Sitzung des
            Deutschen Bundestages', 'termin': '2024-05-20T09:00:00+02:00', 'gremium': {'parlament':
            'BT', 'wahlperiode': 20, 'name': 'plenum'}, 'nummer': 143, 'public': True, 'link':
            'https://www.bundestag.de/sitzung/20240520', 'tops': [{'nummer': 1, 'titel': 'Eröffnung
            der Sitzung'}, {'nummer': 3, 'titel': 'Erste Beratung des von den Fraktionen SPD, BÜNDNIS
            90/DIE GRÜNEN und FDP eingebrachten Entwurfs eines Gesetzes zur Änderung des
            Bundeswahlgesetzes', 'vorgang_id': ['123e4567-e89b-12d3-a456-426614174000'], 'dokumente':
            []}], 'dokumente': [{'api_id': 'c1d2e3f4-a5b6-7890-cdef-1234567890gh', 'typ': 'tops',
            'titel': 'Tagesordnung der 143. Sitzung des Deutschen Bundestages', 'volltext': 'TOP 1:
            Eröffnung der Sitzung\nTOP 2: Fragestunde\nTOP 3: Erste Beratung des Gesetzentwurfs zur
            Änderung des Bundeswahlgesetzes\n...', 'hash': 'a1b2c3d4e5f6g7h8i9j0', 'zp_modifiziert':
            '2024-05-15T14:30:00+02:00', 'zp_referenz': '2024-05-20T09:00:00+02:00', 'link':
            'https://www.bundestag.de/tagesordnung/20240520', 'autoren': [{'organisation': 'Deutscher
            Bundestag'}]}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        sid=sid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    sid: UUID,
    *,
    client: AuthenticatedClient,
    body: Sitzung,
) -> Response[Any]:
    r"""Administrative endpoint to directly set or replace a parliamentary session without merging or
    matching. Replaces the entire session data if it exists, or creates a new one if it doesn't.

    Args:
        sid (UUID):
        body (Sitzung): Sitzung oder Anhörung. Eine Anhörung wird es, wenn Experten geladen
            werden. Abstrahiert und kann daher sowohl Plenarsitzung als auch Ausschusssitzung sein.
            Example: {'api_id': 'b1a2c3d4-e5f6-7890-fedc-1234567890ab', 'titel': '143. Sitzung des
            Deutschen Bundestages', 'termin': '2024-05-20T09:00:00+02:00', 'gremium': {'parlament':
            'BT', 'wahlperiode': 20, 'name': 'plenum'}, 'nummer': 143, 'public': True, 'link':
            'https://www.bundestag.de/sitzung/20240520', 'tops': [{'nummer': 1, 'titel': 'Eröffnung
            der Sitzung'}, {'nummer': 3, 'titel': 'Erste Beratung des von den Fraktionen SPD, BÜNDNIS
            90/DIE GRÜNEN und FDP eingebrachten Entwurfs eines Gesetzes zur Änderung des
            Bundeswahlgesetzes', 'vorgang_id': ['123e4567-e89b-12d3-a456-426614174000'], 'dokumente':
            []}], 'dokumente': [{'api_id': 'c1d2e3f4-a5b6-7890-cdef-1234567890gh', 'typ': 'tops',
            'titel': 'Tagesordnung der 143. Sitzung des Deutschen Bundestages', 'volltext': 'TOP 1:
            Eröffnung der Sitzung\nTOP 2: Fragestunde\nTOP 3: Erste Beratung des Gesetzentwurfs zur
            Änderung des Bundeswahlgesetzes\n...', 'hash': 'a1b2c3d4e5f6g7h8i9j0', 'zp_modifiziert':
            '2024-05-15T14:30:00+02:00', 'zp_referenz': '2024-05-20T09:00:00+02:00', 'link':
            'https://www.bundestag.de/tagesordnung/20240520', 'autoren': [{'organisation': 'Deutscher
            Bundestag'}]}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        sid=sid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
