import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Dict, Any
import joblib
import os
from dotenv import load_dotenv

load_dotenv()

class ProductRecommender:
    def __init__(self):
        self.model_path = os.getenv("MODEL_PATH", "./models")
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.similarity_matrix = None
        self.products_df = None
        
    def fit(self, products_data: List[Dict[str, Any]]):
        """
        Treina o modelo de recomendação com os dados dos produtos
        
        Args:
            products_data: Lista de dicionários contendo informações dos produtos
        """
        # Converte os dados para DataFrame
        self.products_df = pd.DataFrame(products_data)
        
        # Combina informações relevantes para o vetorizador
        self.products_df['content'] = self.products_df['name'] + ' ' + \
                                    self.products_df['category'] + ' ' + \
                                    self.products_df['description']
        
        # Cria matriz TF-IDF
        tfidf_matrix = self.vectorizer.fit_transform(self.products_df['content'])
        
        # Calcula similaridade entre produtos
        self.similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
        
        # Salva o modelo
        self._save_model()
    
    def recommend_products(self, product_id: int, n_recommendations: int = 5) -> List[int]:
        """
        Recomenda produtos similares a um produto específico
        
        Args:
            product_id: ID do produto base
            n_recommendations: Número de recomendações desejadas
            
        Returns:
            Lista de IDs dos produtos recomendados
        """
        if self.similarity_matrix is None:
            self._load_model()
            
        # Encontra o índice do produto
        product_idx = self.products_df[self.products_df['id'] == product_id].index[0]
        
        # Obtém similaridades
        similar_products = list(enumerate(self.similarity_matrix[product_idx]))
        
        # Ordena por similaridade
        similar_products = sorted(similar_products, key=lambda x: x[1], reverse=True)
        
        # Remove o próprio produto
        similar_products = similar_products[1:n_recommendations+1]
        
        # Retorna IDs dos produtos recomendados
        return [self.products_df.iloc[i[0]]['id'] for i in similar_products]
    
    def recommend_for_user(self, user_id: int, n_recommendations: int = 5) -> List[int]:
        """
        Recomenda produtos baseado no histórico do usuário
        
        Args:
            user_id: ID do usuário
            n_recommendations: Número de recomendações desejadas
            
        Returns:
            Lista de IDs dos produtos recomendados
        """
        # TODO: Implementar recomendação baseada em histórico do usuário
        # Por enquanto, retorna recomendações aleatórias
        return np.random.choice(self.products_df['id'].values, n_recommendations, replace=False).tolist()
    
    def _save_model(self):
        """Salva o modelo treinado"""
        os.makedirs(self.model_path, exist_ok=True)
        joblib.dump({
            'vectorizer': self.vectorizer,
            'similarity_matrix': self.similarity_matrix,
            'products_df': self.products_df
        }, os.path.join(self.model_path, 'recommender_model.joblib'))
    
    def _load_model(self):
        """Carrega o modelo treinado"""
        model_data = joblib.load(os.path.join(self.model_path, 'recommender_model.joblib'))
        self.vectorizer = model_data['vectorizer']
        self.similarity_matrix = model_data['similarity_matrix']
        self.products_df = model_data['products_df'] 