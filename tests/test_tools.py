"""
🧪 Pruebas Unitarias - Herramientas Adicionales
==============================================

Conjunto de pruebas unitarias para validar las herramientas adicionales:
- Codificación Huffman
- Simulador Blockchain
- Verificador de Integridad

Autor: CryptoUNS Team
Fecha: 06 de julio, 2025
Versión: 1.0.0
"""

import unittest
import sys
import os
import tempfile
import time

# Agregar el directorio src al path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Importar módulos del sistema
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Importar las clases necesarias
from src.crypto.tools import HuffmanCoding, Blockchain, Block, IntegrityVerifier
from src.utils.constants import *
from src.utils.exceptions import *

class TestHuffmanCoding(unittest.TestCase):
    """Pruebas unitarias para codificación Huffman"""
    
    def setUp(self):
        """Configurar el entorno de pruebas"""
        self.huffman = HuffmanCoding()
    
    def test_huffman_frequency_table(self):
        """Probar construcción de tabla de frecuencias"""
        text = "hello"
        freq_table = self.huffman.build_frequency_table(text)
        
        expected = {'h': 1, 'e': 1, 'l': 2, 'o': 1}
        self.assertEqual(freq_table, expected)
    
    def test_huffman_basic_encoding(self):
        """Probar codificación básica de Huffman"""
        text = "hello world"
        encoded, codes, tree = self.huffman.encode(text)
        
        # Verificar que el texto codificado es binario
        self.assertTrue(all(bit in '01' for bit in encoded))
        
        # Verificar que todos los caracteres tienen códigos
        unique_chars = set(text)
        self.assertEqual(set(codes.keys()), unique_chars)
        
        # Verificar que los códigos son strings binarios
        for code in codes.values():
            self.assertTrue(all(bit in '01' for bit in code))
    
    def test_huffman_encoding_decoding(self):
        """Probar codificación y decodificación completa"""
        text = "this is a test message for huffman coding"
        
        # Codificar
        encoded, codes, tree = self.huffman.encode(text)
        
        # Decodificar
        decoded = self.huffman.decode(encoded, tree)
        
        # Verificar que coinciden
        self.assertEqual(decoded, text)
    
    def test_huffman_single_character(self):
        """Probar Huffman con un solo carácter"""
        text = "aaaa"
        encoded, codes, tree = self.huffman.encode(text)
        decoded = self.huffman.decode(encoded, tree)
        
        self.assertEqual(decoded, text)
        self.assertIn('a', codes)
    
    def test_huffman_compression_stats(self):
        """Probar estadísticas de compresión"""
        text = "this is a test message"
        encoded, codes, tree = self.huffman.encode(text)
        
        stats = self.huffman.get_compression_stats(text, encoded)
        
        # Verificar estructura de estadísticas
        self.assertIn("original_length", stats)
        self.assertIn("encoded_length", stats)
        self.assertIn("compression_ratio", stats)
        self.assertIn("space_saved_percent", stats)
        
        # Verificar valores lógicos
        self.assertEqual(stats["original_length"], len(text))
        self.assertEqual(stats["encoded_length"], len(encoded))
        self.assertGreaterEqual(stats["compression_ratio"], 0)
    
    def test_huffman_empty_text(self):
        """Probar Huffman con texto vacío"""
        with self.assertRaises(InvalidInputError):
            self.huffman.encode("")
    
    def test_huffman_tree_visualization(self):
        """Probar visualización del árbol"""
        text = "hello"
        encoded, codes, tree = self.huffman.encode(text)
        
        visualization = self.huffman.visualize_tree(tree)
        
        # Verificar que la visualización contiene elementos esperados
        self.assertIsInstance(visualization, str)
        self.assertGreater(len(visualization), 0)
    
    def test_huffman_repeated_text(self):
        """Probar Huffman con texto repetitivo (mejor compresión)"""
        text = "aaabbbcccdddeeefffggghhhiiijjjkkklllmmmnnnooopppqqqrrrssstttuuuvvvwwwxxxyyyzzz"
        
        encoded, codes, tree = self.huffman.encode(text)
        decoded = self.huffman.decode(encoded, tree)
        
        self.assertEqual(decoded, text)
        
        # Verificar compresión
        stats = self.huffman.get_compression_stats(text, encoded)
        self.assertLess(stats["compression_ratio"], 1.0)  # Debería haber compresión

