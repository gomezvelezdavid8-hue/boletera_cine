[app]

# Nombre visible de la app en el celular
title = Boletera Cine

# Nombre del paquete (sin espacios, minúsculas)
package.name = boleteracine
package.domain = org.equipo

# Carpeta donde está el código fuente (. = esta misma carpeta)
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Versión de la app
version = 0.1

# Librerías que necesita la app para funcionar
# (agregar aquí cualquier librería nueva que usen: ej. si David usa
#  una librería de QR, se agrega separada por coma)
requirements = python3,kivy

# Orientación de pantalla
orientation = portrait

# Ícono y pantalla de carga (opcional, poner la ruta cuando tengan uno)
# icon.filename = %(source.dir)s/assets/icon.png
# presplash.filename = %(source.dir)s/assets/presplash.png

[buildozer]

# Nivel de detalle en los mensajes al compilar (2 = todo el detalle)
log_level = 2

# Permisos de Android que la app va a pedir
# (agregar INTERNET si en el futuro se conecta a internet/pagos reales)
android.permissions = INTERNET
