import sqlite3


class DB:
    RUTA_DB = "db_etl.db"

    def __init__(self):
        self.conexion = None

    def conectar_db(self, ruta_db=None):
        if ruta_db is None:
            ruta_db = self.RUTA_DB
        conexion = sqlite3.connect(ruta_db)
        self.conexion = conexion
        return conexion

    def consultar_db(self, consulta):
        cursor = self.conexion.cursor()
        cursor.execute(consulta)
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

    def insertar_db(self, consulta):
        try:
            cursor = self.conexion.cursor()
            cursor.execute(consulta)
            self.conexion.commit()  # Importante para confirmar la inserción
            cursor.close()
            return True  # O algún mensaje de éxito
        except Exception as e:
            print(f"Error al insertar: {e}")
            return False  # O algún mensaje de error
        return True

    def close_db(self):
        self.conexion.close()
        self.conexion = None

    def modificar_tabla_espacios_obligados(self):
        try:
            cursor = self.conexion.cursor()
            cursor.execute(
                "ALTER TABLE espacios_obligados ADD COLUMN estado_auxiliar TIPO_DATO"
            )
            cursor.execute("UPDATE espacios_obligados SET estado_auxiliar = estado")
            self.conexion.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error al modificar la tabla: {e}")
            return False

    def modificar_tabla_agregar_fecha_nacimiento(self):
        try:
            cursor = self.conexion.cursor()
            # Agregar la columna fecha_nacimiento de tipo DATETIME
            cursor.execute("ALTER TABLE users ADD COLUMN fecha_nacimiento DATETIME")

            # Opcional: Actualizar la columna con datos, si es necesario
            # Aquí tendrás que definir cómo quieres establecer estas fechas

            self.conexion.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error al modificar la tabla: {e}")
            return False


# # # Ejemplo de consulta SQL
# db = DB()
# db.conectar_db()
# # consulta = 'SELECT * FROM deas;'

# # # Realizar la consulta
# resultados = db.consultar_db(consulta)

# # Imprimir resultados
# for fila in resultados:
#     print(fila)

# # # Cerrar la conexión
# db.conexion.close()