class TestBlockchain(unittest.TestCase):
    """Pruebas unitarias para simulador Blockchain"""
    
    def setUp(self):
        """Configurar el entorno de pruebas"""
        self.blockchain = Blockchain(difficulty=2)  # Dificultad baja para tests
    
    def test_blockchain_genesis_block(self):
        """Probar creación del bloque génesis"""
        genesis = self.blockchain.chain[0]
        
        self.assertEqual(genesis.index, 0)
        self.assertEqual(genesis.data, "Genesis Block")
        self.assertEqual(genesis.previous_hash, "0")
        self.assertIsNotNone(genesis.hash)
    
    def test_blockchain_add_block(self):
        """Probar adición de bloques"""
        initial_length = len(self.blockchain.chain)
        
        # Agregar bloque
        new_block = self.blockchain.add_block("Test transaction")
        
        # Verificar que se agregó
        self.assertEqual(len(self.blockchain.chain), initial_length + 1)
        self.assertEqual(new_block.data, "Test transaction")
        self.assertEqual(new_block.index, initial_length)
        
        # Verificar enlaces
        previous_block = self.blockchain.chain[-2]
        self.assertEqual(new_block.previous_hash, previous_block.hash)
    
    def test_blockchain_chain_validation(self):
        """Probar validación de la cadena"""
        # Cadena inicial debe ser válida
        self.assertTrue(self.blockchain.is_chain_valid())
        
        # Agregar algunos bloques
        self.blockchain.add_block("Transaction 1")
        self.blockchain.add_block("Transaction 2")
        self.blockchain.add_block("Transaction 3")
        
        # Cadena debe seguir siendo válida
        self.assertTrue(self.blockchain.is_chain_valid())
    
    def test_blockchain_tampering_detection(self):
        """Probar detección de alteraciones"""
        # Agregar bloques
        self.blockchain.add_block("Transaction 1")
        self.blockchain.add_block("Transaction 2")
        
        # Cadena debe ser válida inicialmente
        self.assertTrue(self.blockchain.is_chain_valid())
        self.assertEqual(len(self.blockchain.detect_tampering()), 0)
        
        # Alterar un bloque
        self.blockchain.tamper_block(1, "Tampered data")
        
        # Debería detectar alteración
        self.assertFalse(self.blockchain.is_chain_valid())
        tampered = self.blockchain.detect_tampering()
        self.assertGreater(len(tampered), 0)
        self.assertIn(1, tampered)
    
    def test_blockchain_block_mining(self):
        """Probar minado de bloques"""
        block = Block(1, "Test data", "previous_hash")
        
        # Verificar que el hash inicial no cumple la dificultad
        self.assertFalse(block.hash.startswith("00"))
        
        # Minar bloque
        block.mine_block(2)
        
        # Verificar prueba de trabajo
        self.assertTrue(block.hash.startswith("00"))
        self.assertGreater(block.nonce, 0)
    
    def test_blockchain_block_validation(self):
        """Probar validación de bloques individuales"""
        # Crear bloque válido
        previous_block = self.blockchain.get_latest_block()
        valid_block = Block(
            index=previous_block.index + 1,
            data="Valid transaction",
            previous_hash=previous_block.hash
        )
        valid_block.mine_block(self.blockchain.difficulty)
        
        # Debería ser válido
        self.assertTrue(self.blockchain.is_valid_new_block(valid_block, previous_block))
        
        # Crear bloque inválido (índice incorrecto)
        invalid_block = Block(
            index=previous_block.index + 5,  # Índice incorrecto
            data="Invalid transaction",
            previous_hash=previous_block.hash
        )
        
        # No debería ser válido
        self.assertFalse(self.blockchain.is_valid_new_block(invalid_block, previous_block))
    
    def test_blockchain_empty_data(self):
        """Probar blockchain con datos vacíos"""
        with self.assertRaises(InvalidInputError):
            self.blockchain.add_block("")
    
    def test_blockchain_info(self):
        """Probar información de la blockchain"""
        # Agregar algunos bloques
        self.blockchain.add_block("Transaction 1")
        self.blockchain.add_block("Transaction 2")
        
        info = self.blockchain.get_chain_info()
        
        # Verificar estructura
        self.assertIn("length", info)
        self.assertIn("difficulty", info)
        self.assertIn("is_valid", info)
        self.assertIn("latest_block", info)
        
        # Verificar valores
        self.assertEqual(info["length"], 3)  # Genesis + 2 bloques
        self.assertEqual(info["difficulty"], 2)
        self.assertTrue(info["is_valid"])
    
    def test_blockchain_json_export(self):
        """Probar exportación a JSON"""
        self.blockchain.add_block("Transaction 1")
        
        json_data = self.blockchain.to_json()
        
        # Verificar que es JSON válido
        import json
        parsed = json.loads(json_data)
        
        self.assertIsInstance(parsed, list)
        self.assertEqual(len(parsed), 2)  # Genesis + 1 bloque

