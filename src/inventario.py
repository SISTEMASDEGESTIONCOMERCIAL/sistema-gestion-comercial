"""Consultas, entradas y movimientos de inventario."""
from archivos import leer_json, guardar_json
from estructuras import entero_no_negativo, fecha_actual
from productos import cargar_productos, guardar_productos

ARCHIVO_MOVIMIENTOS = "movimientos_inventario.json"


def cargar_movimientos():
    datos = leer_json(ARCHIVO_MOVIMIENTOS, [])
    return datos if isinstance(datos, list) else []


def registrar_movimiento(codigo, tipo, cantidad, descripcion=""):
    movimientos = cargar_movimientos()
    movimientos.append({"fecha": fecha_actual(), "codigo_producto": str(codigo),
                        "tipo": tipo, "cantidad": int(cantidad), "descripcion": descripcion})
    guardar_json(ARCHIVO_MOVIMIENTOS, movimientos)


def consultar_inventario():
    productos = [p for p in cargar_productos() if p.get("activo", True)]
    if not productos:
        print("No hay productos activos registrados.")
        return
    print("\n--- INVENTARIO ---")
    for p in productos:
        bajo = int(p.get("cantidad", 0)) <= int(p.get("stock_minimo", 0))
        estado = "STOCK BAJO" if bajo else "Disponible"
        print(f"{p['codigo']} | {p['nombre']} | Existencias: {p['cantidad']} | Mínimo: {p['stock_minimo']} | {estado}")


def registrar_entrada():
    productos = cargar_productos()
    codigo = input("Código del producto: ").strip()
    producto = next((p for p in productos if str(p.get("codigo")) == codigo and p.get("activo", True)), None)
    if not producto:
        print("Producto activo no encontrado.")
        return
    try:
        cantidad = entero_no_negativo(input("Cantidad que ingresa: "), "Cantidad")
        if cantidad == 0:
            print("La cantidad debe ser mayor que cero.")
            return
        descripcion = input("Descripción (opcional): ").strip()
    except ValueError as error:
        print(f"Error: {error}")
        return
    producto["cantidad"] = int(producto["cantidad"]) + cantidad
    guardar_productos(productos)
    try:
        registrar_movimiento(codigo, "ENTRADA", cantidad, descripcion)
    except OSError as error:
        print(f"Las existencias se actualizaron, pero no se guardó el historial: {error}")
        return
    print(f"Entrada registrada. Existencias actuales: {producto['cantidad']}.")


def historial_movimientos():
    movimientos = cargar_movimientos()
    if not movimientos:
        print("No hay movimientos de inventario registrados.")
        return
    print("\n--- HISTORIAL DE MOVIMIENTOS ---")
    for m in movimientos:
        print(f"{m['fecha']} | {m['codigo_producto']} | {m['tipo']} | {m['cantidad']} | {m.get('descripcion', '')}")


def menu_inventario():
    while True:
        print("\n===== GESTIÓN DE INVENTARIO =====")
        print("1. Consultar existencias\n2. Registrar entrada\n3. Historial de movimientos\n0. Volver")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1": consultar_inventario()
        elif opcion == "2": registrar_entrada()
        elif opcion == "3": historial_movimientos()
        elif opcion == "0": return
        else: print("Opción no válida.")
