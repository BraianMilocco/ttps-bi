import sqlite3

def conectar_db(ruta_db):
    conexion = sqlite3.connect(ruta_db)
    return conexion

def consultar_db(conexion, consulta):
    cursor = conexion.cursor()
    cursor.execute(consulta)
    resultados = cursor.fetchall()
    cursor.close()
    return resultados

# Ruta a tu archivo de base de datos SQLite
ruta_db = 'test.db'

# Conectar a la base de datos
conexion = conectar_db(ruta_db)

# Ejemplo de consulta SQL
consulta = 'SELECT * FROM deas;'

# Realizar la consulta
resultados = consultar_db(conexion, consulta)

# Imprimir resultados
for fila in resultados:
    print(fila)

# Cerrar la conexión
conexion.close()
