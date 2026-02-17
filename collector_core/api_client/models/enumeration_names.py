from enum import Enum


class EnumerationNames(str, Enum):
    DOKUMENTENTYPEN = "dokumententypen"
    PARLAMENTE = "parlamente"
    SCHLAGWORTE = "schlagworte"
    STATIONSTYPEN = "stationstypen"
    VGIDTYPEN = "vgidtypen"
    VORGANGSTYPEN = "vorgangstypen"

    def __str__(self) -> str:
        return str(self.value)
