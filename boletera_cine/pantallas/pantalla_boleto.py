"""
pantallas/pantalla_boleto.py
----------------------------
Boleto digital final, con un código QR real (librería `qrcode`) que
codifica los datos de la compra: película, sala, horario y asientos.

Este es el uso de "librería externa" correspondiente al Sprint 2
(Unidad 2) para la tarea de David Velez.
"""

import io
import random
import string

from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.app import App
from kivy.core.image import Image as CoreImage

import qrcode

from datos.peliculas import obtener_pelicula_por_id
from pantallas.barra_progreso import BarraProgreso

KV = """
<PantallaBoleto>:
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
                text: "Tu Boleto"
                font_size: "18sp"
                bold: True

        BarraProgreso:
            paso_actual: 4

        ScrollView:
            BoxLayout:
                orientation: "vertical"
                padding: dp(20)
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height

                BoxLayout:
                    orientation: "vertical"
                    canvas.before:
                        Color:
                            rgba: 0.15, 0.15, 0.18, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [12]
                    padding: dp(16)
                    spacing: dp(6)
                    size_hint_y: None
                    height: dp(230)

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
                        id: lbl_detalle
                        text: "-"
                        font_size: "13sp"
                        color: 0.8, 0.8, 0.8, 1
                        halign: "left"
                        text_size: self.size
                        size_hint_y: None
                        height: dp(60)

                    Label:
                        id: lbl_folio
                        text: "-"
                        font_size: "12sp"
                        color: 0.5, 0.9, 0.6, 1
                        halign: "left"
                        text_size: self.size
                        size_hint_y: None
                        height: dp(20)

                    Label:
                        id: lbl_total
                        text: "-"
                        font_size: "16sp"
                        bold: True
                        halign: "left"
                        text_size: self.size
                        size_hint_y: None
                        height: dp(28)

                BoxLayout:
                    orientation: "vertical"
                    size_hint_y: None
                    height: dp(280)
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [12]
                    padding: dp(16)

                    Image:
                        id: img_qr

                Label:
                    text: "Presenta este código QR en taquilla."
                    font_size: "12sp"
                    color: 0.6, 0.6, 0.6, 1
                    size_hint_y: None
                    height: dp(30)

        BoxLayout:
            size_hint_y: None
            height: dp(70)
            padding: dp(10)
            canvas.before:
                Color:
                    rgba: 0.08, 0.08, 0.1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

            Button:
                text: "Nueva compra"
                background_color: 0.2, 0.6, 0.3, 1
                on_release: root.nueva_compra()
"""

Builder.load_string(KV)


class PantallaBoleto(Screen):
    """Nombre registrado en el ScreenManager: 'boleto'"""

    folio = ""

    def on_pre_enter(self, *args):
        app = App.get_running_app()

        try:
            pelicula = obtener_pelicula_por_id(app.pelicula_seleccionada)
        except Exception:
            pelicula = None

        if not pelicula or not app.asientos_seleccionados:
            self.ids.lbl_titulo.text = "No hay boleto que mostrar"
            self.ids.lbl_detalle.text = "Vuelve a la cartelera para comprar."
            self.ids.lbl_folio.text = ""
            self.ids.lbl_total.text = ""
            self.ids.img_qr.texture = None
            return

        cantidad = len(app.asientos_seleccionados)
        total = cantidad * pelicula["precio"]

        # Genera un folio único simple para esta compra
        self.folio = "BOL-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

        self.ids.lbl_titulo.text = pelicula["titulo"]
        self.ids.lbl_detalle.text = (
            f"{pelicula['sala']}\n"
            f"Horario: {app.horario_seleccionado}\n"
            f"Asientos: {', '.join(app.asientos_seleccionados)}"
        )
        self.ids.lbl_folio.text = f"Folio: {self.folio}"
        self.ids.lbl_total.text = f"Total pagado: ${total:.2f}"

        try:
            self.generar_qr(pelicula, app)
        except Exception:
            # Si por alguna razón falla la generación del QR (ej. datos
            # corruptos), el boleto se sigue mostrando con su información,
            # solo se avisa que el QR no se pudo generar.
            self.ids.lbl_folio.text = f"Folio: {self.folio}  (QR no disponible)"

    def generar_qr(self, pelicula, app):
        """Genera un código QR real con los datos del boleto y lo muestra."""
        contenido = (
            f"BOLETERA CINE\n"
            f"Folio: {self.folio}\n"
            f"Pelicula: {pelicula['titulo']}\n"
            f"Sala: {pelicula['sala']}\n"
            f"Horario: {app.horario_seleccionado}\n"
            f"Asientos: {','.join(app.asientos_seleccionados)}"
        )

        qr = qrcode.QRCode(box_size=8, border=2)
        qr.add_data(contenido)
        qr.make(fit=True)
        img_pil = qr.make_image(fill_color="black", back_color="white")

        buffer = io.BytesIO()
        img_pil.save(buffer, format="PNG")
        buffer.seek(0)

        core_img = CoreImage(buffer, ext="png")
        self.ids.img_qr.texture = core_img.texture

    def nueva_compra(self):
        app = App.get_running_app()
        app.reiniciar_compra()
        self.manager.current = "cartelera"
