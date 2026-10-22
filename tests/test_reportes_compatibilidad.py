import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ventas import _lineas_de_venta


class TestCompatibilidadVentas(unittest.TestCase):
    def test_venta_nueva_con_varios_productos(self):
        venta = {"productos": [{"producto": "A", "cantidad": 2, "total": 22.4}]}
        self.assertEqual(_lineas_de_venta(venta)[0]["cantidad"], 2)

    def test_venta_antigua_un_producto(self):
        venta = {"producto": "B", "cantidad": 3, "total": 30}
        lineas = _lineas_de_venta(venta)
        self.assertEqual(lineas[0]["producto"], "B")
        self.assertEqual(lineas[0]["cantidad"], 3)


if __name__ == "__main__":
    unittest.main()
