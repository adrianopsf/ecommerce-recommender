# Sistema de Recomendação e Análise de Sentimento para E-commerce

Este projeto implementa um sistema de recomendação de produtos e análise de sentimento para e-commerce, utilizando técnicas avançadas de Machine Learning e Processamento de Linguagem Natural.

## 🚀 Funcionalidades

- Sistema de recomendação de produtos personalizado
- Análise de sentimento das avaliações dos clientes
- Dashboard interativo para visualização de insights
- API REST para integração com sistemas existentes
- Pipeline completo de processamento de dados

## 📋 Pré-requisitos

- Python 3.9+
- PostgreSQL 12+
- Git
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/adrianopsf/ecommerce-recommender.git
cd ecommerce-recommender
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o PostgreSQL:
   - Instale o PostgreSQL se ainda não tiver: https://www.postgresql.org/download/
   - Crie um banco de dados chamado `ecommerce_db`:
     ```sql
     CREATE DATABASE ecommerce_db;
     ```
   - Anote a senha do usuário postgres que você definiu durante a instalação

5. Configure o arquivo .env:
```bash
cp .env.example .env
```
Edite o arquivo `.env` com suas configurações:
```
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce_db
DB_USER=postgres
DB_PASSWORD=sua_senha_aqui  # Substitua pela senha que você definiu

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Model Configuration
MODEL_PATH=./models
DATA_PATH=./data
```

6. Inicialize o banco de dados:
```bash
python src/database/init_db.py
```

## 📊 Dados de Exemplo

O projeto inclui dados de exemplo que podem ser usados para testar o sistema. Os dados estão disponíveis na pasta `data/` e incluem:

1. Produtos:
   - ID do produto
   - Nome
   - Descrição
   - Categoria
   - Preço
   - Imagem

2. Avaliações:
   - ID do usuário
   - ID do produto
   - Nota (1-5)
   - Comentário
   - Data

3. Usuários:
   - ID do usuário
   - Nome
   - Email
   - Histórico de compras

Para carregar os dados de exemplo no banco de dados:
```bash
python src/database/load_sample_data.py
```

## 🏃‍♂️ Executando o Projeto

1. Inicie o servidor de desenvolvimento:
```bash
uvicorn src.api.main:app --reload
```
A API estará disponível em: http://localhost:8000

2. Acesse o dashboard:
```bash
streamlit run src/dashboard/app.py
```
O dashboard estará disponível em: http://localhost:8501

## 📁 Estrutura do Projeto

```
├── data/                   # Dados brutos e processados
│   ├── raw/               # Dados brutos
│   └── processed/         # Dados processados
├── models/                 # Modelos treinados
├── notebooks/              # Jupyter notebooks de análise
├── src/
│   ├── api/               # API FastAPI
│   ├── dashboard/         # Dashboard Streamlit
│   ├── database/          # Configuração do banco de dados
│   ├── ml/                # Modelos de ML
│   ├── preprocessing/     # Pipeline de pré-processamento
│   └── utils/             # Funções utilitárias
├── tests/                 # Testes unitários
├── .env                   # Variáveis de ambiente
├── .gitignore            # Arquivos ignorados pelo git
├── requirements.txt       # Dependências do projeto
└── README.md             # Documentação
```

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes. 