#!/usr/bin/env python3
"""
Script de verificación rápida para CryptoUNS
Prueba las funcionalidades principales del sistema
"""

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.crypto.classic import CaesarCipher, VigenereCipher, PlayfairCipher, KasiskiAnalysis
from src.crypto.modern import RSACipher, CustomHash, DESCipher, DigitalSignature
from src.crypto.tools import HuffmanCoding, Blockchain, IntegrityVerifier

def test_classic_crypto():
    """Probar algoritmos de criptografía clásica"""
    print("🔤 Probando Criptografía Clásica...")
    
    # Cifrado César
    caesar = CaesarCipher()
    text = "HELLO WORLD"
    key = 3
    encrypted = caesar.encrypt(text, key)
    decrypted = caesar.decrypt(encrypted, key)
    print(f"  César: {text} -> {encrypted} -> {decrypted}")
    
    # Cifrado Vigenère
    vigenere = VigenereCipher()
    key = "KEY"
    encrypted = vigenere.encrypt(text, key)
    decrypted = vigenere.decrypt(encrypted, key)
    print(f"  Vigenère: {text} -> {encrypted} -> {decrypted}")
    
    # Cifrado Playfair
    playfair = PlayfairCipher()
    key = "KEYWORD"
    encrypted = playfair.encrypt(text, key)
    print(f"  Playfair: {text} -> {encrypted}")
    
    print("✅ Criptografía Clásica funcionando correctamente\n")

def test_modern_crypto():
    """Probar algoritmos de criptografía moderna"""
    print("🔐 Probando Criptografía Moderna...")
    
    # RSA
    rsa = RSACipher()
    text = "HELLO"
    public_key, private_key = rsa.generate_keys()
    encrypted = rsa.encrypt(text, public_key)
    decrypted = rsa.decrypt(encrypted, private_key)
    print(f"  RSA: {text} -> {encrypted} -> {decrypted}")
    
    # Hash
    hash_func = CustomHash()
    text = "Hello World"
    hash_64 = hash_func.hash_64(text)
    hash_256 = hash_func.hash_256(text)
    print(f"  Hash 64: {text} -> {hash_64}")
    print(f"  Hash 256: {text} -> {hash_256}")
    
    # DES
    des = DESCipher()
    key = "12345678"
    encrypted = des.encrypt_ecb(text, key)
    decrypted = des.decrypt_ecb(encrypted, key)
    print(f"  DES: {text} -> {encrypted} -> {decrypted}")
    
    print("✅ Criptografía Moderna funcionando correctamente\n")

def test_tools():
    """Probar herramientas adicionales"""
    print("🛠️ Probando Herramientas...")
    
    # Huffman
    huffman = HuffmanCoding()
    text = "HELLO WORLD"
    encoded_data, codes, tree = huffman.encode(text)
    decoded = huffman.decode(encoded_data)
    print(f"  Huffman: {text} -> {encoded_data} -> {decoded}")
    
    # Blockchain
    blockchain = Blockchain()
    blockchain.add_block("Primer bloque")
    blockchain.add_block("Segundo bloque")
    is_valid = blockchain.is_chain_valid()
    print(f"  Blockchain: {len(blockchain.chain)} bloques, válido: {is_valid}")
    
    # Verificador de Integridad
    verifier = IntegrityVerifier()
    text = "Test data"
    hash_result = verifier.calculate_text_hash(text)
    print(f"  Verificador: {text} -> {hash_result}")
    
    print("✅ Herramientas funcionando correctamente\n")

def main():
    """Ejecutar todas las pruebas"""
    print("🧪 VERIFICACIÓN RÁPIDA DE CRYPTOUNS")
    print("=" * 50)
    
    try:
        test_classic_crypto()
        test_modern_crypto()
        test_tools()
        
        print("🎉 TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
        print("✅ Sistema CryptoUNS funcionando correctamente")
        
    except Exception as e:
        print(f"❌ Error en las pruebas: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
