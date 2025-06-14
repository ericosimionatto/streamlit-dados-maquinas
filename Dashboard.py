# ---------------------------------------------
# UNOESC Campos de Joaçaba
# Pós Graduação em Industria 4.0 e IA
# Disciplçina: Digitalização
# Professor: Natan Cavasin
# Trabalho: Implemetar Dashboard com Streamlit
# Aluno: Érico Simionatto
# Python, Dataset, Dataframe, Streamlit 
# 14/06/2025
# ---------------------------------------------

# Importando as bibliotecas que serão utilizadas
import streamlit as st
import pandas as pd
import plotly.express as px
# ---------------------------------------------

# Importando a base de dados do arquivo CSV
dados_maq = pd.read_csv("smart_manufacturing_data.csv")
#
# ---------------------------------------------

# Fazer o tratamento do campo de data. Facilia na visualização e Manipulação dos dados
dados_maq['timestamp'] = pd.to_datetime(dados_maq['timestamp'])

# Configurando o layout da pagins do Streamlit
st.set_page_config(layout='wide', page_title='Monitoramento de Máquinas')

# Configurando o título do Dashboard
st.title(":blue[<Dashboard] :blue[para Monitoramento] :blue[de Máquinas>]")

# Estrutura de seleção para usuário escolher o que deseja visualizar
# Filtros com sidebar

# Construção para FILTROS (Máquina, status, Eventos, Datas)
with st.sidebar:
          
    # Opção em Checkbox. Opção para selecionar todas as Máquinas
    # value=True vem marcado por padrão
    todas_maquinas = st.checkbox("Selecionar todas as Máquinas", value=True) 

    if todas_maquinas:
        
        # Ao marcar/selecionar todas as Máquinas, dataset será copiado p/ filtro seguinte
        dados_maq_filtrados = dados_maq.copy()
    else:
        
        # Optar por filtro único ou filtro múltiplo
        filtro_multiplas_maq = st.checkbox("Filtrar mais de uma Máquina?")

        if filtro_multiplas_maq:

            # Máquinas, status e as anomalias: Seleção multipla
            machine_filter = st.multiselect("Marque a(s) Máquinas:", dados_maq['machine'].unique(), default=dados_maq['machine'].unique())
            status_filter = st.multiselect("Marque os Status da Máquina:", dados_maq['machine_status'].unique(), default=dados_maq['machine_status'].unique())
            anomaly_filter = st.multiselect("Marque um ou mais Indicadores de Anomalia:", dados_maq['anomaly_flag'].unique(), default=dados_maq['anomaly_flag'].unique())

            # Atribuir os parâmetros de FILTRO multiplo dataframe original
            dados_maq_filtrados = dados_maq[
                (dados_maq['machine'].isin(machine_filter)) &
                (dados_maq['machine_status'].isin(status_filter)) &
                (dados_maq['anomaly_flag'].isin(anomaly_filter))
            ]
        else:
            # Marcar/Selecionar opção única do filtro com selectbox
            machine_filter = st.selectbox("Selecione Máquina:", dados_maq['machine'].unique())
            status_filter = st.selectbox("Selecione Status da Máquina:", dados_maq['machine_status'].unique())
            anomaly_filter = st.selectbox("Selecione Indicador de Anomalia:", dados_maq['anomaly_flag'].unique())

            # dados_maq filtrados a partir das seleções únicas
            dados_maq_filtrados = dados_maq[
                (dados_maq['machine'] == machine_filter) &
                (dados_maq['machine_status'] == status_filter) &
                (dados_maq['anomaly_flag'] == anomaly_filter)
            ]
    
    # Exibir o Total de registros filtrados
    st.markdown(f"### Número de registros filtrados: {len(dados_maq_filtrados)}")
    
    # DATAS, período, linha do tempo. Filtro fazendo uso de datas
    st.subheader("Filtra por Data")

    # Data mínima
    data_min = dados_maq['timestamp'].min().date()

    # Data maxima
    data_max = dados_maq['timestamp'].max().date()

    # Utilizando SLIDER p/ selecionar o intervalo de datas que o usuário deseja visualizar
    data_selecionada = st.slider("Selecionar intervalo de datas:",
                                 min_value=data_min,
                                 max_value=data_max,
                                 value=(data_min, data_max))

    # Aplicando seleção/filtro de datas indicado pelo usuario
    dados_maq_filtrados = dados_maq_filtrados[
        (dados_maq_filtrados['timestamp'].dt.date >= data_selecionada[0]) &
        (dados_maq_filtrados['timestamp'].dt.date <= data_selecionada[1])
    ]