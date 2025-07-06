"""
🧪 Pruebas Unitarias - Criptografía Moderna
==========================================

Conjunto de pruebas unitarias para validar los algoritmos de criptografía moderna:
- RSA (Rivest-Shamir-Adleman)
- Funciones Hash personalizadas
- DES (Data Encryption Standard)
- Firma Digital

Autor: CryptoUNS Team
Fecha: 06 de julio, 2025
Versión: 1.0.0
"""

import unittest
import sys
import os

# Agregar el directorio src al path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Importar módulos del sistema
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Importar las clases necesarias
from src.crypto.modern import RSACipher, CustomHash, DESCipher, DigitalSignature
from src.utils.constants import *
from src.utils.exceptions import *

class TestRSACipher(unittest.TestCase):
    """Pruebas unitarias para el algoritmo RSA"""
    
    def setUp(self):
        """Configurar el entorno de pruebas"""
        self.rsa = RSACipher(key_size=1024)  # Usar tamaño pequeño para tests
    
    def test_rsa_prime_generation(self):
        """Probar generación de números primos"""
        prime = self.rsa.generate_prime(16)
        self.assertTrue(self.rsa.is_prime(prime))
        self.assertTrue(prime.bit_length() == 16)
    
    def test_rsa_prime_validation(self):
        """Probar validación de números primos"""
        # Números primos conocidos
        self.assertTrue(self.rsa.is_prime(17))
        self.assertTrue(self.rsa.is_prime(19))
        self.assertTrue(self.rsa.is_prime(23))
        
        # Números no primos
        self.assertFalse(self.rsa.is_prime(4))
        self.assertFalse(self.rsa.is_prime(15))
        self.assertFalse(self.rsa.is_prime(21))
    
    def test_rsa_gcd(self):
        """Probar cálculo de máximo común divisor"""
        self.assertEqual(self.rsa.gcd(48, 18), 6)
        self.assertEqual(self.rsa.gcd(17, 13), 1)
        self.assertEqual(self.rsa.gcd(100, 25), 25)
    
    def test_rsa_mod_inverse(self):
        """Probar cálculo de inverso modular"""
        # 3 * 7 ≡ 1 (mod 10)
        self.assertEqual(self.rsa.mod_inverse(3, 10), 7)
        
        # 5 * 3 ≡ 1 (mod 7)
        self.assertEqual(self.rsa.mod_inverse(5, 7), 3)
    
    def test_rsa_key_generation(self):
        """Probar generación de claves RSA"""
        public_key, private_key = self.rsa.generate_keys()
        
        # Verificar estructura de claves
        self.assertEqual(len(public_key), 2)
        self.assertEqual(len(private_key), 2)
        
        # Verificar que n es el mismo en ambas claves
        self.assertEqual(public_key[1], private_key[1])
        
        # Verificar que las claves son diferentes
        self.assertNotEqual(public_key[0], private_key[0])
    
    def test_rsa_encryption_decryption(self):
        """Probar cifrado y descifrado RSA"""
        # Generar claves
        public_key, private_key = self.rsa.generate_keys()
        
        # Mensaje de prueba
        message = "Hello RSA!"
        
        # Cifrar
        encrypted = self.rsa.encrypt(message, public_key)
        
        # Descifrar
        decrypted = self.rsa.decrypt(encrypted, private_key)
        
        self.assertEqual(decrypted, message)
    
    def test_rsa_long_message(self):
        """Probar RSA con mensaje largo"""
        # Generar claves
        public_key, private_key = self.rsa.generate_keys()
        
        # Mensaje largo
        message = "This is a very long message that should be split into multiple blocks for RSA encryption. " * 3
        
        # Cifrar y descifrar
        encrypted = self.rsa.encrypt(message, public_key)
        decrypted = self.rsa.decrypt(encrypted, private_key)
        
        self.assertEqual(decrypted, message)
    
    def test_rsa_empty_message(self):
        """Probar RSA con mensaje vacío"""
        with self.assertRaises(InvalidInputError):
            self.rsa.encrypt("", None)
    
    def test_rsa_key_info(self):
        """Probar información de claves RSA"""
        # Generar claves
        self.rsa.generate_keys()
        
        # Obtener información
        info = self.rsa.get_key_info()
        
        self.assertIn("key_size", info)
        self.assertIn("public_key", info)
        self.assertIn("private_key", info)
        self.assertEqual(info["key_size"], 1024)

