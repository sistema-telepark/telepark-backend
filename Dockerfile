# ============================================================
# Dockerfile — Telepark Backend
# Base: python:3.14-slim (single stage)
# Django 6.0.6 + DRF 3.17.1 + MySQL 8.4
# ============================================================

FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instalar dependencias de compilación y runtime para mysqlclient
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    libffi-dev \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar requirements primero (caching de capas)
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt

# Copiar el proyecto
COPY . .

# Las migraciones se auto-generan en entrypoint.sh (makemigrations --noinput)

# Crear directorio static si no existe
RUN mkdir -p static

# Puerto de exposición
EXPOSE 8080

# Entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
