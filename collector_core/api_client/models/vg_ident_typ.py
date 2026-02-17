from enum import Enum


class VgIdentTyp(str, Enum):
    API_ID = "api-id"
    INITDRUCKS = "initdrucks"
    SONSTIG = "sonstig"
    VORGNR = "vorgnr"

    def __str__(self) -> str:
        return str(self.value)
