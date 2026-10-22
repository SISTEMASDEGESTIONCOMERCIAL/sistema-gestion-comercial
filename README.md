# Sistema de Gestión Comercial

Sistema de consola desarrollado en Python para administrar productos, clientes, ventas, inventario y reportes de una pequeña empresa. Los datos se guardan en archivos JSON locales.

## Requisitos
- Python 3.10 o superior recomendado.
- No requiere instalar librerías externas.
- Windows, Linux o macOS.

## Ejecutar
1. Descargue o clone el repositorio.
2. Abra la carpeta del proyecto en Visual Studio Code.
3. Abra una terminal en la carpeta raíz.
4. Ejecute:

```bash
python src/main.py
```

En Windows también puede funcionar `py src/main.py`. No ejecute los módulos desde dentro de `src`; use el comando desde la carpeta raíz para que Python encuentre los archivos JSON en `data/`.

## Módulos
- `src/productos.py`: altas, consultas, listado, modificación y desactivación.
- `src/clientes.py`: registro y consulta de clientes.
- `src/ventas.py`: ventas de uno o varios productos, IVA del 12 %, historial y actualización de existencias.
- `src/inventario.py`: consulta, entradas y movimientos de entrada/salida.
- `src/reportes.py`: reportes calculados con los archivos guardados.
- `src/archivos.py`: lectura y escritura JSON.
- `src/estructuras.py`: validaciones y utilidades.

## Archivos de datos
Los JSON se crean automáticamente dentro de `data/`: `productos.json`, `clientes.json`, `ventas.json` y `movimientos_inventario.json`. No borre esos archivos si necesita conservar los registros. Haga copias de seguridad antes de realizar cambios manuales.

## Pruebas
Desde la carpeta raíz ejecute:

```bash
python -m unittest discover -s tests -v
```

## Estructura
```text
sistema-gestion-comercial/
├── README.md
├── .gitignore
├── src/
├── data/
├── tests/
└── docs/
    ├── analisis/
    ├── diagramas/
    ├── evidencias/
    ├── manual-tecnico.md
    └── manual-usuario.md
```

## GitHub
Consulte `docs/GITHUB.md` para los pasos de publicación, commits, rama, pull request, Issue y release. La guía no reemplaza el trabajo real del equipo: los commits, el PR y las evidencias deben crearse en el repositorio del equipo.
