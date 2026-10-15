from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Emprestimo(Base):
    __tablename__ = "emprestimos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome_leitor: Mapped[str] = mapped_column(String(120), nullable=False)
    data_emprestimo: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    data_devolucao: Mapped[datetime | None]
    devolvido: Mapped[bool] = mapped_column(default=False)
    livro_id: Mapped[int] = mapped_column(ForeignKey("livros.id"), nullable=False)

    livro: Mapped["Livro"] = relationship(back_populates="emprestimos")
