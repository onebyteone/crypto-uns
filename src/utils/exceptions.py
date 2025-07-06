"""
⚠️ Excepciones Personalizadas - CryptoUNS
========================================

Archivo que define todas las excepciones personalizadas del sistema CryptoUNS.
Proporciona manejo de errores específico para diferentes componentes.

Autor: CryptoUNS Team
Fecha: 06 de julio, 2025
Versión: 1.0.0
"""

from typing import Optional, Any, Dict
import logging

# ===== EXCEPCIÓN BASE =====
class CryptoUNSError(Exception):
    """
    Excepción base para todos los errores del sistema CryptoUNS
    """
    def __init__(self, message: str, error_code: str = "CRYPTO_000", details: Optional[Dict] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)
    
    def __str__(self):
        return f"[{self.error_code}] {self.message}"
    
    def get_full_error(self):
        """Obtener error completo con detalles"""
        error_info = {
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details
        }
        return error_info

# ===== EXCEPCIONES DE CRIPTOGRAFÍA =====
class CryptographyError(CryptoUNSError):
    """Excepción base para errores criptográficos"""
    def __init__(self, message: str, error_code: str = "CRYPTO_001", details: Optional[Dict] = None):
        super().__init__(message, error_code, details)

class InvalidKeyError(CryptographyError):
    """Error de clave inválida"""
    def __init__(self, message: str = "Clave inválida", key_type: str = "unknown", details: Optional[Dict] = None):
        self.key_type = key_type
        error_code = "CRYPTO_002"
        if details is None:
            details = {}
        details["key_type"] = key_type
        super().__init__(message, error_code, details)

class InvalidInputError(CryptographyError):
    """Error de entrada inválida"""
    def __init__(self, message: str = "Entrada inválida", input_type: str = "text", details: Optional[Dict] = None):
        self.input_type = input_type
        error_code = "CRYPTO_003"
        if details is None:
            details = {}
        details["input_type"] = input_type
        super().__init__(message, error_code, details)

class EncryptionError(CryptographyError):
    """Error durante el proceso de cifrado"""
    def __init__(self, message: str = "Error en el cifrado", algorithm: str = "unknown", details: Optional[Dict] = None):
        self.algorithm = algorithm
        error_code = "CRYPTO_004"
        if details is None:
            details = {}
        details["algorithm"] = algorithm
        super().__init__(message, error_code, details)

class DecryptionError(CryptographyError):
    """Error durante el proceso de descifrado"""
    def __init__(self, message: str = "Error en el descifrado", algorithm: str = "unknown", details: Optional[Dict] = None):
        self.algorithm = algorithm
        error_code = "CRYPTO_005"
        if details is None:
            details = {}
        details["algorithm"] = algorithm
        super().__init__(message, error_code, details)

class KeyGenerationError(CryptographyError):
    """Error durante la generación de claves"""
    def __init__(self, message: str = "Error en la generación de claves", algorithm: str = "unknown", details: Optional[Dict] = None):
        self.algorithm = algorithm
        error_code = "CRYPTO_006"
        if details is None:
            details = {}
        details["algorithm"] = algorithm
        super().__init__(message, error_code, details)

class HashError(CryptographyError):
    """Error en funciones hash"""
    def __init__(self, message: str = "Error en función hash", hash_type: str = "unknown", details: Optional[Dict] = None):
        self.hash_type = hash_type
        error_code = "CRYPTO_007"
        if details is None:
            details = {}
        details["hash_type"] = hash_type
        super().__init__(message, error_code, details)

class SignatureError(CryptographyError):
    """Error en firma digital"""
    def __init__(self, message: str = "Error en firma digital", operation: str = "unknown", details: Optional[Dict] = None):
        self.operation = operation
        error_code = "CRYPTO_008"
        if details is None:
            details = {}
        details["operation"] = operation
        super().__init__(message, error_code, details)

# ===== EXCEPCIONES DE VALIDACIÓN =====
class ValidationError(CryptoUNSError):
    """Excepción base para errores de validación"""
    def __init__(self, message: str, error_code: str = "VALID_001", details: Optional[Dict] = None):
        super().__init__(message, error_code, details)

