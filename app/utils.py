import random

def generar_codigo():
    """Genera un código de 4 dígitos"""
    return str(random.randint(1000, 9999))
