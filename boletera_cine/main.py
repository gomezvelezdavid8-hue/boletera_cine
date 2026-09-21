"""
main.py
--------
Punto de entrada de la aplicación "Boletera de Cine".

Cómo correrlo:
    pip install -r requirements.txt
    python main.py

Cada integrante trabaja en SU PROPIO archivo dentro de pantallas/:

    pantallas/pantalla_cartelera.py   -> Manuel Alvarez
    pantallas/pantalla_asientos.py    -> José Angel
    pantallas/pantalla_carrito.py     -> Jorge Gael
    pantallas/pantalla_boleto.py      -> David Velez

(Se retiraron del alcance las pantallas de Login y Dulcería por
decisión del equipo.)

Este archivo (main.py) casi no debería cambiar: solo se toca si se
agrega o renombra una pantalla nueva.
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window
from kivy.properties import NumericProperty, ListProperty, StringProperty

from pantallas.pantalla_cartelera import PantallaCartelera
from pantallas.pantalla_asientos import PantallaAsientos
from pantallas.pantalla_carrito import PantallaCarrito
from pantallas.pantalla_boleto import PantallaBoleto

# Tamaño de ventana para pruebas en escritorio, simulando un celular Android
# estándar. Esto NO afecta la versión móvil/APK real.
Window.size = (360, 800)


class AplicacionBoletera(App):
    """
    Estado global simple compartido entre pantallas.
    Cualquier pantalla puede leerlo/escribirlo así:
        from kivy.app import App
        app = App.get_running_app()
        app.pelicula_seleccionada
        app.horario_seleccionado
        app.asientos_seleccionados
    """
    pelicula_seleccionada = NumericProperty(0)
    horario_seleccionado = StringProperty("")
    asientos_seleccionados = ListProperty([])

    def build(self):
        self.title = "Boletera de Cine y Palomitas"

        gestor = ScreenManager(transition=FadeTransition())
        gestor.add_widget(PantallaCartelera(name="cartelera"))
        gestor.add_widget(PantallaAsientos(name="asientos"))
        gestor.add_widget(PantallaCarrito(name="carrito"))
        gestor.add_widget(PantallaBoleto(name="boleto"))

        gestor.current = "cartelera"
        return gestor

    def reiniciar_compra(self):
        """Limpia la selección actual para empezar una compra nueva."""
        self.pelicula_seleccionada = 0
        self.horario_seleccionado = ""
        self.asientos_seleccionados = []


if __name__ == "__main__":
    AplicacionBoletera().run()
