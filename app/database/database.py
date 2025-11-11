import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

from app.models import Base

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./mapeamento_pcd.db")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    """Função geradora para obter uma sessão de banco de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Cria as tabelas no banco de dados
def init_db():
    """Inicializa o banco de dados criando todas as tabelas."""
    # Base.metadata.drop_all(bind=engine)  # Limpar tabelas existentes (opcional)
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()