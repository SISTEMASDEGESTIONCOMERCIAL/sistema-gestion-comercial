"""Registro sencillo de clientes para asociarlos a ventas."""
from archivos import leer_json, guardar_json
from estructuras import texto_no_vacio

ARCHIVO = "clientes.json"


def cargar_clientes():
    datos = leer_json(ARCHIVO, [])
    return datos if isinstance(datos, list) else []


def guardar_clientes(clientes):
    guardar_json(ARCHIVO, clientes)


def buscar_cliente(codigo):
    codigo = str(codigo).strip()
    return next((c for c in cargar_clientes() if str(c.get("codigo", "")) == codigo), None)


def registrar_cliente():
    clientes = cargar_clientes()
    try:
        codigo = texto_no_vacio(input("Código/identificación: "), "Código")
        if any(str(c.get("codigo")) == codigo for c in clientes):
            print("Ese código de cliente ya existe.")
            return
        nombre = texto_no_vacio(input("Nombre del cliente: "), "Nombre")
        telefono = input("Teléfono (opcional): ").strip()
    except ValueError as error:
        print(f"Error: {error}")
        return
    clientes.append({"codigo": codigo, "nombre": nombre, "telefono": telefono, "activo": True})
    guardar_clientes(clientes)
    print("Cliente registrado correctamente.")


def listar_clientes():
    clientes = cargar_clientes()
    if not clientes:
        print("No hay clientes registrados.")
        return
    print("\n--- CLIENTES ---")
    for c in clientes:
        print(f"Código: {c['codigo']} | Nombre: {c['nombre']} | Teléfono: {c.get('telefono', '')}")


def menu_clientes():
    while True:
        print("\n===== GESTIÓN DE CLIENTES =====\n1. Registrar cliente\n2. Listar clientes\n0. Volver")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1": registrar_cliente()
        elif opcion == "2": listar_clientes()
        elif opcion == "0": return
        else: print("Opción no válida.")
