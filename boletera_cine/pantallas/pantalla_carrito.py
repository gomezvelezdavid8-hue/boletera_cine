"""
pantallas/pantalla_carrito.py
----------------------------
Resumen de la compra antes de confirmar: película, horario, asientos
elegidos y total a pagar. Al confirmar, navega a Boleto.
"""

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import BooleanProperty

from datos.peliculas import obtener_pelicula_por_id
from pantallas.barra_progreso import BarraProgreso

KV = """
<PantallaCarrito>:
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
                text: "Carrito de Compras"
                font_size: "18sp"
                bold: True

        BarraProgreso:
            paso_actual: 3

        BoxLayout:
            orientation: "vertical"
            padding: dp(20)
            spacing: dp(14)

            BoxLayout:
                orientation: "vertical"
                canvas.before:
                    Color:
                        rgba: 0.15, 0.15, 0.18, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [10]
                padding: dp(14)
                spacing: dp(8)

                Label:
                    id: lbl_titulo
                    text: "-"
                    font_size: "18sp"
                    bold: True
                    halign: "left"
                    text_size: self.size
                    size_hint_y: None
                    height: dp(26)

                Label:
                    id: lbl_horario
                    text: "-"
                    font_size: "13sp"
                    color: 0.8, 0.8, 0.8, 1
                    halign: "left"
                    text_size: self.size
                    size_hint_y: None
                    height: dp(22)

                Label:
                    id: lbl_asientos
                    text: "-"
                    font_size: "13sp"
                    color: 0.6, 0.8, 1, 1
                    halign: "left"
                    text_size: self.size
                    size_hint_y: None
                    height: dp(40)

                Label:
                    id: lbl_precio_unitario
                    text: "-"
                    font_size: "12sp"
                    color: 0.7, 0.7, 0.7, 1
                    halign: "left"
                    text_size: self.size
                    size_hint_y: None
                    height: dp(20)

            Label:
                id: lbl_aviso
                text: ""
                font_size: "12sp"
                color: 1, 0.4, 0.4, 1
                size_hint_y: None
                height: dp(20)

            Widget:

            BoxLayout:
                size_hint_y: None
                height: dp(40)
                Label:
                    text: "Total a pagar:"
                    font_size: "16sp"
                    halign: "left"
                    text_size: self.size
                Label:
                    id: lbl_total
                    text: "$0.00"
                    font_size: "20sp"
                    bold: True
                    halign: "right"
                    text_size: self.size

        BoxLayout:
            size_hint_y: None
            height: dp(70)
            padding: dp(10)
            spacing: dp(10)
            canvas.before:
                Color:
                    rgba: 0.08, 0.08, 0.1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

            Button:
                text: "< Editar asientos"
                on_release: root.manager.current = "asientos"

            Button:
                text: "Confirmar compra"
                background_color: 0.2, 0.6, 0.3, 1
                disabled: root.hay_carrito_vacio
                on_release: root.confirmar()
"""

Builder.load_string(KV)


class PantallaCarrito(Screen):
    """Nombre registrado en el ScreenManager: 'carrito'"""

    hay_carrito_vacio = BooleanProperty(False)

    def on_pre_enter(self, *args):
        app = App.get_running_app()

        try:
            pelicula = obtener_pelicula_por_id(app.pelicula_seleccionada)
        except Exception:
            pelicula = None

        if not pelicula or not app.asientos_seleccionados:
            self.hay_carrito_vacio = True
            self.ids.lbl_titulo.text = "No hay nada en el carrito"
            self.ids.lbl_horario.text = ""
            self.ids.lbl_asientos.text = ""
            self.ids.lbl_precio_unitario.text = ""
            self.ids.lbl_total.text = "$0.00"
            self.ids.lbl_aviso.text = "Vuelve a Asientos y elige al menos un lugar"
            return

        self.hay_carrito_vacio = False
        self.ids.lbl_aviso.text = ""

        cantidad = len(app.asientos_seleccionados)
        total = cantidad * pelicula["precio"]

        self.ids.lbl_titulo.text = pelicula["titulo"]
        self.ids.lbl_horario.text = f"{pelicula['sala']}  |  Horario: {app.horario_seleccionado}"
        self.ids.lbl_asientos.text = f"Asientos: {', '.join(app.asientos_seleccionados)}"
        self.ids.lbl_precio_unitario.text = (
            f"{cantidad} boleto(s) x ${pelicula['precio']:.2f}"
        )
        self.ids.lbl_total.text = f"${total:.2f}"

    def confirmar(self):
        app = App.get_running_app()
        if not app.asientos_seleccionados:
            self.ids.lbl_aviso.text = "No se puede confirmar: el carrito está vacío"
            return
        self.manager.current = "boleto"
