"""
📊 Data Module - Configuración y Datos
====================================

Módulo que contiene la configuración y datos del sistema CryptoUNS.

Componentes:
- config: Configuración general de la aplicación
- themes: Temas personalizados para la interfaz

Funcionalidades:
- Configuración de la aplicación
- Temas visuales personalizados
- Constantes de configuración
- Datos de la aplicación
"""

__version__ = "1.0.0"
__author__ = "CryptoUNS Team"

# Importaciones de módulos data
try:
    from .config import *
    from .themes import *
except ImportError:
    # Los módulos se importarán cuando sean creados
    pass
