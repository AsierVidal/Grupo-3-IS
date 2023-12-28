import unittest
from funciones import sumar

class TestFunciones(unittest.TestCase):
    def test_sumar_positivos(self):
        self.assertEqual(sumar(2, 3), 5)

    def test_sumar_negativos(self):
        self.assertEqual(sumar(-2, -3), -5)

    def test_sumar_mezcla(self):
        self.assertEqual(sumar(1, -4), -3)

if __name__ == '__main__':
    unittest.main()