class InvalidLengthError(ValidationError):
    """Error de longitud inválida"""
    def __init__(self, message: str = "Longitud inválida", min_length: int = 0, max_length: int = 0, actual_length: int = 0, details: Optional[Dict] = None):
        self.min_length = min_length
        self.max_length = max_length
        self.actual_length = actual_length
        error_code = "VALID_002"
        if details is None:
            details = {}
        details.update({
            "min_length": min_length,
            "max_length": max_length,
            "actual_length": actual_length
        })
        super().__init__(message, error_code, details)

class InvalidFormatError(ValidationError):
    """Error de formato inválido"""
    def __init__(self, message: str = "Formato inválido", expected_format: str = "unknown", actual_format: str = "unknown", details: Optional[Dict] = None):
        self.expected_format = expected_format
        self.actual_format = actual_format
        error_code = "VALID_003"
        if details is None:
            details = {}
        details.update({
            "expected_format": expected_format,
            "actual_format": actual_format
        })
        super().__init__(message, error_code, details)

class InvalidRangeError(ValidationError):
    """Error de rango inválido"""
    def __init__(self, message: str = "Valor fuera de rango", min_value: Any = None, max_value: Any = None, actual_value: Any = None, details: Optional[Dict] = None):
        self.min_value = min_value
        self.max_value = max_value
        self.actual_value = actual_value
        error_code = "VALID_004"
        if details is None:
            details = {}
        details.update({
            "min_value": min_value,
            "max_value": max_value,
            "actual_value": actual_value
        })
        super().__init__(message, error_code, details)

# ===== EXCEPCIONES DE ARCHIVOS =====
class FileError(CryptoUNSError):
    """Excepción base para errores de archivos"""
    def __init__(self, message: str, error_code: str = "FILE_001", details: Optional[Dict] = None):
        super().__init__(message, error_code, details)

class FileNotFoundError(FileError):
    """Error de archivo no encontrado"""
    def __init__(self, message: str = "Archivo no encontrado", file_path: str = "", details: Optional[Dict] = None):
        self.file_path = file_path
        error_code = "FILE_002"
        if details is None:
            details = {}
        details["file_path"] = file_path
        super().__init__(message, error_code, details)

class FilePermissionError(FileError):
    """Error de permisos de archivo"""
    def __init__(self, message: str = "Permisos insuficientes", file_path: str = "", operation: str = "unknown", details: Optional[Dict] = None):
        self.file_path = file_path
        self.operation = operation
        error_code = "FILE_003"
        if details is None:
            details = {}
        details.update({
            "file_path": file_path,
            "operation": operation
        })
        super().__init__(message, error_code, details)

class FileSizeError(FileError):
    """Error de tamaño de archivo"""
    def __init__(self, message: str = "Tamaño de archivo inválido", file_path: str = "", file_size: int = 0, max_size: int = 0, details: Optional[Dict] = None):
        self.file_path = file_path
        self.file_size = file_size
        self.max_size = max_size
        error_code = "FILE_004"
        if details is None:
            details = {}
        details.update({
            "file_path": file_path,
            "file_size": file_size,
            "max_size": max_size
        })
        super().__init__(message, error_code, details)

class FileFormatError(FileError):
    """Error de formato de archivo"""
    def __init__(self, message: str = "Formato de archivo inválido", file_path: str = "", expected_format: str = "unknown", actual_format: str = "unknown", details: Optional[Dict] = None):
        self.file_path = file_path
        self.expected_format = expected_format
        self.actual_format = actual_format
        error_code = "FILE_005"
        if details is None:
            details = {}
        details.update({
            "file_path": file_path,
            "expected_format": expected_format,
            "actual_format": actual_format
        })
        super().__init__(message, error_code, details)

# ===== EXCEPCIONES DE INTERFAZ =====
class GUIError(CryptoUNSError):
    """Excepción base para errores de interfaz gráfica"""
    def __init__(self, message: str, error_code: str = "GUI_001", details: Optional[Dict] = None):
        super().__init__(message, error_code, details)

class ComponentError(GUIError):
    """Error en componentes de la interfaz"""
    def __init__(self, message: str = "Error en componente", component_name: str = "unknown", details: Optional[Dict] = None):
        self.component_name = component_name
        error_code = "GUI_002"
        if details is None:
            details = {}
        details["component_name"] = component_name
        super().__init__(message, error_code, details)

class ThemeError(GUIError):
    """Error en tema de la interfaz"""
    def __init__(self, message: str = "Error en tema", theme_name: str = "unknown", details: Optional[Dict] = None):
        self.theme_name = theme_name
        error_code = "GUI_003"
        if details is None:
            details = {}
        details["theme_name"] = theme_name
        super().__init__(message, error_code, details)

