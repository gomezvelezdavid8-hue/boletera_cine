-- ============================================================
-- schema.sql
-- Estructura de la base de datos de la Boletera de Cine y Palomitas
-- Motor: PostgreSQL 16
-- ============================================================

DROP TABLE IF EXISTS boleto_asientos CASCADE;
DROP TABLE IF EXISTS boletos CASCADE;
DROP TABLE IF EXISTS funciones CASCADE;
DROP TABLE IF EXISTS eventos CASCADE;
DROP TABLE IF EXISTS asientos CASCADE;
DROP TABLE IF EXISTS salas CASCADE;

CREATE TABLE salas (
    id_sala             SERIAL PRIMARY KEY,
    nombre              VARCHAR(50) NOT NULL UNIQUE,
    filas               SMALLINT NOT NULL,
    columnas_por_bloque SMALLINT NOT NULL
);

CREATE TABLE asientos (
    id_asiento  SERIAL PRIMARY KEY,
    id_sala     INT NOT NULL REFERENCES salas(id_sala) ON DELETE CASCADE,
    fila        CHAR(1) NOT NULL,
    columna     SMALLINT NOT NULL,
    codigo      VARCHAR(4) NOT NULL,
    UNIQUE (id_sala, fila, columna)
);

CREATE TABLE eventos (
    id_evento       SERIAL PRIMARY KEY,
    titulo          VARCHAR(150) NOT NULL,
    genero          VARCHAR(80),
    duracion_min    SMALLINT,
    clasificacion   VARCHAR(10),
    sinopsis        TEXT,
    precio          NUMERIC(8,2) NOT NULL,
    poster_url      VARCHAR(255),
    tipo            VARCHAR(10) NOT NULL CHECK (tipo IN ('pelicula', 'show'))
);

CREATE TABLE funciones (
    id_funcion  SERIAL PRIMARY KEY,
    id_evento   INT NOT NULL REFERENCES eventos(id_evento) ON DELETE CASCADE,
    id_sala     INT NOT NULL REFERENCES salas(id_sala) ON DELETE CASCADE,
    fecha       DATE NOT NULL,
    hora        TIME NOT NULL,
    UNIQUE (id_evento, id_sala, fecha, hora)
);

CREATE TABLE boletos (
    id_boleto       SERIAL PRIMARY KEY,
    folio           VARCHAR(20) NOT NULL UNIQUE,
    id_funcion      INT NOT NULL REFERENCES funciones(id_funcion) ON DELETE CASCADE,
    total           NUMERIC(8,2) NOT NULL,
    fecha_compra    TIMESTAMP NOT NULL DEFAULT now(),
    qr_data         TEXT
);

CREATE TABLE boleto_asientos (
    id_boleto_asiento  SERIAL PRIMARY KEY,
    id_boleto          INT NOT NULL REFERENCES boletos(id_boleto) ON DELETE CASCADE,
    id_asiento         INT NOT NULL REFERENCES asientos(id_asiento) ON DELETE CASCADE,
    id_funcion         INT NOT NULL REFERENCES funciones(id_funcion) ON DELETE CASCADE,
    UNIQUE (id_funcion, id_asiento)
);

CREATE INDEX idx_funciones_evento ON funciones(id_evento);
CREATE INDEX idx_asientos_sala ON asientos(id_sala);
CREATE INDEX idx_boleto_asientos_funcion ON boleto_asientos(id_funcion);
