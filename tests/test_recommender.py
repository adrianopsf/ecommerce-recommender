import pytest
from src.ml.recommender import ProductRecommender
import pandas as pd
import numpy as np

@pytest.fixture
def sample_products():
    return [
        {
            "id": 1,
            "name": "Smartphone XYZ",
            "category": "Eletrônicos",
            "description": "Último modelo com câmera de alta resolução"
        },
        {
            "id": 2,
            "name": "Notebook ABC",
            "category": "Eletrônicos",
            "description": "Notebook potente para trabalho e jogos"
        },
        {
            "id": 3,
            "name": "Fone de Ouvido Bluetooth",
            "category": "Acessórios",
            "description": "Áudio de alta qualidade e cancelamento de ruído"
        }
    ]

def test_recommender_initialization():
    recommender = ProductRecommender()
    assert recommender.similarity_matrix is None
    assert recommender.products_df is None

def test_recommender_fit(sample_products):
    recommender = ProductRecommender()
    recommender.fit(sample_products)
    
    assert recommender.similarity_matrix is not None
    assert recommender.products_df is not None
    assert len(recommender.products_df) == len(sample_products)

def test_recommend_products(sample_products):
    recommender = ProductRecommender()
    recommender.fit(sample_products)
    
    recommendations = recommender.recommend_products(product_id=1, n_recommendations=2)
    
    assert len(recommendations) == 2
    assert all(isinstance(rec_id, int) for rec_id in recommendations)
    assert 1 not in recommendations  # O produto base não deve estar nas recomendações

def test_recommend_for_user(sample_products):
    recommender = ProductRecommender()
    recommender.fit(sample_products)
    
    recommendations = recommender.recommend_for_user(user_id=1, n_recommendations=2)
    
    assert len(recommendations) == 2
    assert all(isinstance(rec_id, int) for rec_id in recommendations)
    assert len(set(recommendations)) == len(recommendations)  # Não deve haver duplicatas 