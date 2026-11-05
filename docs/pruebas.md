# Plan y resultados de pruebas

- **Fecha de ejecución:** 2026-11-03
- **Entorno:** Python 3.12, ejecución desde la raíz del proyecto.
- **Cómo repetirlas:** `python -m unittest discover -s tests -v` (31 pruebas, usan una carpeta temporal y no tocan `data/`).
- **Resultado global:** 31 pruebas ejecutadas, 31 aprobadas.

> Las pruebas automáticas están en `tests/test_flujos.py` (P01–P13 y extras) y simulan lo que el usuario escribe en el teclado. **Falta que el equipo ejecute los casos manualmente en el programa y guarde las capturas en `docs/evidencias/`** (columna "Captura").

| ID | Caso | Datos utilizados | Resultado esperado | Resultado obtenido | Conclusión | Captura |
|---|---|---|---|---|---|---|
| P01 | Registrar producto válido | Código P01, precio 10, cantidad 5, mínimo 2 | Producto guardado | "Producto registrado correctamente"; 1 producto en `productos.json` | Aprobada | Pendiente |
| P02 | Código duplicado | Repetir código P01 | Rechazar duplicado | "ya existe un producto con ese código"; sigue habiendo 1 producto | Aprobada | Pendiente |
| P03 | Precio negativo | Precio -1 | Rechazar y no guardar | "precio no puede ser negativo"; no se crea el archivo | Aprobada | Pendiente |
| P04 | Cantidad de tipo incorrecto | Cantidad `abc` | Error y no guardar | "cantidad debe ser un número entero"; no se guarda | Aprobada | Pendiente |
| P05 | Venta válida | 2 unidades a Q10 | Subtotal Q20, IVA Q2.40, total Q22.40; stock baja de 5 a 3 | Valores idénticos; stock 3; venta #1 guardada | Aprobada | Pendiente |
| P06 | Vender más de lo disponible | Stock 3, vender 4 | Rechazar cantidad | "Existencias insuficientes"; "Venta cancelada"; stock sigue en 3 | Aprobada | Pendiente |
| P07 | Cliente inexistente | Cliente C999 | Cancelar venta | "Cliente no encontrado"; no se crea `ventas.json` | Aprobada | Pendiente |
| P08 | Entrada de inventario | Entrada de 5 unidades (stock 5) | Stock 10 y movimiento ENTRADA | Stock 10; movimiento ENTRADA, 5, "Compra" | Aprobada | Pendiente |
| P09 | Stock mínimo | Cantidad 2, mínimo 2 | Aparece en reporte de stock bajo | P01 aparece en el reporte | Aprobada | Pendiente |
| P10 | Reportes sin ventas | Sin `ventas.json` | Mensaje claro, sin excepción | "No hay ventas registradas / datos de ventas" | Aprobada | Pendiente |
| P11 | Persistencia | Registrar y volver a leer desde disco | Datos permanecen | Producto recuperado desde el archivo | Aprobada | Pendiente |
| P12 | Opción inválida en menú | `9`, `abc`, Enter | Mostrar error y volver al menú | 3 mensajes "Opción no válida"; el programa sigue y sale con 0 | Aprobada | Pendiente |
| P13 | Consultar producto inexistente | Código NOEXISTE | "Producto no encontrado" | Mensaje esperado | Aprobada | Pendiente |

## Pruebas adicionales (también automatizadas)

| Caso | Datos | Resultado obtenido | Conclusión |
|---|---|---|---|
| Venta de varios productos | 2 × Q10 + 1 × Q3 | Subtotal Q23.00, IVA Q2.76, total Q25.76 | Aprobada |
| Cantidad negativa y texto en venta | `-1`, `xx` | Mensajes "mayor que cero" y "entera válida" | Aprobada |
| Producto desactivado | Desactivar P01 e intentar vender | "No hay productos activos con existencias" | Aprobada |
| Entrada negativa | `-3` | Rechazada; stock sin cambios | Aprobada |
| Venta genera movimiento | Venta #1 de 2 unidades | Movimiento SALIDA, 2, "Venta #1" | Aprobada |
| Stock inicial en historial | Registrar con cantidad 5 | Movimiento ENTRADA "Existencia inicial" | Aprobada |
| Desactivar y reactivar | P01 | `activo` pasa a falso y luego a verdadero | Aprobada |
| JSON dañado | `productos.json` con `{{{` | Aviso y copia `.danado-*.bak`; no se pierde el original | Aprobada |

## Verificación de cálculos con los datos de ejemplo (`data/ejemplo/`)

Para probar a mano: copiar los 4 JSON de `data/ejemplo/` a `data/` y abrir **Reportes**.

| Reporte | Cálculo esperado | Resultado obtenido |
|---|---|---|
| Ingresos totales | 78.40 + 22.68 + 207.20 | Q308.28 |
| Producto más vendido | Cuaderno rayado: 4 + 6 | 10 unidades |
| Valor del inventario activo | 40×12.50 + 8×2 + 25×6.75 + 5×55 | Q959.75 |
| Stock bajo | P002 (8 ≤ 10) y P004 (5 ≤ 5) | Ambos listados |
| Promedio diario | (101.08 + 207.20) / 2 días | Q154.14 |
| Promedio mensual | (101.08 + 207.20) / 2 meses | Q154.14 |
