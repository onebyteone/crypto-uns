"""
🔐 CryptoUNS - Sistema Criptográfico Integral
=============================================

Paquete principal del sistema CryptoUNS.
Contiene módulos para criptografía clásica, moderna y herramientas adicionales.

Módulos:
- gui: Interfaz gráfica de usuario
- crypto: Algoritmos criptográficos
- utils: Utilidades generales
- data: Configuración y datos

Autor: CryptoUNS Team
Fecha: 06 de julio, 2025
Versión: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "CryptoUNS Team"
__email__ = "crypto@uns.edu.ar"
__license__ = "MIT"

# Información del paquete
__title__ = "CryptoUNS"
__description__ = "Sistema Criptográfico Integral"
__url__ = "https://github.com/onebyteone/crypto-uns"

# Importaciones principales
from .gui import *
from .crypto import *
from .utils import *
from .data import *
