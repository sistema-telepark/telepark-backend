#!/bin/bash
# entrypoint.sh — Telepark Backend
# Espera a MySQL, ejecuta migraciones, inicia Django
# Usa Python para probar conexión (no requiere mysql-client)

set -e

# Variables de conexión
DB_HOST="${DB_HOST:-db}"
DB_PORT="${DB_PORT:-3306}"
DB_USER="${DB_USER:-teleparkUser}"
DB_PASSWORD="${DB_PASSWORD:-teleparkUser}"
DB_DATABASE="${DB_DATABASE:-teleparkbackend}"
TIMEOUT=60
INTERVAL=3

echo "Esperando a MySQL en $DB_HOST:$DB_PORT ..."

# Loop de espera usando Python (no requiere mysqladmin)
elapsed=0
while true; do
    result=$(python -c "
import MySQLdb
try:
    conn = MySQLdb.connect(
        host='${DB_HOST}',
        port=int(${DB_PORT}),
        user='${DB_USER}',
        passwd='${DB_PASSWORD}',
        db='${DB_DATABASE}'
    )
    conn.close()
    print('OK')
except Exception as e:
    print('FAIL')
" 2>/dev/null)
    
    if [ "$result" = "OK" ]; then
        echo "MySQL esta listo."
        break
    fi
    
    elapsed=$((elapsed + INTERVAL))
    if [ "$elapsed" -ge "$TIMEOUT" ]; then
        echo "ERROR: MySQL no esta disponible despues de ${TIMEOUT}s"
        echo "   Host: $DB_HOST:$DB_PORT"
        echo "   User: $DB_USER"
        exit 1
    fi
    echo "   MySQL no responde aun... (${elapsed}s/${TIMEOUT}s)"
    sleep $INTERVAL
done

# Verificar configuracion de Django
echo "Verificando configuracion de Django..."
python manage.py check --deploy 2>&1 | grep -v "WARNINGS" || true

# Generar migraciones a partir de los modelos (auto-detecta cambios)
echo "Ejecutando makemigrations..."
python manage.py makemigrations --noinput

# Aplicar migraciones a la base de datos
echo "Ejecutando migrate..."
python manage.py migrate

echo "Migraciones aplicadas correctamente."

# Cargar catálogo geográfico GeoRef (idempotente)
echo "Ejecutando cargar_georef..."
python manage.py cargar_georef

# Crear usuario admin (idempotente)
echo "Ejecutando bootstrap_admin..."
python manage.py bootstrap_admin

# Iniciar servidor de desarrollo
echo "Iniciando servidor Django en 0.0.0.0:8080..."
exec python manage.py runserver 0.0.0.0:8080
