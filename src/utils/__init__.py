"""
🛠️ Utils Module - Utilidades Generales
=====================================

Módulo que contiene utilidades generales del sistema CryptoUNS.

Componentes:
- file_manager: Manejo de archivos
- validators: Validaciones de entrada
- constants: Constantes del sistema

Funcionalidades:
- Gestión de archivos y directorios
- Validaciones de entrada de usuario
- Constantes del sistema
- Utilidades auxiliares
"""

__version__ = "1.0.0"
__author__ = "CryptoUNS Team"

# Importaciones de módulos utils
try:
    from .file_manager import *
    from .validators import *
    from .constants import *
except ImportError:
    # Los módulos se importarán cuando sean creados
    pass
