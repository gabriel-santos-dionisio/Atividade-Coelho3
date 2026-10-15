from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EmprestimoCreate(BaseModel):
    nome_leitor: str = Field(min_length=2, max_length=120)
    livro_id: int


class EmprestimoUpdate(BaseModel):
    nome_leitor: str | None = Field(default=None, min_length=2, max_length=120)


class EmprestimoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome_leitor: str
    livro_id: int
    data_emprestimo: datetime
    data_devolucao: datetime | None
    devolvido: bool
