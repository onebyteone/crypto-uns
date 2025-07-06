"""
🔢 Constantes del Sistema - CryptoUNS
===================================

Archivo que contiene todas las constantes utilizadas en el sistema CryptoUNS.

Autor: CryptoUNS Team
Fecha: 06 de julio, 2025
Versión: 1.0.0
"""

import string
from typing import List, Dict, Tuple

# ===== CONSTANTES GENERALES =====
APP_TITLE = "CryptoUNS - Sistema Criptográfico Integral"
APP_VERSION = "1.0.0"
APP_AUTHOR = "CryptoUNS Team"
COPYRIGHT = "© 2025 CryptoUNS Team. Todos los derechos reservados."

# ===== CONSTANTES DE INTERFAZ =====
WINDOW_TITLE = "🔐 CryptoUNS"
WINDOW_ICON = "🔐"

# Mensajes de la interfaz
MESSAGES = {
    'welcome': "¡Bienvenido a CryptoUNS!",
    'ready': "Listo",
    'processing': "Procesando...",
    'success': "Operación exitosa",
    'error': "Error en la operación",
    'warning': "Advertencia",
    'info': "Información",
    'loading': "Cargando...",
    'saving': "Guardando...",
    'copying': "Copiando...",
    'empty_field': "Este campo no puede estar vacío",
    'invalid_input': "Entrada inválida",
    'file_not_found': "Archivo no encontrado",
    'permission_denied': "Permiso denegado"
}

# Etiquetas de botones
BUTTON_LABELS = {
    'encrypt': "🔒 Cifrar",
    'decrypt': "🔓 Descifrar",
    'generate': "⚙️ Generar",
    'copy': "📋 Copiar",
    'paste': "📋 Pegar",
    'clear': "🗑️ Limpiar",
    'save': "💾 Guardar",
    'load': "📁 Cargar",
    'help': "❓ Ayuda",
    'about': "ℹ️ Acerca de",
    'exit': "🚪 Salir",
    'back': "← Atrás",
    'next': "Siguiente →",
    'cancel': "Cancelar",
    'ok': "Aceptar",
    'analyze': "🔍 Analizar",
    'verify': "✅ Verificar",
    'compress': "📦 Comprimir",
    'decompress': "📤 Descomprimir"
}

# Etiquetas de menú
MENU_LABELS = {
    'classic_crypto': "📚 Criptografía Clásica",
    'modern_crypto': "🔒 Criptografía Moderna",
    'tools': "🛠️ Herramientas",
    'about': "ℹ️ Acerca de",
    'caesar': "Cifrado César",
    'vigenere': "Cifrado Vigenère",
    'playfair': "Cifrado Playfair",
    'kasiski': "Método de Kasiski",
    'rsa': "Algoritmo RSA",
    'hash': "Funciones Hash",
    'des': "Cifrado DES",
    'digital_signature': "Firma Digital",
    'huffman': "Codificación Huffman",
    'blockchain': "Simulador Blockchain",
    'integrity': "Verificador de Integridad"
}

# ===== CONSTANTES CRIPTOGRÁFICAS =====

# Alfabeto inglés
ENGLISH_ALPHABET = string.ascii_uppercase
ENGLISH_ALPHABET_LOWER = string.ascii_lowercase
ALPHABET_SIZE = 26

# Alfabeto español (incluyendo Ñ)
SPANISH_ALPHABET = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
SPANISH_ALPHABET_LOWER = "abcdefghijklmnñopqrstuvwxyz"
SPANISH_ALPHABET_SIZE = 27

# Caracteres especiales
DIGITS = string.digits
PUNCTUATION = string.punctuation
WHITESPACE = string.whitespace
PRINTABLE = string.printable

# Alfabeto por defecto (inglés)
DEFAULT_ALPHABET = ENGLISH_ALPHABET
DEFAULT_ALPHABET_LOWER = ENGLISH_ALPHABET_LOWER
DEFAULT_ALPHABET_SIZE = ALPHABET_SIZE

# ===== CONSTANTES DE CIFRADO CÉSAR =====
CAESAR_MIN_KEY = 1
CAESAR_MAX_KEY = 25
CAESAR_DEFAULT_KEY = 3