class TestIntegrityVerifier(unittest.TestCase):
    """Pruebas unitarias para verificador de integridad"""
    
    def setUp(self):
        """Configurar el entorno de pruebas"""
        self.verifier = IntegrityVerifier()
    
    def test_text_hash_calculation(self):
        """Probar cálculo de hash de texto"""
        text = "Hello, World!"
        
        # Probar diferentes algoritmos
        sha256_hash = self.verifier.calculate_text_hash(text, "sha256")
        sha1_hash = self.verifier.calculate_text_hash(text, "sha1")
        md5_hash = self.verifier.calculate_text_hash(text, "md5")
        
        # Verificar longitudes esperadas
        self.assertEqual(len(sha256_hash), 64)  # SHA-256: 32 bytes = 64 hex chars
        self.assertEqual(len(sha1_hash), 40)    # SHA-1: 20 bytes = 40 hex chars
        self.assertEqual(len(md5_hash), 32)     # MD5: 16 bytes = 32 hex chars
        
        # Verificar consistencia
        self.assertEqual(sha256_hash, self.verifier.calculate_text_hash(text, "sha256"))
    
    def test_file_hash_calculation(self):
        """Probar cálculo de hash de archivo"""
        # Crear archivo temporal
        test_content = "This is test content for file hashing"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write(test_content)
            temp_file_path = temp_file.name
        
        try:
            # Calcular hash del archivo
            file_hash = self.verifier.calculate_file_hash(temp_file_path, "sha256")
            
            # Calcular hash del contenido directamente
            text_hash = self.verifier.calculate_text_hash(test_content, "sha256")
            
            # Deberían coincidir
            self.assertEqual(file_hash, text_hash)
        
        finally:
            # Limpiar archivo temporal
            os.unlink(temp_file_path)
    
    def test_text_integrity_verification(self):
        """Probar verificación de integridad de texto"""
        text = "Test message for integrity verification"
        expected_hash = self.verifier.calculate_text_hash(text, "sha256")
        
        # Verificación correcta
        result = self.verifier.verify_text_integrity(text, expected_hash, "sha256")
        
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["calculated_hash"], expected_hash)
        self.assertEqual(result["text_length"], len(text))
        
        # Verificación incorrecta
        wrong_hash = "0" * 64
        result_wrong = self.verifier.verify_text_integrity(text, wrong_hash, "sha256")
        
        self.assertFalse(result_wrong["is_valid"])
        self.assertNotEqual(result_wrong["calculated_hash"], wrong_hash)
    
    def test_file_integrity_verification(self):
        """Probar verificación de integridad de archivo"""
        test_content = "File content for integrity testing"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write(test_content)
            temp_file_path = temp_file.name
        
        try:
            # Calcular hash correcto
            expected_hash = self.verifier.calculate_file_hash(temp_file_path, "sha256")
            
            # Verificación correcta
            result = self.verifier.verify_file_integrity(temp_file_path, expected_hash, "sha256")
            
            self.assertTrue(result["is_valid"])
            self.assertEqual(result["calculated_hash"], expected_hash)
            self.assertGreater(result["file_size"], 0)
        
        finally:
            os.unlink(temp_file_path)
    
    def test_file_comparison(self):
        """Probar comparación de archivos"""
        content1 = "Content of first file"
        content2 = "Content of second file"
        content3 = "Content of first file"  # Igual al primero
        
        # Crear archivos temporales
        files = []
        for content in [content1, content2, content3]:
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
                temp_file.write(content)
                files.append(temp_file.name)
        
        try:
            # Comparar archivos diferentes
            result1 = self.verifier.compare_files(files[0], files[1], "sha256")
            self.assertFalse(result1["are_identical"])
            
            # Comparar archivos iguales
            result2 = self.verifier.compare_files(files[0], files[2], "sha256")
            self.assertTrue(result2["are_identical"])
            
            # Verificar estructura del resultado
            self.assertIn("file1", result1)
            self.assertIn("file2", result1)
            self.assertIn("algorithm", result1)
            self.assertIn("are_identical", result1)
        
        finally:
            # Limpiar archivos temporales
            for file_path in files:
                os.unlink(file_path)
    
    def test_integrity_report(self):
        """Probar generación de reporte de integridad"""
        # Preparar elementos para verificar
        items = [
            {
                "text": "Test message 1",
                "expected_hash": self.verifier.calculate_text_hash("Test message 1", "sha256")
            },
            {
                "text": "Test message 2",
                "expected_hash": "0" * 64  # Hash incorrecto
            }
        ]
        
        # Generar reporte
        report = self.verifier.generate_integrity_report(items, "sha256")
        
        # Verificar estructura
        self.assertIn("algorithm", report)
        self.assertIn("results", report)
        self.assertIn("summary", report)
        
        # Verificar resultados
        self.assertEqual(len(report["results"]), 2)
        self.assertEqual(report["summary"]["total"], 2)
        self.assertEqual(report["summary"]["valid"], 1)
        self.assertEqual(report["summary"]["invalid"], 1)
    
    def test_invalid_algorithm(self):
        """Probar algoritmo hash inválido"""
        with self.assertRaises(InvalidInputError):
            self.verifier.calculate_text_hash("test", "invalid_algorithm")
    
    def test_nonexistent_file(self):
        """Probar archivo inexistente"""
        with self.assertRaises(FileNotFoundError):
            self.verifier.calculate_file_hash("/nonexistent/path/file.txt")

