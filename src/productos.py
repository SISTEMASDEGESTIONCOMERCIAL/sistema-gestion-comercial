"""Gestión de productos del sistema comercial."""
from archivos import leer_json, guardar_json
from estructuras import texto_no_vacio, dinero_no_negativo, entero_no_negativo

ARCHIVO = "productos.json"


def cargar_productos():
    datos = leer_json(ARCHIVO, [])
    return datos if isinstance(datos, list) else []


def guardar_productos(productos):
    guardar_json(ARCHIVO, productos)


def buscar_producto(codigo, incluir_inactivos=True):
    codigo = str(codigo).strip()
    return next((p for p in cargar_productos()
                 if str(p.get("codigo", "")) == codigo
                 and (incluir_inactivos or p.get("activo", True))), None)


def registrar_producto():
    productos = cargar_productos()
    try:
        codigo = texto_no_vacio(input("Código: "), "Código")
        if any(str(p.get("codigo")) == codigo for p in productos):
            print("Error: ya existe un producto con ese código.")
            return
        nombre = texto_no_vacio(input("Nombre: "), "Nombre")
        categoria = texto_no_vacio(input("Categoría: "), "Categoría")
        precio = dinero_no_negativo(input("Precio de venta (Q): "))
        cantidad = entero_no_negativo(input("Cantidad inicial: "))
        minimo = entero_no_negativo(input("Stock mínimo: "), "Stock mínimo")
    except ValueError as error:
        print(f"Error: {error}")
        return
    productos.append({"codigo": codigo, "nombre": nombre, "categoria": categoria,
                      "precio": precio, "cantidad": cantidad,
                      "stock_minimo": minimo, "activo": True})
    guardar_productos(productos)
    if cantidad > 0:
        from inventario import registrar_movimiento  # import local: evita dependencia circular
        try:
            registrar_movimiento(codigo, "ENTRADA", cantidad, "Existencia inicial")
        except OSError as error:
            print(f"El producto se guardó, pero no se registró el movimiento inicial: {error}")
    print("Producto registrado correctamente.")


def listar_productos(solo_activos=False):
    productos = cargar_productos()
    if solo_activos:
        productos = [p for p in productos if p.get("activo", True)]
    if not productos:
        print("No hay productos para mostrar.")
        return
    print("\n--- LISTADO DE PRODUCTOS ---")
    for p in productos:
        estado = "Activo" if p.get("activo", True) else "Inactivo"
        print(f"{p['codigo']} | {p['nombre']} | {p['categoria']} | Q{float(p['precio']):.2f} | "
              f"Existencias: {p['cantidad']} | Mínimo: {p['stock_minimo']} | {estado}")


def consultar_producto():
    codigo = input("Código del producto: ").strip()
    producto = buscar_producto(codigo)
    if not producto:
        print("Producto no encontrado.")
        return
    print(f"Código: {producto['codigo']} | Nombre: {producto['nombre']} | Categoría: {producto['categoria']} | "
          f"Precio: Q{float(producto['precio']):.2f} | Cantidad: {producto['cantidad']} | "
          f"Stock mínimo: {producto['stock_minimo']} | Activo: {producto.get('activo', True)}")


def modificar_producto():
    productos = cargar_productos()
    codigo = input("Código del producto a modificar: ").strip()
    producto = next((p for p in productos if str(p.get("codigo")) == codigo), None)
    if not producto:
        print("Producto no encontrado.")
        return
    print("Deje vacío un campo para conservar el valor actual.")
    try:
        nombre = input(f"Nombre [{producto['nombre']}]: ").strip()
        categoria = input(f"Categoría [{producto['categoria']}]: ").strip()
        precio = input(f"Precio [{producto['precio']}]: ").strip()
        minimo = input(f"Stock mínimo [{producto['stock_minimo']}]: ").strip()
        if nombre: producto["nombre"] = texto_no_vacio(nombre, "Nombre")
        if categoria: producto["categoria"] = texto_no_vacio(categoria, "Categoría")
        if precio: producto["precio"] = dinero_no_negativo(precio)
        if minimo: producto["stock_minimo"] = entero_no_negativo(minimo, "Stock mínimo")
    except ValueError as error:
        print(f"Error: {error}")
        return
    guardar_productos(productos)
    print("Producto actualizado.")


def desactivar_producto():
    productos = cargar_productos()
    codigo = input("Código del producto a desactivar: ").strip()
    producto = next((p for p in productos if str(p.get("codigo")) == codigo), None)
    if not producto:
        print("Producto no encontrado.")
        return
    producto["activo"] = False
    guardar_productos(productos)
    print("Producto desactivado; su historial se conserva.")


def reactivar_producto():
    productos = cargar_productos()
    codigo = input("Código del producto a reactivar: ").strip()
    producto = next((p for p in productos if str(p.get("codigo")) == codigo), None)
    if not producto:
        print("Producto no encontrado.")
        return
    if producto.get("activo", True):
        print("El producto ya está activo.")
        return
    producto["activo"] = True
    guardar_productos(productos)
    print("Producto reactivado; ya puede venderse de nuevo.")


def menu_productos():
    while True:
        print("\n===== GESTIÓN DE PRODUCTOS =====")
        print("1. Registrar producto\n2. Consultar por código\n3. Listar productos\n4. Modificar producto\n5. Desactivar producto\n6. Reactivar producto\n0. Volver")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1": registrar_producto()
        elif opcion == "2": consultar_producto()
        elif opcion == "3": listar_productos()
        elif opcion == "4": modificar_producto()
        elif opcion == "5": desactivar_producto()
        elif opcion == "6": reactivar_producto()
        elif opcion == "0": return
        else: print("Opción no válida.")