class TestCustomHash(unittest.TestCase):
    """Pruebas unitarias para funciones hash personalizadas"""
    
    def setUp(self):
        """Configurar el entorno de pruebas"""
        self.hash_func = CustomHash()
    
    def test_hash_64(self):
        """Probar función hash de 64 bits"""
        data = "Hello World"
        hash_result = self.hash_func.hash_64(data)
        
        # Verificar longitud (64 bits = 16 caracteres hex)
        self.assertEqual(len(hash_result), 16)
        
        # Verificar que es hexadecimal
        int(hash_result, 16)  # Debería funcionar sin error
        
        # Verificar consistencia
        self.assertEqual(self.hash_func.hash_64(data), hash_result)
        
        # Verificar que diferentes datos producen diferentes hashes
        self.assertNotEqual(self.hash_func.hash_64(data), self.hash_func.hash_64(data + "x"))
    
    def test_hash_128(self):
        """Probar función hash de 128 bits"""
        data = "Hello World"
        hash_result = self.hash_func.hash_128(data)
        
        # Verificar longitud (128 bits = 32 caracteres hex)
        self.assertEqual(len(hash_result), 32)
        
        # Verificar que es hexadecimal
        int(hash_result, 16)  # Debería funcionar sin error
        
        # Verificar consistencia
        self.assertEqual(self.hash_func.hash_128(data), hash_result)
    
    def test_hash_256(self):
        """Probar función hash de 256 bits"""
        data = "Hello World"
        hash_result = self.hash_func.hash_256(data)
        
        # Verificar longitud (256 bits = 64 caracteres hex)
        self.assertEqual(len(hash_result), 64)
        
        # Verificar que es hexadecimal
        int(hash_result, 16)  # Debería funcionar sin error
        
        # Verificar consistencia
        self.assertEqual(self.hash_func.hash_256(data), hash_result)
    
    def test_sha256_wrapper(self):
        """Probar wrapper SHA-256"""
        data = "Hello World"
        hash_result = self.hash_func.sha256_wrapper(data)
        
        # Verificar longitud SHA-256 (256 bits = 64 caracteres hex)
        self.assertEqual(len(hash_result), 64)
        
        # Verificar que es hexadecimal
        int(hash_result, 16)  # Debería funcionar sin error
        
        # Verificar consistencia
        self.assertEqual(self.hash_func.sha256_wrapper(data), hash_result)
    
    def test_hash_empty_data(self):
        """Probar hash con datos vacíos"""
        with self.assertRaises(InvalidInputError):
            self.hash_func.hash_64("")
        
        with self.assertRaises(InvalidInputError):
            self.hash_func.hash_128("")
        
        with self.assertRaises(InvalidInputError):
            self.hash_func.hash_256("")
    
    def test_verify_integrity(self):
        """Probar verificación de integridad"""
        data = "Hello World"
        
        # Generar hashes
        hash_64 = self.hash_func.hash_64(data)
        hash_128 = self.hash_func.hash_128(data)
        hash_256 = self.hash_func.hash_256(data)
        hash_sha256 = self.hash_func.sha256_wrapper(data)
        
        # Verificar integridad correcta
        self.assertTrue(self.hash_func.verify_integrity(data, hash_64, "64"))
        self.assertTrue(self.hash_func.verify_integrity(data, hash_128, "128"))
        self.assertTrue(self.hash_func.verify_integrity(data, hash_256, "256"))
        self.assertTrue(self.hash_func.verify_integrity(data, hash_sha256, "sha256"))
        
        # Verificar integridad incorrecta
        self.assertFalse(self.hash_func.verify_integrity(data + "x", hash_64, "64"))
        self.assertFalse(self.hash_func.verify_integrity(data, hash_64 + "x", "64"))