# ===== CONSTANTES DE CIFRADO VIGENÈRE =====
VIGENERE_MIN_KEY_LENGTH = 2
VIGENERE_MAX_KEY_LENGTH = 50

# ===== CONSTANTES DE CIFRADO PLAYFAIR =====
PLAYFAIR_MATRIX_SIZE = 5
PLAYFAIR_ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # Sin J
PLAYFAIR_SUBSTITUTE_CHAR = "X"
PLAYFAIR_DUPLICATE_CHAR = "J"
PLAYFAIR_REPLACEMENT_CHAR = "I"

# ===== CONSTANTES DE RSA =====
RSA_KEY_SIZES = [512, 1024, 2048, 4096]
RSA_DEFAULT_KEY_SIZE = 1024
RSA_MIN_KEY_SIZE = 512
RSA_MAX_KEY_SIZE = 4096
RSA_PUBLIC_EXPONENT = 65537  # Comúnmente usado

# Números primos pequeños para testing
SMALL_PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151,
    157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233,
    239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317
]

# ===== CONSTANTES DE HASH =====
HASH_ALGORITHMS = {
    'MD5': 128,      # bits
    'SHA1': 160,     # bits
    'SHA256': 256,   # bits
    'SHA512': 512,   # bits
    'Custom64': 64,  # bits
    'Custom128': 128, # bits
    'Custom256': 256  # bits
}

HASH_DEFAULT_ALGORITHM = 'SHA256'

# ===== CONSTANTES DE DES =====
DES_KEY_SIZE = 8  # bytes
DES_BLOCK_SIZE = 8  # bytes
DES_MODES = ['ECB', 'CBC']
DES_DEFAULT_MODE = 'CBC'

# ===== CONSTANTES DE HUFFMAN =====
HUFFMAN_EOF_SYMBOL = "EOF"
HUFFMAN_SEPARATOR = "|"

# ===== CONSTANTES DE BLOCKCHAIN =====
BLOCKCHAIN_GENESIS_BLOCK = "Genesis Block"
BLOCKCHAIN_HASH_ALGORITHM = "SHA256"
BLOCKCHAIN_DIFFICULTY = 4  # Número de ceros al inicio del hash

# ===== CONSTANTES DE VALIDACIÓN =====
VALIDATION_RULES = {
    'min_text_length': 1,
    'max_text_length': 1000000,  # 1MB
    'min_key_length': 1,
    'max_key_length': 100,
    'min_file_size': 1,
    'max_file_size': 50 * 1024 * 1024,  # 50MB
    'allowed_extensions': ['.txt', '.md', '.rtf', '.json', '.xml']
}

# ===== CONSTANTES DE ARCHIVOS =====
FILE_EXTENSIONS = {
    'text': ['.txt', '.md', '.rtf'],
    'data': ['.json', '.xml', '.csv'],
    'image': ['.png', '.jpg', '.jpeg', '.gif', '.bmp'],
    'executable': ['.exe', '.msi', '.app', '.deb', '.rpm'],
    'archive': ['.zip', '.rar', '.7z', '.tar', '.gz']
}

DEFAULT_ENCODING = 'utf-8'
BACKUP_ENCODING = 'latin-1'

# ===== CONSTANTES DE COLORES =====
COLORS = {
    'primary': '#007bff',
    'secondary': '#6c757d',
    'success': '#28a745',
    'warning': '#ffc107',
    'danger': '#dc3545',
    'info': '#17a2b8',
    'light': '#f8f9fa',
    'dark': '#343a40',
    'white': '#ffffff',
    'black': '#000000',
    'gray': '#6c757d',
    'red': '#dc3545',
    'green': '#28a745',
    'blue': '#007bff',
    'yellow': '#ffc107',
    'orange': '#fd7e14',
    'purple': '#6f42c1',
    'pink': '#e83e8c',
    'cyan': '#17a2b8'
}

# ===== CONSTANTES DE REGEX =====
REGEX_PATTERNS = {
    'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'phone': r'^\+?1?\d{9,15}$',
    'url': r'^https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?$',
    'ipv4': r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
    'hex': r'^[0-9a-fA-F]+$',
    'binary': r'^[01]+$',
    'alphabetic': r'^[a-zA-Z]+$',
    'alphanumeric': r'^[a-zA-Z0-9]+$',
    'numeric': r'^[0-9]+$'
}

