from auxiliares import get_random_index
from localidades import provincias_localidades_en_db
from db import DB

db_original = DB()
db_original.conectar_db("test.db")

db_datawarehouse = DB()
db_datawarehouse.conectar_db("db_etl_test.db")

def data_or_null(data):
    if data:
        return f"'{data}'"
    return "NULL"

def get_entidades(offset=0, limit=10000):
    consulta = (
        f"SELECT id, razon_social, cuit FROM entidades LIMIT {limit} OFFSET {offset}"
    )
    entidades = db_original.consultar_db(consulta)
    return entidades

def get_sedes_espacios(offset=0, limit=50000):
    consulta = (
        "SELECT e.id, s.sector, s.tipo, s.superficie, s.cantidad_pisos, s.cantidad_personas_externas, "
        "s.cantidad_personas_estables, e.aprobado, e.estado_auxiliar, e.cardio_asistido_desde, e.cardio_asistido_vence, "
        "e.ddjj_personal_capacitado, e.ddjj_senaletica_adecuada, e.ddjj_cantidad_deas FROM sedes as s, espacios_obligados as e "
        f"WHERE e.sede_id = s.id LIMIT {limit} OFFSET {offset}"
    )
    sedes_espacios = db_original.consultar_db(consulta)
    return sedes_espacios

def get_representantes(offset=0, limit=10000):
    consulta = (
        f"SELECT id, rol, fecha_nacimiento FROM users LIMIT {limit} OFFSET {offset}"
    )
    representantes = db_original.consultar_db(consulta)
    return representantes

def get_muertes_subitas(offset=0, limit=10000):
    consulta = (
        f"SELECT id, fecha, sexo, edad, fallecio, rcp, tiempo_rcp FROM muertes_subitas LIMIT {limit} OFFSET {offset}"
    )
    muertes_subitas = db_original.consultar_db(consulta)
    return muertes_subitas

def get_inconvenientes(offset=0, limit=10000):
    consulta = (
        f"SELECT id, fecha, falta_insumos, estaba_en_sitio, respondio_con_descargas_electricas, cantidad_de_descargas FROM incovenientes LIMIT {limit} OFFSET {offset}"
    )
    inconvenientes = db_original.consultar_db(consulta)
    return inconvenientes

def get_hechos_espacios(offset=0, limit=10000):
    try:
        consulta = (
        "SELECT  espacios_obligados.id, sedes.entidad_id, espacio_user.user_id, espacio_user.valida, espacio_user.pendiente, "
        "espacio_user.fecha_creacion, sedes.localidad_id "
        "FROM  espacios_obligados INNER JOIN sedes  ON espacios_obligados.sede_id = sedes.id "
        "INNER  JOIN espacio_user ON espacios_obligados.id = espacio_user.espacio_id "
        f"LIMIT {limit} OFFSET {offset}"
        )
        hechos_espacios = db_original.consultar_db(consulta)
    except Exception as e:
        print(f"Error al consultar: {e}")
        return False
    return hechos_espacios

def get_hechos_muertes_subitas(offset=0, limit=10000):
    try:
        consulta = (
            "SELECT espacios_obligados.id, muertes_subitas.id, incovenientes.id, sedes.localidad_id "
            "FROM espacios_obligados "
            "INNER JOIN sedes ON espacios_obligados.sede_id = sedes.id "
            "INNER JOIN muertes_subitas ON muertes_subitas.espacio_obligado_id = espacios_obligados.id "
            "LEFT JOIN incovenientes ON muertes_subitas.id = incovenientes.muerte_subita_id "  # Asumiendo que la relación se basa en muerte_subita_id
            f"LIMIT {limit} OFFSET {offset}"
        )
        hechos_muertes_subitas = db_original.consultar_db(consulta)
    except Exception as e:
        print(f"Error al consultar: {e}")
        return False
    return hechos_muertes_subitas

def mover_entidades_a_warehouse():
    offset = 0
    limit = 10000
    while True:
        base_sql = "INSERT INTO entidades (id, razon_social, cuit) VALUES "
        entidades = get_entidades(offset, limit)
        if not entidades:
            break
        for entidad in entidades:
            base_sql += f"({entidad[0]}, {data_or_null(entidad[1])}, {data_or_null(entidad[2])}), "

        base_sql = base_sql[:-2] + ";"
        offset += limit
        db_datawarehouse.insertar_db(base_sql)

def mover_sedes_espacios_a_warehouse():
    offset = 0
    limit = 50000
    while True:
        base_sql = (
            "INSERT INTO sedes_espacios "
            "(id, sector, tipo, superficie, cantidad_pisos, cantidad_personas_externas, "
            "cantidad_personas_estables, aprobado, estado, cardio_asistido_desde, cardio_asistido_vence, "
            "personal_capacitado, senaletica_adecuada, deas) VALUES """
        )
        sedes_espacios = get_sedes_espacios(offset, limit)
        if not sedes_espacios:
            break
        for sede_espacio in sedes_espacios:
            base_sql += (
                f"({sede_espacio[0]}, {data_or_null(sede_espacio[1])}, {data_or_null(sede_espacio[2])}, "
                f"{sede_espacio[3]}, {sede_espacio[4]}, {sede_espacio[5]}, {sede_espacio[6]}, "
                f"{sede_espacio[7]}, '{sede_espacio[8]}', {data_or_null(sede_espacio[9])}, {data_or_null(sede_espacio[10])}, "
                f"{sede_espacio[11]}, {sede_espacio[12]}, {sede_espacio[13]}), "
            )
        base_sql = base_sql[:-2] + ";"
        offset += limit
        
        db_datawarehouse.insertar_db(base_sql)

