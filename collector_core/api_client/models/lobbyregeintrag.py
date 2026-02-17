from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.autor import Autor


T = TypeVar("T", bound="Lobbyregeintrag")


@_attrs_define
class Lobbyregeintrag:
    """Eintrag im Bundestagslobbyregister zu einem bestimmten Vorgang

    Example:
        {'organisation': {'organisation': 'Bundesverband der Deutschen Industrie e.V.', 'lobbyregister':
            'https://www.lobbyregister.bundestag.de/suche/experte/12345'}, 'interne_id': 'LR-ID-12345678', 'intention':
            'Stellungnahme zu Auswirkungen der Gesetzesänderung auf die deutsche Wirtschaft und Vorschläge zur Anpassung in
            § 15 des Gesetzesentwurfs.', 'link': 'https://www.lobbyregister.bundestag.de/eintragung/12345678',
            'betroffene_drucksachen': ['BT-Drs. 20/12345', 'BT-Drs. 20/12346']}

    Attributes:
        organisation (Autor): Eine Person oder Organisation, die eine bestimmte Funktion übernommen hat. Z.B: Autor
            einer Stellungnahme, Experte bei einer Anhörung, Initiator eines Vorgangs. Example: {'person': 'Prof. Dr.
            Susanne Meyer', 'organisation': 'Universität Heidelberg', 'fachgebiet': 'Verfassungsrecht', 'lobbyregister':
            'https://www.lobbyregister.bundestag.de/suche/experte/12345'}.
        interne_id (str): Interne ID des Lobbyregisters, notwendig für die bildung von Links
        intention (str): Lobbyregistereintrag zu dem  Was und Warum man auf den Vorgang Einfluss nehmen will
        link (str): Direktlink zum Lobbyregistereintrag
        betroffene_drucksachen (list[str]): Stringarray mit betroffenen Drucksachennummern. Wird in der Datenbank
            _nicht_ integriert und nur flach aufgelegt
    """

    organisation: Autor
    interne_id: str
    intention: str
    link: str
    betroffene_drucksachen: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        organisation = self.organisation.to_dict()

        interne_id = self.interne_id

        intention = self.intention

        link = self.link

        betroffene_drucksachen = self.betroffene_drucksachen

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "organisation": organisation,
                "interne_id": interne_id,
                "intention": intention,
                "link": link,
                "betroffene_drucksachen": betroffene_drucksachen,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.autor import Autor

        d = dict(src_dict)
        organisation = Autor.from_dict(d.pop("organisation"))

        interne_id = d.pop("interne_id")

        intention = d.pop("intention")

        link = d.pop("link")

        betroffene_drucksachen = cast(list[str], d.pop("betroffene_drucksachen"))

        lobbyregeintrag = cls(
            organisation=organisation,
            interne_id=interne_id,
            intention=intention,
            link=link,
            betroffene_drucksachen=betroffene_drucksachen,
        )

        lobbyregeintrag.additional_properties = d
        return lobbyregeintrag

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
