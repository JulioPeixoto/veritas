from pydantic import BaseModel
from enum import Enum


class DocsType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    HTML = "html"
    MD = "md"


class DocsIndexingRequest(BaseModel):
    name: str = ""
    description: str = ""
