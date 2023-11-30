import string

from db import DB
from auxiliares import (
    sectores,
    tipos,
    latitudes,
    longitudes,
    id_generator,
    get_random_index,
    get_random_from_range,
    estados,
    generar_fecha_aleatoria,
    fechas_estado_vencido,
)

db = DB()
db.conectar_db()

INSERT_AT = 5000


def get_ids_entidades():
    consulta = "SELECT id FROM entidades;"
    resultados = db.consultar_db(consulta)
    return [resultado[0] for resultado in resultados]


def get_entidad(id):
    base_id = 100

    return {
        "id": base_id + id,
        "cuit": id_generator(25, string.digits),
        "razon_social": id_generator(30),
    }


def get_sede(id, entidad_id):
    base_id = 20
    _id = base_id + id
    sector = get_random_index(sectores)
    tipo = get_random_index(tipos[sector])
    return {
        "id": _id,
        "nombre": id_generator(25),
        "numero": _id,
        "sector": sector,
        "tipo": tipo,
        "latitud": latitudes(),
        "longitud": longitudes(),
        "superficie": get_random_from_range(100, 10000),
        "cantidad_pisos": get_random_from_range(0, 20),
        "cantidad_personas_externas": get_random_from_range(0, 1000),
        "cantidad_personas_estables": get_random_from_range(0, 1000),
        "provincia_id": get_random_from_range(1, 24),
        "entidad_id": entidad_id,
    }


def get_espacio(id, sede_id):
    id_base = 5020
    _id = id_base + id
    estado_auxiliar = get_random_index(estados)
    desde, hasta = fechas_estado_vencido(estado_auxiliar)
    return {
        "id": _id,
        "nombre": id_generator(25),
        "aprobado": get_random_index(
            [True, False, True, True, True, True, True, True, True]
        ),
        "estado": "En proceso de ser Cardio-Asistido",
        "estado_auxiliar": estado_auxiliar,
        "sede_id": sede_id,
        "cardio_asistido_desde": desde,
        "cardio_asistido_vence": hasta,
        "cardio_asistido_vencido": (
            estado_auxiliar == "Cardio-Asistido Certificado Vencido"
        ),
        "ddjj_personal_capacitado": True
        if estado_auxiliar != "En proceso de ser Cardio-Asistido"
        else get_random_index([True, False]),
        "ddjj_senaletica_adecuada": True
        if estado_auxiliar != "En proceso de ser Cardio-Asistido"
        else get_random_index([True, False]),
        "ddjj_cantidad_deas": get_random_from_range(0, 10)
        if estado_auxiliar != "En proceso de ser Cardio-Asistido"
        else get_random_from_range(1, 300),
    }


# cantidad_creada = 0
# entidades = []

# # Crear Entidades
# for i in range(100000):
#     entidades.append(get_entidad(i))
#     cantidad_creada += 1
#     if cantidad_creada ==  INSERT_AT:
#         consulta = 'INSERT INTO entidades (id, cuit, razon_social) VALUES '
#         for entidad in entidades:
#             consulta += '({}, "{}", "{}"),'.format(entidad["id"], entidad["cuit"], entidad["razon_social"])
#         consulta = consulta[:-1] + ';'
#         resultad = db.insertar_db(consulta)
#         if not resultad:
#             break
#         cantidad_creada = 0
#         entidades = []

# sedes = []
# sedes_creadas = 0
# entidades_ids = get_ids_entidades()

# for i in range(1000000):
#     sedes.append(get_sede(i, get_random_index(entidades_ids)))
#     sedes_creadas += 1
#     if sedes_creadas == INSERT_AT:
#         consulta = "INSERT INTO sedes (id, nombre, numero, sector, tipo, latitud, longitud, superficie, cantidad_pisos, cantidad_personas_externas, cantidad_personas_estables, provincia_id, entidad_id) VALUES "
#         for sede in sedes:
#             consulta += (
#                 '({}, "{}", {}, "{}", "{}", {}, {}, {}, {}, {}, {}, {}, {}),'.format(
#                     sede["id"],
#                     sede["nombre"],
#                     sede["numero"],
#                     sede["sector"],
#                     sede["tipo"],
#                     sede["latitud"],
#                     sede["longitud"],
#                     sede["superficie"],
#                     sede["cantidad_pisos"],
#                     sede["cantidad_personas_externas"],
#                     sede["cantidad_personas_estables"],
#                     sede["provincia_id"],
#                     sede["entidad_id"],
#                 )
#             )
#         consulta = consulta[:-1] + ";"
#         resultad = db.insertar_db(consulta)
#         if not resultad:
#             break
#         sedes_creadas = 0
#         sedes = []

# Crear Espacio
espacios = []
espacios_creados = 0
id_sede_start = 5020
while id_sede_start < 1000020:
    espacios.append(get_espacio(espacios_creados, id_sede_start))
    espacios_creados += 1
    id_sede_start += 1
    if espacios_creados == INSERT_AT:
        consulta = "INSERT INTO espacios_obligados (id, nombre, aprobado, estado, estado_auxiliar, sede_id, cardio_asistido_desde, cardio_asistido_vence, cardio_asistido_vencido, ddjj_personal_capacitado, ddjj_senaletica_adecuada, ddjj_cantidad_deas) VALUES "
        for espacio in espacios:
            consulta += (
                '({}, "{}", {}, "{}", "{}", {}, "{}", "{}", {}, {}, {}, {}),'.format(
                    espacio["id"],
                    espacio["nombre"],
                    espacio["aprobado"],
                    espacio["estado"],
                    espacio["estado_auxiliar"],
                    espacio["sede_id"],
                    espacio["cardio_asistido_desde"],
                    espacio["cardio_asistido_vence"],
                    espacio["cardio_asistido_vencido"],
                    espacio["ddjj_personal_capacitado"],
                    espacio["ddjj_senaletica_adecuada"],
                    espacio["ddjj_cantidad_deas"],
                )
            )
        consulta = consulta[:-1] + ";"
        resultad = db.insertar_db(consulta)
        if not resultad:
            break
        espacios = []
if espacios:
    consulta = "INSERT INTO espacios_obligados (id, nombre, aprobado, estado, estado_auxiliar, sede_id, cardio_asistido_desde, cardio_asistido_vence, cardio_asistido_vencido, ddjj_personal_capacitado, ddjj_senaletica_adecuada, ddjj_cantidad_deas) VALUES "
    for espacio in espacios:
        consulta += (
            '({}, "{}", {}, "{}", "{}", {}, "{}", "{}", {}, {}, {}, {}),'.format(
                espacio["id"],
                espacio["nombre"],
                espacio["aprobado"],
                espacio["estado"],
                espacio["estado_auxiliar"],
                espacio["sede_id"],
                espacio["cardio_asistido_desde"],
                espacio["cardio_asistido_vence"],
                espacio["cardio_asistido_vencido"],
                espacio["ddjj_personal_capacitado"],
                espacio["ddjj_senaletica_adecuada"],
                espacio["ddjj_cantidad_deas"],
            )
        )
    consulta = consulta[:-1] + ";"
    resultad = db.insertar_db(consulta)
    espacios_creados = 0
    espacios = []
