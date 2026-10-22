# Análisis de procesos funcionales

## 1. Registro de productos
- **Objetivo:** añadir un producto identificable al catálogo.
- **Entradas:** código, nombre, categoría, precio, cantidad inicial y stock mínimo.
- **Procesamiento:** limpiar textos, comprobar que el código no exista, validar números no negativos y guardar el catálogo.
- **Salidas:** confirmación o mensaje de error.
- **Reglas:** código único; precio y cantidades no negativos; nombre y categoría obligatorios.
- **Errores:** código duplicado, campo vacío, valor numérico inválido o error de archivo.
- **Diagrama:** `../diagramas/registro_producto.mmd`.

## 2. Consulta y modificación de productos
- **Objetivo:** recuperar información por código y mantenerla actualizada.
- **Entradas:** código y campos opcionales a modificar.
- **Procesamiento:** buscar coincidencia; si existe, validar los campos informados y guardar cambios; los campos vacíos conservan su valor.
- **Salidas:** detalle actualizado o aviso de producto inexistente.
- **Reglas:** no modificar códigos duplicados; precio y stock mínimo no negativos.
- **Errores:** código inexistente, dato inválido o fallo de persistencia.
- **Diagrama:** `../diagramas/consulta_modificacion.mmd`.

## 3. Registro de ventas
- **Objetivo:** registrar una transacción, calcular impuestos y actualizar existencias.
- **Entradas:** uno o más códigos de producto, cantidades y código de cliente opcional.
- **Procesamiento:** validar productos activos y cantidades, acumular líneas, calcular subtotal, IVA del 12 % y total, asignar número y fecha, guardar venta, descontar stock y registrar movimientos de salida.
- **Salidas:** detalle de venta, total y confirmación; o mensaje de error.
- **Reglas:** cantidades enteras positivas; no vender más de lo disponible; cliente debe existir si se indica un código.
- **Errores:** producto/cliente inexistente, cantidad inválida, stock insuficiente o error de archivo.
- **Diagrama:** `../diagramas/registro_venta.mmd`.

## 4. Actualización de inventario
- **Objetivo:** controlar entradas, salidas y niveles de existencias.
- **Entradas:** código, cantidad y descripción de entrada; las salidas provienen de ventas.
- **Procesamiento:** verificar producto activo, validar cantidad positiva, actualizar existencias y registrar fecha, tipo, cantidad y descripción.
- **Salidas:** existencias actualizadas e historial de movimientos.
- **Reglas:** las entradas deben ser positivas; el stock bajo se identifica cuando cantidad <= stock mínimo.
- **Errores:** código inexistente, cantidad inválida o fallo al guardar.
- **Diagrama:** `../diagramas/actualizacion_inventario.mmd`.

## 5. Lectura y escritura de archivos
- **Objetivo:** conservar datos entre ejecuciones.
- **Entradas:** nombre permitido y estructura de datos.
- **Procesamiento:** leer JSON; manejar archivo ausente o JSON inválido; guardar a un archivo temporal y reemplazar el destino.
- **Salidas:** estructura cargada o aviso; confirmación implícita al guardar sin excepción.
- **Reglas:** los archivos se almacenan dentro de `data/`; no se aceptan rutas arbitrarias.
- **Errores:** permisos, archivo dañado o datos con formato inesperado.
- **Diagrama:** `../diagramas/lectura_archivos.mmd`.

## 6. Generación de reportes
- **Objetivo:** resumir catálogo, ventas, inventario y desempeño.
- **Entradas:** archivos JSON guardados.
- **Procesamiento:** recorrer los registros y calcular ingresos, unidades vendidas por producto, valor del inventario, productos bajo mínimo y promedio diario.
- **Salidas:** reportes impresos en consola.
- **Reglas:** las cifras se calculan desde datos persistidos; los importes se muestran con dos decimales.
- **Errores:** archivos vacíos o fechas antiguas no válidas para el promedio.
- **Diagrama:** `../diagramas/generacion_reportes.mmd`.

## 7. Pruebas
Los casos sugeridos están en `../pruebas.md`. El equipo debe completar el resultado obtenido y adjuntar capturas de la ejecución real en `../evidencias/`.
