"""Punto de entrada del Sistema de Gestión Comercial."""
from productos import menu_productos
from ventas import menu_ventas
from clientes import menu_clientes
from inventario import menu_inventario
from reportes import menu_reportes


def mostrar_menu():
    print("\n========== SISTEMA DE GESTIÓN COMERCIAL ==========")
    print("1. Gestionar productos")
    print("2. Gestionar ventas")
    print("3. Gestionar clientes")
    print("4. Gestionar inventario")
    print("5. Ver reportes y estadísticas")
    print("0. Salir")


def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1": menu_productos()
        elif opcion == "2": menu_ventas()
        elif opcion == "3": menu_clientes()
        elif opcion == "4": menu_inventario()
        elif opcion == "5": menu_reportes()
        elif opcion == "0":
            print("Gracias por utilizar el sistema.")
            break
        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()