def mover_representantes_a_warehouse():
    offset = 0
    limit = 10000
    while True:
        base_sql = "INSERT INTO representantes (id, rol, fecha_nacimiento) VALUES "
        representantes = get_representantes(offset, limit)
        if not representantes:
            break
        for representante in representantes:
            base_sql += f"({representante[0]}, {data_or_null(representante[1])}, {data_or_null(representante[2])}), "

        base_sql = base_sql[:-2] + ";"
        offset += limit
        db_datawarehouse.insertar_db(base_sql)

def mover_muertes_subitas_a_warehouse():
    offset = 0
    limit = 10000
    while True:
        base_sql = "INSERT INTO muertes_subitas (id, fecha, sexo, edad, fallecio, rcp, tiempo_rcp) VALUES "
        muertes_subitas = get_muertes_subitas(offset, limit)
        if not muertes_subitas:
            break
        for muerte_subita in muertes_subitas:
            base_sql += f"({muerte_subita[0]}, {data_or_null(muerte_subita[1])}, {data_or_null(muerte_subita[2])}, {muerte_subita[3]}, {muerte_subita[4]}, {muerte_subita[5]}, {muerte_subita[6]}), "

        base_sql = base_sql[:-2] + ";"
        offset += limit
        db_datawarehouse.insertar_db(base_sql)

def mover_inconvenientes_a_warehouse():
    offset = 0
    limit = 10000
    while True:
        base_sql = "INSERT INTO inconvenientes (id, fecha, falta_insumos, en_sitio, respondido_a_descargas, cantidad_descargas) VALUES "
        inconvenientes = get_inconvenientes(offset, limit)
        if not inconvenientes:
            break
        for inconveniente in inconvenientes:
            base_sql += f"({inconveniente[0]}, {data_or_null(inconveniente[1])}, {inconveniente[2]}, {inconveniente[3]}, {inconveniente[4]}, {inconveniente[5]}), "

        base_sql = base_sql[:-2] + ";"
        offset += limit
        db_datawarehouse.insertar_db(base_sql)

def llenar_tabla_hechos_warehouse():
    offset = 0
    limit = 50000
    _id = 1
    while True:
        base_sql = (
            "INSERT INTO hechos_espacios (id, id_sedes_espacios, id_entidades, "
            "id_representantes, valida, pendiente, "
            "fecha_creacion, id_localidades) VALUES "
        )
        hechos_espacios = get_hechos_espacios(offset, limit)
        if not hechos_espacios:
            break
        for hecho_espacio in hechos_espacios:
            base_sql += (
                f"({_id}, {hecho_espacio[0]}, {hecho_espacio[1]}, {hecho_espacio[2]}, {hecho_espacio[3]}, {hecho_espacio[4]}, "
                f"{data_or_null(hecho_espacio[5])}, {hecho_espacio[6]}), "
            )
            _id += 1
        base_sql = base_sql[:-2] + ";"
        offset += limit
        db_datawarehouse.insertar_db(base_sql)

def llenar_tabla_hechos_muertes_subitas_warehouse():
    offset = 0
    limit = 50000
    _id = 1
    while True:
        base_sql = (
            "INSERT INTO hechos_muertes_subitas (id, id_sedes_espacios, id_muertes_subitas, id_inconvenientes, id_localidades) VALUES "
        )
        hechos_muertes_subitas = get_hechos_muertes_subitas(offset, limit)
        if not hechos_muertes_subitas:
            break
        for hecho_muerte_subita in hechos_muertes_subitas:
            inconveniente = hecho_muerte_subita[2] if hecho_muerte_subita[2] else "NULL"
            base_sql += (
                f"({_id}, {hecho_muerte_subita[0]}, {hecho_muerte_subita[1]}, {inconveniente}, {hecho_muerte_subita[3]}), "
            )
            _id += 1
        base_sql = base_sql[:-2] + ";"
        offset += limit
        funco = db_datawarehouse.insertar_db(base_sql)
        if not funco:
            print(f"Error al insertar: {offset}")
            break

# mover_entidades_a_warehouse()
# mover_sedes_espacios_a_warehouse()
# mover_representantes_a_warehouse()
# mover_muertes_subitas_a_warehouse()
# mover_inconvenientes_a_warehouse()

# TABLAS DE HECHOS
# llenar_tabla_hechos_warehouse()
llenar_tabla_hechos_muertes_subitas_warehouse()