class TestDESCipher(unittest.TestCase):
    """Pruebas unitarias para el algoritmo DES"""
    
    def setUp(self):
        """Configurar el entorno de pruebas"""
        self.des = DESCipher()
        self.valid_key = "12345678"  # 8 caracteres
    
    def test_des_key_validation(self):
        """Probar validación de claves DES"""
        # Clave válida
        self.assertTrue(self.des.validate_key("12345678"))
        
        # Claves inválidas
        self.assertFalse(self.des.validate_key("123"))      # Muy corta
        self.assertFalse(self.des.validate_key("123456789"))  # Muy larga
        self.assertFalse(self.des.validate_key(""))         # Vacía
    
    def test_des_ecb_encryption_decryption(self):
        """Probar cifrado y descifrado DES ECB"""
        plaintext = "Hello DES!"
        
        # Cifrar
        ciphertext = self.des.encrypt_ecb(plaintext, self.valid_key)
        
        # Verificar que el resultado es hexadecimal
        bytes.fromhex(ciphertext)  # Debería funcionar sin error
        
        # Descifrar
        decrypted = self.des.decrypt_ecb(ciphertext, self.valid_key)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_des_cbc_encryption_decryption(self):
        """Probar cifrado y descifrado DES CBC"""
        plaintext = "Hello DES CBC!"
        
        # Cifrar
        ciphertext, iv = self.des.encrypt_cbc(plaintext, self.valid_key)
        
        # Verificar que los resultados son hexadecimales
        bytes.fromhex(ciphertext)  # Debería funcionar sin error
        bytes.fromhex(iv)          # Debería funcionar sin error
        
        # Descifrar
        decrypted = self.des.decrypt_cbc(ciphertext, self.valid_key, iv)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_des_cbc_with_custom_iv(self):
        """Probar DES CBC con IV personalizado"""
        plaintext = "Hello DES!"
        custom_iv = "abcdefgh"  # 8 caracteres
        
        # Cifrar con IV personalizado
        ciphertext, iv = self.des.encrypt_cbc(plaintext, self.valid_key, custom_iv)
        
        # Descifrar
        decrypted = self.des.decrypt_cbc(ciphertext, self.valid_key, iv)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_des_invalid_key(self):
        """Probar DES con clave inválida"""
        with self.assertRaises(InvalidKeyError):
            self.des.encrypt_ecb("Hello", "123")  # Clave muy corta
        
        with self.assertRaises(InvalidKeyError):
            self.des.decrypt_ecb("abcd", "123")  # Clave muy corta
    
    def test_des_empty_plaintext(self):
        """Probar DES con texto vacío"""
        with self.assertRaises(InvalidInputError):
            self.des.encrypt_ecb("", self.valid_key)
    
    def test_des_long_message(self):
        """Probar DES con mensaje largo"""
        plaintext = "This is a very long message that will be split into multiple blocks for DES encryption. " * 5
        
        # ECB
        ciphertext_ecb = self.des.encrypt_ecb(plaintext, self.valid_key)
        decrypted_ecb = self.des.decrypt_ecb(ciphertext_ecb, self.valid_key)
        self.assertEqual(decrypted_ecb, plaintext)
        
        # CBC
        ciphertext_cbc, iv = self.des.encrypt_cbc(plaintext, self.valid_key)
        decrypted_cbc = self.des.decrypt_cbc(ciphertext_cbc, self.valid_key, iv)
        self.assertEqual(decrypted_cbc, plaintext)

