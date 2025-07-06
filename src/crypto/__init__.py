"""
🔐 Crypto Module - Algoritmos Criptográficos
==========================================

Módulo que contiene todos los algoritmos criptográficos
del sistema CryptoUNS.

Componentes:
- classic: Criptografía clásica (César, Vigenère, Playfair)
- modern: Criptografía moderna (RSA, Hash, DES, Firma Digital)
- tools: Herramientas adicionales (Huffman, Kasiski, Blockchain)
- utils: Funciones auxiliares para criptografía

Características:
- Implementación segura de algoritmos
- Validaciones de entrada
- Manejo de errores específicos
- Pruebas unitarias incluidas
"""

__version__ = "1.0.0"
__author__ = "CryptoUNS Team"

# Importaciones de módulos crypto
try:
    from .classic import *
    from .modern import *
    from .tools import *
    from .utils import *
except ImportError:
    # Los módulos se importarán cuando sean creados
    pass
