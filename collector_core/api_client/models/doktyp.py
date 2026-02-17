from enum import Enum


class Doktyp(str, Enum):
    ANFRAGE = "anfrage"
    ANTRAG = "antrag"
    ANTWORT = "antwort"
    BESCHLUSSEMPF = "beschlussempf"
    ENTWURF = "entwurf"
    GUTACHTEN = "gutachten"
    MITTEILUNG = "mitteilung"
    PREPARL_ENTWURF = "preparl-entwurf"
    REDEPROTOKOLL = "redeprotokoll"
    SONSTIG = "sonstig"
    STELLUNGNAHME = "stellungnahme"
    TOPS = "tops"
    TOPS_AEND = "tops-aend"
    TOPS_ERGZ = "tops-ergz"

    def __str__(self) -> str:
        return str(self.value)
