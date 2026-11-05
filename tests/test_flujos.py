"""Pruebas de flujo (P01-P13) que simulan al usuario con entradas de teclado.

Usan una carpeta temporal: no tocan los datos reales de data/.
Ejecutar desde la raíz: python -m unittest discover -s tests -v
"""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import archivos  # noqa: E402
import inventario  # noqa: E402
import main  # noqa: E402
import productos  # noqa: E402
import reportes  # noqa: E402
import ventas  # noqa: E402


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._patch = patch.object(archivos, "DATA", Path(self._tmp.name))
        self._patch.start()

    def tearDown(self):
        self._patch.stop()
        self._tmp.cleanup()

    def correr(self, funcion, *entradas):
        """Ejecuta funcion() con entradas simuladas y devuelve lo impreso."""
        salida = io.StringIO()
        with patch("builtins.input", side_effect=list(entradas)), contextlib.redirect_stdout(salida):
            funcion()
        return salida.getvalue()

    def crear(self, codigo="P01", nombre="Lapiz", precio="10", cantidad="5", minimo="2"):
        return self.correr(productos.registrar_producto, codigo, nombre, "Papeleria", precio, cantidad, minimo)

    def leer(self, nombre):
        return json.loads((Path(self._tmp.name) / nombre).read_text(encoding="utf-8"))


class TestProductos(Base):
    def test_P01_registro_valido(self):
        salida = self.crear()
        self.assertIn("registrado correctamente", salida)
        self.assertEqual(len(self.leer("productos.json")), 1)

    def test_P02_codigo_duplicado(self):
        self.crear()
        salida = self.crear()
        self.assertIn("ya existe un producto", salida)
        self.assertEqual(len(self.leer("productos.json")), 1)

    def test_P03_precio_negativo(self):
        salida = self.crear(precio="-1")
        self.assertIn("no puede ser negativo", salida)
        self.assertFalse((Path(self._tmp.name) / "productos.json").exists())

    def test_P04_cantidad_texto(self):
        salida = self.crear(cantidad="abc")
        self.assertIn("debe ser un número entero", salida)
        self.assertFalse((Path(self._tmp.name) / "productos.json").exists())

    def test_P13_consultar_inexistente(self):
        salida = self.correr(productos.consultar_producto, "NOEXISTE")
        self.assertIn("Producto no encontrado", salida)

    def test_stock_inicial_genera_movimiento(self):
        self.crear()
        movs = self.leer("movimientos_inventario.json")
        self.assertEqual((movs[0]["tipo"], movs[0]["cantidad"]), ("ENTRADA", 5))

    def test_desactivar_y_reactivar(self):
        self.crear()
        self.correr(productos.desactivar_producto, "P01")
        self.assertFalse(self.leer("productos.json")[0]["activo"])
        self.correr(productos.reactivar_producto, "P01")
        self.assertTrue(self.leer("productos.json")[0]["activo"])


class TestVentas(Base):
    def test_P05_venta_valida(self):
        self.crear()
        salida = self.correr(ventas.registrar_venta, "P01", "2", "", "")
        self.assertIn("Q20.00", salida)
        self.assertIn("IVA (12%): Q2.40", salida)
        self.assertIn("TOTAL: Q22.40", salida)
        self.assertEqual(self.leer("productos.json")[0]["cantidad"], 3)
        self.assertEqual(self.leer("ventas.json")[0]["numero"], 1)

    def test_P06_venta_mayor_que_stock(self):
        self.crear(cantidad="3")
        salida = self.correr(ventas.registrar_venta, "P01", "4", "")
        self.assertIn("Existencias insuficientes", salida)
        self.assertIn("Venta cancelada", salida)
        self.assertEqual(self.leer("productos.json")[0]["cantidad"], 3)

    def test_P07_cliente_inexistente(self):
        self.crear()
        salida = self.correr(ventas.registrar_venta, "P01", "1", "", "C999")
        self.assertIn("Cliente no encontrado", salida)
        self.assertFalse((Path(self._tmp.name) / "ventas.json").exists())

    def test_cantidad_negativa_y_texto_en_venta(self):
        self.crear()
        salida = self.correr(ventas.registrar_venta, "P01", "-1", "P01", "xx", "")
        self.assertIn("mayor que cero", salida)
        self.assertIn("entera válida", salida)

    def test_producto_inactivo_no_se_vende(self):
        self.crear()
        self.correr(productos.desactivar_producto, "P01")
        salida = self.correr(ventas.registrar_venta)
        self.assertIn("No hay productos activos con existencias", salida)

    def test_venta_varios_productos_iva_general(self):
        self.crear()
        self.crear("P02", "Borrador", "3", "4", "1")
        salida = self.correr(ventas.registrar_venta, "P01", "2", "P02", "1", "", "")
        self.assertIn("Subtotal: Q23.00", salida)
        self.assertIn("IVA (12%): Q2.76", salida)
        self.assertIn("TOTAL: Q25.76", salida)


