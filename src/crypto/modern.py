"""
🔒 Criptografía Moderna - CryptoUNS
=================================

Implementación de algoritmos de criptografía moderna:
- RSA (Rivest-Shamir-Adleman)
- Funciones Hash personalizadas
- DES (Data Encryption Standard)
- Firma Digital

Autor: CryptoUNS Team
Fecha: 06 de julio, 2025
Versión: 1.0.0
"""

import random
import math
from typing import Optional, Tuple, Dict, List, Any
import hashlib
import struct
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import secrets

# Importar constantes y excepciones
try:
    from ..utils.constants import *
    from ..utils.exceptions import *
except ImportError:
    # Importación absoluta para cuando se ejecuta directamente
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from utils.constants import *
    from utils.exceptions import *

# ===== ALGORITMO RSA =====
class RSACipher:
    """
    Implementación del algoritmo RSA
    
    RSA es un algoritmo de criptografía asimétrica que utiliza un par de claves
    (pública y privada) para cifrar y descifrar datos.
    """
    
    def __init__(self, key_size: int = RSA_DEFAULT_KEY_SIZE):
        """
        Inicializar cifrado RSA
        
        Args:
            key_size (int): Tamaño de la clave en bits
        """
        self.key_size = key_size
        self.public_key = None
        self.private_key = None
        
    def is_prime(self, n: int, k: int = 10) -> bool:
        """
        Test de primalidad de Miller-Rabin
        
        Args:
            n (int): Número a verificar
            k (int): Número de rondas del test
            
        Returns:
            bool: True si es probablemente primo, False si es compuesto
        """
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False
        
        # Escribir n-1 como d * 2^r
        r = 0
        d = n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        
        # Test de Miller-Rabin
        for _ in range(k):
            a = random.randrange(2, n - 1)
            x = pow(a, d, n)
            
            if x == 1 or x == n - 1:
                continue
            
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        
        return True
    
    def generate_prime(self, bits: int) -> int:
        """
        Generar un número primo de cierto tamaño
        
        Args:
            bits (int): Número de bits del primo
            
        Returns:
            int: Número primo generado
        """
        while True:
            # Generar número aleatorio impar
            n = random.getrandbits(bits)
            n |= (1 << bits - 1) | 1  # Asegurar que sea impar y del tamaño correcto
            
            # Verificar si es primo
            if self.is_prime(n):
                return n
    
    def gcd(self, a: int, b: int) -> int:
        """
        Calcular el máximo común divisor
        
        Args:
            a (int): Primer número
            b (int): Segundo número
            
        Returns:
            int: MCD de a y b
        """
        while b:
            a, b = b, a % b
        return a
    
    def extended_gcd(self, a: int, b: int) -> Tuple[int, int, int]:
        """
        Algoritmo extendido de Euclides
        
        Args:
            a (int): Primer número
            b (int): Segundo número
            
        Returns:
            Tuple[int, int, int]: (gcd, x, y) donde ax + by = gcd
        """
        if a == 0:
            return b, 0, 1
        
        gcd, x1, y1 = self.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        
        return gcd, x, y
    
    def mod_inverse(self, a: int, m: int) -> int:
        """
        Calcular el inverso modular de a módulo m
        
        Args:
            a (int): Número base
            m (int): Módulo
            
        Returns:
            int: Inverso modular
            
        Raises:
            ValueError: Si el inverso no existe
        """
        gcd, x, _ = self.extended_gcd(a, m)
        if gcd != 1:
            raise ValueError("El inverso modular no existe")
        return (x % m + m) % m
    
    def generate_keys(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """
        Generar par de claves RSA
        
        Returns:
            Tuple: ((e, n), (d, n)) - (clave_pública, clave_privada)
        """
        # Generar dos números primos grandes
        bits = self.key_size // 2
        p = self.generate_prime(bits)
        q = self.generate_prime(bits)
        
        # Asegurar que p != q
        while p == q:
            q = self.generate_prime(bits)
        
        # Calcular n y φ(n)
        n = p * q
        phi_n = (p - 1) * (q - 1)
        
        # Elegir e (exponente público)
        e = 65537  # Valor comúnmente usado
        while self.gcd(e, phi_n) != 1:
            e += 2
        
        # Calcular d (exponente privado)
        d = self.mod_inverse(e, phi_n)
        
        # Almacenar claves
        self.public_key = (e, n)
        self.private_key = (d, n)
        
        return self.public_key, self.private_key
    
    def encrypt(self, message: str, public_key: Optional[Tuple[int, int]] = None) -> List[int]:
        """
        Cifrar mensaje usando RSA
        
        Args:
            message (str): Mensaje a cifrar
            public_key (Optional[Tuple[int, int]]): Clave pública (e, n)
            
        Returns:
            List[int]: Lista de bloques cifrados
        """
        if not message:
            raise InvalidInputError("El mensaje no puede estar vacío")
        
        # Usar clave pública proporcionada o la generada
        if public_key:
            e, n = public_key
        elif self.public_key:
            e, n = self.public_key
        else:
            raise KeyGenerationError("No hay clave pública disponible")
        
        # Convertir mensaje a bytes
        message_bytes = message.encode('utf-8')
        
        # Calcular tamaño máximo de bloque
        block_size = (n.bit_length() - 1) // 8
        
        # Cifrar en bloques
        encrypted_blocks = []
        for i in range(0, len(message_bytes), block_size):
            block = message_bytes[i:i + block_size]
            # Convertir bytes a entero
            block_int = int.from_bytes(block, 'big')
            
            # Verificar que el bloque sea menor que n
            if block_int >= n:
                raise EncryptionError("El bloque es demasiado grande para la clave")
            
            # Cifrar bloque
            encrypted_block = pow(block_int, e, n)
            encrypted_blocks.append(encrypted_block)
        
        return encrypted_blocks
    
    def decrypt(self, encrypted_blocks: List[int], private_key: Optional[Tuple[int, int]] = None) -> str:
        """
        Descifrar bloques cifrados usando RSA
        
        Args:
            encrypted_blocks (List[int]): Lista de bloques cifrados
            private_key (Optional[Tuple[int, int]]): Clave privada (d, n)
            
        Returns:
            str: Mensaje descifrado
        """
        if not encrypted_blocks:
            raise InvalidInputError("No hay bloques para descifrar")
        
        # Usar clave privada proporcionada o la generada
        if private_key:
            d, n = private_key
        elif self.private_key:
            d, n = self.private_key
        else:
            raise KeyGenerationError("No hay clave privada disponible")
        
        # Calcular tamaño máximo de bloque
        block_size = (n.bit_length() - 1) // 8
        
        # Descifrar bloques
        decrypted_bytes = bytearray()
        for encrypted_block in encrypted_blocks:
            # Descifrar bloque
            decrypted_block = pow(encrypted_block, d, n)
            
            # Convertir a bytes
            block_bytes = decrypted_block.to_bytes((decrypted_block.bit_length() + 7) // 8, 'big')
            decrypted_bytes.extend(block_bytes)
        
        # Convertir a string
        return decrypted_bytes.decode('utf-8')
    
    def validate_key_size(self, key_size: int) -> bool:
        """
        Validar tamaño de clave RSA
        
        Args:
            key_size (int): Tamaño de clave en bits
            
        Returns:
            bool: True si es válido
        """
        return key_size in RSA_KEY_SIZES
    
    def get_key_info(self) -> Dict[str, Any]:
        """
        Obtener información sobre las claves generadas
        
        Returns:
            Dict: Información de las claves
        """
        if not self.public_key or not self.private_key:
            return {"error": "No hay claves generadas"}
        
        e, n = self.public_key
        d, _ = self.private_key
        
        return {
            "key_size": self.key_size,
            "public_key": {
                "e": e,
                "n": n,
                "n_bits": n.bit_length()
            },
            "private_key": {
                "d": d,
                "n": n
            },
            "n_hex": hex(n),
            "e_hex": hex(e),
            "d_hex": hex(d)
        }

# ===== FUNCIONES HASH PERSONALIZADAS =====
class CustomHash:
    """
    Implementación de funciones hash personalizadas
    """
    
    def __init__(self):
        """Inicializar generador de hash"""
        pass
    
    def hash_64(self, data: str) -> str:
        """
        Función hash personalizada de 64 bits
        
        Args:
            data (str): Datos a hashear
            
        Returns:
            str: Hash de 64 bits en hexadecimal
        """
        if not data:
            raise InvalidInputError("Los datos no pueden estar vacíos")
        
        # Convertir a bytes
        data_bytes = data.encode('utf-8')
        
        # Inicializar valor hash
        hash_val = 0x811c9dc5  # Valor inicial FNV
        
        # Procesar cada byte
        for byte in data_bytes:
            hash_val ^= byte
            hash_val *= 0x01000193  # Multiplicador FNV
            hash_val &= 0xFFFFFFFFFFFFFFFF  # Mantener 64 bits
        
        # Mezclar bits adicional
        hash_val ^= hash_val >> 32
        hash_val ^= hash_val >> 16
        hash_val ^= hash_val >> 8
        hash_val &= 0xFFFFFFFFFFFFFFFF
        
        return f"{hash_val:016x}"
    
    def hash_128(self, data: str) -> str:
        """
        Función hash personalizada de 128 bits
        
        Args:
            data (str): Datos a hashear
            
        Returns:
            str: Hash de 128 bits en hexadecimal
        """
        if not data:
            raise InvalidInputError("Los datos no pueden estar vacíos")
        
        # Usar dos funciones hash de 64 bits con semillas diferentes
        data_bytes = data.encode('utf-8')
        
        # Primera mitad
        hash1 = 0x811c9dc5
        for i, byte in enumerate(data_bytes):
            hash1 ^= byte
            hash1 *= 0x01000193
            hash1 ^= i  # Añadir posición como variación
            hash1 &= 0xFFFFFFFFFFFFFFFF
        
        # Segunda mitad (procesamiento inverso)
        hash2 = 0x811c9dc5
        for i, byte in enumerate(reversed(data_bytes)):
            hash2 ^= byte
            hash2 *= 0x01000193
            hash2 ^= (i * 3)  # Diferente factor
            hash2 &= 0xFFFFFFFFFFFFFFFF
        
        return f"{hash1:016x}{hash2:016x}"
    
    def hash_256(self, data: str) -> str:
        """
        Función hash personalizada de 256 bits
        
        Args:
            data (str): Datos a hashear
            
        Returns:
            str: Hash de 256 bits en hexadecimal
        """
        if not data:
            raise InvalidInputError("Los datos no pueden estar vacíos")
        
        # Usar cuatro funciones hash de 64 bits con diferentes semillas
        data_bytes = data.encode('utf-8')
        
        # Cuatro hashes con diferentes procesamiento
        hashes = []
        seeds = [0x811c9dc5, 0x9E3779B9, 0x85ebca6b, 0xc2b2ae35]
        multipliers = [0x01000193, 0x40014141, 0x27d4eb2d, 0x165667b1]
        
        for seed, mult in zip(seeds, multipliers):
            hash_val = seed
            for i, byte in enumerate(data_bytes):
                hash_val ^= byte
                hash_val *= mult
                hash_val ^= (i * seed) & 0xFF
                hash_val &= 0xFFFFFFFFFFFFFFFF
            
            # Mezclar bits
            hash_val ^= hash_val >> 32
            hash_val ^= hash_val >> 16
            hash_val &= 0xFFFFFFFFFFFFFFFF
            
            hashes.append(f"{hash_val:016x}")
        
        return ''.join(hashes)
    
    def sha256_wrapper(self, data: str) -> str:
        """
        Wrapper para SHA-256 estándar
        
        Args:
            data (str): Datos a hashear
            
        Returns:
            str: Hash SHA-256 en hexadecimal
        """
        if not data:
            raise InvalidInputError("Los datos no pueden estar vacíos")
        
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
    
    def verify_integrity(self, data: str, expected_hash: str, algorithm: str = "256") -> bool:
        """
        Verificar integridad de datos usando hash
        
        Args:
            data (str): Datos originales
            expected_hash (str): Hash esperado
            algorithm (str): Algoritmo hash a usar
            
        Returns:
            bool: True si coinciden los hashes
        """
        if algorithm == "64":
            calculated_hash = self.hash_64(data)
        elif algorithm == "128":
            calculated_hash = self.hash_128(data)
        elif algorithm == "256":
            calculated_hash = self.hash_256(data)
        elif algorithm == "sha256":
            calculated_hash = self.sha256_wrapper(data)
        else:
            raise InvalidInputError(f"Algoritmo no soportado: {algorithm}")
        
        return calculated_hash.lower() == expected_hash.lower()

# ===== ALGORITMO DES =====
class DESCipher:
    """
    Implementación del algoritmo DES (Data Encryption Standard)
    """
    
    def __init__(self):
        """Inicializar cifrado DES"""
        pass
    
    def validate_key(self, key: str) -> bool:
        """
        Validar clave DES
        
        Args:
            key (str): Clave a validar
            
        Returns:
            bool: True si es válida
        """
        # DES requiere clave de 8 bytes (64 bits)
        return len(key) == 8
    
    def encrypt_ecb(self, plaintext: str, key: str) -> str:
        """
        Cifrar usando DES en modo ECB
        
        Args:
            plaintext (str): Texto plano
            key (str): Clave de 8 bytes
            
        Returns:
            str: Texto cifrado en hexadecimal
        """
        if not self.validate_key(key):
            raise InvalidKeyError("La clave DES debe tener exactamente 8 caracteres")
        
        if not plaintext:
            raise InvalidInputError("El texto no puede estar vacío")
        
        # Convertir clave a bytes
        key_bytes = key.encode('utf-8')
        
        # Crear cifrador DES
        cipher = DES.new(key_bytes, DES.MODE_ECB)
        
        # Rellenar texto para que sea múltiplo de 8
        plaintext_bytes = plaintext.encode('utf-8')
        padded_text = pad(plaintext_bytes, DES.block_size)
        
        # Cifrar
        ciphertext = cipher.encrypt(padded_text)
        
        return ciphertext.hex()
    
    def decrypt_ecb(self, ciphertext_hex: str, key: str) -> str:
        """
        Descifrar usando DES en modo ECB
        
        Args:
            ciphertext_hex (str): Texto cifrado en hexadecimal
            key (str): Clave de 8 bytes
            
        Returns:
            str: Texto descifrado
        """
        if not self.validate_key(key):
            raise InvalidKeyError("La clave DES debe tener exactamente 8 caracteres")
        
        if not ciphertext_hex:
            raise InvalidInputError("El texto cifrado no puede estar vacío")
        
        try:
            # Convertir hex a bytes
            ciphertext = bytes.fromhex(ciphertext_hex)
            
            # Convertir clave a bytes
            key_bytes = key.encode('utf-8')
            
            # Crear cifrador DES
            cipher = DES.new(key_bytes, DES.MODE_ECB)
            
            # Descifrar
            padded_plaintext = cipher.decrypt(ciphertext)
            
            # Quitar padding
            plaintext = unpad(padded_plaintext, DES.block_size)
            
            return plaintext.decode('utf-8')
        
        except Exception as e:
            raise DecryptionError(f"Error al descifrar: {str(e)}")
    
    def encrypt_cbc(self, plaintext: str, key: str, iv: Optional[str] = None) -> Tuple[str, str]:
        """
        Cifrar usando DES en modo CBC
        
        Args:
            plaintext (str): Texto plano
            key (str): Clave de 8 bytes
            iv (Optional[str]): Vector de inicialización (8 bytes)
            
        Returns:
            Tuple[str, str]: (texto_cifrado_hex, iv_hex)
        """
        if not self.validate_key(key):
            raise InvalidKeyError("La clave DES debe tener exactamente 8 caracteres")
        
        if not plaintext:
            raise InvalidInputError("El texto no puede estar vacío")
        
        # Generar IV si no se proporciona
        if iv is None:
            iv = secrets.token_bytes(8)
        else:
            iv = iv.encode('utf-8')
        
        if len(iv) != 8:
            raise InvalidInputError("El IV debe tener exactamente 8 bytes")
        
        # Convertir clave a bytes
        key_bytes = key.encode('utf-8')
        
        # Crear cifrador DES
        cipher = DES.new(key_bytes, DES.MODE_CBC, iv)
        
        # Rellenar texto
        plaintext_bytes = plaintext.encode('utf-8')
        padded_text = pad(plaintext_bytes, DES.block_size)
        
        # Cifrar
        ciphertext = cipher.encrypt(padded_text)
        
        return ciphertext.hex(), iv.hex()
    
    def decrypt_cbc(self, ciphertext_hex: str, key: str, iv_hex: str) -> str:
        """
        Descifrar usando DES en modo CBC
        
        Args:
            ciphertext_hex (str): Texto cifrado en hexadecimal
            key (str): Clave de 8 bytes
            iv_hex (str): IV en hexadecimal
            
        Returns:
            str: Texto descifrado
        """
        if not self.validate_key(key):
            raise InvalidKeyError("La clave DES debe tener exactamente 8 caracteres")
        
        if not ciphertext_hex or not iv_hex:
            raise InvalidInputError("El texto cifrado y el IV no pueden estar vacíos")
        
        try:
            # Convertir hex a bytes
            ciphertext = bytes.fromhex(ciphertext_hex)
            iv = bytes.fromhex(iv_hex)
            
            # Convertir clave a bytes
            key_bytes = key.encode('utf-8')
            
            # Crear cifrador DES
            cipher = DES.new(key_bytes, DES.MODE_CBC, iv)
            
            # Descifrar
            padded_plaintext = cipher.decrypt(ciphertext)
            
            # Quitar padding
            plaintext = unpad(padded_plaintext, DES.block_size)
            
            return plaintext.decode('utf-8')
        
        except Exception as e:
            raise DecryptionError(f"Error al descifrar: {str(e)}")

# ===== FIRMA DIGITAL =====
class DigitalSignature:
    """
    Implementación de firma digital usando RSA
    """
    
    def __init__(self):
        """Inicializar sistema de firma digital"""
        self.rsa = RSACipher()
        self.hash_func = CustomHash()
    
    def generate_keys(self, key_size: int = 2048) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """
        Generar par de claves para firma digital
        
        Args:
            key_size (int): Tamaño de clave en bits
            
        Returns:
            Tuple: (clave_pública, clave_privada)
        """
        self.rsa.key_size = key_size
        return self.rsa.generate_keys()
    
    def sign_message(self, message: str, private_key: Optional[Tuple[int, int]] = None) -> str:
        """
        Firmar un mensaje
        
        Args:
            message (str): Mensaje a firmar
            private_key (Optional[Tuple[int, int]]): Clave privada para firmar
            
        Returns:
            str: Firma digital en hexadecimal
        """
        if not message:
            raise InvalidInputError("El mensaje no puede estar vacío")
        
        # Generar hash del mensaje
        message_hash = self.hash_func.sha256_wrapper(message)
        
        # Usar clave privada proporcionada o la generada
        if private_key:
            d, n = private_key
        elif self.rsa.private_key:
            d, n = self.rsa.private_key
        else:
            raise KeyGenerationError("No hay clave privada disponible")
        
        # Convertir hash a entero
        hash_int = int(message_hash, 16)
        
        # Verificar que el hash sea menor que n
        if hash_int >= n:
            raise SignatureError("El hash es demasiado grande para la clave")
        
        # Firmar (cifrar hash con clave privada)
        signature = pow(hash_int, d, n)
        
        return f"{signature:x}"
    
    def verify_signature(self, message: str, signature_hex: str, public_key: Optional[Tuple[int, int]] = None) -> bool:
        """
        Verificar una firma digital
        
        Args:
            message (str): Mensaje original
            signature_hex (str): Firma en hexadecimal
            public_key (Optional[Tuple[int, int]]): Clave pública para verificar
            
        Returns:
            bool: True si la firma es válida
        """
        if not message or not signature_hex:
            raise InvalidInputError("El mensaje y la firma no pueden estar vacíos")
        
        try:
            # Generar hash del mensaje
            message_hash = self.hash_func.sha256_wrapper(message)
            
            # Usar clave pública proporcionada o la generada
            if public_key:
                e, n = public_key
            elif self.rsa.public_key:
                e, n = self.rsa.public_key
            else:
                raise KeyGenerationError("No hay clave pública disponible")
            
            # Convertir firma a entero
            signature = int(signature_hex, 16)
            
            # Verificar firma (descifrar con clave pública)
            decrypted_hash = pow(signature, e, n)
            
            # Comparar hashes
            return f"{decrypted_hash:x}" == message_hash
        
        except Exception:
            return False
    
    def sign_and_verify_demo(self, message: str) -> Dict[str, Any]:
        """
        Demostración completa de firma y verificación
        
        Args:
            message (str): Mensaje a firmar
            
        Returns:
            Dict: Información completa del proceso
        """
        # Generar claves
        public_key, private_key = self.generate_keys()
        
        # Firmar mensaje
        signature = self.sign_message(message, private_key)
        
        # Verificar firma
        is_valid = self.verify_signature(message, signature, public_key)
        
        # Generar hash del mensaje
        message_hash = self.hash_func.sha256_wrapper(message)
        
        return {
            "message": message,
            "message_hash": message_hash,
            "public_key": {
                "e": public_key[0],
                "n": public_key[1]
            },
            "private_key": {
                "d": private_key[0],
                "n": private_key[1]
            },
            "signature": signature,
            "verification": is_valid,
            "process_steps": [
                "1. Generar hash SHA-256 del mensaje",
                "2. Cifrar hash con clave privada (firmar)",
                "3. Descifrar firma con clave pública",
                "4. Comparar hash original con hash descifrado"
            ]
        }

# ===== EXPORTAR CLASES =====
__all__ = [
    'RSACipher',
    'CustomHash',
    'DESCipher',
    'DigitalSignature'
]
