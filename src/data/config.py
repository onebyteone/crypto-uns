"""
⚙️ Configuración Base - CryptoUNS
===============================

Archivo de configuración central del sistema CryptoUNS.
Contiene todas las configuraciones y parámetros de la aplicación.

Autor: CryptoUNS Team
Fecha: 06 de julio, 2025
Versión: 1.0.0
"""

import os
from pathlib import Path

# ===== INFORMACIÓN DE LA APLICACIÓN =====
APP_NAME = "CryptoUNS"
APP_VERSION = "1.0.0"
APP_AUTHOR = "CryptoUNS Team"
APP_DESCRIPTION = "Sistema Criptográfico Integral"
APP_URL = "https://github.com/onebyteone/crypto-uns"

# ===== CONFIGURACIÓN DE VENTANA =====
class WindowConfig:
    """Configuración de la ventana principal"""
    WIDTH = 1200
    HEIGHT = 800
    MIN_WIDTH = 800
    MIN_HEIGHT = 600
    TITLE = f"{APP_NAME} v{APP_VERSION}"
    ICON_PATH = "assets/icons/crypto_icon.ico"
    RESIZABLE = True
    CENTERED = True

# ===== CONFIGURACIÓN DE TEMA =====
class ThemeConfig:
    """Configuración de temas visuales"""
    DEFAULT_THEME = "darkly"
    AVAILABLE_THEMES = [
        "darkly",
        "flatly", 
        "pulse",
        "solar",
        "cyborg",
        "superhero",
        "vapor",
        "litera"
    ]
    
    # Paleta de colores
    COLORS = {
        'primary': '#007bff',
        'secondary': '#6c757d',
        'success': '#28a745',
        'warning': '#ffc107',
        'danger': '#dc3545',
        'info': '#17a2b8',
        'light': '#f8f9fa',
        'dark': '#343a40'
    }

# ===== CONFIGURACIÓN DE FUENTES =====
class FontConfig:
    """Configuración de fuentes"""
    DEFAULT_FAMILY = "Segoe UI"
    MONOSPACE_FAMILY = "Consolas"
    
    # Tamaños de fuente
    SMALL_SIZE = 9
    NORMAL_SIZE = 11
    LARGE_SIZE = 13
    TITLE_SIZE = 16
    
    # Configuraciones específicas
    DEFAULT_FONT = (DEFAULT_FAMILY, NORMAL_SIZE)
    MONOSPACE_FONT = (MONOSPACE_FAMILY, NORMAL_SIZE)
    TITLE_FONT = (DEFAULT_FAMILY, TITLE_SIZE, "bold")

# ===== CONFIGURACIÓN DE DIRECTORIOS =====
class PathConfig:
    """Configuración de rutas y directorios"""
    # Directorio base del proyecto
    BASE_DIR = Path(__file__).parent.parent.parent
    
    # Directorios principales
    SRC_DIR = BASE_DIR / "src"
    ASSETS_DIR = BASE_DIR / "assets"
    DOCS_DIR = BASE_DIR / "docs"
    TESTS_DIR = BASE_DIR / "tests"
    DIST_DIR = BASE_DIR / "dist"
    
    # Subdirectorios de assets
    ICONS_DIR = ASSETS_DIR / "icons"
    IMAGES_DIR = ASSETS_DIR / "images"
    TEMPLATES_DIR = ASSETS_DIR / "templates"
    
    # Archivos de configuración
    CONFIG_FILE = BASE_DIR / "config.json"
    LOG_FILE = BASE_DIR / "crypto_uns.log"

# ===== CONFIGURACIÓN DE CRIPTOGRAFÍA =====
class CryptoConfig:
    """Configuración de algoritmos criptográficos"""
    
    # Configuración César
    CAESAR_MIN_KEY = 1
    CAESAR_MAX_KEY = 25
    CAESAR_DEFAULT_KEY = 3
    
    # Configuración Vigenère
    VIGENERE_MIN_KEY_LENGTH = 2
    VIGENERE_MAX_KEY_LENGTH = 50
    
    # Configuración RSA
    RSA_MIN_KEY_SIZE = 512
    RSA_DEFAULT_KEY_SIZE = 1024
    RSA_MAX_KEY_SIZE = 4096
    
    # Configuración Hash
    HASH_TYPES = ["MD5", "SHA1", "SHA256", "SHA512", "Custom64", "Custom128", "Custom256"]
    DEFAULT_HASH_TYPE = "SHA256"
    
    # Configuración DES
    DES_KEY_SIZE = 8  # 8 bytes = 64 bits
    DES_MODES = ["ECB", "CBC"]
    DES_DEFAULT_MODE = "CBC"

