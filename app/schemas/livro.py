from pydantic import BaseModel, ConfigDict, Field

from app.schemas.autor import AutorResponse


class LivroCreate(BaseModel):
    titulo: str = Field(min_length=1, max_length=200)
    isbn: str = Field(min_length=10, max_length=20)
    ano_publicacao: int | None = Field(default=None, ge=0, le=2100)
    exemplares_disponiveis: int = Field(default=1, ge=0)
    autor_id: int


class LivroUpdate(BaseModel):
    titulo: str | None = Field(default=None, min_length=1, max_length=200)
    ano_publicacao: int | None = Field(default=None, ge=0, le=2100)
    exemplares_disponiveis: int | None = Field(default=None, ge=0)
    autor_id: int | None = None


class LivroResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    isbn: str
    ano_publicacao: int | None
    exemplares_disponiveis: int
    autor: AutorResponse
