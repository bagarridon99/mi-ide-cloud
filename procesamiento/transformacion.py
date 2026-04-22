import hashlib
import pandas as pd


def resumen_supervivencia(almacen_datos: dict) -> None:
    """Crea tabla resumen con conteo de pasajeros que sobrevivieron o no en TITANIC."""
    df = almacen_datos["TITANIC"]
    resumen = (
        df.groupby("sobrevivio")
        .size()
        .reset_index(name="cantidad")
    )
    resumen["estado"] = resumen["sobrevivio"].map({0: "No sobrevivió", 1: "Sobrevivió"})
    resumen = resumen[["estado", "cantidad"]]
    almacen_datos["TITANIC_supervivencia"] = resumen
    print(f"  [OK] TITANIC_supervivencia creado ({len(resumen)} filas)")


def agregar_unique_key(almacen_datos: dict) -> None:
    """Agrega columna UniqueKey a Libreria usando hash MD5 de titulo+autor+año."""
    df = almacen_datos["Libreria"].copy()
    df["UniqueKey"] = df.apply(
        lambda row: hashlib.md5(
            f"{row['titulo']}|{row['autor']}|{row['año_publicacion']}".encode()
        ).hexdigest()[:12],
        axis=1,
    )
    almacen_datos["Libreria"] = df
    print(f"  [OK] UniqueKey agregada a Libreria ({len(df)} registros)")


def promedio_temperatura(almacen_datos: dict) -> None:
    """Crea tabla resumen con el promedio de temperatura por ciudad en Clima."""
    df = almacen_datos["Clima"]
    resumen = (
        df.groupby("ciudad")["temperatura_C"]
        .mean()
        .round(2)
        .reset_index()
        .rename(columns={"temperatura_C": "temperatura_promedio_C"})
    )
    almacen_datos["Clima_promedio"] = resumen
    print(f"  [OK] Clima_promedio creado ({len(resumen)} ciudades)")


def filtrar_menores_titanic(almacen_datos: dict) -> None:
    """Elimina de TITANIC todos los pasajeros menores de 10 años."""
    df = almacen_datos["TITANIC"]
    antes = len(df)
    df_filtrado = df[df["edad_anios"].isna() | (df["edad_anios"] >= 10)].reset_index(drop=True)
    almacen_datos["TITANIC"] = df_filtrado
    eliminados = antes - len(df_filtrado)
    print(f"  [OK] TITANIC filtrado: {eliminados} menores de 10 años eliminados "
          f"({len(df_filtrado)} registros restantes)")
