"""
🧪 Pruebas Unitarias - Criptografía Clásica
==========================================

Conjunto de pruebas unitarias para validar los algoritmos de criptografía clásica:
- Cifrado César
- Cifrado Vigenère
- Cifrado Playfair
- Método de Kasiski

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
from src.crypto.classic import CaesarCipher, VigenereCipher, PlayfairCipher, KasiskiAnalysis
from src.utils.constants import *
from src.utils.exceptions import *

class TestCaesarCipher(unittest.TestCase):
    """Pruebas unitarias para el cifrado César"""
    
    def setUp(self):
        """Configurar el entorno de pruebas"""
        self.cipher = CaesarCipher()
    
    def test_caesar_basic_encryption(self):
        """Probar cifrado básico César"""
        plaintext = "HELLO"
        key = 3
        expected = "KHOOR"
        result = self.cipher.encrypt(plaintext, key)
        self.assertEqual(result, expected)
    
    def test_caesar_basic_decryption(self):
        """Probar descifrado básico César"""
        ciphertext = "KHOOR"
        key = 3
        expected = "HELLO"
        result = self.cipher.decrypt(ciphertext, key)
        self.assertEqual(result, expected)
    
    def test_caesar_with_spaces(self):
        """Probar cifrado César con espacios"""
        plaintext = "HELLO WORLD"
        key = 5
        encrypted = self.cipher.encrypt(plaintext, key)
        decrypted = self.cipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, "HELLO WORLD")
    
    def test_caesar_wrap_around(self):
        """Probar cifrado César con wraparound del alfabeto"""
        plaintext = "XYZ"
        key = 3
        expected = "ABC"
        result = self.cipher.encrypt(plaintext, key)
        self.assertEqual(result, expected)
    
    def test_caesar_zero_key(self):
        """Probar cifrado César con clave 0"""
        plaintext = "HELLO"
        key = 0
        result = self.cipher.encrypt(plaintext, key)
        self.assertEqual(result, plaintext)
    
    def test_caesar_negative_key(self):
        """Probar cifrado César con clave negativa"""
        plaintext = "HELLO"
        key = -3
        encrypted = self.cipher.encrypt(plaintext, key)
        decrypted = self.cipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, plaintext)
    
    def test_caesar_large_key(self):
        """Probar cifrado César con clave mayor al tamaño del alfabeto"""
        plaintext = "HELLO"
        key = 29  # 26 + 3
        expected = "KHOOR"  # Equivalente a clave 3
        result = self.cipher.encrypt(plaintext, key)
        self.assertEqual(result, expected)
    
    def test_caesar_key_validation(self):
        """Probar validación de claves"""
        self.assertTrue(self.cipher.validate_key(5))
        self.assertTrue(self.cipher.validate_key(0))
        self.assertTrue(self.cipher.validate_key(-5))
        self.assertTrue(self.cipher.validate_key(100))
    
    def test_caesar_brute_force(self):
        """Probar fuerza bruta del cifrado César"""
        ciphertext = "KHOOR"
        results = self.cipher.brute_force_attack(ciphertext)
        self.assertEqual(len(results), 26)
        self.assertIn(("HELLO", 3), results)
    
    def test_caesar_frequency_analysis(self):
        """Probar análisis de frecuencia"""
        text = "HELLO WORLD"
        freq = self.cipher.frequency_analysis(text)
        self.assertIn('L', freq)
        self.assertEqual(freq['L'], 3)

class TestVigenereCipher(unittest.TestCase):
    """Pruebas unitarias para el cifrado Vigenère"""
    
    def setUp(self):
        """Configurar el entorno de pruebas"""
        self.cipher = VigenereCipher()
    
    def test_vigenere_basic_encryption(self):
        """Probar cifrado básico Vigenère"""
        plaintext = "HELLO"
        key = "KEY"
        expected = "RIJVS"
        result = self.cipher.encrypt(plaintext, key)
        self.assertEqual(result, expected)
    
    def test_vigenere_basic_decryption(self):
        """Probar descifrado básico Vigenère"""
        ciphertext = "RIJVS"
        key = "KEY"
        expected = "HELLO"
        result = self.cipher.decrypt(ciphertext, key)
        self.assertEqual(result, expected)
    
    def test_vigenere_long_text(self):
        """Probar cifrado Vigenère con texto largo"""
        plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
        key = "SECRET"
        encrypted = self.cipher.encrypt(plaintext, key)
        decrypted = self.cipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, plaintext)
    
    def test_vigenere_single_char_key(self):
        """Probar cifrado Vigenère con clave de un carácter (equivalente a César)"""
        plaintext = "HELLO"
        key = "C"
        encrypted = self.cipher.encrypt(plaintext, key)
        
        # Debería ser equivalente a César con clave 2 (C = posición 2)
        caesar = CaesarCipher()
        caesar_result = caesar.encrypt(plaintext, 2)
        self.assertEqual(encrypted, caesar_result)
    
    def test_vigenere_key_validation(self):
        """Probar validación de claves Vigenère"""
        self.assertTrue(self.cipher.validate_key("KEY"))
        self.assertTrue(self.cipher.validate_key("A"))
        self.assertTrue(self.cipher.validate_key("VERYLONGKEY"))
        self.assertFalse(self.cipher.validate_key(""))
        self.assertFalse(self.cipher.validate_key("123"))
        self.assertFalse(self.cipher.validate_key("KEY123"))
    
    def test_vigenere_generate_key(self):
        """Probar generación de claves Vigenère"""
        key = self.cipher.generate_key(10)
        self.assertEqual(len(key), 10)
        self.assertTrue(all(c in ENGLISH_ALPHABET for c in key))
    
    def test_vigenere_autokey_encryption(self):
        """Probar cifrado Vigenère con autoclave"""
        plaintext = "HELLO"
        key = "KEY"
        encrypted = self.cipher.encrypt_autokey(plaintext, key)
        decrypted = self.cipher.decrypt_autokey(encrypted, key)
        self.assertEqual(decrypted, plaintext)
    
    def test_vigenere_kasiski_analysis(self):
        """Probar análisis de Kasiski básico"""
        # Texto con repeticiones para análisis
        text = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
        key = "ABC"
        encrypted = self.cipher.encrypt(text, key)
        
        # Buscar repeticiones
        repetitions = self.cipher.find_repetitions(encrypted)
        self.assertIsInstance(repetitions, list)

class TestPlayfairCipher(unittest.TestCase):
    """Pruebas unitarias para el cifrado Playfair"""
    
    def setUp(self):
        """Configurar el entorno de pruebas"""
        self.cipher = PlayfairCipher()
    
    def test_playfair_matrix_creation(self):
        """Probar creación de la matriz Playfair"""
        key = "KEYWORD"
        matrix = self.cipher.create_matrix(key)
        self.assertEqual(len(matrix), 5)
        self.assertEqual(len(matrix[0]), 5)
        
        # Verificar que no hay duplicados
        chars = [char for row in matrix for char in row]
        self.assertEqual(len(chars), len(set(chars)))
    
    def test_playfair_text_preparation(self):
        """Probar preparación del texto para Playfair"""
        text = "HELLO"
        prepared = self.cipher.prepare_text(text)
        self.assertEqual(len(prepared) % 2, 0)  # Debe ser par
        
        # Probar con letras dobles
        text_double = "BALLOON"
        prepared_double = self.cipher.prepare_text(text_double)
        self.assertNotIn("LL", prepared_double)
        self.assertNotIn("OO", prepared_double)
    
    def test_playfair_basic_encryption(self):
        """Probar cifrado básico Playfair"""
        plaintext = "HELLO"
        key = "KEYWORD"
        encrypted = self.cipher.encrypt(plaintext, key)
        decrypted = self.cipher.decrypt(encrypted, key)
        
        # Verificar que el descifrado coincida con el original preparado
        prepared = self.cipher.prepare_text(plaintext)
        self.assertEqual(decrypted, prepared)
    
    def test_playfair_same_row(self):
        """Probar cifrado Playfair con letras en la misma fila"""
        key = "KEYWORD"
        matrix = self.cipher.create_matrix(key)
        
        # Encontrar dos letras en la misma fila
        row_chars = matrix[0][:2]  # Primeras dos letras de la primera fila
        plaintext = row_chars[0] + row_chars[1]
        
        encrypted = self.cipher.encrypt(plaintext, key)
        decrypted = self.cipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, plaintext)
    
    def test_playfair_same_column(self):
        """Probar cifrado Playfair con letras en la misma columna"""
        key = "KEYWORD"
        matrix = self.cipher.create_matrix(key)
        
        # Encontrar dos letras en la misma columna
        col_chars = [matrix[0][0], matrix[1][0]]  # Primera columna
        plaintext = col_chars[0] + col_chars[1]
        
        encrypted = self.cipher.encrypt(plaintext, key)
        decrypted = self.cipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, plaintext)
    
    def test_playfair_key_validation(self):
        """Probar validación de claves Playfair"""
        self.assertTrue(self.cipher.validate_key("KEYWORD"))
        self.assertTrue(self.cipher.validate_key("A"))
        self.assertTrue(self.cipher.validate_key("VERYLONGKEYWORD"))
        self.assertFalse(self.cipher.validate_key(""))
        self.assertFalse(self.cipher.validate_key("123"))
        self.assertFalse(self.cipher.validate_key("KEY123"))
    
    def test_playfair_generate_key(self):
        """Probar generación de claves Playfair"""
        key = self.cipher.generate_key(8)
        self.assertEqual(len(key), 8)
        self.assertTrue(all(c in PLAYFAIR_ALPHABET for c in key))

class TestKasiskiAnalysis(unittest.TestCase):
    """Pruebas unitarias para el análisis de Kasiski"""
    
    def setUp(self):
        """Configurar el entorno de pruebas"""
        self.analysis = KasiskiAnalysis()
    
    def test_kasiski_find_repetitions(self):
        """Probar búsqueda de repeticiones"""
        text = "ABCABCDEFABCGHI"
        repetitions = self.analysis.find_repetitions(text)
        self.assertIsInstance(repetitions, list)
        
        # Debería encontrar "ABC" repetido
        abc_reps = [rep for rep in repetitions if rep['sequence'] == 'ABC']
        self.assertTrue(len(abc_reps) > 0)
    
    def test_kasiski_calculate_distances(self):
        """Probar cálculo de distancias"""
        repetitions = [
            {'sequence': 'ABC', 'positions': [0, 6, 12]},
            {'sequence': 'DEF', 'positions': [3, 9]}
        ]
        distances = self.analysis.calculate_distances(repetitions)
        self.assertIsInstance(distances, list)
        self.assertIn(6, distances)  # 6-0 = 6, 12-6 = 6
    
    def test_kasiski_find_common_factors(self):
        """Probar búsqueda de factores comunes"""
        distances = [6, 12, 18, 24]
        factors = self.analysis.find_common_factors(distances)
        self.assertIsInstance(factors, dict)
        self.assertIn(6, factors)
        self.assertIn(3, factors)
        self.assertIn(2, factors)
    
    def test_kasiski_estimate_key_length(self):
        """Probar estimación de longitud de clave"""
        # Crear un texto cifrado con clave conocida
        vigenere = VigenereCipher()
        plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG" * 3
        key = "SECRET"
        ciphertext = vigenere.encrypt(plaintext, key)
        
        estimated_lengths = self.analysis.estimate_key_length(ciphertext)
        self.assertIsInstance(estimated_lengths, list)
        
        # La longitud correcta (6) debería estar entre las estimaciones
        lengths = [item[0] for item in estimated_lengths]
        self.assertIn(6, lengths)
    
    def test_kasiski_full_analysis(self):
        """Probar análisis completo de Kasiski"""
        # Crear un texto cifrado con clave conocida
        vigenere = VigenereCipher()
        plaintext = "ATTACKATDAWN" * 10
        key = "LEMON"
        ciphertext = vigenere.encrypt(plaintext, key)
        
        analysis_result = self.analysis.analyze(ciphertext)
        self.assertIsInstance(analysis_result, dict)
        self.assertIn('repetitions', analysis_result)
        self.assertIn('distances', analysis_result)
        self.assertIn('factors', analysis_result)
        self.assertIn('key_length_estimates', analysis_result)

class TestCryptoClassicIntegration(unittest.TestCase):
    """Pruebas de integración para criptografía clásica"""
    
    def test_crypto_roundtrip(self):
        """Probar cifrado y descifrado completo"""
        plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
        
        # César
        caesar = CaesarCipher()
        caesar_encrypted = caesar.encrypt(plaintext, 7)
        caesar_decrypted = caesar.decrypt(caesar_encrypted, 7)
        self.assertEqual(caesar_decrypted, plaintext)
        
        # Vigenère
        vigenere = VigenereCipher()
        vigenere_encrypted = vigenere.encrypt(plaintext, "KEYWORD")
        vigenere_decrypted = vigenere.decrypt(vigenere_encrypted, "KEYWORD")
        self.assertEqual(vigenere_decrypted, plaintext)
        
        # Playfair
        playfair = PlayfairCipher()
        playfair_encrypted = playfair.encrypt(plaintext, "KEYWORD")
        playfair_decrypted = playfair.decrypt(playfair_encrypted, "KEYWORD")
        # Para Playfair, comparamos con el texto preparado
        prepared = playfair.prepare_text(plaintext)
        self.assertEqual(playfair_decrypted, prepared)
    
    def test_different_alphabets(self):
        """Probar con diferentes alfabetos"""
        # Alfabeto personalizado
        custom_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        
        caesar = CaesarCipher(alphabet=custom_alphabet)
        plaintext = "HELLO123"
        encrypted = caesar.encrypt(plaintext, 5)
        decrypted = caesar.decrypt(encrypted, 5)
        self.assertEqual(decrypted, plaintext)
    
    def test_error_handling(self):
        """Probar manejo de errores"""
        caesar = CaesarCipher()
        vigenere = VigenereCipher()
        playfair = PlayfairCipher()
        
        # Probar con texto vacío
        with self.assertRaises(CryptographyError):
            caesar.encrypt("", 5)
        
        with self.assertRaises(CryptographyError):
            vigenere.encrypt("", "KEY")
        
        with self.assertRaises(CryptographyError):
            playfair.encrypt("", "KEY")
        
        # Probar con clave inválida
        with self.assertRaises(CryptographyError):
            vigenere.encrypt("HELLO", "")
        
        with self.assertRaises(CryptographyError):
            playfair.encrypt("HELLO", "")

if __name__ == '__main__':
    # Configurar el entorno de pruebas
    unittest.main(verbosity=2)
