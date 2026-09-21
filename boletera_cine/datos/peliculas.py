"""
datos/peliculas.py
------------------
Conectado a PostgreSQL (Sprint 4). Devuelve la misma forma de diccionario
que la versión simulada, por lo que pantallas/ no necesita cambios.
"""

from datos.conexion import consultar

_CONSULTA_BASE = """
    SELECT
        e.id_evento AS id,
        e.titulo,
        e.genero,
        e.duracion_min,
        e.clasificacion,
        s.nombre AS sala,
        e.sinopsis,
        e.precio,
        e.poster_url AS poster,
        e.tipo,
        array_agg(DISTINCT to_char(f.hora, 'HH24:MI') ORDER BY to_char(f.hora, 'HH24:MI')) AS horarios
    FROM eventos e
    JOIN funciones f ON f.id_evento = e.id_evento
    JOIN salas s ON s.id_sala = f.id_sala
    {filtro}
    GROUP BY e.id_evento, s.nombre
    ORDER BY e.titulo;
"""


def _formatear(fila):
    fila = dict(fila)
    fila["duracion"] = f"{fila.pop('duracion_min')} min"
    fila["precio"] = float(fila["precio"])
    return fila


def obtener_peliculas():
    filas = consultar(_CONSULTA_BASE.format(filtro=""))
    return [_formatear(f) for f in filas]


def obtener_pelicula_por_id(pelicula_id):
    filas = consultar(_CONSULTA_BASE.format(filtro="WHERE e.id_evento = %s"), (pelicula_id,))
    if not filas:
        return None
    return _formatear(filas[0])
