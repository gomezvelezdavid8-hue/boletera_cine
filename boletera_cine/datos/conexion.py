"""
datos/conexion.py
-------------------
Módulo central de conexión a PostgreSQL.
"""

import os
import psycopg2
import psycopg2.extras

CONFIG = {
    "host": os.environ.get("BOLETERA_DB_HOST", "localhost"),
    "port": os.environ.get("BOLETERA_DB_PORT", "5432"),
    "dbname": os.environ.get("BOLETERA_DB_NAME", "boletera_cine"),
    "user": os.environ.get("BOLETERA_DB_USER", "boletera_user"),
    "password": os.environ.get("BOLETERA_DB_PASSWORD", "boletera_pass"),
}


def conectar():
    return psycopg2.connect(**CONFIG)


def consultar(sql, parametros=None):
    conexion = conectar()
    try:
        with conexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(sql, parametros or ())
            return [dict(fila) for fila in cursor.fetchall()]
    finally:
        conexion.close()
