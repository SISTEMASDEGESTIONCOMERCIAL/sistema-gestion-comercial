import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from estructuras import texto_no_vacio, entero_no_negativo, dinero_no_negativo


class TestValidaciones(unittest.TestCase):
    def test_texto_limpia_espacios(self):
        self.assertEqual(texto_no_vacio("  Ana ", "Nombre"), "Ana")

    def test_texto_vacio_rechazado(self):
        with self.assertRaises(ValueError):
            texto_no_vacio("  ", "Nombre")

    def test_entero_no_negativo(self):
        self.assertEqual(entero_no_negativo("4"), 4)

    def test_entero_negativo_rechazado(self):
        with self.assertRaises(ValueError):
            entero_no_negativo("-1")

    def test_entero_texto_rechazado(self):
        with self.assertRaises(ValueError):
            entero_no_negativo("abc")

    def test_dinero_redondeado(self):
        self.assertEqual(dinero_no_negativo("12.345"), 12.35)

    def test_dinero_negativo_rechazado(self):
        with self.assertRaises(ValueError):
            dinero_no_negativo("-2")


if __name__ == "__main__":
    unittest.main()
