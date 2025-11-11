import streamlit as st
import pandas as pd
import plotly.express as px
from app.database import get_pessoas_pcd
from app.ui.st_utils import get_db_session

def dashboard():
    """Exibe o dashboard com gráficos e estatísticas sobre pessoas com deficiência."""
    st.subheader("Dashboard de Pessoas com Deficiência")


    with get_db_session() as session:
        pessoas_pcd = get_pessoas_pcd(session)

    if not pessoas_pcd:
        st.info("Nenhum dado disponível para exibir o dashboard.")
        return

    # Converter dados para DataFrame
    data = []
    for p in pessoas_pcd:
        data.append({
            "Nome": p.nome,
            "Tipo Deficiência": p.tipo_deficiencia,
            "Grau Deficiência": p.grau_deficiencia,
            "Sexo": p.sexo,
            "Vínculo Serviço": p.vinculo_servico,
            "Latitude": p.lat,
            "Longitude": p.lon,
        })

    df = pd.DataFrame(data)

    with st.container():
        st.markdown(
            f"""
            <div style="text-align:center; background-color:#2b2933; padding:40px; border-radius:20px;">
                <h1 style="font-size:64px; margin-bottom:0; color:#0066cc;">{len(df)}</h1>
                <p style="font-size:18px; color:#fff;">Pessoas PCD cadastradas</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # Gráfico de Tipos de Deficiência
    st.markdown("#### Distribuição por Tipo de Deficiência")
    type_counts = df['Tipo Deficiência'].value_counts().reset_index()
    type_counts.columns = ['Tipo Deficiência', 'Contagem']
    fig_type = px.bar(type_counts, x='Tipo Deficiência', y='Contagem', title='Contagem por Tipo de Deficiência')
    st.plotly_chart(fig_type, use_container_width=True)

    # Gráfico de Grau de Deficiência
    st.markdown("#### Distribuição por Grau de Deficiência")
    grau_counts = df['Grau Deficiência'].value_counts().reset_index()
    grau_counts.columns = ['Grau Deficiência', 'Contagem']
    fig_grau = px.pie(grau_counts, values='Contagem', names='Grau Deficiência',
                      title='Distribuição por Grau de Deficiência')
    st.plotly_chart(fig_grau, use_container_width=True)

    # Mapa de Localização
    st.markdown("#### Mapa de Localização (Apenas com Lat/Lon)")
    map_data = df.dropna(subset=['Latitude', 'Longitude'])
    if not map_data.empty:
        st.map(map_data, latitude='Latitude', longitude='Longitude', size=10, color='#0044ff')
    else:
        st.info("Nenhum dado de Latitude/Longitude disponível para o mapa.")