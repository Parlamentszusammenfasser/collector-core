from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.dokument import Dokument
from ...types import Response


def _get_kwargs(
    api_id: UUID,
    *,
    body: Dokument,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/v2/dokument/{api_id}".format(
            api_id=quote(str(api_id), safe=""),
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
    api_id: UUID,
    *,
    client: AuthenticatedClient,
    body: Dokument,
) -> Response[Any]:
    r"""Administrative endpoint to upload or update documents for future reference. Creates a new document
    with the specified ID or replaces an existing one.

    Args:
        api_id (UUID):
        body (Dokument): Ein Dokument. Kann z.B. ein Protokoll, eine Drucksache oder eine
            Stellungnahme sein. Man beachte, dass für verschiedene Typen verschiedene Felder nur
            formal optional sind. So ist zum Beispiel für jede Stellungnahme eine Meinung gefragt und
            für jeden Gesetzesentwurf ein Vorwort. Da Dokumente relativ große Objekte werden können
            (O(kB)), wird überall wo sie Teilobjekte sind (bei Stationen und Sitzungen) nur die UUID
            vom Server returned, und das Dokument muss in einem zweiten Request geladen werden.
            Example: {'api_id': 'a1b2c3d4-e5f6-7890-abcd-1234567890ab', 'typ': 'entwurf', 'titel':
            'Entwurf eines Gesetzes zur Änderung des Bundeswahlgesetzes', 'kurztitel': 'Änderung des
            Bundeswahlgesetzes', 'vorwort': 'Mit dem vorliegenden Entwurf soll das Bundeswahlgesetz an
            die aktuellen Anforderungen angepasst werden.', 'volltext': 'Der Bundestag hat mit
            Zustimmung des Bundesrates das folgende Gesetz beschlossen:\n\nArtikel 1\nÄnderung des
            Bundeswahlgesetzes\n\nDas Bundeswahlgesetz in der Fassung der Bekanntmachung vom 23. Juli
            1993 (BGBl. I S. 1288, 1594) wird wie folgt geändert:\n\n1. § 1 Absatz 1 wird wie folgt
            gefasst: [...]', 'zusammenfassung': 'Änderung des Bundeswahlgesetzes zur Anpassung an
            aktuelle Anforderungen.', 'zp_modifiziert': '2024-03-15T14:30:00+01:00', 'zp_referenz':
            '2024-03-01T00:00:00+01:00', 'zp_erstellt': '2024-03-10T09:15:00+01:00', 'link':
            'https://dip.bundestag.de/dokument/12345', 'hash': 'a1b2c3d4e5f6g7h8i9j0', 'meinung': 4,
            'schlagworte': ['wahlrecht', 'bundestagswahl', 'reform'], 'autoren': [{'person': 'Dr.
            Maria Schmidt', 'organisation': 'Bundesministerium des Innern', 'fachgebiet':
            'Wahlrecht'}], 'drucksnr': 'BT-Drs. 20/12345'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        api_id=api_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    api_id: UUID,
    *,
    client: AuthenticatedClient,
    body: Dokument,
) -> Response[Any]:
    r"""Administrative endpoint to upload or update documents for future reference. Creates a new document
    with the specified ID or replaces an existing one.

    Args:
        api_id (UUID):
        body (Dokument): Ein Dokument. Kann z.B. ein Protokoll, eine Drucksache oder eine
            Stellungnahme sein. Man beachte, dass für verschiedene Typen verschiedene Felder nur
            formal optional sind. So ist zum Beispiel für jede Stellungnahme eine Meinung gefragt und
            für jeden Gesetzesentwurf ein Vorwort. Da Dokumente relativ große Objekte werden können
            (O(kB)), wird überall wo sie Teilobjekte sind (bei Stationen und Sitzungen) nur die UUID
            vom Server returned, und das Dokument muss in einem zweiten Request geladen werden.
            Example: {'api_id': 'a1b2c3d4-e5f6-7890-abcd-1234567890ab', 'typ': 'entwurf', 'titel':
            'Entwurf eines Gesetzes zur Änderung des Bundeswahlgesetzes', 'kurztitel': 'Änderung des
            Bundeswahlgesetzes', 'vorwort': 'Mit dem vorliegenden Entwurf soll das Bundeswahlgesetz an
            die aktuellen Anforderungen angepasst werden.', 'volltext': 'Der Bundestag hat mit
            Zustimmung des Bundesrates das folgende Gesetz beschlossen:\n\nArtikel 1\nÄnderung des
            Bundeswahlgesetzes\n\nDas Bundeswahlgesetz in der Fassung der Bekanntmachung vom 23. Juli
            1993 (BGBl. I S. 1288, 1594) wird wie folgt geändert:\n\n1. § 1 Absatz 1 wird wie folgt
            gefasst: [...]', 'zusammenfassung': 'Änderung des Bundeswahlgesetzes zur Anpassung an
            aktuelle Anforderungen.', 'zp_modifiziert': '2024-03-15T14:30:00+01:00', 'zp_referenz':
            '2024-03-01T00:00:00+01:00', 'zp_erstellt': '2024-03-10T09:15:00+01:00', 'link':
            'https://dip.bundestag.de/dokument/12345', 'hash': 'a1b2c3d4e5f6g7h8i9j0', 'meinung': 4,
            'schlagworte': ['wahlrecht', 'bundestagswahl', 'reform'], 'autoren': [{'person': 'Dr.
            Maria Schmidt', 'organisation': 'Bundesministerium des Innern', 'fachgebiet':
            'Wahlrecht'}], 'drucksnr': 'BT-Drs. 20/12345'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        api_id=api_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
