import streamlit as st
import pandas as pd
import plotly.express as px

# CSS (estiliza partes especificas)
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #FDB713; /* Amarelo ODS 7 */
        padding: 2rem 1rem; 
        color: white;
    }

    [data-testid="stSidebar"] .stMultiSelect [data-testid="stMarkdownContainer"] p {
        background-color: #FDB713;
        color: #ffffff;
        border-radius: 5px;
        padding: 2px 6px;
        margin: 2px;
    }
    </style>
""", unsafe_allow_html=True)

# Configuração da URL (pagina)
st.set_page_config(page_title="Dashboard ODS 7", layout="wide")

# Carregar dados em CSV
@st.cache_data
def carregar_dados():
    # Supondo que o arquivo CSV está na mesma pasta
    df = pd.read_csv('acesso_eletricidade_limpo.csv')
    df = df.rename(columns={'Pais': 'Entidade'})
    return df

df = carregar_dados()

# Título 
st.title("Acessibilidade à Eletricidade")

# Sidebar
try:
    st.sidebar.image('images.png')
except:
    st.sidebar.warning("Imagem 'images.png' não encontrada.")

st.sidebar.header("Filtros")

lista_entidades = sorted(df['Entidade'].unique())
lista_anos = sorted(df['Ano'].unique())

entidades_selecionados = st.sidebar.multiselect(
    label="Escolha as entidades para visualizar:",
    options=lista_entidades,
    default=['Brazil', 'Angola', 'South Africa', 'United States', 'India'] 
)

# Filtrar dados
df_filtrado = df[df['Entidade'].isin(entidades_selecionados)]

# Criar abas 
tab1, tab2, tab3 = st.tabs(["Evolução", "Média por Entidade", "Foco em um Ano"])

# Visualização com o plotly
with tab1:
    st.subheader("Evolução do Acesso à Eletricidade")
    fig1 = px.line(
        df_filtrado,
        x='Ano',
        y='Percentual_Acesso',
        color='Entidade',
        markers=True,
        title='Evolução do Acesso à Eletricidade nas Entidades Selecionados',
        labels={'Percentual_Acesso': '% da População com Acesso'}
    )
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    st.subheader("Média do Percentual de Acesso à Eletricidade (2000–2023)")
    df_media = (
        df_filtrado.groupby('Entidade')['Percentual_Acesso']
        .mean()
        .reset_index()
        .sort_values(by='Percentual_Acesso', ascending=True) # Mudei para 'ascending=True' para melhor visualização horizontal
    )
    
    fig2 = px.bar(
        df_media,
        x='Percentual_Acesso', # Eixo X agora é o valor
        y='Entidade',          # Eixo Y agora é a categoria
        orientation='h',       # Define a orientação como horizontal
        color='Entidade',
        title='Média do Acesso à Eletricidade por País',
        labels={'Percentual_Acesso': 'Média % da População com Acesso', 'Entidade': 'Entidade'}
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("Comparativo de Acesso à Eletricidade em um Ano Específico")
    ano_foco = st.selectbox("Escolha o ano de foco:", lista_anos, index=len(lista_anos)-1)
    df_ano = df[df['Ano'] == ano_foco].copy() # Usar .copy() para evitar SettingWithCopyWarning
    df_ano = df_ano[df_ano['Entidade'].isin(entidades_selecionados)]
    df_ano['Percentual_Acesso_Texto'] = df_ano['Percentual_Acesso'].apply(lambda x: f'{x:.1f}%')


    fig3 = px.strip(
        df_ano,
        x='Percentual_Acesso',
        y='Entidade',
        orientation='h', # Orientação horizontal para melhor leitura
        color='Entidade',
        hover_name='Entidade',
        hover_data={'Percentual_Acesso': ':.2f', 'Entidade': False},
        title=f'Comparativo de Acesso à Eletricidade em {ano_foco}',
        labels={'Percentual_Acesso': '% da População com Acesso', 'Entidade': 'Entidade'}
    )
    # Ajuste para aumentar o tamanho dos pontos
    fig3.update_traces(marker=dict(size=15))
    st.plotly_chart(fig3, use_container_width=True)


with st.expander("Ver dados filtrados"):
    st.dataframe(df_filtrado)
