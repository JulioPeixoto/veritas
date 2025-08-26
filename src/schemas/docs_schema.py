from enum import Enum

from pydantic import BaseModel


class DocsType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    HTML = "html"
    MD = "md"


class DocsIndexingRequest(BaseModel):
    name: str = ""
    description: str = ""
