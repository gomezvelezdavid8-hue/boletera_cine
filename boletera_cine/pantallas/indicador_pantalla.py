"""
pantallas/indicador_pantalla.py
----------------------------------
Widget visual que representa el "frente" de la sala, y cambia de forma
y texto según el tipo de evento:

  - tipo="pelicula" -> trapecio con efecto de perspectiva, texto "PANTALLA"
  - tipo="show"     -> arco curvo tipo escenario, texto "TEATRO"

Se coloca arriba del mapa de asientos para darle contexto al usuario
de hacia dónde está viendo.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Quad, RoundedRectangle
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.metrics import dp

KV = """
<IndicadorPantalla>:
    orientation: "vertical"
    size_hint_y: None
    height: dp(60)
    padding: dp(10), 0

    Widget:
        id: forma

    Label:
        id: lbl_tipo
        text: "PANTALLA" if root.tipo == "pelicula" else "TEATRO"
        font_size: "11sp"
        bold: True
        color: (0.6, 0.85, 1, 1) if root.tipo == "pelicula" else (1, 0.8, 0.5, 1)
        size_hint_y: None
        height: dp(18)
"""

Builder.load_string(KV)


class IndicadorPantalla(BoxLayout):
    """
    tipo: "pelicula" (pantalla de cine) o "show" (escenario de teatro).
    Dibuja una forma distinta según el tipo y redibuja automáticamente
    cuando la propiedad cambia.
    """

    tipo = StringProperty("pelicula")

    def on_kv_post(self, base_widget):
        self.ids.forma.bind(pos=self._redibujar, size=self._redibujar)
        self._redibujar()

    def on_tipo(self, *args):
        self._redibujar()

    def _redibujar(self, *args):
        w = self.ids.forma
        w.canvas.before.clear()
        x, y = w.pos
        ancho, alto = w.size
        if ancho <= 0 or alto <= 0:
            return

        with w.canvas.before:
            if self.tipo == "show":
                # Escenario de teatro: barra redondeada (efecto de proscenio)
                Color(0.85, 0.6, 0.25, 0.45)
                RoundedRectangle(
                    pos=(x, y),
                    size=(ancho, alto),
                    radius=[(alto * 0.5, alto * 0.5)] * 4,
                )
            else:
                # Pantalla de cine: trapecio con efecto de perspectiva
                Color(0.75, 0.85, 1, 0.35)
                margen_inferior = ancho * 0.22
                Quad(points=[
                    x + margen_inferior, y,
                    x + ancho - margen_inferior, y,
                    x + ancho, y + alto,
                    x, y + alto,
                ])
