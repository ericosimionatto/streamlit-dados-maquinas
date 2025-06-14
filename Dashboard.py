# ----------------------------------------
# UNOESC Campos de Joaçaba
# Pós Graduação em Industria 4.0 e IA
# Disciplçina: Digitalização
# Professor: Natan Cavasin
# Trabalho: Implemetar Dashboard com Streamlit
# Aluno: Érico Simionatto
# Python, Dataset, Dataframe, Streamlit 
# 14/06/2025
# ----------------------------------------

# Importando as bibliotecas que serão utilizadas
import streamlit as st
import pandas as pd
import plotly.express as px

# Configurando o título do Dashboard
st.title("Dashboard para Análise dos Dados")

st.text("Clique nas abas abaixo para ver as análises")


# Carregar o dataset. Importando do arquivo CSV
dados = pd.read_csv("smart_manufacturing_data.csv")

# Criar três abas para a análise de dados
aba1, aba2, aba3 = st.tabs(["RELAÇÃO DE MÁQUINAS", "RODANDO", "PARADAS"])

# Aba 1: RELAÇÃO DE MÁQUINAS
with aba1:
    # Trazer todos os nomes das máquinas e o número total de eventos por máquina
    st.subheader("Relação de Máquinas")
    st.write("Lista de máquinas e o número total de eventos por máquina")

    # Agrupar os dados por máquina e contar o número de eventos
    maquina_eventos = dados.groupby('machine').size().reset_index(name='total_events')
    st.write(maquina_eventos)

    
    # Obter o número de máquinas
    maquinas = dados['machine'].unique()
    num_maquinas = len(maquinas)    
    st.write(f"Número total de máquinas: {num_maquinas}")

    # Contar todos os registros do dataset
    num_registros = len(dados)  
    
    st.write(f"Número total de registros: {num_registros}".replace(",", "."))
    

# Aba 1: SOMENTE AS MÁQUINAS RODANDO
with aba2:
    # Filtrar as máquinas que estão rodando no mês de Janeiro de 01/01/2025 até 31/01/2025  
    dados['timestamp'] = pd.to_datetime(dados['timestamp'])
    dados['timestamp'] = dados['timestamp'].dt.strftime('%B').str.lower()  # Converter para mês em minúsculas   
    dados['timestamp'] = dados['timestamp'].replace({'january': 'janeiro'})  # Substituir janeiro por janeiro em português
    dados = dados[dados['timestamp'] == 'janeiro']  # Filtrar apenas janeiro    
    maquinas_rodando = dados[dados['machine_status'] == 'Running']['machine'].unique()
    st.write(maquinas_rodando)


    # Obter o número de máquinas rodando
    num_maquinas_rodando = len(maquinas_rodando)    
    st.write(f"Número total de máquinas rodando: {num_maquinas_rodando}")
