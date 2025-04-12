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
- PostgreSQL
- Git

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/ecommerce-recommender.git
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

4. Configure o arquivo .env:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. Inicialize o banco de dados:
```bash
python src/database/init_db.py
```

## 🏃‍♂️ Executando o Projeto

1. Inicie o servidor de desenvolvimento:
```bash
uvicorn src.api.main:app --reload
```

2. Acesse o dashboard:
```bash
streamlit run src/dashboard/app.py
```

## 📁 Estrutura do Projeto

```
├── data/                   # Dados brutos e processados
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