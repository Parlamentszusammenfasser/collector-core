from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.vorgangstyp import Vorgangstyp
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.autor import Autor
    from ..models.lobbyregeintrag import Lobbyregeintrag
    from ..models.station import Station
    from ..models.touched_by_item import TouchedByItem
    from ..models.vg_ident import VgIdent


T = TypeVar("T", bound="Vorgang")


@_attrs_define
class Vorgang:
    """'Master-Objekt' der API. Der Wrapper um Stationen, die den Beratungsverlauf tatsächlich beschreiben. Ein Vorgang
    kann dabei nicht nur ein Gesetz, sondern auch ein parlamentarischer Antrag sein.

        Example:
            {'api_id': '123e4567-e89b-12d3-a456-426614174000', 'titel': 'Gesetz zur Änderung des Bundeswahlgesetzes und
                anderer Gesetze', 'kurztitel': 'Wahlrechtsreform', 'wahlperiode': 20, 'verfassungsaendernd': False, 'typ': 'gg-
                einspruch', 'ids': [{'id': '20/12345', 'typ': 'initdrucks'}, {'id': 'WR-2024-01', 'typ': 'vorgnr'}], 'links':
                ['https://www.bundestag.de/dokumente/textarchiv/2024/wahlrechtsreform',
                'https://dip.bundestag.de/vorgang/123456'], 'initiatoren': [{'person': 'Dr. Friedrich Merz', 'organisation':
                'CDU/CSU-Fraktion', 'fachgebiet': 'Innenpolitik'}, {'organisation': 'SPD-Fraktion'}], 'stationen': [{'api_id':
                'f1e2d3c4-b5a6-7890-abcd-1234567890cd', 'titel': 'Erste Lesung im Bundestag', 'zp_start':
                '2024-04-15T10:00:00+02:00', 'zp_modifiziert': '2024-04-15T13:45:00+02:00', 'parlament': 'BT', 'typ': 'parl-
                vollvlsgn', 'dokumente': []}], 'lobbyregister': [{'organisation': {'organisation': 'Bundesverband der Deutschen
                Industrie e.V.', 'person': 'Dr. Johannes Weber'}, 'interne_id': 'LR-ID-12345678', 'intention': 'Stellungnahme zu
                Auswirkungen der Gesetzesänderung auf die deutsche Wirtschaft.', 'link':
                'https://www.lobbyregister.bundestag.de/eintragung/12345678', 'betroffene_drucksachen': ['BT-Drs. 20/12345']}]}

        Attributes:
            api_id (UUID):  Example: 123e4567-e89b-12d3-a456-426614174000.
            titel (str):
            wahlperiode (int): Nummer der Wahlperiode, in der der Vorgang stattfindet
            verfassungsaendernd (bool):
            typ (Vorgangstyp): Der Gesetzgebungstrack auf dem wir uns befinden. Zum Beispiel: gesetzgebung -
                Einspruchsgesetz. Legt fest, welche Stationen im Vorgang möglich sind zusammen mit den Parlamenten in den
                Stationen
            initiatoren (list[Autor]): Liste von Personen oder Organisationen, die den Vorgang initiiert haben. Kann z.B.
                eine Person, eine Organisation oder ein Gremium sein.
            stationen (list[Station]):
            touched_by (list[TouchedByItem] | Unset): list of scraper uuids / key database ids that have touched this object
            kurztitel (str | Unset):
            ids (list[VgIdent] | Unset):
            links (list[str] | Unset):
            lobbyregister (list[Lobbyregeintrag] | Unset):
    """

    api_id: UUID
    titel: str
    wahlperiode: int
    verfassungsaendernd: bool
    typ: Vorgangstyp
    initiatoren: list[Autor]
    stationen: list[Station]
    touched_by: list[TouchedByItem] | Unset = UNSET
    kurztitel: str | Unset = UNSET
    ids: list[VgIdent] | Unset = UNSET
    links: list[str] | Unset = UNSET
    lobbyregister: list[Lobbyregeintrag] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        api_id = str(self.api_id)

        titel = self.titel

        wahlperiode = self.wahlperiode

        verfassungsaendernd = self.verfassungsaendernd

        typ = self.typ.value

        initiatoren = []
        for initiatoren_item_data in self.initiatoren:
            initiatoren_item = initiatoren_item_data.to_dict()
            initiatoren.append(initiatoren_item)

        stationen = []
        for stationen_item_data in self.stationen:
            stationen_item = stationen_item_data.to_dict()
            stationen.append(stationen_item)

        touched_by: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.touched_by, Unset):
            touched_by = []
            for componentsschemastouched_by_item_data in self.touched_by:
                componentsschemastouched_by_item = componentsschemastouched_by_item_data.to_dict()
                touched_by.append(componentsschemastouched_by_item)

        kurztitel = self.kurztitel

        ids: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.ids, Unset):
            ids = []
            for ids_item_data in self.ids:
                ids_item = ids_item_data.to_dict()
                ids.append(ids_item)

        links: list[str] | Unset = UNSET
        if not isinstance(self.links, Unset):
            links = self.links

        lobbyregister: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.lobbyregister, Unset):
            lobbyregister = []
            for lobbyregister_item_data in self.lobbyregister:
                lobbyregister_item = lobbyregister_item_data.to_dict()
                lobbyregister.append(lobbyregister_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "api_id": api_id,
                "titel": titel,
                "wahlperiode": wahlperiode,
                "verfassungsaendernd": verfassungsaendernd,
                "typ": typ,
                "initiatoren": initiatoren,
                "stationen": stationen,
            }
        )
        if touched_by is not UNSET:
            field_dict["touched_by"] = touched_by
        if kurztitel is not UNSET:
            field_dict["kurztitel"] = kurztitel
        if ids is not UNSET:
            field_dict["ids"] = ids
        if links is not UNSET:
            field_dict["links"] = links
        if lobbyregister is not UNSET:
            field_dict["lobbyregister"] = lobbyregister

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.autor import Autor
        from ..models.lobbyregeintrag import Lobbyregeintrag
        from ..models.station import Station
        from ..models.touched_by_item import TouchedByItem
        from ..models.vg_ident import VgIdent

        d = dict(src_dict)
        api_id = UUID(d.pop("api_id"))

        titel = d.pop("titel")

        wahlperiode = d.pop("wahlperiode")

        verfassungsaendernd = d.pop("verfassungsaendernd")

        typ = Vorgangstyp(d.pop("typ"))

        initiatoren = []
        _initiatoren = d.pop("initiatoren")
        for initiatoren_item_data in _initiatoren:
            initiatoren_item = Autor.from_dict(initiatoren_item_data)

            initiatoren.append(initiatoren_item)

        stationen = []
        _stationen = d.pop("stationen")
        for stationen_item_data in _stationen:
            stationen_item = Station.from_dict(stationen_item_data)

            stationen.append(stationen_item)

        _touched_by = d.pop("touched_by", UNSET)
        touched_by: list[TouchedByItem] | Unset = UNSET
        if _touched_by is not UNSET:
            touched_by = []
            for componentsschemastouched_by_item_data in _touched_by:
                componentsschemastouched_by_item = TouchedByItem.from_dict(
                    componentsschemastouched_by_item_data
                )

                touched_by.append(componentsschemastouched_by_item)

        kurztitel = d.pop("kurztitel", UNSET)

        _ids = d.pop("ids", UNSET)
        ids: list[VgIdent] | Unset = UNSET
        if _ids is not UNSET:
            ids = []
            for ids_item_data in _ids:
                ids_item = VgIdent.from_dict(ids_item_data)

                ids.append(ids_item)

        links = cast(list[str], d.pop("links", UNSET))

        _lobbyregister = d.pop("lobbyregister", UNSET)
        lobbyregister: list[Lobbyregeintrag] | Unset = UNSET
        if _lobbyregister is not UNSET:
            lobbyregister = []
            for lobbyregister_item_data in _lobbyregister:
                lobbyregister_item = Lobbyregeintrag.from_dict(lobbyregister_item_data)

                lobbyregister.append(lobbyregister_item)

        vorgang = cls(
            api_id=api_id,
            titel=titel,
            wahlperiode=wahlperiode,
            verfassungsaendernd=verfassungsaendernd,
            typ=typ,
            initiatoren=initiatoren,
            stationen=stationen,
            touched_by=touched_by,
            kurztitel=kurztitel,
            ids=ids,
            links=links,
            lobbyregister=lobbyregister,
        )

        vorgang.additional_properties = d
        return vorgang

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