class WindowError(GUIError):
    """Error en ventana de la aplicación"""
    def __init__(self, message: str = "Error en ventana", window_name: str = "unknown", details: Optional[Dict] = None):
        self.window_name = window_name
        error_code = "GUI_004"
        if details is None:
            details = {}
        details["window_name"] = window_name
        super().__init__(message, error_code, details)

# ===== EXCEPCIONES DE CONFIGURACIÓN =====
class ConfigurationError(CryptoUNSError):
    """Excepción base para errores de configuración"""
    def __init__(self, message: str, error_code: str = "CONFIG_001", details: Optional[Dict] = None):
        super().__init__(message, error_code, details)

class InvalidConfigError(ConfigurationError):
    """Error de configuración inválida"""
    def __init__(self, message: str = "Configuración inválida", config_key: str = "unknown", details: Optional[Dict] = None):
        self.config_key = config_key
        error_code = "CONFIG_002"
        if details is None:
            details = {}
        details["config_key"] = config_key
        super().__init__(message, error_code, details)

class MissingConfigError(ConfigurationError):
    """Error de configuración faltante"""
    def __init__(self, message: str = "Configuración faltante", config_key: str = "unknown", details: Optional[Dict] = None):
        self.config_key = config_key
        error_code = "CONFIG_003"
        if details is None:
            details = {}
        details["config_key"] = config_key
        super().__init__(message, error_code, details)

# ===== EXCEPCIONES DE ALGORITMOS ESPECÍFICOS =====
class CaesarCipherError(CryptographyError):
    """Error específico del cifrado César"""
    def __init__(self, message: str = "Error en cifrado César", key: int = 0, details: Optional[Dict] = None):
        self.key = key
        error_code = "CAESAR_001"
        if details is None:
            details = {}
        details["key"] = key
        super().__init__(message, error_code, details)

class VigenereCipherError(CryptographyError):
    """Error específico del cifrado Vigenère"""
    def __init__(self, message: str = "Error en cifrado Vigenère", key: str = "", details: Optional[Dict] = None):
        self.key = key
        error_code = "VIGENERE_001"
        if details is None:
            details = {}
        details["key"] = key
        super().__init__(message, error_code, details)

class PlayfairCipherError(CryptographyError):
    """Error específico del cifrado Playfair"""
    def __init__(self, message: str = "Error en cifrado Playfair", key: str = "", details: Optional[Dict] = None):
        self.key = key
        error_code = "PLAYFAIR_001"
        if details is None:
            details = {}
        details["key"] = key
        super().__init__(message, error_code, details)

class RSAError(CryptographyError):
    """Error específico del algoritmo RSA"""
    def __init__(self, message: str = "Error en RSA", operation: str = "unknown", details: Optional[Dict] = None):
        self.operation = operation
        error_code = "RSA_001"
        if details is None:
            details = {}
        details["operation"] = operation
        super().__init__(message, error_code, details)

class DESError(CryptographyError):
    """Error específico del cifrado DES"""
    def __init__(self, message: str = "Error en DES", mode: str = "unknown", details: Optional[Dict] = None):
        self.mode = mode
        error_code = "DES_001"
        if details is None:
            details = {}
        details["mode"] = mode
        super().__init__(message, error_code, details)

class HuffmanError(CryptographyError):
    """Error específico de codificación Huffman"""
    def __init__(self, message: str = "Error en codificación Huffman", operation: str = "unknown", details: Optional[Dict] = None):
        self.operation = operation
        error_code = "HUFFMAN_001"
        if details is None:
            details = {}
        details["operation"] = operation
        super().__init__(message, error_code, details)

class BlockchainError(CryptographyError):
    """Error específico de blockchain"""
    def __init__(self, message: str = "Error en blockchain", operation: str = "unknown", details: Optional[Dict] = None):
        self.operation = operation
        error_code = "BLOCKCHAIN_001"
        if details is None:
            details = {}
        details["operation"] = operation
        super().__init__(message, error_code, details)

class KasiskiError(CryptographyError):
    """Error específico del método de Kasiski"""
    def __init__(self, message: str = "Error en método de Kasiski", analysis_type: str = "unknown", details: Optional[Dict] = None):
        self.analysis_type = analysis_type
        error_code = "KASISKI_001"
        if details is None:
            details = {}
        details["analysis_type"] = analysis_type
        super().__init__(message, error_code, details)

