"""Reportes calculados desde los archivos JSON almacenados."""
from collections import Counter
from datetime import datetime
from productos import cargar_productos
from clientes import cargar_clientes
from ventas import cargar_ventas, _lineas_de_venta


def reporte_productos():
    productos = cargar_productos()
    print("\n--- LISTADO GENERAL DE PRODUCTOS ---")
    if not productos:
        print("No hay productos registrados.")
        return
    for p in productos:
        print(f"{p['codigo']} | {p['nombre']} | {p['categoria']} | Q{float(p['precio']):.2f} | Existencias: {p['cantidad']} | Mínimo: {p['stock_minimo']} | {'Activo' if p.get('activo', True) else 'Inactivo'}")


def reporte_stock_bajo():
    productos = [p for p in cargar_productos() if p.get("activo", True) and int(p.get("cantidad", 0)) <= int(p.get("stock_minimo", 0))]
    print("\n--- PRODUCTOS EN STOCK MÍNIMO O BAJO ---")
    if not productos:
        print("No hay productos en stock mínimo o bajo.")
        return
    for p in productos:
        print(f"{p['codigo']} | {p['nombre']} | Existencias: {p['cantidad']} | Mínimo: {p['stock_minimo']}")


def reporte_ventas():
    ventas = cargar_ventas()
    print("\n--- HISTORIAL Y RESUMEN DE VENTAS ---")
    if not ventas:
        print("No hay ventas registradas.")
        return
    ingresos = sum(float(v.get("total", 0)) for v in ventas)
    print(f"Transacciones registradas: {len(ventas)}")
    print(f"Ingresos totales (IVA incluido): Q{ingresos:.2f}")
    for v in ventas:
        print(f"Venta #{v.get('numero')} | {v.get('fecha')} | {v.get('cliente', 'Venta general')} | Q{float(v.get('total', 0)):.2f}")


def reporte_producto_mas_vendido():
    contador = Counter()
    nombres = {}
    for venta in cargar_ventas():
        for linea in _lineas_de_venta(venta):
            codigo = str(linea.get("codigo_producto", linea.get("producto", "")))
            contador[codigo] += int(linea.get("cantidad", 0))
            nombres[codigo] = linea.get("producto", codigo)
    print("\n--- PRODUCTO MÁS VENDIDO ---")
    if not contador:
        print("No hay datos de ventas.")
        return
    codigo, cantidad = contador.most_common(1)[0]
    print(f"{nombres[codigo]}: {cantidad} unidad(es).")


def reporte_valor_inventario():
    productos = [p for p in cargar_productos() if p.get("activo", True)]
    valor = sum(float(p.get("precio", 0)) * int(p.get("cantidad", 0)) for p in productos)
    print(f"\nValor de venta del inventario activo disponible: Q{valor:.2f}")


def reporte_promedio_ventas():
    ventas = cargar_ventas()
    print("\n--- PROMEDIO DE VENTAS POR DÍA ---")
    if not ventas:
        print("No hay ventas registradas.")
        return
    por_dia = {}
    for v in ventas:
        fecha = str(v.get("fecha", ""))[:10]
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            continue
        por_dia[fecha] = por_dia.get(fecha, 0.0) + float(v.get("total", 0))
    if not por_dia:
        print("No hay fechas válidas para calcular el promedio.")
        return
    promedio = sum(por_dia.values()) / len(por_dia)
    print(f"Días con ventas: {len(por_dia)} | Promedio diario: Q{promedio:.2f}")


def reporte_general():
    print("\n===== REPORTE GENERAL =====")
    print(f"Productos registrados: {len(cargar_productos())}")
    print(f"Clientes registrados: {len(cargar_clientes())}")
    reporte_ventas()
    reporte_stock_bajo()
    reporte_producto_mas_vendido()
    reporte_valor_inventario()
    reporte_promedio_ventas()


def menu_reportes():
    while True:
        print("\n===== REPORTES Y ESTADÍSTICAS =====")
        print("1. Listado general de productos\n2. Productos en stock mínimo o bajo\n3. Historial e ingresos por ventas\n4. Producto más vendido\n5. Valor del inventario\n6. Promedio diario de ventas\n7. Reporte general\n0. Volver")
        opcion = input("Seleccione una opción: ").strip()
        acciones = {"1": reporte_productos, "2": reporte_stock_bajo, "3": reporte_ventas,
                    "4": reporte_producto_mas_vendido, "5": reporte_valor_inventario,
                    "6": reporte_promedio_ventas, "7": reporte_general}
        if opcion == "0": return
        accion = acciones.get(opcion)
        if accion: accion()
        else: print("Opción no válida.")
