from funciones import sumar

def test_sumar_positivos():
    assert sumar(2, 3) == 5

def test_sumar_negativos():
    assert sumar(-2, -3) == -5

def test_sumar_mezcla():
    assert sumar(1, -4) == -3
    