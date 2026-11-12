from dataclasses import dataclass
from enum import Enum
import re


class DocumentStatus(str, Enum):
    STORED = "stored"
    TRASHED = "trashed"


@dataclass
class Document:
    id: int | None
    paper_id: int
    original_filename: str
    storage_key: str
    content_type: str
    size_bytes: int
    checksum_sha256: str
    status: DocumentStatus = DocumentStatus.STORED

    def __post_init__(self):
        self.original_filename = self.original_filename.strip()
        self.storage_key = self.storage_key.strip()
        self.checksum_sha256 = self.checksum_sha256.lower()

        if self.paper_id <= 0:
            raise ValueError("Invalid paper ID")

        if not self.original_filename:
            raise ValueError("Filename cannot be empty")

        if not self.storage_key:
            raise ValueError("Storage key cannot be empty")

        if self.content_type != "application/pdf":
            raise ValueError("Only PDF documents are supported")

        if self.size_bytes <= 0:
            raise ValueError("File size must be positive")

        if not re.fullmatch(r"[a-f0-9]{64}", self.checksum_sha256):
            raise ValueError("Invalid SHA-256 checksum")

    def trash(self):
        if self.status == DocumentStatus.TRASHED:
            raise ValueError("Document is already trashed")

        self.status = DocumentStatus.TRASHED

    def restore(self):
        if self.status != DocumentStatus.TRASHED:
            raise ValueError("Only trashed documents can be restored")

        self.status = DocumentStatus.STORED