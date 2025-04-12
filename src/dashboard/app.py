import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import numpy as np

# Carrega variáveis de ambiente
load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="E-commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Título e descrição
st.title("📊 E-commerce Analytics Dashboard")
st.markdown("""
    Este dashboard fornece insights sobre vendas, recomendações e análise de sentimento das avaliações.
""")

# Sidebar
st.sidebar.title("Filtros")
date_range = st.sidebar.date_input(
    "Período de análise",
    value=(datetime.now() - timedelta(days=30), datetime.now())
)

# Funções auxiliares para carregar dados
@st.cache_data
def load_sales_data():
    # TODO: Implementar carregamento de dados reais
    return pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', end='2023-12-31', freq='D'),
        'sales': np.random.randint(100, 1000, size=365),
        'revenue': np.random.uniform(1000, 10000, size=365)
    })

@st.cache_data
def load_sentiment_data():
    # TODO: Implementar carregamento de dados reais
    return pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', end='2023-12-31', freq='D'),
        'sentiment': np.random.choice(['POSITIVE', 'NEUTRAL', 'NEGATIVE'], size=365, p=[0.6, 0.3, 0.1]),
        'score': np.random.uniform(0, 1, size=365)
    })

# Carrega os dados
sales_data = load_sales_data()
sentiment_data = load_sentiment_data()

# Filtra os dados pelo período selecionado
sales_data = sales_data[
    (sales_data['date'] >= pd.to_datetime(date_range[0])) &
    (sales_data['date'] <= pd.to_datetime(date_range[1]))
]

sentiment_data = sentiment_data[
    (sentiment_data['date'] >= pd.to_datetime(date_range[0])) &
    (sentiment_data['date'] <= pd.to_datetime(date_range[1]))
]

# Layout em colunas
col1, col2 = st.columns(2)

# Gráfico de vendas
with col1:
    st.subheader("Vendas Diárias")
    fig_sales = px.line(
        sales_data,
        x='date',
        y='sales',
        title='Evolução das Vendas'
    )
    st.plotly_chart(fig_sales, use_container_width=True)

# Gráfico de receita
with col2:
    st.subheader("Receita Diária")
    fig_revenue = px.line(
        sales_data,
        x='date',
        y='revenue',
        title='Evolução da Receita'
    )
    st.plotly_chart(fig_revenue, use_container_width=True)

# Análise de sentimento
st.subheader("Análise de Sentimento das Avaliações")
col3, col4 = st.columns(2)

# Distribuição de sentimento
with col3:
    sentiment_dist = sentiment_data['sentiment'].value_counts()
    fig_sentiment = px.pie(
        values=sentiment_dist.values,
        names=sentiment_dist.index,
        title='Distribuição de Sentimento'
    )
    st.plotly_chart(fig_sentiment, use_container_width=True)

# Evolução do sentimento
with col4:
    fig_sentiment_trend = px.line(
        sentiment_data.groupby('date')['score'].mean().reset_index(),
        x='date',
        y='score',
        title='Evolução do Sentimento Médio'
    )
    st.plotly_chart(fig_sentiment_trend, use_container_width=True)

# Recomendações
st.subheader("Recomendações de Produtos")
# TODO: Implementar visualização de recomendações

# Métricas principais
st.subheader("Métricas Principais")
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        "Total de Vendas",
        f"R$ {sales_data['revenue'].sum():,.2f}",
        f"{((sales_data['revenue'].sum() / sales_data['revenue'].sum()) - 1) * 100:.1f}%"
    )

with col6:
    st.metric(
        "Média de Vendas Diárias",
        f"{sales_data['sales'].mean():.0f}",
        f"{((sales_data['sales'].mean() / sales_data['sales'].mean()) - 1) * 100:.1f}%"
    )

with col7:
    st.metric(
        "Avaliações Positivas",
        f"{len(sentiment_data[sentiment_data['sentiment'] == 'POSITIVE']):,}",
        f"{len(sentiment_data[sentiment_data['sentiment'] == 'POSITIVE']) / len(sentiment_data) * 100:.1f}%"
    )

with col8:
    st.metric(
        "Score Médio de Sentimento",
        f"{sentiment_data['score'].mean():.2f}",
        f"{((sentiment_data['score'].mean() / sentiment_data['score'].mean()) - 1) * 100:.1f}%"
    )

# Rodapé
st.markdown("---")
st.markdown("Desenvolvido com ❤️ usando Streamlit") 