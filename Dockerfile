FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Expor porta (Render/Railway usam variável PORT)
EXPOSE 8080

# Comando para iniciar Streamlit
# Render define automaticamente a variável PORT
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0

