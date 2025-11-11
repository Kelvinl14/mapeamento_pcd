import streamlit as st
from app.database import SessionLocal, init_db
from app.database.crud import get_instituicoes
from app.models import Instituicao

def get_db_session():
    """Retorna uma nova sessão de banco de dados."""
    return SessionLocal()

def init_app_state():
    """Inicializa o estado da aplicação Streamlit."""
    if 'db_initialized' not in st.session_state:
        try:
            init_db()
            st.session_state['db_initialized'] = True
        except Exception as e:
            st.error(f"Erro ao inicializar o banco de dados: {e}")
            st.session_state['db_initialized'] = False

    if 'instituicoes' not in st.session_state:
        st.session_state['instituicoes'] = []
        with get_db_session() as db:
            st.session_state['instituicoes'] = get_instituicoes(db)

    if 'current_view' not in st.session_state:
        st.session_state['current_view'] = 'dashboard'

def get_instituicao_options() -> dict[str, str]:
    """Retorna um dicionário de nomes de instituições para IDs."""
    options = {"Nenhuma": None}
    for inst in st.session_state['instituicoes']:
        options[inst.nome] = inst.id
    return options

def get_instituicao_by_id(inst_id: str) -> Instituicao | None:
    """Busca uma instituição pelo ID no estado da sessão."""
    for inst in st.session_state['instituicoes']:
        if inst.id == inst_id:
            return inst
    return None