# Use uma imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    netcat-traditional \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos de requisitos
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Adiciona o diretório de scripts do Python ao PATH
ENV PATH="/root/.local/bin:${PATH}"

# Copia o código fonte
COPY . .

# Expõe as portas necessárias
EXPOSE 8000 8501

# Comando padrão (pode ser sobrescrito no docker-compose)
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"] 