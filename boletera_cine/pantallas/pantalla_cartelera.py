"""
pantallas/pantalla_cartelera.py
----------------------------
Responsable (Sprint 1): Manuel Alvarez
Tarea: "Diseño de interfaz para ver la cartelera y lista de películas
disponibles a los clientes."

Esta pantalla muestra las películas disponibles como una lista de
tarjetas (poster simulado + info). Al presionar "Comprar boletos" navega
a la pantalla de selección de asientos (José Angel), pasándole la
película elegida.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.metrics import dp

from datos.peliculas import obtener_peliculas
from pantallas.barra_progreso import BarraProgreso

KV = """
<TarjetaPelicula>:
    orientation: "horizontal"
    size_hint_y: None
    height: dp(150)
    padding: dp(10)
    spacing: dp(12)
    canvas.before:
        Color:
            rgba: 0.15, 0.15, 0.18, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [10]

    # Poster real de la película (fallback a un color si el archivo no existe)
    BoxLayout:
        size_hint_x: None
        width: dp(90)
        canvas.before:
            Color:
                rgba: 0.35, 0.45, 0.85, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [8]
        Image:
            source: root.poster
            allow_stretch: True
            keep_ratio: False

    BoxLayout:
        orientation: "vertical"
        spacing: dp(2)

        Label:
            text: root.titulo
            font_size: "18sp"
            bold: True
            halign: "left"
            valign: "top"
            text_size: self.size
            size_hint_y: None
            height: dp(26)

        Label:
            text: f"{root.genero}  |  {root.duracion}  |  Clasificación: {root.clasificacion}"
            font_size: "12sp"
            color: 0.8, 0.8, 0.8, 1
            halign: "left"
            valign: "top"
            text_size: self.size
            size_hint_y: None
            height: dp(20)

        Label:
            text: root.sinopsis
            font_size: "12sp"
            color: 0.65, 0.65, 0.65, 1
            halign: "left"
            valign: "top"
            text_size: self.size
            size_hint_y: None
            height: dp(40)
            shorten: True

        Label:
            text: f"Horarios: {root.horarios}"
            font_size: "12sp"
            color: 0.6, 0.8, 1, 1
            halign: "left"
            valign: "top"
            text_size: self.size
            size_hint_y: None
            height: dp(20)

    BoxLayout:
        orientation: "vertical"
        size_hint_x: None
        width: dp(110)
        spacing: dp(6)

        Label:
            text: f"${root.precio:.2f}"
            bold: True
            font_size: "16sp"

        Button:
            text: "Comprar\\nboletos"
            font_size: "12sp"
            halign: "center"
            background_color: 0.2, 0.6, 0.3, 1
            on_release: root.comprar()


<PantallaCartelera>:
    BoxLayout:
        orientation: "vertical"

        BoxLayout:
            size_hint_y: None
            height: dp(56)
            padding: dp(10)
            canvas.before:
                Color:
                    rgba: 0.08, 0.08, 0.1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text: "🎬  Cartelera - Cine Boletera"
                font_size: "20sp"
                bold: True

        BarraProgreso:
            paso_actual: 1

        ScrollView:
            do_scroll_x: False
            BoxLayout:
                id: lista_peliculas
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(10)
                padding: dp(10)
"""

Builder.load_string(KV)


class TarjetaPelicula(BoxLayout):
    """Widget individual que representa una película dentro de la lista."""

    titulo = ObjectProperty("")
    genero = ObjectProperty("")
    duracion = ObjectProperty("")
    clasificacion = ObjectProperty("")
    sinopsis = ObjectProperty("")
    horarios = ObjectProperty("")
    precio = ObjectProperty(0.0)
    poster = ObjectProperty("")

    pelicula_id = None
    screen_ref = None  # referencia a la PantallaCartelera para poder navegar

    def comprar(self):
        """
        Se ejecuta al presionar 'Comprar boletos'.
        Guarda la película seleccionada en el ScreenManager y navega
        a la pantalla de selección de asientos (tarea de José Angel).
        """
        if self.screen_ref:
            self.screen_ref.seleccionar_pelicula(self.pelicula_id)


class PantallaCartelera(Screen):
    """
    Pantalla principal: lista de películas disponibles.
    Nombre registrado en el ScreenManager: 'cartelera'
    """

    def on_pre_enter(self, *args):
        """Se ejecuta cada vez que se entra a esta pantalla: recarga la lista."""
        self.cargar_peliculas()

    def cargar_peliculas(self):
        contenedor = self.ids.lista_peliculas
        contenedor.clear_widgets()

        peliculas = obtener_peliculas()
        for peli in peliculas:
            tarjeta = TarjetaPelicula(
                titulo=peli["titulo"],
                genero=peli["genero"],
                duracion=peli["duracion"],
                clasificacion=peli["clasificacion"],
                sinopsis=peli["sinopsis"],
                horarios=", ".join(peli["horarios"]),
                precio=peli["precio"],
                poster=peli.get("poster", ""),
            )
            tarjeta.pelicula_id = peli["id"]
            tarjeta.screen_ref = self
            contenedor.add_widget(tarjeta)

    def seleccionar_pelicula(self, pelicula_id):
        """
        Pasa la película elegida a la app y navega a la pantalla de asientos.
        José Angel puede leer la película seleccionada en su pantalla con:
            App.get_running_app().pelicula_seleccionada
        """
        app = self.manager.app if hasattr(self.manager, "app") else None
        from kivy.app import App as KivyApp
        app = KivyApp.get_running_app()
        app.pelicula_seleccionada = pelicula_id

        if self.manager.has_screen("asientos"):
            self.manager.current = "asientos"