class TestInventario(Base):
    def test_P08_entrada(self):
        self.crear()
        self.correr(inventario.registrar_entrada, "P01", "5", "Compra")
        self.assertEqual(self.leer("productos.json")[0]["cantidad"], 10)
        ultimo = self.leer("movimientos_inventario.json")[-1]
        self.assertEqual((ultimo["tipo"], ultimo["cantidad"], ultimo["descripcion"]), ("ENTRADA", 5, "Compra"))

    def test_entrada_negativa_rechazada(self):
        self.crear()
        salida = self.correr(inventario.registrar_entrada, "P01", "-3", "")
        self.assertIn("no puede ser negativo", salida)
        self.assertEqual(self.leer("productos.json")[0]["cantidad"], 5)

    def test_P09_stock_minimo_en_reporte(self):
        self.crear(cantidad="2", minimo="2")
        salida = self.correr(reportes.reporte_stock_bajo)
        self.assertIn("P01", salida)

    def test_venta_genera_movimiento_salida(self):
        self.crear()
        self.correr(ventas.registrar_venta, "P01", "2", "", "")
        ultimo = self.leer("movimientos_inventario.json")[-1]
        self.assertEqual((ultimo["tipo"], ultimo["cantidad"], ultimo["descripcion"]), ("SALIDA", 2, "Venta #1"))


class TestReportes(Base):
    def test_P10_reportes_sin_ventas(self):
        for r in (reportes.reporte_ventas, reportes.reporte_producto_mas_vendido, reportes.reporte_promedio_ventas):
            self.assertIn("No hay", self.correr(r))

    def test_reportes_con_datos(self):
        self.crear()
        self.crear("P02", "Borrador", "3", "4", "1")
        self.correr(ventas.registrar_venta, "P01", "2", "P02", "1", "", "")
        self.assertIn("Q25.76", self.correr(reportes.reporte_ventas))
        self.assertIn("Lapiz: 2 unidad", self.correr(reportes.reporte_producto_mas_vendido))
        # (3 x 10) + (3 x 3) = 39
        self.assertIn("Q39.00", self.correr(reportes.reporte_valor_inventario))
        promedio = self.correr(reportes.reporte_promedio_ventas)
        self.assertIn("Promedio diario: Q25.76", promedio)
        self.assertIn("Promedio mensual: Q25.76", promedio)


class TestPersistenciaYMenu(Base):
    def test_P11_persistencia(self):
        self.crear()
        self.assertEqual(productos.cargar_productos()[0]["codigo"], "P01")  # relectura desde disco

    def test_P12_opcion_invalida_no_finaliza(self):
        salida = self.correr(main.main, "9", "abc", "", "0")
        self.assertEqual(salida.count("Opción no válida"), 3)
        self.assertIn("Gracias por utilizar el sistema", salida)

    def test_json_danado_se_respalda(self):
        (Path(self._tmp.name) / "productos.json").write_text("{{{", encoding="utf-8")
        salida = self.correr(productos.listar_productos)
        self.assertIn("copia del archivo dañado", salida)
        self.assertTrue(list(Path(self._tmp.name).glob("productos.danado-*.bak")))


if __name__ == "__main__":
    unittest.main()
