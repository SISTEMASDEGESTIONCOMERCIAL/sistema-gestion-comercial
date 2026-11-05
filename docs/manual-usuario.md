# Manual de usuario

## 1. Propósito
Este programa permite gestionar productos, clientes, ventas, inventario y reportes desde un menú de texto. No se necesita conocer Python para realizar las operaciones.

## 2. Iniciar y cerrar
1. Instale Python 3.10 o superior.
2. Abra la carpeta del proyecto en Visual Studio Code.
3. En la terminal, ejecute `python src/main.py`.
4. Seleccione la opción deseada escribiendo el número y presione Enter.
5. Para cerrar, elija `0. Salir` en el menú principal. Si cierra con Ctrl+C, el programa termina sin perder datos ya guardados.

## 3. Productos
Entre a **Gestionar productos**. Puede registrar un producto con código único, nombre, categoría, precio, cantidad inicial y stock mínimo; consultar por código; listar; modificar campos (deje vacío para conservar el valor actual), desactivar un producto y reactivarlo (opción 6). La desactivación conserva el historial y evita nuevas ventas.

## 4. Clientes
En **Gestionar clientes**, registre un código único, nombre y teléfono opcional. Use la opción de listar para consultar los clientes. Para ventas generales puede dejar vacío el código del cliente.

## 5. Ventas
1. Abra **Gestionar ventas > Registrar venta**.
2. Seleccione el código del primer producto y la cantidad.
3. Repita para agregar otros productos. Para terminar, presione Enter en el campo del código.
4. Introduzca un código de cliente registrado o presione Enter para venta general.
5. Revise subtotal, IVA (12 %) y total. El programa guarda la venta y descuenta las existencias.
6. Use **Historial de ventas** para consultar operaciones anteriores.

No se aceptan cantidades cero, negativas, no enteras ni mayores a las existencias disponibles.

## 6. Inventario
En **Gestionar inventario** puede consultar existencias, registrar entradas de unidades y revisar el historial. Cada entrada y salida de una venta registra fecha, código, tipo, cantidad y descripción. Los productos con cantidad igual o inferior al stock mínimo aparecen como stock bajo.

## 7. Reportes
En **Reportes y estadísticas** encontrará el listado general, productos en stock mínimo o bajo, historial e ingresos por ventas, producto con mayor cantidad de unidades vendidas, valor de venta del inventario disponible, promedio de ventas por día y por mes, y reporte general. Los cálculos se obtienen de los archivos JSON, no de cifras escritas manualmente.

## 8. Mensajes frecuentes
- **Opción no válida:** escriba uno de los números mostrados.
- **Código duplicado:** use un código diferente.
- **Producto/cliente no encontrado:** revise el código o registre primero el elemento.
- **Existencias insuficientes:** reduzca la cantidad o registre una entrada de inventario.
- **Dato debe ser numérico:** introduzca un número válido; no escriba letras en precio o cantidad.

## 9. Conservación de datos
Si un archivo de datos se daña, el programa avisa y guarda una copia con nombre `*.danado-FECHA.bak` en `data/`; conserve esa copia antes de seguir trabajando.
Para practicar con datos de ejemplo, copie los archivos de `data/ejemplo/` a `data/`.
No elimine la carpeta `data/`. Haga copias de seguridad de los JSON antes de reinstalar o modificar el programa. Los datos reales no deben subirse a un repositorio público; el repositorio incluye un `.gitignore` que excluye los JSON de datos.

## 10. Capturas de evidencia
Ejecute el sistema y capture: menú principal, registro y listado de productos, validación de código duplicado, venta con IVA, inventario con entrada y stock bajo, historial y reportes. Guarde las imágenes en `docs/evidencias/` antes de entregar.
