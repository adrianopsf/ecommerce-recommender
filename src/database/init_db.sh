#!/bin/bash

# Verifica se a senha está definida
if [ -z "$DOCKER_DB_PASSWORD" ]; then
    echo "Erro: DOCKER_DB_PASSWORD não está definida"
    exit 1
fi

# Aguarda o PostgreSQL estar pronto
echo "Waiting for PostgreSQL to be ready..."
export PGPASSWORD=${DOCKER_DB_PASSWORD}

# Tenta conectar ao banco de dados
while true; do
    if psql -h db -U postgres -d ecommerce_db -c '\q' 2>/dev/null; then
        echo "PostgreSQL is ready!"
        break
    else
        echo "PostgreSQL is not ready yet. Retrying in 5 seconds..."
        sleep 5
    fi
done

# Inicializa o banco de dados
echo "Initializing database..."
python -m src.database.init_db

# Mantém o container rodando
tail -f /dev/null 