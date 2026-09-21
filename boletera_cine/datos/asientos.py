"""
datos/asientos.py
------------------
Conectado a PostgreSQL (Sprint 4). obtener_mapa_asientos(sala) conserva
la misma firma y forma de resultado que la versión simulada.
"""

from datos.conexion import consultar

FILAS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
COLUMNAS = 12
COLUMNAS_POR_BLOQUE = 6

_CONSULTA_MAPA = """
    SELECT
        a.fila,
        a.columna,
        a.codigo AS id,
        EXISTS (
            SELECT 1 FROM boleto_asientos ba WHERE ba.id_asiento = a.id_asiento
        ) AS ocupado
    FROM asientos a
    JOIN salas s ON s.id_sala = a.id_sala
    WHERE s.nombre = %s
    ORDER BY a.fila, a.columna;
"""


def obtener_mapa_asientos(sala):
    return consultar(_CONSULTA_MAPA, (sala,))
