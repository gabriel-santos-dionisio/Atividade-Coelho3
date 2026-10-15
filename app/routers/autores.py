from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Autor
from app.schemas.autor import AutorCreate, AutorResponse, AutorUpdate

router = APIRouter(prefix="/autores", tags=["Autores"])


def _get_or_404(db: Session, autor_id: int) -> Autor:
    autor = db.get(Autor, autor_id)
    if not autor:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Autor não encontrado")
    return autor


@router.post("/", response_model=AutorResponse, status_code=status.HTTP_201_CREATED)
def criar_autor(dados: AutorCreate, db: Session = Depends(get_db)):
    autor = Autor(**dados.model_dump())
    db.add(autor)
    db.commit()
    db.refresh(autor)
    return autor


@router.get("/", response_model=list[AutorResponse])
def listar_autores(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(Autor).offset(skip).limit(limit).all()


@router.get("/{autor_id}", response_model=AutorResponse)
def obter_autor(autor_id: int, db: Session = Depends(get_db)):
    return _get_or_404(db, autor_id)


@router.put("/{autor_id}", response_model=AutorResponse)
def atualizar_autor(autor_id: int, dados: AutorUpdate, db: Session = Depends(get_db)):
    autor = _get_or_404(db, autor_id)
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(autor, campo, valor)
    db.commit()
    db.refresh(autor)
    return autor


@router.delete("/{autor_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_autor(autor_id: int, db: Session = Depends(get_db)):
    autor = _get_or_404(db, autor_id)
    if autor.livros:
        raise HTTPException(status.HTTP_409_CONFLICT, "Autor possui livros cadastrados")
    db.delete(autor)
    db.commit()
