from fastapi import HTTPException
from pydantic import BaseModel
from src.schemas.docs_schema import DocsType


class InvalidFormatExceptionResponse(BaseModel):
    status_code: int
    detail: str
    headers: dict

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status_code": 400,
                    "detail": "Formato de arquivo inválido: pdf",
                    "headers": {
                        "X-Error": "Formatos válidos: " + ", ".join(DocsType)
                    },
                }
            ]
        }
    }


def InvalidFormatException(type: DocsType):
    raise HTTPException(
        status_code=400,
        detail=f"Formato de arquivo inválido: {type}",
        headers={"X-Error": "Formatos válidos: " + ", ".join(DocsType)},
    )
