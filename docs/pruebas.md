# Plan de pruebas del sistema

Completar la columna “Resultado obtenido” y adjuntar una captura real por cada prueba antes de entregar.

| ID | Caso | Datos | Resultado esperado | Resultado obtenido / conclusión |
|---|---|---|---|---|
| P01 | Registrar producto válido | Código P01, precio 10, cantidad 5, mínimo 2 | Producto guardado | Pendiente de ejecutar |
| P02 | Código de producto duplicado | Repetir P01 | Rechazar duplicado | Pendiente de ejecutar |
| P03 | Precio negativo | Precio -1 | Rechazar precio | Pendiente de ejecutar |
| P04 | Cantidad de texto | Cantidad `abc` | Mostrar error y no guardar | Pendiente de ejecutar |
| P05 | Venta válida | 2 unidades a Q10 | Subtotal Q20, IVA Q2.40, total Q22.40; stock baja en 2 | Pendiente de ejecutar |
| P06 | Venta mayor que stock | Stock 3, vender 4 | Rechazar cantidad | Pendiente de ejecutar |
| P07 | Cliente inexistente | Código de cliente desconocido | Cancelar venta | Pendiente de ejecutar |
| P08 | Entrada de inventario | Entrada 5 unidades | Stock aumenta en 5 y crea movimiento | Pendiente de ejecutar |
| P09 | Stock mínimo | Cantidad igual al mínimo | Aparece en reporte de stock bajo | Pendiente de ejecutar |
| P10 | Reporte sin ventas | Archivo de ventas vacío | Mensaje claro, sin excepción | Pendiente de ejecutar |
| P11 | Persistencia | Registrar y reiniciar programa | Datos permanecen guardados | Pendiente de ejecutar |
| P12 | Opción inválida | Escribir `9` en menú | Mostrar error y volver al menú | Pendiente de ejecutar |

No declares pruebas como aprobadas hasta ejecutarlas. Para cada caso registra fecha, versión del código, datos usados, resultado observado y conclusión.
