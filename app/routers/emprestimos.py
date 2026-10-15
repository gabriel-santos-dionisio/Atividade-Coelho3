from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Emprestimo, Livro
from app.schemas.emprestimo import EmprestimoCreate, EmprestimoResponse, EmprestimoUpdate

router = APIRouter(prefix="/emprestimos", tags=["Empréstimos"])


def _get_or_404(db: Session, emprestimo_id: int) -> Emprestimo:
    emprestimo = db.get(Emprestimo, emprestimo_id)
    if not emprestimo:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Empréstimo não encontrado")
    return emprestimo


@router.post("/", response_model=EmprestimoResponse, status_code=status.HTTP_201_CREATED)
def criar_emprestimo(dados: EmprestimoCreate, db: Session = Depends(get_db)):
    livro = db.get(Livro, dados.livro_id)
    if not livro:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Livro informado não existe")
    if livro.exemplares_disponiveis < 1:
        raise HTTPException(status.HTTP_409_CONFLICT, "Sem exemplares disponíveis")
    livro.exemplares_disponiveis -= 1
    emprestimo = Emprestimo(**dados.model_dump())
    db.add(emprestimo)
    db.commit()
    db.refresh(emprestimo)
    return emprestimo


@router.get("/", response_model=list[EmprestimoResponse])
def listar_emprestimos(devolvido: bool | None = None, skip: int = 0, limit: int = 50,
                       db: Session = Depends(get_db)):
    query = db.query(Emprestimo)
    if devolvido is not None:
        query = query.filter(Emprestimo.devolvido == devolvido)
    return query.offset(skip).limit(limit).all()


@router.get("/{emprestimo_id}", response_model=EmprestimoResponse)
def obter_emprestimo(emprestimo_id: int, db: Session = Depends(get_db)):
    return _get_or_404(db, emprestimo_id)


@router.put("/{emprestimo_id}", response_model=EmprestimoResponse)
def atualizar_emprestimo(emprestimo_id: int, dados: EmprestimoUpdate,
                         db: Session = Depends(get_db)):
    emprestimo = _get_or_404(db, emprestimo_id)
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(emprestimo, campo, valor)
    db.commit()
    db.refresh(emprestimo)
    return emprestimo


@router.patch("/{emprestimo_id}/devolver", response_model=EmprestimoResponse)
def devolver_livro(emprestimo_id: int, db: Session = Depends(get_db)):
    emprestimo = _get_or_404(db, emprestimo_id)
    if emprestimo.devolvido:
        raise HTTPException(status.HTTP_409_CONFLICT, "Empréstimo já foi devolvido")
    emprestimo.devolvido = True
    emprestimo.data_devolucao = datetime.utcnow()
    emprestimo.livro.exemplares_disponiveis += 1
    db.commit()
    db.refresh(emprestimo)
    return emprestimo


@router.delete("/{emprestimo_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_emprestimo(emprestimo_id: int, db: Session = Depends(get_db)):
    emprestimo = _get_or_404(db, emprestimo_id)
    if not emprestimo.devolvido:
        emprestimo.livro.exemplares_disponiveis += 1
    db.delete(emprestimo)
    db.commit()
