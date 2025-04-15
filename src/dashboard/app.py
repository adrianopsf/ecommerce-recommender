import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import numpy as np
from src.ml.recommender import ProductRecommender
from src.ml.sentiment_analyzer import SentimentAnalyzer
from src.database.config import get_db
from src.database.models import Product, Review, Purchase, PurchaseItem
from sqlalchemy import func

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

# Funções auxiliares para carregar dados
@st.cache_data
def load_sales_data():
    """Carrega dados de vendas do banco de dados"""
    db = next(get_db())
    try:
        # Obtém vendas diárias
        sales_query = db.query(
            func.date(Purchase.created_at).label('date'),
            func.sum(PurchaseItem.quantity).label('sales'),
            func.sum(PurchaseItem.price).label('revenue')
        ).join(
            PurchaseItem,
            Purchase.id == PurchaseItem.purchase_id
        ).group_by(
            func.date(Purchase.created_at)
        ).all()
        
        # Converte para DataFrame
        sales_data = pd.DataFrame(sales_query)
        if not sales_data.empty:
            sales_data['date'] = pd.to_datetime(sales_data['date'])
        return sales_data
    finally:
        db.close()

@st.cache_data
def load_sentiment_data():
    """Carrega dados de sentimento do banco de dados"""
    db = next(get_db())
    try:
        # Obtém avaliações diárias
        sentiment_query = db.query(
            func.date(Review.created_at).label('date'),
            Review.sentiment,
            Review.sentiment_score
        ).all()
        
        # Converte para DataFrame
        sentiment_data = pd.DataFrame(sentiment_query)
        if not sentiment_data.empty:
            sentiment_data['date'] = pd.to_datetime(sentiment_data['date'])
        return sentiment_data
    finally:
        db.close()

@st.cache_data
def load_products():
    """Carrega produtos do banco de dados"""
    db = next(get_db())
    try:
        products = db.query(Product).all()
        return [
            {
                "id": p.id,
                "name": p.name,
                "category": p.category,
                "description": p.description,
                "price": p.price
            }
            for p in products
        ]
    finally:
        db.close()

# Carrega os dados
sales_data = load_sales_data()
sentiment_data = load_sentiment_data()
products_data = load_products()

# Inicializa o modelo de recomendação
recommender = ProductRecommender()
if products_data:
    recommender.fit(products_data)

# Obtém a última data disponível
last_date = max(
    sales_data['date'].max() if not sales_data.empty else datetime.now(),
    sentiment_data['date'].max() if not sentiment_data.empty else datetime.now()
)

# Sidebar
st.sidebar.title("Filtros")
date_range = st.sidebar.date_input(
    "Período de análise",
    value=(last_date - timedelta(days=30), last_date)
)

# Filtra os dados pelo período selecionado
if not sales_data.empty:
    sales_data = sales_data[
        (sales_data['date'] >= pd.to_datetime(date_range[0])) &
        (sales_data['date'] <= pd.to_datetime(date_range[1]))
    ]

if not sentiment_data.empty:
    sentiment_data = sentiment_data[
        (sentiment_data['date'] >= pd.to_datetime(date_range[0])) &
        (sentiment_data['date'] <= pd.to_datetime(date_range[1]))
    ]

# Métricas principais
st.subheader("Métricas Principais")
col5, col6, col7, col8 = st.columns(4)

with col5:
    if not sales_data.empty:
        st.metric(
            "Total de Vendas",
            f"R$ {sales_data['revenue'].sum():,.2f}",
            "0%"
        )
    else:
        st.metric("Total de Vendas", "R$ 0,00", "0%")

with col6:
    if not sales_data.empty:
        st.metric(
            "Média de Vendas Diárias",
            f"{sales_data['sales'].mean():.0f}",
            "0%"
        )
    else:
        st.metric("Média de Vendas Diárias", "0", "0%")

with col7:
    if not sentiment_data.empty:
        positive_count = len(sentiment_data[sentiment_data['sentiment'] == 'POSITIVE'])
        total_count = len(sentiment_data)
        percentage = (positive_count / total_count * 100) if total_count > 0 else 0
        st.metric(
            "Avaliações Positivas",
            f"{positive_count:,}",
            f"{percentage:.1f}%"
        )
    else:
        st.metric("Avaliações Positivas", "0", "0%")

with col8:
    if not sentiment_data.empty and not sentiment_data['sentiment_score'].empty:
        st.metric(
            "Score Médio de Sentimento",
            f"{sentiment_data['sentiment_score'].mean():.2f}",
            "0%"
        )
    else:
        st.metric("Score Médio de Sentimento", "0.00", "0%")

# Layout em colunas
col1, col2 = st.columns(2)

# Gráfico de vendas
with col1:
    st.subheader("Vendas Diárias")
    if not sales_data.empty:
        # Cria uma cópia para não modificar o DataFrame original
        sales_data_plot = sales_data.copy()
        # Garante que a coluna date é datetime
        sales_data_plot['date'] = pd.to_datetime(sales_data_plot['date'])
        # Formata a data para mostrar apenas dia/mês/ano
        sales_data_plot['date'] = sales_data_plot['date'].dt.strftime('%d/%m/%Y')
        fig_sales = px.line(
            sales_data_plot,
            x='date',
            y='sales',
            title='Evolução das Vendas',
            labels={'sales': 'Número de Vendas', 'date': 'Data'}
        )
        # Ajusta o layout para melhor visualização
        fig_sales.update_layout(
            xaxis=dict(
                tickangle=45
            ),
            yaxis=dict(
                title='Número de Vendas'
            )
        )
        st.plotly_chart(fig_sales, use_container_width=True)
    else:
        st.warning("Não há dados de vendas para o período selecionado.")

