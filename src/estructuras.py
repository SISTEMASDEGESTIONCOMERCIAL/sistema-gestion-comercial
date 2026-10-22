"""Validaciones y utilidades compartidas."""
from datetime import datetime


def texto_no_vacio(valor, campo):
    valor = str(valor).strip()
    if not valor:
        raise ValueError(f"{campo} no puede estar vacío.")
    return valor


def entero_no_negativo(valor, campo="cantidad"):
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        raise ValueError(f"{campo} debe ser un número entero.")
    if numero < 0:
        raise ValueError(f"{campo} no puede ser negativo.")
    return numero


def dinero_no_negativo(valor, campo="precio"):
    try:
        numero = round(float(valor), 2)
    except (TypeError, ValueError):
        raise ValueError(f"{campo} debe ser numérico.")
    if numero < 0:
        raise ValueError(f"{campo} no puede ser negativo.")
    return numero


def fecha_actual():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
