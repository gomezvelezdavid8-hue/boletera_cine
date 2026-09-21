"""
pantallas/pantalla_asientos.py
----------------------------
Selección de asientos para la función elegida.

Layout tipo sala real: 10 filas x 12 asientos con pasillo central,
indicador de "PANTALLA" arriba (para ubicar hacia dónde está el frente
de la sala) y controles de zoom (+/-) para acercar o alejar el mapa.

Flujo:
  1. Al entrar, lee la película elegida en Cartelera (App.pelicula_seleccionada)
  2. Muestra un selector de horario (Spinner) con los horarios de esa película
  3. Dibuja el mapa de asientos de la sala (datos/asientos.py), coloreando
     ocupados / disponibles / seleccionados
  4. El usuario toca asientos disponibles para seleccionarlos/deseleccionarlos
  5. Al presionar "Continuar al carrito", guarda horario + asientos en el
     estado global y navega a la pantalla de Carrito
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.app import App

from datos.peliculas import obtener_pelicula_por_id
from datos.asientos import obtener_mapa_asientos, COLUMNAS_POR_BLOQUE
from pantallas.barra_progreso import BarraProgreso
from pantallas.indicador_pantalla import IndicadorPantalla

KV = """
<PantallaAsientos>:
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
                id: lbl_pelicula
                text: "Selecciona tus asientos"
                font_size: "16sp"
                bold: True

        BarraProgreso:
            paso_actual: 2

        Spinner:
            id: spinner_horario
            text: "Elige un horario"
            size_hint_y: None
            height: dp(40)
            on_text: root.cambiar_horario(self.text)

        BoxLayout:
            size_hint_y: None
            height: dp(26)
            padding: dp(10), 0
            spacing: dp(10)
            BoxLayout:
                canvas.before:
                    Color:
                        rgba: 0.3, 0.3, 0.3, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size
                size_hint_x: None
                width: dp(14)
            Label:
                text: "Ocupado"
                font_size: "10sp"
                size_hint_x: None
                width: dp(55)
            BoxLayout:
                canvas.before:
                    Color:
                        rgba: 0.2, 0.6, 0.3, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size
                size_hint_x: None
                width: dp(14)
            Label:
                text: "Elegido"
                font_size: "10sp"
                size_hint_x: None
                width: dp(55)
            Label:
                text: ""

        FloatLayout:
            ScrollView:
                id: scroll_asientos
                do_scroll_x: True
                do_scroll_y: True
                BoxLayout:
                    id: contenedor_mapa
                    orientation: "vertical"
                    size_hint: None, None
                    width: max(self.minimum_width, scroll_asientos.width)
                    height: self.minimum_height
                    padding: dp(6), 0

                    IndicadorPantalla:
                        id: indicador_pantalla
                        size_hint_x: None
                        width: grid_asientos.width

                    GridLayout:
                        id: grid_asientos
                        size_hint: None, None
                        width: self.minimum_width
                        height: self.minimum_height
                        pos_hint: {"center_x": 0.5}
                        spacing: dp(3)
                        padding: dp(6), dp(10)

            BoxLayout:
                orientation: "vertical"
                size_hint: None, None
                size: dp(40), dp(84)
                pos_hint: {"right": 0.98, "top": 0.98}
                spacing: dp(4)

                Button:
                    text: "+"
                    bold: True
                    font_size: "18sp"
                    on_release: root.acercar()

                Button:
                    text: "-"
                    bold: True
                    font_size: "18sp"
                    on_release: root.alejar()

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

            Label:
                id: lbl_resumen
                text: "0 asientos - $0.00"
                font_size: "13sp"
                halign: "left"
                valign: "middle"
                text_size: self.size

            Button:
                text: "< Cartelera"
                size_hint_x: None
                width: dp(90)
                on_release: root.manager.current = "cartelera"

            Button:
                text: "Continuar >"
                size_hint_x: None
                width: dp(110)
                background_color: 0.2, 0.6, 0.3, 1
                on_release: root.continuar()
