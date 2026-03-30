FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicação
COPY app_v2.py .
COPY database.py .
COPY models.py .
COPY services.py .
COPY templates/ templates/
COPY static/ static/

# Exposar porta
EXPOSE 3333

# Comando para iniciar
CMD ["python", "app_v2.py"]
