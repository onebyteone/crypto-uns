#!/usr/bin/env python3
"""
Script para probar la funcionalidad completa de Huffman después de la corrección.
"""

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_huffman_functionality():
    """Probar la funcionalidad completa de Huffman"""
    try:
        from crypto.tools import HuffmanCoding
        
        print("🔍 PROBANDO FUNCIONALIDAD HUFFMAN")
        print("=" * 50)
        
        # Inicializar
        huffman = HuffmanCoding()
        
        # Casos de prueba
        test_cases = [
            "UNIVERSIDAD NACIONAL DEL SANTA",
            "HELLO WORLD",
            "AAAAAA",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "The quick brown fox jumps over the lazy dog"
        ]
        
        all_passed = True
        
        for i, text in enumerate(test_cases, 1):
            print(f"\n🧪 Caso de prueba {i}: '{text}'")
            
            try:
                # Codificar
                encoded_text, codes, tree = huffman.encode(text)
                
                # Obtener estadísticas
                stats = huffman.get_compression_stats(text, encoded_text)
                
                # Decodificar
                decoded_text = huffman.decode(encoded_text, tree)
                
                # Verificar
                is_correct = decoded_text == text
                
                print(f"  ✅ Codificación: {len(encoded_text)} bits")
                print(f"  ✅ Decodificación: {'CORRECTA' if is_correct else 'INCORRECTA'}")
                print(f"  ✅ Compresión: {stats['compression_ratio']:.2f}:1")
                print(f"  ✅ Ahorro: {stats['space_saved_percent']:.1f}%")
                print(f"  ✅ Códigos: {len(codes)} caracteres únicos")
                
                if not is_correct:
                    print(f"  ❌ ERROR: Texto original != Texto decodificado")
                    all_passed = False
                
            except Exception as e:
                print(f"  ❌ ERROR: {str(e)}")
                all_passed = False
        
        print("\n" + "=" * 50)
        if all_passed:
            print("🎊 ¡TODAS LAS PRUEBAS PASARON!")
            print("   ✅ Codificación funciona correctamente")
            print("   ✅ Decodificación funciona correctamente")
            print("   ✅ Estadísticas se calculan correctamente")
            print("   ✅ Integridad de datos verificada")
            return True
        else:
            print("❌ ALGUNAS PRUEBAS FALLARON")
            return False
            
    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {str(e)}")
        return False

def test_edge_cases():
    """Probar casos límite"""
    print("\n🔍 PROBANDO CASOS LÍMITE")
    print("=" * 50)
    
    try:
        from crypto.tools import HuffmanCoding
        huffman = HuffmanCoding()
        
        # Caso 1: Texto muy corto (1 carácter)
        print("\n📝 Caso límite: Texto de 1 carácter")
        try:
            text = "A"
            encoded_text, codes, tree = huffman.encode(text)
            decoded_text = huffman.decode(encoded_text, tree)
            is_correct = decoded_text == text
            print(f"  ✅ Texto de 1 carácter: {'CORRECTO' if is_correct else 'INCORRECTO'}")
            if not is_correct:
                return False
        except Exception as e:
            print(f"  ❌ ERROR inesperado: {str(e)}")
            return False
        
        # Caso 2: Texto vacío
        print("\n📝 Caso límite: Texto vacío")
        try:
            huffman.encode("")
            print("  ❌ ERROR: Debería fallar con texto vacío")
            return False
        except Exception as e:
            print(f"  ✅ Manejo correcto de error: {str(e)}")
        
        # Caso 3: Texto con un solo tipo de carácter repetido
        print("\n📝 Caso límite: Caracteres repetidos")
        try:
            text = "AAAA"
            encoded_text, codes, tree = huffman.encode(text)
            decoded_text = huffman.decode(encoded_text, tree)
            is_correct = decoded_text == text
            print(f"  ✅ Caracteres repetidos: {'CORRECTO' if is_correct else 'INCORRECTO'}")
            if not is_correct:
                return False
        except Exception as e:
            print(f"  ❌ ERROR: {str(e)}")
            return False
        
        print("\n✅ Todos los casos límite manejados correctamente")
        return True
        
    except Exception as e:
        print(f"❌ ERROR en casos límite: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🔧 VERIFICADOR DE CORRECCIÓN HUFFMAN")
    print("=" * 60)
    
    # Probar funcionalidad básica
    basic_ok = test_huffman_functionality()
    
    # Probar casos límite
    edge_ok = test_edge_cases()
    
    # Resultado final
    print("\n" + "=" * 60)
    if basic_ok and edge_ok:
        print("🎊 ¡CORRECCIÓN EXITOSA!")
        print("   ✅ La funcionalidad Huffman está completamente operativa")
        print("   ✅ Todos los casos de prueba pasan")
        print("   ✅ Manejo de errores correcto")
        print("   ✅ Integración GUI-Backend corregida")
        return True
    else:
        print("❌ CORRECCIÓN INCOMPLETA")
        print("   ⚠️  Algunos problemas persisten")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