"""

Builder.load_string(KV)

COLOR_DISPONIBLE = (0.25, 0.25, 0.3, 1)
COLOR_OCUPADO = (0.3, 0.3, 0.3, 1)
COLOR_SELECCIONADO = (0.2, 0.6, 0.3, 1)
COLOR_TEXTO_NORMAL = (1, 1, 1, 1)
COLOR_TEXTO_ERROR = (1, 0.4, 0.4, 1)

MAX_ASIENTOS_POR_COMPRA = 8

TAMANO_ASIENTO_BASE = 32  # dp
TAMANO_ASIENTO_MIN = 18
TAMANO_ASIENTO_MAX = 48


class PantallaAsientos(Screen):
    """Nombre registrado en el ScreenManager: 'asientos'"""

    pelicula = None
    seleccionados = None
    tamano_asiento = TAMANO_ASIENTO_BASE

    def on_pre_enter(self, *args):
        self.seleccionados = set()
        self.tamano_asiento = TAMANO_ASIENTO_BASE
        app = App.get_running_app()

        try:
            self.pelicula = obtener_pelicula_por_id(app.pelicula_seleccionada)
        except Exception:
            self.pelicula = None
            self.mostrar_error("No se pudo cargar la información de la película")
            return

        if not self.pelicula:
            self.ids.lbl_pelicula.text = "Elige una película primero"
            self.ids.grid_asientos.clear_widgets()
            self.ids.spinner_horario.values = []
            self.mostrar_error("Vuelve a la cartelera y elige una película")
            return

        self.ids.lbl_pelicula.text = f"{self.pelicula['titulo']} - {self.pelicula['sala']}"
        self.ids.indicador_pantalla.tipo = self.pelicula.get("tipo", "pelicula")
        self.ids.spinner_horario.values = self.pelicula["horarios"]
        self.ids.spinner_horario.text = self.pelicula["horarios"][0]
        self.cambiar_horario(self.pelicula["horarios"][0])

    def cambiar_horario(self, horario):
        """Al cambiar de horario se reinicia la selección (cada función es independiente)."""
        if not self.pelicula:
            return
        self.seleccionados = set()
        self.dibujar_mapa()
        self.actualizar_resumen()

    def acercar(self):
        self.tamano_asiento = min(self.tamano_asiento + 6, TAMANO_ASIENTO_MAX)
        self.dibujar_mapa()

    def alejar(self):
        self.tamano_asiento = max(self.tamano_asiento - 6, TAMANO_ASIENTO_MIN)
        self.dibujar_mapa()

    def dibujar_mapa(self):
        """
        Dibuja el mapa completo: filas A-J, 12 asientos por fila divididos
        en dos bloques de 6 con un pasillo central, más una etiqueta de
        fila al inicio de cada renglón.
        """
        grid = self.ids.grid_asientos
        grid.clear_widgets()
        if not self.pelicula:
            return

        try:
            mapa = obtener_mapa_asientos(self.pelicula["sala"])
        except Exception:
            self.mostrar_error("No se pudo cargar el mapa de asientos de la sala")
            return

        if not mapa:
            self.mostrar_error("Esta sala no tiene asientos configurados")
            return

        tam = dp(self.tamano_asiento)
        tam_etiqueta = dp(self.tamano_asiento * 0.6)
        tam_pasillo = dp(self.tamano_asiento * 0.5)
        fuente = f"{max(8, int(self.tamano_asiento * 0.32))}sp"

        total_columnas = 1 + COLUMNAS_POR_BLOQUE + 1 + COLUMNAS_POR_BLOQUE  # etiqueta + bloque + pasillo + bloque
        grid.cols = total_columnas

        fila_actual = None
        for asiento in mapa:
            if asiento["fila"] != fila_actual:
                fila_actual = asiento["fila"]
                grid.add_widget(Label(
                    text=fila_actual,
                    size_hint=(None, None),
                    size=(tam_etiqueta, tam),
                    font_size=fuente,
                    bold=True,
                    color=(0.7, 0.7, 0.7, 1),
                ))

            if asiento["columna"] == COLUMNAS_POR_BLOQUE + 1:
                # Pasillo central entre el bloque izquierdo y derecho
                grid.add_widget(Widget(size_hint=(None, None), size=(tam_pasillo, tam)))

            btn = Button(
                text=str(asiento["columna"]),
                size_hint=(None, None),
                size=(tam, tam),
                font_size=fuente,
                background_normal="",
                background_disabled_normal="",
            )
            if asiento["ocupado"]:
                btn.background_color = COLOR_OCUPADO
                btn.disabled = True
            else:
                if asiento["id"] in self.seleccionados:
                    btn.background_color = COLOR_SELECCIONADO
                else:
                    btn.background_color = COLOR_DISPONIBLE
                btn.bind(on_release=lambda b, aid=asiento["id"]: self.alternar_asiento(b, aid))
            grid.add_widget(btn)

    def alternar_asiento(self, boton, asiento_id):
        if asiento_id in self.seleccionados:
            self.seleccionados.remove(asiento_id)
            boton.background_color = COLOR_DISPONIBLE
        elif len(self.seleccionados) >= MAX_ASIENTOS_POR_COMPRA:
            self.mostrar_error(f"Máximo {MAX_ASIENTOS_POR_COMPRA} asientos por compra")
            return
        else:
            self.seleccionados.add(asiento_id)
            boton.background_color = COLOR_SELECCIONADO
        self.actualizar_resumen()

    def actualizar_resumen(self):
        cantidad = len(self.seleccionados) if self.seleccionados else 0
        precio = self.pelicula["precio"] if self.pelicula else 0
        total = cantidad * precio
        self.ids.lbl_resumen.color = COLOR_TEXTO_NORMAL
        self.ids.lbl_resumen.text = f"{cantidad} asiento(s) - ${total:.2f}"

    def mostrar_error(self, mensaje):
        self.ids.lbl_resumen.color = COLOR_TEXTO_ERROR
        self.ids.lbl_resumen.text = mensaje

    def continuar(self):
        if not self.pelicula:
            self.mostrar_error("No hay película seleccionada")
            return
        if not self.seleccionados:
            self.mostrar_error("Selecciona al menos 1 asiento")
            return
        if not self.ids.spinner_horario.text or self.ids.spinner_horario.text == "Elige un horario":
            self.mostrar_error("Elige un horario para continuar")
            return

        app = App.get_running_app()
        app.horario_seleccionado = self.ids.spinner_horario.text
        app.asientos_seleccionados = sorted(self.seleccionados)
        self.manager.current = "carrito"
