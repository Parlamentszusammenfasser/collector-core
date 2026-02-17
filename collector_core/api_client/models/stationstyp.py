from enum import Enum


class Stationstyp(str, Enum):
    PARL_ABLEHNUNG = "parl-ablehnung"
    PARL_AKZEPTANZ = "parl-akzeptanz"
    PARL_AUSSCHBER = "parl-ausschber"
    PARL_GGENTWURF = "parl-ggentwurf"
    PARL_INITIATIV = "parl-initiativ"
    PARL_VOLLVLSGN = "parl-vollvlsgn"
    PARL_ZURUECKGZ = "parl-zurueckgz"
    POSTPARL_GSBLT = "postparl-gsblt"
    POSTPARL_KRAFT = "postparl-kraft"
    POSTPARL_VESJA = "postparl-vesja"
    POSTPARL_VESNE = "postparl-vesne"
    PREPARL_ECKPUP = "preparl-eckpup"
    PREPARL_REGBSL = "preparl-regbsl"
    PREPARL_REGENT = "preparl-regent"
    PREPARL_VBEGDE = "preparl-vbegde"
    SONSTIG = "sonstig"

    def __str__(self) -> str:
        return str(self.value)
