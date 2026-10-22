"""Registro de ventas, IVA y actualización de existencias."""
from archivos import leer_json, guardar_json
from estructuras import fecha_actual
from productos import cargar_productos, guardar_productos
from clientes import buscar_cliente
from inventario import registrar_movimiento

ARCHIVO = "ventas.json"
IVA_PORCENTAJE = 0.12


def cargar_ventas():
    datos = leer_json(ARCHIVO, [])
    return datos if isinstance(datos, list) else []


def guardar_ventas(ventas):
    guardar_json(ARCHIVO, ventas)


def registrar_venta():
    productos = cargar_productos()
    disponibles = [p for p in productos if p.get("activo", True) and int(p.get("cantidad", 0)) > 0]
    if not disponibles:
        print("No hay productos activos con existencias.")
        return
    print("\n--- PRODUCTOS DISPONIBLES ---")
    for p in disponibles:
        print(f"{p['codigo']} | {p['nombre']} | Q{float(p['precio']):.2f} | Existencias: {p['cantidad']}")
    carrito = {}
    por_codigo = {str(p["codigo"]): p for p in disponibles}
    while True:
        codigo = input("Código del producto (Enter para terminar): ").strip()
        if not codigo:
            break
        producto = por_codigo.get(codigo)
        if not producto:
            print("Producto no encontrado o sin existencias.")
            continue
        try:
            cantidad = int(input("Cantidad a vender: "))
            if cantidad <= 0:
                print("La cantidad debe ser mayor que cero.")
                continue
            agregada = carrito.get(codigo, {}).get("cantidad", 0)
            restante = int(producto["cantidad"]) - agregada
            if cantidad > restante:
                print(f"Existencias insuficientes. Disponibles para agregar: {restante}.")
                continue
        except ValueError:
            print("Ingrese una cantidad entera válida.")
            continue
        if codigo in carrito:
            carrito[codigo]["cantidad"] += cantidad
        else:
            carrito[codigo] = {"producto": producto, "cantidad": cantidad}
        print("Producto agregado.")
    if not carrito:
        print("Venta cancelada: no se seleccionaron productos.")
        return
    codigo_cliente = input("Código del cliente (Enter para venta general): ").strip()
    cliente = buscar_cliente(codigo_cliente) if codigo_cliente else None
    if codigo_cliente and not cliente:
        print("Cliente no encontrado. La venta no se registró.")
        return

    lineas = []
    for item in carrito.values():
        p, cantidad = item["producto"], item["cantidad"]
        subtotal = round(float(p["precio"]) * cantidad, 2)
        lineas.append({"codigo_producto": str(p["codigo"]), "producto": p["nombre"],
                       "cantidad": cantidad, "precio_unitario": float(p["precio"]),
                       "subtotal": subtotal})
    subtotal_general = round(sum(x["subtotal"] for x in lineas), 2)
    iva_general = round(subtotal_general * IVA_PORCENTAJE, 2)
    total_general = round(subtotal_general + iva_general, 2)
    # Asignar el IVA de las líneas, ajustando la última por redondeo.
    iva_asignado = 0.0
    for i, linea in enumerate(lineas):
        iva = round(iva_general - iva_asignado, 2) if i == len(lineas) - 1 else round(linea["subtotal"] * IVA_PORCENTAJE, 2)
        linea["iva"] = iva
        linea["total"] = round(linea["subtotal"] + iva, 2)
        iva_asignado = round(iva_asignado + iva, 2)

    ventas_previas = cargar_ventas()
    numero = max((int(v.get("numero", 0)) for v in ventas_previas), default=0) + 1
    fecha = fecha_actual()
    codigo_cliente_guardado = cliente["codigo"] if cliente else ""
    nombre_cliente = cliente["nombre"] if cliente else "Venta general"
    registro = {"numero": numero, "fecha": fecha, "codigo_cliente": codigo_cliente_guardado,
                "cliente": nombre_cliente, "subtotal": subtotal_general, "iva": iva_general,
                "total": total_general, "productos": lineas}
    # Guardar primero la venta; si falla, no se descuentan existencias.
    try:
        guardar_ventas(ventas_previas + [registro])
    except (OSError, TypeError, ValueError) as error:
        print(f"No se pudo guardar la venta: {error}")
        return
    for linea in lineas:
        producto = por_codigo[linea["codigo_producto"]]
        producto["cantidad"] = int(producto["cantidad"]) - linea["cantidad"]
    try:
        guardar_productos(productos)
        for linea in lineas:
            registrar_movimiento(linea["codigo_producto"], "SALIDA", linea["cantidad"], f"Venta #{numero}")
    except (OSError, TypeError, ValueError) as error:
        print(f"Advertencia: la venta quedó guardada, pero debe revisar el inventario: {error}")
        return

    print("\n===== VENTA REGISTRADA =====")
    print(f"Venta #{numero} | {fecha} | Cliente: {nombre_cliente}")
    for linea in lineas:
        print(f"{linea['producto']} x{linea['cantidad']} | Subtotal Q{linea['subtotal']:.2f} | IVA Q{linea['iva']:.2f} | Total Q{linea['total']:.2f}")
    print(f"Subtotal: Q{subtotal_general:.2f}")
    print(f"IVA (12%): Q{iva_general:.2f}")
    print(f"TOTAL: Q{total_general:.2f}")


def _lineas_de_venta(venta):
    """Compatibilidad con ventas antiguas (un producto por registro)."""
    if isinstance(venta.get("productos"), list):
        return venta["productos"]
    return [{"codigo_producto": venta.get("codigo_producto", ""),
             "producto": venta.get("producto", "Producto antiguo"),
             "cantidad": int(venta.get("cantidad", 0)),
             "precio_unitario": float(venta.get("precio_unitario", 0)),
             "subtotal": float(venta.get("subtotal", venta.get("total", 0))),
             "iva": float(venta.get("iva", 0)),
             "total": float(venta.get("total", 0))}]


def listar_ventas():
    ventas = cargar_ventas()
    if not ventas:
        print("Todavía no hay ventas registradas.")
        return
    print("\n--- HISTORIAL DE VENTAS ---")
    for v in ventas:
        print(f"Venta #{v.get('numero')} | {v.get('fecha')} | Cliente: {v.get('cliente', 'Venta general')} | Total: Q{float(v.get('total', 0)):.2f}")
        for p in _lineas_de_venta(v):
            print(f"   - {p.get('producto')} x{p.get('cantidad')} | Q{float(p.get('total', 0)):.2f}")


def menu_ventas():
    while True:
        print("\n===== GESTIÓN DE VENTAS =====\n1. Registrar venta\n2. Historial de ventas\n0. Volver")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1": registrar_venta()
        elif opcion == "2": listar_ventas()
        elif opcion == "0": return
        else: print("Opción no válida.")
