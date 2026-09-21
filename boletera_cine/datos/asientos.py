"""
datos/asientos.py
------------------
Fuente de datos SIMULADA del mapa de asientos por sala.

Layout tipo sala de cine real: 10 filas (A-J) x 12 asientos, divididos
en dos bloques de 6 con un pasillo central (como en el ejemplo que
compartió el equipo). En el Sprint 4 (Base de Datos) esto se reemplaza
por una tabla real.
"""

FILAS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
COLUMNAS = 12  # asientos por fila (6 a la izquierda + 6 a la derecha del pasillo)
COLUMNAS_POR_BLOQUE = 6

# Asientos ya vendidos por sala (simulado, no cambia entre corridas)
OCUPADOS_POR_SALA = {
    "Sala 1 - 3D": {
        "C5", "C6", "C7", "C8", "D5", "D6", "D7", "D8",
        "E1", "E2", "F11", "F12", "H4", "H5", "H6", "I9", "I10", "J1", "J2",
    },
    "Sala 2": {
        "B3", "B4", "C9", "C10", "D6", "D7", "E5", "E6", "E7",
        "G1", "G2", "H8", "H9", "I11", "I12",
    },
    "Sala 3": {
        "A1", "A2", "A11", "A12", "D5", "D6", "D7", "D8",
        "F3", "F4", "F9", "F10", "I6", "I7",
    },
    "Sala 4": {
        "C6", "C7", "C8", "E1", "E2", "E11", "E12", "G5", "G6", "G7", "G8",
    },
    "Sala 5": {
        "B5", "B6", "B7", "B8", "E9", "E10", "H1", "H2", "J5", "J6", "J7",
    },
    "Sala 6": {
        "A5", "A6", "A7", "A8", "D1", "D2", "F6", "F7", "H10", "H11", "H12",
    },
    "Teatro Principal": {
        "B4", "B5", "B6", "B7", "E1", "E2", "E11", "E12",
        "G5", "G6", "G7", "I3", "I4", "I9", "I10",
    },
}


def obtener_mapa_asientos(sala):
    """
    Devuelve la lista de asientos de una sala, cada uno como:
        {"id": "A1", "fila": "A", "columna": 1, "ocupado": True/False}
    Ordenados por fila y luego por columna (1 a 12).
    """
    ocupados = OCUPADOS_POR_SALA.get(sala, set())
    mapa = []
    for fila in FILAS:
        for num in range(1, COLUMNAS + 1):
            asiento_id = f"{fila}{num}"
            mapa.append({
                "id": asiento_id,
                "fila": fila,
                "columna": num,
                "ocupado": asiento_id in ocupados,
            })
    return mapa