# ===== CONSTANTES DE TESTING =====
TEST_CASES = {
    'caesar': {
        'text': "HELLO WORLD",
        'key': 3,
        'expected': "KHOOR ZRUOG"
    },
    'vigenere': {
        'text': "HELLO WORLD",
        'key': "KEY",
        'expected': "RIJVS UYVJN"
    },
    'playfair': {
        'text': "HELLO WORLD",
        'key': "MONARCHY",
        'expected': "GATLM ZCLRQ"
    },
    'rsa': {
        'p': 61,
        'q': 53,
        'n': 3233,
        'e': 17,
        'd': 2753
    }
}

# ===== CONSTANTES DE PERFORMANCE =====
PERFORMANCE_LIMITS = {
    'max_threads': 4,
    'timeout_seconds': 30,
    'chunk_size': 8192,
    'cache_size': 100,
    'max_memory_mb': 512
}

# ===== CONSTANTES DE LOGGING =====
LOG_LEVELS = {
    'DEBUG': 10,
    'INFO': 20,
    'WARNING': 30,
    'ERROR': 40,
    'CRITICAL': 50
}

LOG_FORMATS = {
    'simple': '%(levelname)s - %(message)s',
    'detailed': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'debug': '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
}

# ===== FUNCIONES AUXILIARES =====
def get_alphabet(language: str = 'english') -> str:
    """Obtener alfabeto según idioma"""
    if language.lower() == 'spanish':
        return SPANISH_ALPHABET
    return ENGLISH_ALPHABET

def get_alphabet_size(language: str = 'english') -> int:
    """Obtener tamaño del alfabeto según idioma"""
    if language.lower() == 'spanish':
        return SPANISH_ALPHABET_SIZE
    return ALPHABET_SIZE

def is_valid_key_size(algorithm: str, key_size: int) -> bool:
    """Verificar si el tamaño de clave es válido"""
    if algorithm.upper() == 'RSA':
        return key_size in RSA_KEY_SIZES
    elif algorithm.upper() == 'CAESAR':
        return CAESAR_MIN_KEY <= key_size <= CAESAR_MAX_KEY
    elif algorithm.upper() == 'VIGENERE':
        return VIGENERE_MIN_KEY_LENGTH <= key_size <= VIGENERE_MAX_KEY_LENGTH
    return False

def get_hash_bit_size(algorithm: str) -> int:
    """Obtener tamaño en bits del algoritmo hash"""
    return HASH_ALGORITHMS.get(algorithm.upper(), 0)

# ===== EXPORTAR CONSTANTES =====
__all__ = [
    'APP_TITLE', 'APP_VERSION', 'APP_AUTHOR', 'COPYRIGHT',
    'WINDOW_TITLE', 'WINDOW_ICON', 'MESSAGES', 'BUTTON_LABELS', 'MENU_LABELS',
    'ENGLISH_ALPHABET', 'SPANISH_ALPHABET', 'DEFAULT_ALPHABET', 'ALPHABET_SIZE',
    'CAESAR_MIN_KEY', 'CAESAR_MAX_KEY', 'CAESAR_DEFAULT_KEY',
    'VIGENERE_MIN_KEY_LENGTH', 'VIGENERE_MAX_KEY_LENGTH',
    'PLAYFAIR_MATRIX_SIZE', 'PLAYFAIR_ALPHABET', 'PLAYFAIR_SUBSTITUTE_CHAR', 'PLAYFAIR_DUPLICATE_CHAR', 'PLAYFAIR_REPLACEMENT_CHAR',
    'RSA_KEY_SIZES', 'RSA_DEFAULT_KEY_SIZE', 'SMALL_PRIMES',
    'HASH_ALGORITHMS', 'HASH_DEFAULT_ALGORITHM',
    'DES_KEY_SIZE', 'DES_BLOCK_SIZE', 'DES_MODES',
    'VALIDATION_RULES', 'FILE_EXTENSIONS', 'DEFAULT_ENCODING',
    'COLORS', 'REGEX_PATTERNS', 'TEST_CASES', 'PERFORMANCE_LIMITS',
    'LOG_LEVELS', 'LOG_FORMATS',
    'get_alphabet', 'get_alphabet_size', 'is_valid_key_size', 'get_hash_bit_size'
]
