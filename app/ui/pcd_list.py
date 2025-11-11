import streamlit as st
import pandas as pd
from app.database import get_pessoas_pcd, search_pessoas_pcd
from app.ui.st_utils import get_db_session, get_instituicao_by_id


def pcd_list():
    """Exibe a lista de Pessoas PCD e permite busca e edição."""
    st.subheader("Mapeamento de Pessoas com Deficiência (PCD)")

    col_search, col_add = st.columns([3, 1])
    with col_search:
        search_term = st.text_input("Buscar por Nome ou Tipo de Deficiência", key="search_pcd")
    # with col_add:
    #     if st.button("Adicionar Novo", key="add_pcd_btn"):
    #         st.session_state['current_view'] = 'add'
    #         st.rerun()

    with get_db_session() as db:
        if search_term:
            pessoas = search_pessoas_pcd(db, search_term)
        else:
            pessoas = get_pessoas_pcd(db)

    if not pessoas:
        st.info("Nenhuma pessoa PCD encontrada.")
        return

    # Preparar dados para exibição em tabela
    data = []
    for p in pessoas:
        instituicao = get_instituicao_by_id(p.id_instituicao)
        data.append({
            "ID": p.id,
            "Nome": p.nome,
            "Deficiência": p.tipo_deficiencia,
            "Grau": p.grau_deficiencia,
            "Instituição": instituicao.nome if instituicao else "Nenhuma",
            "Vínculo": p.vinculo_servico,
            "Data de Registro": p.data_registro.strftime("%d/%m/%Y"),
        })

    df = pd.DataFrame(data)

    # Exibir a tabela
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Seleção para Edição
    st.markdown("---")
    st.subheader("Editar Registro")

    # Criar uma lista de opções para o selectbox
    options = {f"{p.nome} ({p.tipo_deficiencia})": p.id for p in pessoas}
    selected_name = st.selectbox("Selecione a Pessoa para Editar", options=list(options.keys()))

    if selected_name:
        selected_id = options[selected_name]
        if st.button("Editar Selecionado", key="edit_pcd_btn"):
            st.session_state['current_view'] = 'edit'
            st.session_state['edit_pcd_id'] = selected_id
            st.rerun()

