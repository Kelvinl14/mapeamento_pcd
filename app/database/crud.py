from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.models import Instituicao, PessoaPCD

# --- CRUD para Instituição ---
def get_instituicao(db: Session, instituicao_id: str) -> Optional[Instituicao]:
    """Recupera uma instituição pelo ID."""
    return db.get(Instituicao, instituicao_id)

def get_instituicoes(db: Session, skip: int = 0, limit: int = 100) -> List[Instituicao]:
    """Lista todas as intituições."""
    return db.scalars(select(Instituicao).offset(skip).limit(limit)).all()

def create_instituicao(db: Session, id: str, nome: str, tipo: Optional[str] = None, endereco: Optional[str] = None) -> Instituicao:
    """Cria uma nova instituição."""
    db_instituicao = Instituicao(id=id, nome=nome, tipo=tipo, endereco=endereco)
    db.add(db_instituicao)
    db.commit()
    db.refresh(db_instituicao)
    return db_instituicao

# --- CRUD para PessoaPCD ---

def get_pessoa_pcd(db: Session, pessoa_id: UUID) -> Optional[PessoaPCD]:
    """Recupera uma pessoa PCD pelo ID."""
    return db.get(PessoaPCD, pessoa_id)

def get_pessoas_pcd(db: Session, skip: int = 0, limit: int = 100) -> List[PessoaPCD]:
    """Lista todas as pessoas PCD."""
    return db.scalars(select(PessoaPCD).offset(skip).limit(limit)).all()

def create_pessoa_pcd(db: Session, pessoa: PessoaPCD) -> PessoaPCD:
    """Cria uma nova pessoa PCD."""
    db.add(pessoa)
    db.commit()
    db.refresh(pessoa)
    return pessoa

def update_pessoa_pcd(db: Session, pessoa_id: UUID, data: dict) -> Optional[PessoaPCD]:
    """Atualiza os dados de uma pessoa PCD."""
    db_pessoa = db.get(PessoaPCD, pessoa_id)
    if db_pessoa:
        for key, value in data.items():
            setattr(db_pessoa, key, value)
        db.commit()
        db.refresh(db_pessoa)
    return db_pessoa

def delete_pessoa_pcd(db: Session, pessoa_id: UUID) -> bool:
    """Deleta uma pessoa PCD."""
    db_pessoa = db.get(PessoaPCD, pessoa_id)
    if db_pessoa:
        db.delete(db_pessoa)
        db.commit()
        return True
    return False

def search_pessoas_pcd(db: Session, query: str) -> List[PessoaPCD]:
    """Busca pessoas PCD por nome ou tipo de deficiência."""
    stmt = select(PessoaPCD).where(
        (PessoaPCD.nome.ilike(f"%{query}%")) |
        (PessoaPCD.tipo_deficiencia.ilike(f"%{query}%"))
    )
    return db.scalars(stmt).all()