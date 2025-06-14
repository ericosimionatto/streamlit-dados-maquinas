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
import matplotlib.pyplot as plt

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
    st.markdown(f"### Total de registros filtrados: {len(dados_maq_filtrados)}")

    st.text("-------------------------------------")
    
    # DATAS, período, linha do tempo. Filtro fazendo uso de datas
    st.subheader("Filtrar por Data")

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

# ------------------------------------------------------------------------------------------------------
# Dashboard com Abas

# Criação das abas
abas = st.tabs(["GRÁFICOS", "ANÁLISES", "CORRELAÇÃO Matriz", "SENSORES: Médias"])

with abas[0]:
    st.header("Gráficos para Monitoramento das Máquinas")

    # 1º Gráfico: Consumo de energia por máquina.
    fig1 = px.line(
        dados_maq_filtrados.groupby('machine')['energy_consumption'].sum().reset_index(),        
        x='machine',
        y='energy_consumption',
        title='Consumo de Energia x Máquina'
    )   
    st.plotly_chart(fig1, use_container_width=True)
    

    # 2º Gráfico: Temperaturas média por máquina
    fig2 = px.bar(
        dados_maq_filtrados.groupby('machine')['temperature'].mean().reset_index(),
        x='machine',
        y='temperature',
        title='Temperatura Média x Máquina'
    )
    st.plotly_chart(fig2, use_container_width=True)


    # 3º Gráfico: Vibração média por máquina
    fig3 = px.line(
        dados_maq_filtrados.groupby('machine')['vibration'].mean().reset_index(),
        x='machine',
        y='vibration',  
        title='Vibração Média x Máquina'
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Gráfico 4: Anomalias por tipo de falha (histograma colorido)
    fig4 = px.histogram(
        dados_maq_filtrados,
        x='failure_type',
        color='anomaly_flag',
        title='Anomalias por Tipo de Falha'
    )
    st.plotly_chart(fig4, use_container_width=True)

    # Gráfico 5: Distribuição do status das máquinas (pizza)
    fig5 = px.pie(
        dados_maq_filtrados,
        names='machine_status',
        title='Distribuição do Status das Máquinas'
    )
    st.plotly_chart(fig5, use_container_width=True)

    # Gráfico 6: Temperatura x Vibração (dispersão colorida)
    fig6 = px.scatter(
        dados_maq_filtrados,
        x='temperature',
        y='vibration',
        color='anomaly_flag',
        title='Temperatura x Vibração'
    )
    st.plotly_chart(fig6, use_container_width=True)

    # Gráfico 7: Umidade média por máquina (barras)
    fig7 = px.bar(
        dados_maq_filtrados.groupby('machine')['humidity'].mean().reset_index(),
        x='machine',
        y='humidity',
        title='Umidade Média por Máquina'
    )
    st.plotly_chart(fig7, use_container_width=True)

    # Gráfico 8: Pressão média por máquina (barras)
    fig8 = px.bar(
        dados_maq_filtrados.groupby('machine')['pressure'].mean().reset_index(),
        x='machine',
        y='pressure',
        title='Pressão Média por Máquina'
    )
    st.plotly_chart(fig8, use_container_width=True)

    # Gráfico 9: Evolução temporal da temperatura média geral (linha)
    temp_tempo = dados_maq_filtrados.groupby('timestamp')['temperature'].mean().reset_index()
    fig9 = px.line(
        temp_tempo,
        x='timestamp',
        y='temperature',
        title='Evolução Temporal da Temperatura Média'
    )
    st.plotly_chart(fig9, use_container_width=True)

    # Gráfico 10: Boxplot da vibração por máquina
    fig10 = px.box(
        dados_maq_filtrados,
        x='machine',
        y='vibration',
        title='Distribuição da Vibração por Máquina'
    )
    st.plotly_chart(fig10, use_container_width=True)

    # Gráfico 11: Dispersão 3D temperatura, vibração e consumo de energia
    fig11 = px.scatter_3d(
        dados_maq_filtrados,
        x='temperature',
        y='vibration',
        z='energy_consumption',
        color='machine_status',
        opacity=0.7,
        title='Gráfico 3D: Temperatura, Vibração e Consumo de Energia'
    )
    st.plotly_chart(fig11, use_container_width=True)

    # Gráfico 12: Heatmap temporal da temperatura média diária por máquina
    dados_maq_filtrados['date'] = dados_maq_filtrados['timestamp'].dt.date
    heatmap_data = dados_maq_filtrados.groupby(['machine', 'date'])['temperature'].mean().reset_index()
    heatmap_pivot = heatmap_data.pivot(index='machine', columns='date', values='temperature')
    plt.figure(figsize=(12, 7))
    plt.imshow(heatmap_pivot, cmap='coolwarm', aspect='auto')
    plt.colorbar(label='Temperatura Média')
    plt.title('Heatmap - Temperatura Média Diária por Máquina')
    plt.xlabel('Data')
    plt.ylabel('Máquina')
    st.pyplot(plt)
    plt.close()  # Fecha figura para evitar sobreposição em execuções futuras
# ------------------------------------------------------------------------------------------------------------------------------------------