# Gráfico de receita
with col2:
    st.subheader("Receita Diária")
    if not sales_data.empty:
        # Cria uma cópia para não modificar o DataFrame original
        sales_data_plot = sales_data.copy()
        # Garante que a coluna date é datetime
        sales_data_plot['date'] = pd.to_datetime(sales_data_plot['date'])
        # Formata a data para mostrar apenas dia/mês/ano
        sales_data_plot['date'] = sales_data_plot['date'].dt.strftime('%d/%m/%Y')
        fig_revenue = px.line(
            sales_data_plot,
            x='date',
            y='revenue',
            title='Evolução da Receita',
            labels={'revenue': 'Receita (R$)', 'date': 'Data'}
        )
        # Ajusta o layout para melhor visualização
        fig_revenue.update_layout(
            xaxis=dict(
                tickangle=45
            ),
            yaxis=dict(
                title='Receita (R$)'
            )
        )
        st.plotly_chart(fig_revenue, use_container_width=True)
    else:
        st.warning("Não há dados de receita para o período selecionado.")

# Análise de sentimento
st.subheader("Análise de Sentimento das Avaliações")
col3, col4 = st.columns(2)

# Distribuição de sentimento
with col3:
    if not sentiment_data.empty:
        sentiment_dist = sentiment_data['sentiment'].value_counts().reset_index()
        sentiment_dist.columns = ['sentiment', 'count']
        # Traduz os sentimentos para português
        sentiment_map = {
            'POSITIVE': 'Positivo',
            'NEUTRAL': 'Neutro',
            'NEGATIVE': 'Negativo'
        }
        sentiment_dist['sentiment'] = sentiment_dist['sentiment'].map(sentiment_map)
        fig_sentiment = px.pie(
            sentiment_dist,
            values='count',
            names='sentiment',
            title='Distribuição de Sentimento',
            color='sentiment',
            color_discrete_map={
                'Positivo': 'green',
                'Neutro': 'gray',
                'Negativo': 'red'
            }
        )
        st.plotly_chart(fig_sentiment, use_container_width=True)
    else:
        st.warning("Não há dados de sentimento para o período selecionado.")

# Evolução do sentimento
with col4:
    if not sentiment_data.empty:
        # Cria uma cópia para não modificar o DataFrame original
        sentiment_trend = sentiment_data.copy()
        # Garante que a coluna date é datetime
        sentiment_trend['date'] = pd.to_datetime(sentiment_trend['date'])
        # Agrupa por data e calcula a média
        sentiment_trend = sentiment_trend.groupby('date')['sentiment_score'].mean().reset_index()
        # Formata a data para mostrar apenas dia/mês/ano
        sentiment_trend['date'] = sentiment_trend['date'].dt.strftime('%d/%m/%Y')
        fig_sentiment_trend = px.line(
            sentiment_trend,
            x='date',
            y='sentiment_score',
            title='Evolução do Sentimento Médio'
        )
        # Ajusta o layout para melhor visualização
        fig_sentiment_trend.update_layout(
            xaxis=dict(
                tickangle=45
            ),
            yaxis=dict(
                title='Score de Sentimento',
                range=[0, 1]  # Define o range do score de 0 a 1
            )
        )
        st.plotly_chart(fig_sentiment_trend, use_container_width=True)
    else:
        st.warning("Não há dados de sentimento para o período selecionado.")

# Recomendações
st.subheader("Recomendações de Produtos")
if products_data:
    # Seleciona um produto aleatório para demonstrar as recomendações
    base_product = np.random.choice(products_data)
    
    # Obtém recomendações usando o modelo
    recommended_ids = recommender.recommend_products(base_product['id'], n_recommendations=5)
    
    # Filtra os produtos recomendados
    recommended_products = [p for p in products_data if p['id'] in recommended_ids]
    
    # Cria DataFrame com as recomendações
    recommendations_df = pd.DataFrame(recommended_products)
    
    # Formata os dados
    recommendations_df['price'] = recommendations_df['price'].apply(lambda x: f"R$ {x:,.2f}")
    
    # Exibe o produto base
    st.markdown(f"**Produto Base:** {base_product['name']}")
    
    # Exibe a tabela de recomendações
    st.dataframe(
        recommendations_df.rename(columns={
            'id': 'ID',
            'name': 'Produto',
            'category': 'Categoria',
            'price': 'Preço',
            'description': 'Descrição'
        })
    )
else:
    st.warning("Não há produtos disponíveis para gerar recomendações.")

# Tabela com últimos 5 dias
st.subheader("Últimos 5 Dias de Dados")
if not sales_data.empty and not sentiment_data.empty:
    # Combina dados de vendas e sentimento
    last_5_days = pd.merge(
        sales_data.sort_values('date', ascending=False).head(5),
        sentiment_data.sort_values('date', ascending=False).head(5),
        on='date',
        how='inner'
    )
    
    # Formata a tabela
    last_5_days['date'] = last_5_days['date'].dt.strftime('%d/%m/%Y')
    last_5_days['revenue'] = last_5_days['revenue'].apply(lambda x: f"R$ {x:,.2f}")
    last_5_days['sentiment_score'] = last_5_days['sentiment_score'].apply(lambda x: f"{x:.2f}")
    
    # Renomeia as colunas
    last_5_days = last_5_days.rename(columns={
        'date': 'Data',
        'sales': 'Vendas',
        'revenue': 'Receita',
        'sentiment': 'Sentimento',
        'sentiment_score': 'Score'
    })
    
    # Exibe a tabela
    st.dataframe(last_5_days)
else:
    st.warning("Não há dados suficientes para exibir a tabela dos últimos 5 dias.")

# Rodapé
st.markdown("---")
st.markdown("Desenvolvido com ❤️ usando Streamlit") 