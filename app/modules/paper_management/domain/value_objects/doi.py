import re
from dataclasses import dataclass


@dataclass(frozen=True)
class DOI:
    value: str

    def __post_init__(self):
        normalized = self.value.strip().lower()

        normalized = re.sub(
            r"^(https?://(dx\.)?doi\.org/|doi:)",
            "",
            normalized,
        )

        if not re.fullmatch(r"10\.\d{4,9}/\S+", normalized):
            raise ValueError("Invalid DOI")

        object.__setattr__(self, "value", normalized)