class TestDigitalSignature(unittest.TestCase):
    """Pruebas unitarias para firma digital"""
    
    def setUp(self):
        """Configurar el entorno de pruebas"""
        self.signature = DigitalSignature()
    
    def test_signature_key_generation(self):
        """Probar generación de claves para firma"""
        public_key, private_key = self.signature.generate_keys(1024)
        
        # Verificar estructura de claves
        self.assertEqual(len(public_key), 2)
        self.assertEqual(len(private_key), 2)
        
        # Verificar que n es el mismo en ambas claves
        self.assertEqual(public_key[1], private_key[1])
    
    def test_signature_sign_verify(self):
        """Probar firma y verificación de mensajes"""
        message = "This is a test message for digital signature"
        
        # Generar claves
        public_key, private_key = self.signature.generate_keys(1024)
        
        # Firmar mensaje
        signature = self.signature.sign_message(message, private_key)
        
        # Verificar firma
        is_valid = self.signature.verify_signature(message, signature, public_key)
        
        self.assertTrue(is_valid)
    
    def test_signature_invalid_verification(self):
        """Probar verificación de firma inválida"""
        message = "Original message"
        tampered_message = "Tampered message"
        
        # Generar claves
        public_key, private_key = self.signature.generate_keys(1024)
        
        # Firmar mensaje original
        signature = self.signature.sign_message(message, private_key)
        
        # Verificar con mensaje modificado
        is_valid = self.signature.verify_signature(tampered_message, signature, public_key)
        
        self.assertFalse(is_valid)
    
    def test_signature_empty_message(self):
        """Probar firma con mensaje vacío"""
        with self.assertRaises(InvalidInputError):
            self.signature.sign_message("", None)
    
    def test_signature_demo(self):
        """Probar demostración completa de firma"""
        message = "Demo message for signature"
        
        # Ejecutar demo
        result = self.signature.sign_and_verify_demo(message)
        
        # Verificar resultado
        self.assertIn("message", result)
        self.assertIn("signature", result)
        self.assertIn("verification", result)
        self.assertTrue(result["verification"])
        self.assertEqual(result["message"], message)
    
    def test_signature_different_keys(self):
        """Probar firma con diferentes claves"""
        message = "Test message"
        
        # Generar dos pares de claves diferentes
        public_key1, private_key1 = self.signature.generate_keys(1024)
        public_key2, private_key2 = self.signature.generate_keys(1024)
        
        # Firmar con primera clave privada
        signature = self.signature.sign_message(message, private_key1)
        
        # Verificar con primera clave pública (debería ser válida)
        is_valid1 = self.signature.verify_signature(message, signature, public_key1)
        self.assertTrue(is_valid1)
        
        # Verificar con segunda clave pública (debería ser inválida)
        is_valid2 = self.signature.verify_signature(message, signature, public_key2)
        self.assertFalse(is_valid2)

class TestModernCryptoIntegration(unittest.TestCase):
    """Pruebas de integración para criptografía moderna"""
    
    def test_rsa_with_hash(self):
        """Probar RSA combinado con funciones hash"""
        # Crear mensaje y hash
        message = "Integration test message"
        hash_func = CustomHash()
        message_hash = hash_func.sha256_wrapper(message)
        
        # Cifrar hash con RSA
        rsa = RSACipher(1024)
        public_key, private_key = rsa.generate_keys()
        
        # Cifrar el hash
        encrypted_hash = rsa.encrypt(message_hash, public_key)
        
        # Descifrar el hash
        decrypted_hash = rsa.decrypt(encrypted_hash, private_key)
        
        # Verificar que coinciden
        self.assertEqual(decrypted_hash, message_hash)
    
    def test_hash_consistency(self):
        """Probar consistencia entre diferentes funciones hash"""
        message = "Consistency test"
        hash_func = CustomHash()
        
        # Generar múltiples hashes del mismo mensaje
        hash1 = hash_func.hash_256(message)
        hash2 = hash_func.hash_256(message)
        hash3 = hash_func.hash_256(message)
        
        # Todos deberían ser iguales
        self.assertEqual(hash1, hash2)
        self.assertEqual(hash2, hash3)
    
    def test_full_crypto_workflow(self):
        """Probar flujo completo de criptografía"""
        original_message = "Complete cryptographic workflow test"
        
        # 1. Generar hash del mensaje
        hash_func = CustomHash()
        message_hash = hash_func.sha256_wrapper(original_message)
        
        # 2. Cifrar mensaje con DES
        des = DESCipher()
        des_key = "workflow"
        encrypted_message = des.encrypt_ecb(original_message, des_key)
        
        # 3. Firmar hash del mensaje original
        signature = DigitalSignature()
        public_key, private_key = signature.generate_keys(1024)
        message_signature = signature.sign_message(original_message, private_key)
        
        # 4. Verificar todo el flujo
        # Descifrar mensaje
        decrypted_message = des.decrypt_ecb(encrypted_message, des_key)
        self.assertEqual(decrypted_message, original_message)
        
        # Verificar firma
        is_signature_valid = signature.verify_signature(original_message, message_signature, public_key)
        self.assertTrue(is_signature_valid)
        
        # Verificar integridad con hash
        is_integrity_valid = hash_func.verify_integrity(decrypted_message, message_hash, "sha256")
        self.assertTrue(is_integrity_valid)

if __name__ == '__main__':
    # Configurar el entorno de pruebas
    unittest.main(verbosity=2)
