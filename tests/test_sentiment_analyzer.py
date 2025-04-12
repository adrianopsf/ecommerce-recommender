import pytest
from src.ml.sentiment_analyzer import SentimentAnalyzer

@pytest.fixture
def sentiment_analyzer():
    return SentimentAnalyzer()

@pytest.fixture
def sample_reviews():
    return [
        {
            "id": 1,
            "user_id": 1,
            "product_id": 1,
            "rating": 5,
            "text": "Produto excelente, superou minhas expectativas!"
        },
        {
            "id": 2,
            "user_id": 2,
            "product_id": 1,
            "rating": 1,
            "text": "Péssimo produto, não recomendo a ninguém."
        },
        {
            "id": 3,
            "user_id": 3,
            "product_id": 2,
            "rating": 3,
            "text": "Produto mediano, poderia ser melhor."
        }
    ]

def test_analyze_text_positive(sentiment_analyzer):
    text = "Produto excelente, superou minhas expectativas!"
    result = sentiment_analyzer.analyze_text(text)
    
    assert isinstance(result, dict)
    assert 'sentiment' in result
    assert 'score' in result
    assert result['score'] > 0.5

def test_analyze_text_negative(sentiment_analyzer):
    text = "Péssimo produto, não recomendo a ninguém."
    result = sentiment_analyzer.analyze_text(text)
    
    assert isinstance(result, dict)
    assert 'sentiment' in result
    assert 'score' in result
    assert result['score'] < 0.5

def test_analyze_text_neutral(sentiment_analyzer):
    text = "Produto mediano, poderia ser melhor."
    result = sentiment_analyzer.analyze_text(text)
    
    assert isinstance(result, dict)
    assert 'sentiment' in result
    assert 'score' in result
    assert 0.3 <= result['score'] <= 0.7

def test_analyze_review(sentiment_analyzer, sample_reviews):
    review = sample_reviews[0]
    result = sentiment_analyzer.analyze_review(review)
    
    assert isinstance(result, dict)
    assert 'sentiment' in result
    assert 'sentiment_score' in result
    assert result['sentiment_score'] > 0.5

def test_combine_sentiment_and_rating(sentiment_analyzer):
    # Teste com sentimento positivo e nota alta
    result = sentiment_analyzer._combine_sentiment_and_rating(
        sentiment="POSITIVE",
        sentiment_score=0.8,
        rating=5
    )
    assert result['sentiment'] == "POSITIVE"
    assert result['score'] > 0.7
    
    # Teste com sentimento negativo e nota baixa
    result = sentiment_analyzer._combine_sentiment_and_rating(
        sentiment="NEGATIVE",
        sentiment_score=0.2,
        rating=1
    )
    assert result['sentiment'] == "NEGATIVE"
    assert result['score'] < 0.3
    
    # Teste com sentimento neutro e nota média
    result = sentiment_analyzer._combine_sentiment_and_rating(
        sentiment="NEUTRAL",
        sentiment_score=0.5,
        rating=3
    )
    assert result['sentiment'] == "NEUTRAL"
    assert 0.3 <= result['score'] <= 0.7 