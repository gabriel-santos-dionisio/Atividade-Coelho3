from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Autor(Base):
    __tablename__ = "autores"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    nacionalidade: Mapped[str | None] = mapped_column(String(60))

    livros: Mapped[list["Livro"]] = relationship(back_populates="autor")
