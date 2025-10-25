from fastapi import HTTPException
from pydantic import BaseModel

from src.schemas.store_schema import DocsType


class InvalidFormatExceptionResponse(BaseModel):
    status_code: int
    detail: str
    headers: dict

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status_code": 400,
                    "detail": "Formato de arquivo inválido: .env",
                    "headers": {"X-Error": "Formatos válidos: " + ", ".join(DocsType)},
                }
            ]
        }
    }


def InvalidFormatException(type: DocsType):
    raise HTTPException(
        status_code=400,
        detail={
            "message": "Formato de arquivo inválido",
            "status": "invalid_format",
            "type": type,
            "valid_extensions": [ext.value for ext in DocsType],
        },
        headers={"X-Error": "Formatos válidos: " + ", ".join(DocsType)},
    )