# ===== CONFIGURACIÓN DE INTERFAZ =====
class UIConfig:
    """Configuración de elementos de interfaz"""
    
    # Dimensiones de componentes
    TEXT_AREA_WIDTH = 50
    TEXT_AREA_HEIGHT = 15
    BUTTON_WIDTH = 15
    ENTRY_WIDTH = 30
    
    # Espaciado
    PADDING_SMALL = 5
    PADDING_NORMAL = 10
    PADDING_LARGE = 20
    
    # Configuración de scrollbars
    SCROLLBAR_WIDTH = 15
    
    # Configuración de tooltips
    TOOLTIP_DELAY = 500
    TOOLTIP_WRAPLENGTH = 300

# ===== CONFIGURACIÓN DE LOGGING =====
class LogConfig:
    """Configuración de logging"""
    LEVEL = "INFO"
    FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    FILE_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    BACKUP_COUNT = 5
    ENABLE_CONSOLE = True
    ENABLE_FILE = True

# ===== CONFIGURACIÓN DE VALIDACIONES =====
class ValidationConfig:
    """Configuración de validaciones"""
    
    # Límites de texto
    MAX_TEXT_LENGTH = 1000000  # 1MB
    MIN_TEXT_LENGTH = 1
    
    # Validaciones de clave
    ALLOW_EMPTY_KEY = False
    CASE_SENSITIVE_KEYS = False
    
    # Validaciones de archivo
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    ALLOWED_FILE_EXTENSIONS = ['.txt', '.md', '.rtf', '.json', '.xml']

# ===== CONFIGURACIÓN DE PERFORMANCE =====
class PerformanceConfig:
    """Configuración de rendimiento"""
    
    # Threading
    MAX_THREADS = 4
    TIMEOUT_SECONDS = 30
    
    # Chunk size para archivos grandes
    CHUNK_SIZE = 8192
    
    # Cache
    ENABLE_CACHE = True
    CACHE_SIZE = 100

# ===== CONFIGURACIÓN DE DESARROLLO =====
class DevConfig:
    """Configuración para desarrollo"""
    DEBUG = True
    VERBOSE_LOGGING = True
    SHOW_PERFORMANCE_METRICS = True
    ENABLE_TESTING_MODE = False

# ===== CONFIGURACIÓN DE PRODUCCIÓN =====
class ProdConfig:
    """Configuración para producción"""
    DEBUG = False
    VERBOSE_LOGGING = False
    SHOW_PERFORMANCE_METRICS = False
    ENABLE_TESTING_MODE = False

# ===== CONFIGURACIÓN ACTIVA =====
# Cambiar a ProdConfig para producción
ACTIVE_CONFIG = DevConfig

# ===== FUNCIONES AUXILIARES =====
def get_config_value(key: str, default=None):
    """Obtener valor de configuración"""
    return getattr(ACTIVE_CONFIG, key, default)

def is_debug_mode() -> bool:
    """Verificar si está en modo debug"""
    return get_config_value('DEBUG', False)

def get_app_info() -> dict:
    """Obtener información de la aplicación"""
    return {
        'name': APP_NAME,
        'version': APP_VERSION,
        'author': APP_AUTHOR,
        'description': APP_DESCRIPTION,
        'url': APP_URL
    }

def get_window_config() -> dict:
    """Obtener configuración de ventana"""
    return {
        'width': WindowConfig.WIDTH,
        'height': WindowConfig.HEIGHT,
        'min_width': WindowConfig.MIN_WIDTH,
        'min_height': WindowConfig.MIN_HEIGHT,
        'title': WindowConfig.TITLE,
        'resizable': WindowConfig.RESIZABLE,
        'centered': WindowConfig.CENTERED
    }

# ===== EXPORTAR CONFIGURACIONES =====
__all__ = [
    'APP_NAME', 'APP_VERSION', 'APP_AUTHOR', 'APP_DESCRIPTION', 'APP_URL',
    'WindowConfig', 'ThemeConfig', 'FontConfig', 'PathConfig', 'CryptoConfig',
    'UIConfig', 'LogConfig', 'ValidationConfig', 'PerformanceConfig',
    'DevConfig', 'ProdConfig', 'ACTIVE_CONFIG',
    'get_config_value', 'is_debug_mode', 'get_app_info', 'get_window_config'
]
