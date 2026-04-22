import os
import numpy as np
import pandas as pd
import seaborn as sns

from procesamiento.transformacion import (
    resumen_supervivencia,
    agregar_unique_key,
    promedio_temperatura,
    filtrar_menores_titanic,
)

RAW_DIR = os.path.join(os.path.dirname(__file__), "data", "raw")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "data", "processed")

almacen_datos: dict = {}


# ---------------------------------------------------------------------------
# INGESTA
# ---------------------------------------------------------------------------

def _generar_libreria() -> pd.DataFrame:
    # titulo, autor, año_publicacion, genero_literario, editorial, num_paginas, idioma, pais_origen, calificacion_goodreads
    libros = [
        ("Cien años de soledad",              "Gabriel García Márquez",   1967, "Novela",          "Sudamericana",        432,  "Español",  "Colombia",  4.1),
        ("El Quijote",                         "Miguel de Cervantes",      1605, "Novela",          "Francisco de Robles", 1345, "Español",  "España",    3.9),
        ("1984",                               "George Orwell",            1949, "Distopía",        "Secker & Warburg",    328,  "Inglés",   "Reino Unido", 4.7),
        ("El Principito",                      "Antoine de Saint-Exupéry", 1943, "Fábula",          "Reynal & Hitchcock",  96,   "Francés",  "Francia",   4.3),
        ("Rayuela",                            "Julio Cortázar",           1963, "Novela",          "Sudamericana",        635,  "Español",  "Argentina", 4.1),
        ("La casa de los espíritus",           "Isabel Allende",           1982, "Realismo mágico", "Plaza & Janés",       434,  "Español",  "Chile",     4.1),
        ("Ficciones",                          "Jorge Luis Borges",        1944, "Cuentos",         "Sur",                 224,  "Español",  "Argentina", 4.5),
        ("Pedro Páramo",                       "Juan Rulfo",               1955, "Novela",          "FCE",                 124,  "Español",  "México",    4.0),
        ("Brave New World",                    "Aldous Huxley",            1932, "Distopía",        "Chatto & Windus",     311,  "Inglés",   "Reino Unido", 4.1),
        ("Los detectives salvajes",            "Roberto Bolaño",           1998, "Novela",          "Anagrama",            609,  "Español",  "Chile",     4.0),
        ("El amor en los tiempos del cólera",  "Gabriel García Márquez",   1985, "Novela",          "Oveja Negra",         468,  "Español",  "Colombia",  4.3),
        ("Fahrenheit 451",                     "Ray Bradbury",             1953, "Distopía",        "Ballantine Books",    158,  "Inglés",   "EE.UU.",    4.6),
        ("La sombra del viento",               "Carlos Ruiz Zafón",        2001, "Misterio",        "Planeta",             544,  "Español",  "España",    4.2),
        ("El túnel",                           "Ernesto Sabato",           1948, "Novela",          "Sur",                 124,  "Español",  "Argentina", 3.9),
        ("Sapiens",                            "Yuval Noah Harari",        2011, "No ficción",      "Kinneret",            443,  "Hebreo",   "Israel",    4.4),
    ]
    return pd.DataFrame(libros, columns=[
        "titulo", "autor", "año_publicacion", "genero_literario",
        "editorial", "num_paginas", "idioma", "pais_origen", "calificacion_goodreads",
    ])


def _generar_clima() -> pd.DataFrame:
    np.random.seed(42)
    ciudades = ["Santiago", "Valparaíso", "Concepción", "Antofagasta", "Temuco"]
    condiciones = ["Soleado", "Parcialmente nublado", "Nublado", "Lluvioso"]
    base = {
        "Santiago":    {"temp": 14.5, "viento": 18, "lluvia_prob": 0.10},
        "Valparaíso":  {"temp": 15.2, "viento": 25, "lluvia_prob": 0.15},
        "Concepción":  {"temp": 12.8, "viento": 20, "lluvia_prob": 0.35},
        "Antofagasta": {"temp": 17.6, "viento": 15, "lluvia_prob": 0.02},
        "Temuco":      {"temp": 10.3, "viento": 22, "lluvia_prob": 0.45},
    }
    registros = []
    for ciudad in ciudades:
        b = base[ciudad]
        for i in range(30):
            fecha = pd.Timestamp("2024-01-01") + pd.Timedelta(days=i)
            temp    = round(b["temp"]   + np.random.uniform(-5, 5), 1)
            humedad = round(np.random.uniform(40, 90), 1)
            viento  = round(b["viento"] + np.random.uniform(-8, 8), 1)
            lluvia  = round(np.random.uniform(0, 20) if np.random.rand() < b["lluvia_prob"] else 0.0, 1)
            if lluvia > 5:
                cond = "Lluvioso"
            elif humedad > 75:
                cond = "Nublado"
            elif humedad > 55:
                cond = "Parcialmente nublado"
            else:
                cond = "Soleado"
            registros.append({
                "fecha":              fecha.date(),
                "ciudad":             ciudad,
                "temperatura_C":      temp,
                "humedad_pct":        humedad,
                "viento_kmh":         max(0.0, viento),
                "precipitacion_mm":   lluvia,
                "condicion_clima":    cond,
            })
    return pd.DataFrame(registros)


