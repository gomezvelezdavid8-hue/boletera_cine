"""
datos/peliculas.py
------------------
Fuente de datos SIMULADA (mock) de la cartelera de películas.

En el Sprint 4 (Base de Datos) esto se reemplazará por consultas SQL reales
(tabla 'peliculas' -> ver tarea de Omar Alejandro: "Tablas y lógica para
Cartelera, Películas, Salas y Funciones").

Por ahora, cualquier compañero puede importar PELICULAS desde aquí para
trabajar su pantalla sin depender de que la base de datos ya exista.
"""

PELICULAS = [
    {
        "id": 1,
        "titulo": "Guardianes del Multiverso",
        "genero": "Acción / Ciencia Ficción",
        "duracion": "128 min",
        "clasificacion": "B",
        "sala": "Sala 1 - 3D",
        "horarios": ["14:00", "17:30", "21:00"],
        "sinopsis": "Un equipo de héroes debe evitar el colapso de realidades paralelas.",
        "precio": 65.00,
        "poster": "assets/posters/peli_1.jpg",
        "tipo": "pelicula",
    },
    {
        "id": 2,
        "titulo": "Risas en la Oficina",
        "genero": "Comedia",
        "duracion": "102 min",
        "clasificacion": "A",
        "sala": "Sala 2",
        "horarios": ["13:00", "16:00", "19:00"],
        "sinopsis": "Un empleado torpe intenta salvar la empresa el día del auditor.",
        "precio": 55.00,
        "poster": "assets/posters/peli_2.jpg",
        "tipo": "pelicula",
    },
    {
        "id": 3,
        "titulo": "El Último Faro",
        "genero": "Drama / Suspenso",
        "duracion": "115 min",
        "clasificacion": "B15",
        "sala": "Sala 3",
        "horarios": ["18:00", "20:45"],
        "sinopsis": "Un guardafaro descubre un secreto que cambiará su pueblo para siempre.",
        "precio": 55.00,
        "poster": "assets/posters/peli_3.jpg",
        "tipo": "pelicula",
    },
    {
        "id": 4,
        "titulo": "Aventura Bajo el Mar",
        "genero": "Animación / Familiar",
        "duracion": "95 min",
        "clasificacion": "A",
        "sala": "Sala 4",
        "horarios": ["12:00", "15:00", "17:15"],
        "sinopsis": "Una pequeña tortuga emprende un viaje para encontrar a su familia.",
        "precio": 50.00,
        "poster": "assets/posters/peli_4.jpg",
        "tipo": "pelicula",
    },
    {
        "id": 5,
        "titulo": "Noche de Terror",
        "genero": "Terror",
        "duracion": "98 min",
        "clasificacion": "C",
        "sala": "Sala 5",
        "horarios": ["22:00", "23:30"],
        "sinopsis": "Cinco amigos quedan atrapados en una cabaña con algo que no es humano.",
        "precio": 60.00,
        "poster": "assets/posters/peli_5.jpg",
        "tipo": "pelicula",
    },
    {
        "id": 6,
        "titulo": "Corazones en Ruta",
        "genero": "Romance",
        "duracion": "110 min",
        "clasificacion": "B",
        "sala": "Sala 6",
        "horarios": ["16:30", "19:45"],
        "sinopsis": "Dos desconocidos comparten un viaje en tren que cambia sus vidas.",
        "precio": 55.00,
        "poster": "assets/posters/peli_6.jpg",
        "tipo": "pelicula",
    },
    {
        "id": 7,
        "titulo": "Concierto Sinfónico de Medianoche",
        "genero": "Música / Orquesta",
        "duracion": "90 min",
        "clasificacion": "A",
        "sala": "Teatro Principal",
        "horarios": ["20:00"],
        "sinopsis": "La orquesta local interpreta clásicos bajo un ambiente íntimo.",
        "precio": 120.00,
        "poster": "assets/posters/show_1.jpg",
        "tipo": "show",
    },
    {
        "id": 8,
        "titulo": "Stand Up: Noche de Risas",
        "genero": "Comedia en vivo",
        "duracion": "75 min",
        "clasificacion": "B15",
        "sala": "Teatro Principal",
        "horarios": ["19:00", "21:30"],
        "sinopsis": "Tres comediantes locales se suben al escenario a hacerte reír.",
        "precio": 95.00,
        "poster": "assets/posters/show_2.jpg",
        "tipo": "show",
    },
]


def obtener_peliculas():
    """Devuelve la lista completa de películas (simulación de SELECT * FROM peliculas)."""
    return PELICULAS


def obtener_pelicula_por_id(pelicula_id):
    """Simula un SELECT ... WHERE id = ? para obtener el detalle de una película."""
    for p in PELICULAS:
        if p["id"] == pelicula_id:
            return p
    return None
