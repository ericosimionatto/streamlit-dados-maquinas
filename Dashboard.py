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

# colorir o fundo da página com as cores cinza e azul claro
st.markdown(
    """
    <style>
    .reportview-container {
        background-color: #f0f0f0; /* Cinza claro */
    }
    .stApp {
        background-color: #e0f7fa; /* Azul claro */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Configurando o título do Dashboard
st.title(":orange[Dashboard] :orange[para Monitoramento] :orange[de Máquinas]")



# Estrutura de seleção para usuário escolher o que deseja visualizar
# Filtros com sidebar

# Construção para FILTROS (Máquina, status, Eventos, Datas)
with st.sidebar:

    # Incluir uma imagem no topo da barra lateral
    st.image("https://i2aiportal.blob.core.windows.net/static/content/2022/6/21/883719download.jpg.900x450_q85_crop.jpg", width=200)
    st.header("Filtros de Seleção")
          
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
abas = st.tabs(["| 📈GRÁFICOS", "| 💡ANÁLISES", "| 🔄️ SENSORES: Médias", "| 📚CORRELAÇÃO Matriz", "| 📥DOWNLOAD DOS DADOS"])

with abas[0]:
    st.header("Principais Gráficos")

    #Pintar o texto de laranja
    st.markdown("<span style='color: green;'>Use os filtros na barra lateral para selecionar as máquinas, status e anomalias desejadas</span>", unsafe_allow_html=True) 
    
    

    # 1º Gráfico: Situação das Máquinas conforme status: histograma
    fig1 = px.histogram(
        dados_maq_filtrados,
        x='machine_status',
        color='machine_status',
        title='Situação geral das Máquinas por Status',
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

    # 4º Gráfico: Anomalias por tipo de falha: Pizza
    fig4 = px.pie(
        dados_maq_filtrados,        
        color='anomaly_flag',
        names='anomaly_flag',
        title='Anomalias x Tipo de Falha'
    )
    st.plotly_chart(fig4, use_container_width=True)

    # 5º Gráfico: Consumo de energia por máquina.
    fig5 = px.line(
        dados_maq_filtrados.groupby('machine')['energy_consumption'].sum().reset_index(),        
        x='machine',
        y='energy_consumption',
        title='Consumo de Energia x Máquina'
    )   
    st.plotly_chart(fig5, use_container_width=True)

    # 7º Gráfico: Umidade média por máquina
    fig7 = px.line(
        dados_maq_filtrados.groupby('machine')['humidity'].mean().reset_index(),
        x='machine',
        y='humidity',
        title='Umidade Média x Máquina'
    )
    st.plotly_chart(fig7, use_container_width=True)

    # 8º Gráfico: Pressão média por máquina
    fig8 = px.bar(
        dados_maq_filtrados.groupby('machine')['pressure'].mean().reset_index(),
        x='machine',
        y='pressure',
        title='Pressão Média x Máquina'
    )
    st.plotly_chart(fig8, use_container_width=True)

    # 9º Gráfico: Linha do tempo que mostra a evolução da temperatura
    tempo_temperatura = dados_maq_filtrados.groupby('timestamp')['temperature'].mean().reset_index()
    fig9 = px.line(
        tempo_temperatura,
        x='timestamp',
        y='temperature',
        title='Linha do tempo: evolução da temperatura'
    )
    st.plotly_chart(fig9, use_container_width=True)

    # 10º Gráfico: Umidade por máquina tipo boxplot
    fig10 = px.box(
        dados_maq_filtrados,
        x='machine',
        y='humidity',
        title='Situação da Umidade por Máquina'
    )
    st.plotly_chart(fig10, use_container_width=True)

    # 11º Gráfico: Dispersão 3D Pressão, Temperatura,  Consumo de Energia
    fig11 = px.scatter_3d(
        dados_maq_filtrados,
        x='pressure',
        y='temperature',
        z='energy_consumption',
        color='machine_status',
        opacity=0.7,
        title='Pressão | Temperatura | Consumo de Energia'
    )
    st.plotly_chart(fig11, use_container_width=True)
    
#---------------------------------------------------------------------------------------------------------------------------
with abas[1]:
    st.header("ANÁLISES")

    # Eventos indicando Sim/Não "Yes" e "no" na featrure maintenance_required [1 e 0]
    dados_maq_filtrados['maintenance_required'] = dados_maq_filtrados['maintenance_required'].map({'Yes': 1, 'no': 0})

    # Máquinas que precisam de manutenção
    maq_precisa_manut = dados_maq_filtrados[dados_maq_filtrados['maintenance_required'] == 1]
    qtde_maq_manut = maq_precisa_manut['machine'].nunique()

    # Litas a Qtde de máquinas que precisam de manutenção
    st.markdown(f"### Total de Máquinas que precisam de manutenção: {qtde_maq_manut}")


    # Gráfico: Temperatura x Consumo de Energia: dispersão
    fig_temperatura_energia = px.scatter(
        dados_maq_filtrados,
        x='temperature',
        y='energy_consumption',
        color='energy_consumption',
        title='Temperatura x Consumo de Energia',
    )
    st.plotly_chart(fig_temperatura_energia, use_container_width=True)    

    # Gráfico de Risco de Parada/Interrupção
    fig_risco_parada = px.pie(              
        dados_maq_filtrados,        
        color='downtime_risk',
        names='downtime_risk',
        title='Risco de Parada/Interrupção'
    )
    st.plotly_chart(fig_risco_parada, use_container_width=True)

    # Gráfico 14: Barras agrupadas da média de temperatura e vibração por status da máquina
    media_status = dados_maq_filtrados.groupby('machine_status')[['temperature', 'vibration']].mean().reset_index()
    fig14 = px.bar(
        media_status,
        x='machine_status',
        y=['temperature', 'vibration'],
        barmode='group',
        title='Média de Temperatura e Vibração por Status da Máquina'
    )
    st.plotly_chart(fig14, use_container_width=True)

# -------------------------------------------------------------------------------------------------------------------------------------------
# Tabela de médias dos sensores por máquina
with abas[2]:
    st.header("Sensores: Médias por Máquina")

    # Selecionado as colunas/features que identificam os sensores
    sensores = ['energy_consumption','temperature', 'pressure', 'vibration', 'humidity']

    # Calcular a média
    medias_por_maquina = dados_maq_filtrados.groupby('machine')[sensores].mean().reset_index()

    # Listar a Tabela. Arredondar as médias e renomear as colunas
    st.dataframe(
        medias_por_maquina.style.format({col: '{:.0f}' for col in sensores}),
        height=400,
        width=000,           
        use_container_width=True,
        hide_index=True,
        column_config={
            'machine': st.column_config.Column("Máquina", width="medium"),
            'energy_consumption': st.column_config.Column("Consumo de Energia (kWh)", width="small"),
            'temperature': st.column_config.Column("Temperatura (°C)", width="small"),
            'pressure': st.column_config.Column("Pressão (Pa)", width="small"),
            'vibration': st.column_config.Column("Vibração (m/s²)", width="small"),
            'humidity': st.column_config.Column("Umidade (%)", width="small")
        }
    )    
    
    # Mostrar tabela com o máximos dos sensores de temperatura, vibração, pressão, umidade e consumo de energia por máquina
    st.subheader("Sensores: Máximos dos  por Máquina")
    maximos_por_maquina = dados_maq_filtrados.groupby('machine')[sensores].max().reset_index()
    st.dataframe(
        maximos_por_maquina.style.format({col: '{:.0f}' for col in sensores}),
        height=400,
        width=400,           
        use_container_width=True,
        hide_index=True,
        column_config={
            'machine': st.column_config.Column("Máquina", width="medium"),
            'energy_consumption': st.column_config.Column("Consumo de Energia (kWh)", width="small"),
            'temperature': st.column_config.Column("Temperatura (°C)", width="small"),
            'pressure': st.column_config.Column("Pressão (Pa)", width="small"),
            'vibration': st.column_config.Column("Vibração (m/s²)", width="small"),
            'humidity': st.column_config.Column("Umidade (%)", width="small")
        }
    )
        

# -------------------------------------------------------------------------------------------------------------------------------------------
with abas[3]:
    st.header("Matriz de Correlação")

    # Selecionar colunas numéricas para correlação
    colunas_numericas = dados_maq_filtrados.select_dtypes(include=['float64', 'int64'])
    correlacao = colunas_numericas.corr()

    # Plotar matriz de correlação com matplotlib
    plt.figure(figsize=(10, 8))
    plt.imshow(correlacao, cmap='coolwarm', aspect='auto')
    plt.colorbar(label='Correlação')
    plt.title("Matriz de Correlação entre Features")
    st.pyplot(plt)
    plt.close()

# -------------------------------------------------------------------------------------------------------------------------------------------
# Criar nova Aba ou página para exibir os dados e permitir o download
with abas[4]:
    st.expander("📥 Download dos Dados Filtrados", expanded=True)
    st.markdown("### Dados Filtrados")
    
    # Exibir os dados filtrados em uma tabela
    st.dataframe(dados_maq_filtrados, use_container_width=True)

    # Exibir a quantidade de registros filtrados
    st.markdown(f"### Total de registros: {len(dados_maq_filtrados)}")
    
    # Trazer a quantidade de maquinas
    quantidade_maquinas = dados_maq_filtrados['machine'].nunique()
    st.markdown(f"### Total de Máquinas: {quantidade_maquinas}")    

    # Trazer a quantidade de colunas
    quantidade_colunas = dados_maq_filtrados.shape[1]   
    st.markdown(f"### Total de Colunas: {quantidade_colunas}")
            

    # Botão para download dos dados filtrados
    csv = dados_maq_filtrados.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download dos Dados Filtrados (CSV)",
        data=csv,
        file_name='dados_filtrados.csv',
        mime='text/csv'
    )
