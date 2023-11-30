import sqlite3

# Conectar a la base de datos SQLite
conexion = sqlite3.connect("db_etl.db")
cursor = conexion.cursor()

# Crear tabla 'entidad'
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS entidad (
    id INTEGER PRIMARY KEY,
    cuit TEXT,
    razon_social TEXT
)
"""
)

# Crear tabla 'provincia'
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS provincia (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    extension_km REAL NOT NULL,
    poblacion INTEGER NOT NULL,
    dias_duracion_certificado INTEGER NOT NULL
)
"""
)

# Crear tabla 'user'
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    rol TEXT NOT NULL,
    provincia_id INTEGER,
    FOREIGN KEY (provincia_id) REFERENCES provincia(id)
)
"""
)

# Crear tabla 'espacio_obligado'
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS espacio_obligado (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    aprobado BOOLEAN NOT NULL,
    estado TEXT NOT NULL,
    cantidad_deas INTEGER,
    cardio_asistido_vencido BOOLEAN,
    cardio_asistido_desde DATE,
    cardio_asistido_vence DATE,
    sector TEXT,
    superficie_mts INTEGER,
    cantidad_pisos INTEGER,
    cantidad_personas_externas INTEGER,
    provincia_id INTEGER,
    entidad_id INTEGER,
    FOREIGN KEY (provincia_id) REFERENCES provincia(id),
    FOREIGN KEY (entidad_id) REFERENCES entidad(id)
)
"""
)

# Crear tabla 'muerte_subita'
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS muerte_subita (
    id INTEGER PRIMARY KEY,
    fecha DATE NOT NULL,
    sexo CHAR(15),
    edad INTEGER,
    fallecio BOOLEAN,
    rcp BOOLEAN,
    tiempo_rcp INTEGER,
    falta_insumos BOOLEAN,
    respondio_a_descargas BOOLEAN,
    cantidad_descargas INTEGER,
    estaba_en_sitio BOOLEAN,
    espacio_id INTEGER,
    FOREIGN KEY (espacio_id) REFERENCES espacio_obligado(id)
)
"""
)

# Crear tabla 'user_espacio'
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS user_espacio (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    espacio_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (espacio_id) REFERENCES espacio_obligado(id)
)
"""
)

# Confirmar y guardar los cambios en la base de datos
conexion.commit()

# Cerrar la conexión a la base de datos
conexion.close()
