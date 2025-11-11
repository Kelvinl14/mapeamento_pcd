import streamlit as st
from app.ui.st_utils import init_app_state, get_db_session
from app.ui.dashboard import dashboard
from app.ui.pcd_list import pcd_list
from app.ui.pcd_form import pcd_form
from app.ui.instituicao_manager import instituicao_manager
from app.database import get_pessoa_pcd

# Configuração da página
st.set_page_config(
    page_title="Mapeamento PCD",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inicializar o estado da aplicação e o DB
init_app_state()

# Sidebar para navegação
st.sidebar.title("Navegação")
view_options = {
    'dashboard': 'Dashboard',
    'list': 'Lista de PCDs',
    'add': 'Cadastrar PCD',
    'instituicoes': 'Gerenciar Instituições',
}

# Determinar a view atual
current_view_key = st.sidebar.radio(
    "Selecione a Visualização",
    options=list(view_options.keys()),
    format_func=lambda x: view_options[x],
    key='sidebar_view_radio'
)

# Atualizar o estado da sessão se a navegação for diferente da atual
# if current_view_key != st.session_state.get('current_view'):
#     st.session_state['current_view'] = current_view_key
#     # Limpar o ID de edição ao mudar de view
#     if 'edit_pcd_id' in st.session_state:
#         del st.session_state['edit_pcd_id']
#     st.rerun()
if st.session_state.get('current_view') != 'edit':
    if current_view_key != st.session_state.get('current_view'):
        st.session_state['current_view'] = current_view_key
        if 'edit_pcd_id' in st.session_state:
            del st.session_state['edit_pcd_id']
        st.rerun()


# Lógica de renderização da view
st.title("Sistema de Mapeamento de Pessoas com Deficiência (PCD)")

if st.session_state['current_view'] == 'dashboard':
    dashboard()

elif st.session_state['current_view'] == 'list':
    pcd_list()

elif st.session_state['current_view'] == 'add':
    pcd_form()

elif st.session_state['current_view'] == 'edit':
    if 'edit_pcd_id' in st.session_state:
        pcd_id = st.session_state['edit_pcd_id']
        with get_db_session() as db:
            pessoa_pcd = get_pessoa_pcd(db, pcd_id)
        if pessoa_pcd:
            pcd_form(pessoa_pcd)
        else:
            st.error("Pessoa PCD não encontrada para edição.")
            st.session_state['current_view'] = 'list'
            st.rerun()
    else:
        st.session_state['current_view'] = 'list'
        st.rerun()

elif st.session_state['current_view'] == 'instituicoes':
    instituicao_manager()