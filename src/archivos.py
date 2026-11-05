"""Funciones seguras para leer y guardar archivos JSON del sistema."""
import json
import shutil
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"
DATA.mkdir(exist_ok=True)


def ruta_archivo(nombre):
    """Devuelve una ruta dentro de data; evita rutas arbitrarias."""
    if Path(nombre).name != nombre:
        raise ValueError("El nombre debe ser un archivo, no una ruta.")
    return DATA / nombre


def _respaldar_dañado(ruta):
    """Copia el archivo dañado antes de que un guardado posterior lo sobrescriba."""
    destino = ruta.with_name(f"{ruta.stem}.danado-{datetime.now():%Y%m%d-%H%M%S}.bak")
    try:
        shutil.copy2(ruta, destino)
        return destino
    except OSError:
        return None


def leer_json(nombre, predeterminado):
    ruta = ruta_archivo(nombre)
    if not ruta.exists():
        return predeterminado.copy() if isinstance(predeterminado, (dict, list)) else predeterminado
    try:
        with ruta.open("r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        return datos
    except (OSError, json.JSONDecodeError):
        respaldo = _respaldar_dañado(ruta)
        print(f"Aviso: no se pudo leer {nombre}. Se usará una estructura vacía.")
        if respaldo:
            print(f"Se conservó una copia del archivo dañado en data/{respaldo.name}.")
        return predeterminado.copy() if isinstance(predeterminado, (dict, list)) else predeterminado


def guardar_json(nombre, datos):
    ruta = ruta_archivo(nombre)
    temporal = ruta.with_suffix(ruta.suffix + ".tmp")
    with temporal.open("w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)
    temporal.replace(ruta)
