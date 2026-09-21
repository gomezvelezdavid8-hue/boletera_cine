# Boletera de Cine y Palomitas

Proyecto de la materia **Tópicos Avanzados de Programación**, desarrollado con
metodología **Scrum**.

## Cómo ejecutar el proyecto (VSCode / Visual Studio)

1. Instala Python 3.10+ si no lo tienes.
2. Abre esta carpeta (`boletera_cine`) en tu editor.
3. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```
4. Corre la aplicación:
   ```
   python main.py
   ```

Se abrirá una ventana con proporción de celular (360x800) mostrando la
Cartelera de películas.

## Alcance del proyecto

Por decisión del equipo, se retiraron del alcance las pantallas de **Login**
y **Dulcería**. El flujo final de la app es:

```
Cartelera → Selección de Asientos → Carrito → Boleto digital (QR)
```

## Estructura del proyecto

```
boletera_cine/
├── main.py                       # Punto de entrada, registra las pantallas
├── requirements.txt
├── buildozer.spec                 # Config. para generar el APK (Sprint 5)
├── datos/
│   ├── peliculas.py                # Datos simulados de películas
│   └── asientos.py                 # Mapa de asientos por sala (simulado)
├── pantallas/
│   ├── pantalla_cartelera.py       # Manuel Alvarez — lista de películas
│   ├── pantalla_asientos.py        # José Angel — selección de asientos
│   ├── pantalla_carrito.py         # Jorge Gael — resumen de compra
│   └── pantalla_boleto.py          # David Velez — boleto digital con QR
└── assets/
    └── posters/                    # Imágenes de las películas
```

## Clases principales

| Archivo | Clase |
|---|---|
| `main.py` | `AplicacionBoletera` |
| `pantallas/pantalla_cartelera.py` | `PantallaCartelera`, `TarjetaPelicula` |
| `pantallas/pantalla_asientos.py` | `PantallaAsientos` |
| `pantallas/pantalla_carrito.py` | `PantallaCarrito` |
| `pantallas/pantalla_boleto.py` | `PantallaBoleto` |

## Cómo funciona el flujo completo

1. **Cartelera**: el usuario ve las películas disponibles y presiona
   "Comprar boletos" en la que le interesa.
2. **Asientos**: elige un horario (Spinner) y toca los asientos disponibles
   en el mapa de la sala. Los ocupados están bloqueados (gris), los elegidos
   se marcan en verde. Puede continuar solo si eligió al menos 1 asiento.
3. **Carrito**: muestra el resumen (película, horario, asientos, total) antes
   de confirmar.
4. **Boleto**: genera un folio único y un **código QR real** (librería
   `qrcode`) con los datos de la compra. El botón "Nueva compra" reinicia
   todo el flujo.

## Estado global compartido (`main.py`)

Todas las pantallas comparten estos datos a través de la clase
`AplicacionBoletera`:

```python
from kivy.app import App
app = App.get_running_app()

app.pelicula_seleccionada   # id de la película elegida (int)
app.horario_seleccionado    # horario elegido (str)
app.asientos_seleccionados  # lista de asientos, ej. ["A1", "A2"]
```

## Funciones principales (español)

| Archivo | Función | Qué hace |
|---|---|---|
| `datos/peliculas.py` | `obtener_peliculas()` | Devuelve la lista completa de películas |
| `datos/peliculas.py` | `obtener_pelicula_por_id(id)` | Busca una película específica |
| `datos/asientos.py` | `obtener_mapa_asientos(sala)` | Devuelve los asientos de una sala (ocupados/libres) |
| `pantalla_cartelera.py` | `cargar_peliculas()` | Dibuja las tarjetas de películas |
| `pantalla_cartelera.py` | `seleccionar_pelicula(id)` | Guarda la película elegida y navega a Asientos |
| `pantalla_asientos.py` | `dibujar_mapa()` | Dibuja los botones de asientos de la sala |
| `pantalla_asientos.py` | `alternar_asiento(boton, id)` | Selecciona/deselecciona un asiento |
| `pantalla_asientos.py` | `continuar()` | Guarda horario + asientos y navega a Carrito |
| `pantalla_carrito.py` | `confirmar()` | Navega a la pantalla de Boleto |
| `pantalla_boleto.py` | `generar_qr(pelicula, app)` | Genera el código QR del boleto |
| `pantalla_boleto.py` | `nueva_compra()` | Reinicia la selección y vuelve a Cartelera |

## Librerías utilizadas

- **kivy** — interfaz gráfica (todas las pantallas).
- **qrcode** + **pillow** — generación del código QR del boleto (Sprint 2).

## Mapeo con el cronograma Scrum

| Sprint | Unidad | Contenido |
|---|---|---|
| 1 | 1 | Interfaz / Componentes — **completado** |
| 2 | 2 | Librerías — QR **completado** |
| 3 | 3 | Hilos y Concurrencia — pendiente |
| 4 | 4 | Base de Datos (SQL) — pendiente, hoy los datos son simulados en `datos/` |
| 5 | 5 | Dispositivos móviles / APK — pendiente (ver `buildozer.spec`) |

**Fecha de entrega prevista:** 10 de septiembre.

## Próximo paso natural: Sprint 4 (Base de Datos)

Actualmente `datos/peliculas.py` y `datos/asientos.py` usan listas de Python
fijas (mock data). Cuando trabajen el Sprint 4, esas mismas funciones
(`obtener_peliculas()`, `obtener_pelicula_por_id()`, `obtener_mapa_asientos()`)
se deben reemplazar por consultas SQL reales (por ejemplo con SQLite), sin
tener que tocar las pantallas — ya están preparadas para eso.

## Cómo agregar tus propios pósters

1. Guarda tus imágenes dentro de `assets/posters/`.
2. Nómbralas igual que las de ejemplo (`peli_1.jpg`, `peli_2.jpg`, etc.) para
   reemplazarlas directo, o usa otro nombre y actualiza la ruta en el campo
   `"poster"` dentro de `datos/peliculas.py`.
3. Tamaño recomendado: proporción vertical, ej. 300x450 px.
