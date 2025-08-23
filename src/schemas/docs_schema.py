from pydantic import BaseModel
from enum import Enum
from typing import Optional

class DocsType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    HTML = "html"
    MD = "md"
    

class DocsIndexingRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
