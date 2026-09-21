"""
pantallas/barra_progreso.py
------------------------------
Widget reusable que muestra en qué paso del flujo de compra está el
usuario: Cartelera -> Asientos -> Carrito -> Boleto.

Se usa igual en las 4 pantallas, solo cambia el número de paso_actual:

    BarraProgreso:
        paso_actual: 2   # 1=Cartelera, 2=Asientos, 3=Carrito, 4=Boleto
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivy.lang import Builder
from kivy.metrics import dp

KV = """
<CirculoPaso@Label>:
    completado: False
    size_hint: None, None
    size: dp(26), dp(26)
    bold: True
    font_size: "12sp"
    color: 1, 1, 1, 1
    canvas.before:
        Color:
            rgba: (0.2, 0.6, 0.3, 1) if self.completado else (0.3, 0.3, 0.35, 1)
        Ellipse:
            pos: self.pos
            size: self.size

<BarraProgreso>:
    orientation: "horizontal"
    size_hint_y: None
    height: dp(58)
    padding: dp(16), dp(6)
    canvas.before:
        Color:
            rgba: 0.08, 0.08, 0.1, 1
        Rectangle:
            pos: self.pos
            size: self.size
"""

Builder.load_string(KV)

PASOS = ["Cartelera", "Asientos", "Carrito", "Boleto"]


class BarraProgreso(BoxLayout):
    """
    paso_actual: número de paso en el que está el usuario (1 a 4).
    Los pasos ya completados o el actual se muestran en verde,
    los pendientes en gris.
    """

    paso_actual = NumericProperty(1)

    def on_paso_actual(self, *args):
        self.dibujar()

    def on_kv_post(self, base_widget):
        self.dibujar()

    def dibujar(self):
        self.clear_widgets()
        for i, nombre in enumerate(PASOS, start=1):
            completado = i <= self.paso_actual

            columna = BoxLayout(orientation="vertical", spacing=dp(2))

            fila_circulo = BoxLayout()
            from kivy.factory import Factory
            circulo = Factory.CirculoPaso(text=str(i))
            circulo.completado = completado
            fila_circulo.add_widget(circulo)
            columna.add_widget(fila_circulo)

            etiqueta = Label(
                text=nombre,
                font_size="9sp",
                color=(1, 1, 1, 1) if completado else (0.55, 0.55, 0.55, 1),
                size_hint_y=None,
                height=dp(16),
            )
            columna.add_widget(etiqueta)

            self.add_widget(columna)
