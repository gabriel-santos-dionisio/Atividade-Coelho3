from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Autor, Livro
from app.schemas.livro import LivroCreate, LivroResponse, LivroUpdate

router = APIRouter(prefix="/livros", tags=["Livros"])


def _get_or_404(db: Session, livro_id: int) -> Livro:
    livro = db.get(Livro, livro_id)
    if not livro:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Livro não encontrado")
    return livro


def _verificar_autor(db: Session, autor_id: int) -> None:
    if not db.get(Autor, autor_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Autor informado não existe")


@router.post("/", response_model=LivroResponse, status_code=status.HTTP_201_CREATED)
def criar_livro(dados: LivroCreate, db: Session = Depends(get_db)):
    _verificar_autor(db, dados.autor_id)
    if db.query(Livro).filter(Livro.isbn == dados.isbn).first():
        raise HTTPException(status.HTTP_409_CONFLICT, "ISBN já cadastrado")
    livro = Livro(**dados.model_dump())
    db.add(livro)
    db.commit()
    db.refresh(livro)
    return livro


@router.get("/", response_model=list[LivroResponse])
def listar_livros(autor_id: int | None = None, skip: int = 0, limit: int = 50,
                  db: Session = Depends(get_db)):
    query = db.query(Livro)
    if autor_id is not None:
        query = query.filter(Livro.autor_id == autor_id)
    return query.offset(skip).limit(limit).all()


@router.get("/{livro_id}", response_model=LivroResponse)
def obter_livro(livro_id: int, db: Session = Depends(get_db)):
    return _get_or_404(db, livro_id)


@router.put("/{livro_id}", response_model=LivroResponse)
def atualizar_livro(livro_id: int, dados: LivroUpdate, db: Session = Depends(get_db)):
    livro = _get_or_404(db, livro_id)
    campos = dados.model_dump(exclude_unset=True)
    if "autor_id" in campos:
        _verificar_autor(db, campos["autor_id"])
    for campo, valor in campos.items():
        setattr(livro, campo, valor)
    db.commit()
    db.refresh(livro)
    return livro


@router.delete("/{livro_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = _get_or_404(db, livro_id)
    if livro.emprestimos:
        raise HTTPException(status.HTTP_409_CONFLICT, "Livro possui empréstimos registrados")
    db.delete(livro)
    db.commit()
