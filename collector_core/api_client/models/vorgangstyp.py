from enum import Enum


class Vorgangstyp(str, Enum):
    BW_EINSATZ = "bw-einsatz"
    GG_EINSPRUCH = "gg-einspruch"
    GG_LAND_PARL = "gg-land-parl"
    GG_LAND_VOLK = "gg-land-volk"
    GG_ZUSTIMMUNG = "gg-zustimmung"
    SONSTIG = "sonstig"

    def __str__(self) -> str:
        return str(self.value)
