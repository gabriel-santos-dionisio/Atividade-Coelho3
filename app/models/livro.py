from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Livro(Base):
    __tablename__ = "livros"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    isbn: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    ano_publicacao: Mapped[int | None]
    exemplares_disponiveis: Mapped[int] = mapped_column(default=1)
    autor_id: Mapped[int] = mapped_column(ForeignKey("autores.id"), nullable=False)

    autor: Mapped["Autor"] = relationship(back_populates="livros")
    emprestimos: Mapped[list["Emprestimo"]] = relationship(back_populates="livro")
