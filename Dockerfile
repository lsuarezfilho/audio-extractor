FROM python:3.10-slim

# Instalar ffmpeg e dependências básicas
RUN apt update && \
    apt install -y ffmpeg curl && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Comando de inicialização
CMD ["python", "server.py"]
