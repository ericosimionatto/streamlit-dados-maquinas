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

# Carregar o dataset. Importando do arquivo CSV
dados = pd.read_csv("smart_manufacturing_data.csv")

# Visualizando os dados do dataset
st.subheader("Visualização dos Dados")
st.write("As primeiras linhas do dataset são:")
st.dataframe(dados.head())