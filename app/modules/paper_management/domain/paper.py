from dataclasses import dataclass


@dataclass
class Paper:
    id: int | None
    title: str
    doi: str | None = None
    authors: tuple[str, ...] = ()
    publication_year: int | None = None

    def __post_init__(self):
        self.title = self.title.strip()

        if not self.title:
            raise ValueError("Paper title cannot be empty")

        if self.doi:
            self.doi = self.doi.strip().lower()

        if self.publication_year is not None:
            if not 1000 <= self.publication_year <= 2100:
                raise ValueError("Invalid publication year")
