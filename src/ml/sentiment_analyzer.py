from transformers import pipeline
import os
from dotenv import load_dotenv
from typing import Dict, Any
import joblib

load_dotenv()

class SentimentAnalyzer:
    def __init__(self):
        self.model_path = os.getenv("MODEL_PATH", "./models")
        self.sentiment_pipeline = None
        self._load_model()
    
    def _load_model(self):
        """Carrega o modelo de análise de sentimento"""
        try:
            # Tenta carregar o modelo salvo
            model_data = joblib.load(os.path.join(self.model_path, 'sentiment_model.joblib'))
            self.sentiment_pipeline = model_data['pipeline']
        except:
            # Se não encontrar o modelo, carrega um novo
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="neuralmind/bert-base-portuguese-cased",
                tokenizer="neuralmind/bert-base-portuguese-cased"
            )
            self._save_model()
    
    def _save_model(self):
        """Salva o modelo de análise de sentimento"""
        os.makedirs(self.model_path, exist_ok=True)
        joblib.dump({
            'pipeline': self.sentiment_pipeline
        }, os.path.join(self.model_path, 'sentiment_model.joblib'))
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analisa o sentimento de um texto
        
        Args:
            text: Texto a ser analisado
            
        Returns:
            Dicionário com o resultado da análise
        """
        if not text.strip():
            return {
                'sentiment': 'NEUTRAL',
                'score': 0.5
            }
        
        # Limita o tamanho do texto para o modelo
        max_length = 512
        if len(text) > max_length:
            text = text[:max_length]
        
        # Realiza a análise
        result = self.sentiment_pipeline(text)[0]
        
        # Converte o resultado para o formato desejado
        sentiment_map = {
            'POSITIVE': 'POSITIVE',
            'NEGATIVE': 'NEGATIVE',
            'NEUTRAL': 'NEUTRAL'
        }
        
        return {
            'sentiment': sentiment_map.get(result['label'], 'NEUTRAL'),
            'score': result['score']
        }
    
    def analyze_review(self, review: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisa o sentimento de uma avaliação
        
        Args:
            review: Dicionário com os dados da avaliação
            
        Returns:
            Dicionário com o resultado da análise
        """
        text = review.get('text', '')
        rating = review.get('rating', 0)
        
        # Obtém a análise de sentimento do texto
        sentiment_result = self.analyze_text(text)
        
        # Combina a análise de sentimento com a nota
        final_sentiment = self._combine_sentiment_and_rating(
            sentiment_result['sentiment'],
            sentiment_result['score'],
            rating
        )
        
        return {
            **review,
            'sentiment': final_sentiment['sentiment'],
            'sentiment_score': final_sentiment['score']
        }
    
    def _combine_sentiment_and_rating(
        self,
        sentiment: str,
        sentiment_score: float,
        rating: int
    ) -> Dict[str, Any]:
        """
        Combina a análise de sentimento com a nota da avaliação
        
        Args:
            sentiment: Sentimento do texto
            sentiment_score: Score do sentimento
            rating: Nota da avaliação
            
        Returns:
            Dicionário com o sentimento final e score
        """
        # Mapeia a nota para um score (0 a 1)
        rating_score = rating / 5.0
        
        # Combina os scores
        combined_score = (sentiment_score + rating_score) / 2
        
        # Determina o sentimento final
        if combined_score >= 0.7:
            final_sentiment = 'POSITIVE'
        elif combined_score <= 0.3:
            final_sentiment = 'NEGATIVE'
        else:
            final_sentiment = 'NEUTRAL'
        
        return {
            'sentiment': final_sentiment,
            'score': combined_score
        } 