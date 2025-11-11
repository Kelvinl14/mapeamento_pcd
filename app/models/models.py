from __future__ import annotations
from typing import Optional
from datetime import date, datetime
from uuid import uuid4, UUID

from sqlalchemy import String, Text, Date, Boolean, Float, ForeignKey, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    """Classe base declarativa."""
    pass

class Instituicao(Base):
    """Tabela de instituições ligadas às pessoas PCD."""
    __tablename__ = "instituicoes"

    id: Mapped[str] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    tipo: Mapped[Optional[str]] = mapped_column(String(50))
    endereco: Mapped[Optional[str]] = mapped_column(Text)

    pessoas: Mapped[list[PessoaPCD]] = relationship(
        back_populates="instituicao", cascade="all, delete-orphan"
    )
    def __repr__(self) -> str:
        return f"Instituicao(id={self.id!r}, nome={self.nome!r})"

class PessoaPCD(Base):
    """Tabela de mapeamento de pessoas com deficiência."""
    __tablename__ = "pessoas_pcd"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,  # substitui gen_random_uuid() para SQLite
    )
    nome: Mapped[str] = mapped_column(String(120))
    data_nascimento: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    sexo: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    tipo_deficiencia: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    grau_deficiencia: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    endereco: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    lat: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    lon: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    vinculo_servico: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    id_instituicao: Mapped[Optional[str]] = mapped_column(
        ForeignKey("instituicoes.id"), nullable=True
    )
    acessibilidade_necessaria: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    contato: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    consentimento: Mapped[bool] = mapped_column(Boolean, default=False)
    origem_registro: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    data_registro: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.utcnow
    )
    hash_identificador: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)

    instituicao: Mapped[Optional[Instituicao]] = relationship(back_populates="pessoas")

    def __repr__(self) -> str:
        return (
            f"PessoaPCD(id={self.id!r}, nome={self.nome!r}, "
            f"tipo_deficiencia={self.tipo_deficiencia!r}, "
            f"instituicao={self.id_instituicao!r})"
        )