class TestToolsIntegration(unittest.TestCase):
    """Pruebas de integración para herramientas adicionales"""
    
    def test_huffman_blockchain_integration(self):
        """Probar integración entre Huffman y Blockchain"""
        # Comprimir datos con Huffman
        huffman = HuffmanCoding()
        original_data = "Transaction data to be compressed and stored in blockchain"
        
        compressed_data, codes, tree = huffman.encode(original_data)
        
        # Almacenar datos comprimidos en blockchain
        blockchain = Blockchain(difficulty=1)
        block = blockchain.add_block(compressed_data)
        
        # Verificar que el bloque contiene los datos comprimidos
        self.assertEqual(block.data, compressed_data)
        
        # Verificar que se puede recuperar y descomprimir
        retrieved_data = blockchain.get_latest_block().data
        decompressed_data = huffman.decode(retrieved_data, tree)
        
        self.assertEqual(decompressed_data, original_data)
    
    def test_integrity_verification_with_blockchain(self):
        """Probar verificación de integridad con blockchain"""
        # Crear blockchain con datos
        blockchain = Blockchain(difficulty=1)
        blockchain.add_block("Transaction 1")
        blockchain.add_block("Transaction 2")
        
        # Verificar integridad usando hashes de bloques
        verifier = IntegrityVerifier()
        
        for block in blockchain.chain:
            # Recalcular hash y comparar
            expected_hash = block.calculate_hash()
            
            # Simular verificación de integridad del bloque
            block_data = f"{block.index}{block.data}{block.previous_hash}{block.timestamp}{block.nonce}"
            calculated_hash = verifier.calculate_text_hash(block_data, "sha256")
            
            # Los hashes deberían coincidir
            self.assertEqual(expected_hash, calculated_hash)
    
    def test_complete_workflow(self):
        """Probar flujo completo con todas las herramientas"""
        # 1. Comprimir datos con Huffman
        huffman = HuffmanCoding()
        original_message = "Important document that needs to be compressed, stored securely, and verified for integrity"
        
        compressed_data, codes, tree = huffman.encode(original_message)
        
        # 2. Almacenar en blockchain
        blockchain = Blockchain(difficulty=1)
        block = blockchain.add_block(compressed_data)
        
        # 3. Verificar integridad
        verifier = IntegrityVerifier()
        
        # Verificar integridad del mensaje original
        original_hash = verifier.calculate_text_hash(original_message, "sha256")
        
        # Recuperar datos de blockchain
        stored_data = blockchain.get_latest_block().data
        
        # Descomprimir
        recovered_message = huffman.decode(stored_data, tree)
        
        # Verificar integridad del mensaje recuperado
        recovered_hash = verifier.calculate_text_hash(recovered_message, "sha256")
        
        # Todo debería coincidir
        self.assertEqual(original_message, recovered_message)
        self.assertEqual(original_hash, recovered_hash)
        
        # Verificar que la blockchain es válida
        self.assertTrue(blockchain.is_chain_valid())
        
        # Verificar estadísticas de compresión
        stats = huffman.get_compression_stats(original_message, compressed_data)
        self.assertLess(stats["compression_ratio"], 1.0)  # Debería haber compresión

if __name__ == '__main__':
    # Configurar el entorno de pruebas
    unittest.main(verbosity=2)