def ingestar_datos():
    print("=" * 60)
    print("FASE 1 — INGESTA DE DATOS")
    print("=" * 60)

    # TITANIC
    df_titanic = sns.load_dataset("titanic").rename(columns={
        "survived":    "sobrevivio",
        "pclass":      "clase_pasajero",
        "sex":         "sexo",
        "age":         "edad_anios",
        "sibsp":       "hermanos_conyuges_abordo",
        "parch":       "padres_hijos_abordo",
        "fare":        "tarifa_usd",
        "embarked":    "codigo_puerto",
        "class":       "clase_nombre",
        "who":         "tipo_pasajero",
        "adult_male":  "es_adulto_masculino",
        "deck":        "cubierta",
        "embark_town": "ciudad_embarque",
        "alive":       "estado_supervivencia",
        "alone":       "viajaba_solo",
    })
    almacen_datos["TITANIC"] = df_titanic
    df_titanic.to_csv(os.path.join(RAW_DIR, "titanic.csv"), index=False)
    print(f"  [OK] TITANIC cargado       → {df_titanic.shape[0]} filas x {df_titanic.shape[1]} columnas")

    # Libreria
    df_libreria = _generar_libreria()
    almacen_datos["Libreria"] = df_libreria
    df_libreria.to_csv(os.path.join(RAW_DIR, "libreria.csv"), index=False)
    print(f"  [OK] Libreria generada     → {df_libreria.shape[0]} filas x {df_libreria.shape[1]} columnas")

    # Clima
    df_clima = _generar_clima()
    almacen_datos["Clima"] = df_clima
    df_clima.to_csv(os.path.join(RAW_DIR, "clima.csv"), index=False)
    print(f"  [OK] Clima generado        → {df_clima.shape[0]} filas x {df_clima.shape[1]} columnas")


# ---------------------------------------------------------------------------
# TRANSFORMACIONES
# ---------------------------------------------------------------------------

def transformar_datos():
    print()
    print("=" * 60)
    print("FASE 2 — TRANSFORMACIONES")
    print("=" * 60)
    resumen_supervivencia(almacen_datos)
    agregar_unique_key(almacen_datos)
    promedio_temperatura(almacen_datos)
    filtrar_menores_titanic(almacen_datos)


# ---------------------------------------------------------------------------
# EXPORTAR DATOS PROCESADOS
# ---------------------------------------------------------------------------

def exportar_procesados():
    print()
    print("=" * 60)
    print("FASE 3 — EXPORTAR A data/processed/")
    print("=" * 60)
    for nombre, df in almacen_datos.items():
        ruta = os.path.join(PROCESSED_DIR, f"{nombre.lower()}.csv")
        df.to_csv(ruta, index=False)
        print(f"  [OK] {nombre} → {ruta}")


# ---------------------------------------------------------------------------
# RESUMEN FINAL
# ---------------------------------------------------------------------------

def mostrar_resumen():
    print()
    print("=" * 60)
    print("RESUMEN DE almacen_datos")
    print("=" * 60)
    for nombre, df in almacen_datos.items():
        print(f"\n  [{nombre}]  {df.shape[0]} filas x {df.shape[1]} columnas")
        print(f"  Columnas: {list(df.columns)}")
        print(df.head(3).to_string(index=False))
        print()


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    ingestar_datos()
    transformar_datos()
    exportar_procesados()
    mostrar_resumen()
