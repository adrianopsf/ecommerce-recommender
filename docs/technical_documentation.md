# Documentação Técnica - Sistema de Recomendação e Análise de Sentimento

## Visão Geral

Este documento descreve a arquitetura e implementação do sistema de recomendação e análise de sentimento para e-commerce.

## Arquitetura do Sistema

O sistema é composto pelos seguintes componentes principais:

1. **API REST (FastAPI)**
   - Endpoints para produtos, usuários e avaliações
   - Integração com o sistema de recomendação
   - Processamento de análise de sentimento

2. **Sistema de Recomendação**
   - Baseado em similaridade de conteúdo (TF-IDF)
   - Recomendação personalizada por usuário
   - Filtragem colaborativa

3. **Análise de Sentimento**
   - Modelo BERT em português
   - Análise de texto e avaliações
   - Combinação com notas numéricas

4. **Dashboard (Streamlit)**
   - Visualização de métricas
   - Análise de tendências
   - Monitoramento em tempo real

5. **Banco de Dados (PostgreSQL)**
   - Armazenamento de dados estruturados
   - Relacionamentos entre entidades
   - Índices para otimização

## Fluxo de Dados

1. **Coleta de Dados**
   - Produtos cadastrados
   - Avaliações dos usuários
   - Histórico de compras

2. **Processamento**
   - Limpeza e normalização
   - Extração de features
   - Treinamento de modelos

3. **Análise**
   - Cálculo de similaridade
   - Classificação de sentimento
   - Geração de recomendações

4. **Visualização**
   - Dashboard interativo
   - Relatórios automáticos
   - Alertas de tendências

## Modelos de Machine Learning

### Sistema de Recomendação

```python
class ProductRecommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.similarity_matrix = None
        
    def fit(self, products_data):
        # Implementação do treinamento
        pass
        
    def recommend_products(self, product_id, n_recommendations):
        # Implementação da recomendação
        pass
```

### Análise de Sentimento

```python
class SentimentAnalyzer:
    def __init__(self):
        self.model = pipeline("sentiment-analysis")
        
    def analyze_text(self, text):
        # Implementação da análise
        pass
        
    def analyze_review(self, review):
        # Implementação da análise de avaliação
        pass
```

## API Endpoints

### Produtos
- `GET /products/` - Lista todos os produtos
- `GET /products/{id}` - Obtém detalhes de um produto
- `GET /products/{id}/recommendations` - Obtém recomendações

### Avaliações
- `POST /reviews/` - Cria uma nova avaliação
- `GET /reviews/{id}` - Obtém detalhes de uma avaliação
- `GET /reviews/product/{id}` - Lista avaliações de um produto

### Usuários
- `GET /users/{id}/recommendations` - Obtém recomendações personalizadas
- `GET /users/{id}/history` - Obtém histórico de compras

## Banco de Dados

### Diagrama ER

```
User
  - id (PK)
  - name
  - email
  - created_at
  - updated_at

Product
  - id (PK)
  - name
  - description
  - price
  - category
  - stock
  - created_at
  - updated_at

Review
  - id (PK)
  - user_id (FK)
  - product_id (FK)
  - rating
  - text
  - sentiment
  - sentiment_score
  - created_at
  - updated_at

Purchase
  - id (PK)
  - user_id (FK)
  - total_amount
  - status
  - created_at
  - updated_at

PurchaseItem
  - id (PK)
  - purchase_id (FK)
  - product_id (FK)
  - quantity
  - price
  - created_at
```

## Configuração e Deploy

### Requisitos
- Python 3.9+
- PostgreSQL 12+
- Docker (opcional)

### Instalação
1. Clone o repositório
2. Crie ambiente virtual
3. Instale dependências
4. Configure variáveis de ambiente
5. Inicialize banco de dados

### Deploy
1. Configure servidor
2. Instale dependências
3. Configure nginx/apache
4. Inicie serviços
5. Configure monitoramento

## Monitoramento e Manutenção

### Métricas
- Latência da API
- Taxa de acerto das recomendações
- Precisão da análise de sentimento
- Uso de recursos

### Logs
- Acesso à API
- Erros e exceções
- Performance dos modelos
- Alterações no banco de dados

## Segurança

### Autenticação
- JWT tokens
- OAuth2 (opcional)
- Rate limiting

### Dados
- Criptografia em trânsito
- Backup automático
- Controle de acesso

## Próximos Passos

1. Implementar A/B testing
2. Adicionar mais modelos de recomendação
3. Melhorar visualizações
4. Otimizar performance
5. Expandir análise de sentimento 