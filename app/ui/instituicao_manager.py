import streamlit as st
import pandas as pd
from app.database import get_instituicoes, create_instituicao
from app.ui.st_utils import get_db_session
from uuid import uuid4


def instituicao_manager():
    """Gerencia o cadastro de instituições."""
    st.subheader("Gerenciamento de Instituições")

    # Formulário de Cadastro
    with st.expander("Cadastrar Nova Instituição", expanded=False):
        with st.form(key="instituicao_form", clear_on_submit=True):
            nome = st.text_input("Nome da Instituição")
            tipo = st.text_input("Tipo (Ex: ONG, Escola, Hospital)")
            endereco = st.text_area("Endereço")

            submit_button = st.form_submit_button(label="Cadastrar Instituição")

            if submit_button:
                if not nome:
                    st.error("O nome da instituição é obrigatório.")
                else:
                    # Usar um ID simples para Instituição, como um UUID ou um slug.
                    # Vou usar um slug simples baseado no nome para facilitar, mas o modelo espera 'str'.
                    # Para simplificar, vou usar o nome como ID, mas o ideal seria um UUID ou slug.
                    # Vou usar um UUID para garantir unicidade.
                    inst_id = str(uuid4())
                    with get_db_session() as db:
                        try:
                            create_instituicao(db, id=inst_id, nome=nome, tipo=tipo, endereco=endereco)
                            st.success(f"Instituição '{nome}' cadastrada com sucesso!")
                            # Recarregar a lista de instituições na sessão
                            st.session_state['instituicoes'] = get_instituicoes(db)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao cadastrar instituição: {e}")

    # Lista de Instituições
    st.markdown("---")
    st.subheader("Instituições Cadastradas")

    with get_db_session() as db:
        instituicoes = get_instituicoes(db)

    if not instituicoes:
        st.info("Nenhuma instituição cadastrada.")
        return

    # Preparar dados para exibição em tabela
    data = []
    for inst in instituicoes:
        data.append({
            "ID": inst.id,
            "Nome": inst.nome,
            "Tipo": inst.tipo,
            "Endereço": inst.endereco,
        })

    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)