# ===== MANEJADOR DE EXCEPCIONES =====
class ExceptionHandler:
    """Manejador centralizado de excepciones"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger("CryptoUNS")
    
    def handle_exception(self, exception: Exception, context: str = "unknown"):
        """Manejar excepción y registrar en log"""
        if isinstance(exception, CryptoUNSError):
            self.logger.error(f"Error en {context}: {exception}")
            return exception.get_full_error()
        else:
            self.logger.error(f"Error no controlado en {context}: {exception}")
            return {
                "error_code": "UNKNOWN_001",
                "message": str(exception),
                "context": context,
                "details": {}
            }
    
    def log_error(self, error_code: str, message: str, details: Optional[Dict] = None):
        """Registrar error en log"""
        error_info = {
            "error_code": error_code,
            "message": message,
            "details": details or {}
        }
        self.logger.error(f"[{error_code}] {message}")
        return error_info

# ===== FUNCIONES AUXILIARES =====
def create_error_response(error: Exception, context: str = "unknown") -> Dict:
    """Crear respuesta de error estandarizada"""
    if isinstance(error, CryptoUNSError):
        return {
            "success": False,
            "error": error.get_full_error(),
            "context": context
        }
    else:
        return {
            "success": False,
            "error": {
                "error_code": "UNKNOWN_001",
                "message": str(error),
                "details": {}
            },
            "context": context
        }

def validate_and_raise(condition: bool, exception: Exception):
    """Validar condición y lanzar excepción si es falsa"""
    if not condition:
        raise exception

# ===== DECORADORES PARA MANEJO DE ERRORES =====
def handle_crypto_errors(func):
    """Decorador para manejar errores criptográficos"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CryptographyError as e:
            logger = logging.getLogger("CryptoUNS")
            logger.error(f"Error criptográfico en {func.__name__}: {e}")
            raise
        except Exception as e:
            logger = logging.getLogger("CryptoUNS")
            logger.error(f"Error no controlado en {func.__name__}: {e}")
            raise CryptographyError(f"Error inesperado en {func.__name__}: {str(e)}")
    return wrapper

def handle_validation_errors(func):
    """Decorador para manejar errores de validación"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            logger = logging.getLogger("CryptoUNS")
            logger.error(f"Error de validación en {func.__name__}: {e}")
            raise
        except Exception as e:
            logger = logging.getLogger("CryptoUNS")
            logger.error(f"Error no controlado en {func.__name__}: {e}")
            raise ValidationError(f"Error inesperado en {func.__name__}: {str(e)}")
    return wrapper

def handle_file_errors(func):
    """Decorador para manejar errores de archivos"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileError as e:
            logger = logging.getLogger("CryptoUNS")
            logger.error(f"Error de archivo en {func.__name__}: {e}")
            raise
        except Exception as e:
            logger = logging.getLogger("CryptoUNS")
            logger.error(f"Error no controlado en {func.__name__}: {e}")
            raise FileError(f"Error inesperado en {func.__name__}: {str(e)}")
    return wrapper

# ===== EXPORTAR EXCEPCIONES =====
__all__ = [
    # Excepciones base
    'CryptoUNSError',
    
    # Excepciones criptográficas
    'CryptographyError', 'InvalidKeyError', 'InvalidInputError', 'EncryptionError',
    'DecryptionError', 'KeyGenerationError', 'HashError', 'SignatureError',
    
    # Excepciones de validación
    'ValidationError', 'InvalidLengthError', 'InvalidFormatError', 'InvalidRangeError',
    
    # Excepciones de archivos
    'FileError', 'FileNotFoundError', 'FilePermissionError', 'FileSizeError', 'FileFormatError',
    
    # Excepciones de interfaz
    'GUIError', 'ComponentError', 'ThemeError', 'WindowError',
    
    # Excepciones de configuración
    'ConfigurationError', 'InvalidConfigError', 'MissingConfigError',
    
    # Excepciones de algoritmos específicos
    'CaesarCipherError', 'VigenereCipherError', 'PlayfairCipherError', 'RSAError',
    'DESError', 'HuffmanError', 'BlockchainError', 'KasiskiError',
    
    # Utilidades
    'ExceptionHandler', 'create_error_response', 'validate_and_raise',
    
    # Decoradores
    'handle_crypto_errors', 'handle_validation_errors', 'handle_file_errors'
]
