import streamlit as st
from datetime import date
from uuid import uuid4
from app.models import PessoaPCD
from app.database import create_pessoa_pcd, update_pessoa_pcd, delete_pessoa_pcd
from app.ui.st_utils import get_db_session, get_instituicao_options


def pcd_form(pessoa_pcd: PessoaPCD = None):
    """Formulário para criação e edição de PessoaPCD."""
    is_edit = pessoa_pcd is not None
    st.subheader(f"{'Editar' if is_edit else 'Cadastrar'} Pessoa com Deficiência")

    col_cancel, _ = st.columns([1, 3])
    if is_edit:
        with col_cancel:
            if st.button("Voltar"):
                st.session_state['current_view'] = 'list'
                if 'edit_pcd_id' in st.session_state:
                    del st.session_state['edit_pcd_id']
                st.rerun()

    with st.form(key="pcd_form", clear_on_submit=not is_edit):
        # Dados Pessoais
        st.markdown("#### Dados Pessoais")
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome Completo", value=pessoa_pcd.nome if is_edit else "")
            data_nascimento = st.date_input("Data de Nascimento",
                                            value=pessoa_pcd.data_nascimento if is_edit and pessoa_pcd.data_nascimento else date(
                                                2000, 1, 1), max_value=date.today())
        with col2:
            sexo = st.selectbox("Sexo", options=["", "Masculino", "Feminino", "Outro"],
                                index=["", "Masculino", "Feminino", "Outro"].index(
                                    pessoa_pcd.sexo) if is_edit and pessoa_pcd.sexo else 0)
            contato = st.text_input("Contato (Telefone/Email)", value=pessoa_pcd.contato if is_edit else "")

        # Dados da Deficiência
        st.markdown("#### Dados da Deficiência")
        col3, col4 = st.columns(2)
        with col3:
            tipo_deficiencia = st.text_input("Tipo de Deficiência",
                                             value=pessoa_pcd.tipo_deficiencia if is_edit else "")
        with col4:
            grau_deficiencia = st.selectbox("Grau da Deficiência", options=["", "Leve", "Moderado", "Grave"],
                                            index=["", "Leve", "Moderado", "Grave"].index(
                                                pessoa_pcd.grau_deficiencia) if is_edit and pessoa_pcd.grau_deficiencia else 0)

        acessibilidade_necessaria = st.text_area("Acessibilidade Necessária",
                                                 value=pessoa_pcd.acessibilidade_necessaria if is_edit else "")

        # Localização e Vínculo
        st.markdown("#### Localização e Vínculo")
        endereco = st.text_input("Endereço Completo", value=pessoa_pcd.endereco if is_edit else "")
        col5, col6 = st.columns(2)
        with col5:
            lat = st.number_input("Latitude", value=pessoa_pcd.lat if is_edit and pessoa_pcd.lat else 0.0,
                                  format="%.6f")
        with col6:
            lon = st.number_input("Longitude", value=pessoa_pcd.lon if is_edit and pessoa_pcd.lon else 0.0,
                                  format="%.6f")

        instituicao_options = get_instituicao_options()
        current_inst_name = next((name for name, id in instituicao_options.items() if id == pessoa_pcd.id_instituicao),
                                 "Nenhuma") if is_edit else "Nenhuma"
        instituicao_selecionada = st.selectbox("Instituição de Vínculo", options=list(instituicao_options.keys()),
                                               index=list(instituicao_options.keys()).index(current_inst_name))
        id_instituicao = instituicao_options[instituicao_selecionada]

        vinculo_servico = st.text_input("Vínculo com Serviço (Ex: CRAS, CAPS)",
                                        value=pessoa_pcd.vinculo_servico if is_edit else "")

        # Outros Dados
        st.markdown("#### Outros Dados")
        col7, col8 = st.columns(2)
        with col7:
            consentimento = st.checkbox("Consentimento para Mapeamento",
                                        value=pessoa_pcd.consentimento if is_edit else False)
        with col8:
            origem_registro = st.text_input("Origem do Registro", value=pessoa_pcd.origem_registro if is_edit else "")

        # Botões de Ação
        col_submit, col_delete = st.columns([1, 1])
        with col_submit:
            submit_button = st.form_submit_button(label=f"{'Atualizar' if is_edit else 'Cadastrar'}")

        if is_edit:
            with col_delete:
                delete_button = st.form_submit_button(label="Excluir", type="primary")
        else:
            delete_button = False

        if submit_button:
            if not nome or not tipo_deficiencia:
                st.error("Nome e Tipo de Deficiência são campos obrigatórios.")
                return

            with get_db_session() as db:
                if is_edit:
                    # Atualizar
                    data_to_update = {
                        "nome": nome,
                        "data_nascimento": data_nascimento,
                        "sexo": sexo if sexo else None,
                        "tipo_deficiencia": tipo_deficiencia,
                        "grau_deficiencia": grau_deficiencia if grau_deficiencia else None,
                        "endereco": endereco if endereco else None,
                        "lat": lat,
                        "lon": lon,
                        "vinculo_servico": vinculo_servico if vinculo_servico else None,
                        "id_instituicao": id_instituicao,
                        "acessibilidade_necessaria": acessibilidade_necessaria if acessibilidade_necessaria else None,
                        "contato": contato if contato else None,
                        "consentimento": consentimento,
                        "origem_registro": origem_registro if origem_registro else None,
                    }
                    updated_pessoa = update_pessoa_pcd(db, pessoa_pcd.id, data_to_update)
                    if updated_pessoa:
                        st.success(f"Pessoa PCD '{nome}' atualizada com sucesso!")
                        st.session_state['current_view'] = 'list'  # Voltar para a lista
                        st.rerun()
                    else:
                        st.error("Erro ao atualizar pessoa PCD.")
                else:
                    # Criar
                    new_pessoa = PessoaPCD(
                        id=uuid4(),
                        nome=nome,
                        data_nascimento=data_nascimento,
                        sexo=sexo if sexo else None,
                        tipo_deficiencia=tipo_deficiencia,
                        grau_deficiencia=grau_deficiencia if grau_deficiencia else None,
                        endereco=endereco if endereco else None,
                        lat=lat,
                        lon=lon,
                        vinculo_servico=vinculo_servico if vinculo_servico else None,
                        id_instituicao=id_instituicao,
                        acessibilidade_necessaria=acessibilidade_necessaria if acessibilidade_necessaria else None,
                        contato=contato if contato else None,
                        consentimento=consentimento,
                        origem_registro=origem_registro if origem_registro else None,
                    )
                    created_pessoa = create_pessoa_pcd(db, new_pessoa)
                    if created_pessoa:
                        st.success(f"Pessoa PCD '{nome}' cadastrada com sucesso!")
                        # Não precisa de rerun, o clear_on_submit=True já limpa o formulário
                    else:
                        st.error("Erro ao cadastrar pessoa PCD.")


        if delete_button:
            if st.session_state.get('confirm_delete', False):
                with get_db_session() as db:
                    if delete_pessoa_pcd(db, pessoa_pcd.id):
                        st.success(f"Pessoa PCD '{pessoa_pcd.nome}' excluída com sucesso!")
                        st.session_state['current_view'] = 'list'  # Voltar para a lista
                        st.session_state['confirm_delete'] = False
                        st.rerun()
                    else:
                        st.error("Erro ao excluir pessoa PCD.")
            else:
                st.session_state['confirm_delete'] = True
                st.warning("Clique em 'Excluir' novamente para confirmar a exclusão.")