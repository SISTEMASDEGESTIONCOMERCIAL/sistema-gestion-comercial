# Manual técnico

## Arquitectura
Aplicación de consola organizada por módulos, con separación entre interacción, reglas de negocio y persistencia JSON. No requiere dependencias de terceros.

## Componentes
- `main.py`: ciclo principal, navegación y salida controlada.
- `productos.py`: catálogo, reglas de unicidad, precios/cantidades no negativos y estado activo.
- `clientes.py`: registro y búsqueda de clientes.
- `ventas.py`: carrito de una o más líneas, validación de stock, subtotal, IVA 12 %, total, registro de venta y descuento de existencias.
- `inventario.py`: entradas y movimientos de entrada/salida (el stock inicial de un producto también genera una entrada).
- `reportes.py`: cálculos derivados de los datos guardados.
- `archivos.py`: rutas controladas y lectura/escritura JSON mediante archivo temporal.
- `estructuras.py`: validaciones compartidas y formato de fecha.

## Modelo de datos
- Producto: `codigo`, `nombre`, `categoria`, `precio`, `cantidad`, `stock_minimo`, `activo`.
- Cliente: `codigo`, `nombre`, `telefono`, `activo`.
- Venta: `numero`, `fecha`, `codigo_cliente`, `cliente`, `subtotal`, `iva`, `total`, `productos`.
- Línea de venta: `codigo_producto`, `producto`, `cantidad`, `precio_unitario`, `subtotal`, `iva`, `total`.
- Movimiento: `fecha`, `codigo_producto`, `tipo`, `cantidad`, `descripcion`.

## Persistencia
Los datos se escriben en `data/*.json`. `archivos.py` guarda primero en un archivo temporal y luego lo reemplaza para reducir el riesgo de dejar un JSON parcialmente escrito. Se recomienda copia de seguridad. JSON es adecuado para el alcance académico, pero no ofrece transacciones multiarchivo ni control de concurrencia de una base de datos.

## Ejemplo de registros (JSON)
```json
// productos.json
{"codigo": "P001", "nombre": "Cuaderno rayado", "categoria": "Papelería", "precio": 12.5, "cantidad": 40, "stock_minimo": 10, "activo": true}
// movimientos_inventario.json
{"fecha": "2026-10-05 10:15:00", "codigo_producto": "P001", "tipo": "SALIDA", "cantidad": 4, "descripcion": "Venta #1"}
```
Más ejemplos completos en `data/ejemplo/`.

## Reglas de negocio
1. No se admiten códigos duplicados para productos o clientes.
2. Precio, cantidades y stock mínimo no pueden ser negativos.
3. Las ventas solo incluyen productos activos con existencias suficientes.
4. El IVA se calcula al 12 % sobre el subtotal general.
5. Cada venta tiene número consecutivo calculado desde los registros guardados.
6. Una venta descuenta las existencias y crea movimientos de salida.
7. Entradas de inventario aumentan existencias y crean movimientos de entrada.
8. Los reportes se calculan a partir de los archivos almacenados.

## Ejecución y pruebas
Desde la raíz: `python src/main.py`. Pruebas automatizadas: `python -m unittest discover -s tests -v` (31 pruebas: validaciones, flujos de productos, ventas, inventario, reportes y menú, con carpeta temporal). Además, el equipo debe realizar y documentar pruebas manuales de cada flujo con capturas reales.

## Recuperación ante archivos dañados
`archivos.leer_json` copia el archivo ilegible a `data/<nombre>.danado-<fecha>.bak` antes de continuar con una lista vacía, para que un guardado posterior no destruya el original.

## Limitaciones conocidas
La aplicación está pensada para un único usuario local. No es una solución de facturación fiscal ni sustituye los requisitos legales de una factura. La escritura de varios archivos JSON no constituye una transacción atómica; después de un fallo durante la actualización de existencias, se deben verificar los archivos antes de seguir operando.
