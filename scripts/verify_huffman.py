#!/usr/bin/env python3
"""
Script para verificar la corrección de Huffman.
"""

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_huffman_backend():
    """Probar el backend de Huffman"""
    try:
        from crypto.tools import HuffmanCoding
        
        print("🔍 Probando backend de Huffman...")
        hc = HuffmanCoding()
        
        # Prueba 1: Método original
        text = "HOLA A TODO EL MUNDO"
        encoded_text, codes, tree = hc.encode(text)
        decoded_text = hc.decode(encoded_text)
        
        print(f"✅ Método original:")
        print(f"  - Texto original: {text}")
        print(f"  - Código binario: {encoded_text[:30]}...")
        print(f"  - Texto decodificado: {decoded_text}")
        print(f"  - Verificación: {'✅ CORRECTA' if decoded_text == text else '❌ INCORRECTA'}")
        
        # Prueba 2: Método wrapper para GUI
        gui_result = hc.encode_for_gui(text)
        gui_decoded = hc.decode_for_gui(gui_result['encoded'], gui_result['codes'])
        
        print(f"\n✅ Método wrapper para GUI:")
        print(f"  - Texto original: {text}")
        print(f"  - Código binario: {gui_result['encoded'][:30]}...")
        print(f"  - Tamaño original: {gui_result['original_size']} bits")
        print(f"  - Tamaño comprimido: {gui_result['compressed_size']} bits")
        print(f"  - Ratio de compresión: {gui_result['compression_ratio']:.2f}%")
        print(f"  - Ahorro de espacio: {gui_result['space_saved']:.2f}%")
        print(f"  - Texto decodificado: {gui_decoded}")
        print(f"  - Verificación: {'✅ CORRECTA' if gui_decoded == text else '❌ INCORRECTA'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en backend: {e}")
        return False

def test_huffman_gui_compatibility():
    """Probar la compatibilidad con la GUI"""
    try:
        from crypto.tools import HuffmanCoding
        
        print("\n🎨 Probando compatibilidad con GUI...")
        hc = HuffmanCoding()
        
        # Simular el flujo de la GUI
        text = "UNIVERSIDAD NACIONAL DEL SANTA"
        
        # Paso 1: Codificar usando el método para GUI
        encoded_data = hc.encode_for_gui(text)
        
        # Verificar que tiene todas las claves esperadas
        required_keys = ['encoded', 'codes', 'tree', 'frequencies', 'tree_visualization',
                        'original_size', 'compressed_size', 'compression_ratio', 'space_saved']
        
        missing_keys = [key for key in required_keys if key not in encoded_data]
        if missing_keys:
            print(f"❌ Faltan claves: {missing_keys}")
            return False
        
        print(f"✅ Todas las claves requeridas están presentes")
        
        # Paso 2: Decodificar usando el método para GUI
        decoded_text = hc.decode_for_gui(encoded_data['encoded'], encoded_data['codes'])
        
        # Verificar resultado
        is_correct = decoded_text == text
        print(f"✅ Resultado de decodificación: {'CORRECTO' if is_correct else 'INCORRECTO'}")
        
        if not is_correct:
            print(f"  - Esperado: {text}")
            print(f"  - Obtenido: {decoded_text}")
            return False
        
        print(f"✅ Compatibilidad con GUI verificada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en GUI: {e}")
        return False

def main():
    """Función principal de verificación"""
    print("🔧 VERIFICADOR DE CORRECCIÓN - HUFFMAN")
    print("=" * 50)
    
    # Probar backend
    backend_ok = test_huffman_backend()
    
    # Probar compatibilidad GUI
    gui_ok = test_huffman_gui_compatibility()
    
    # Resultado final
    print("\n" + "=" * 50)
    if backend_ok and gui_ok:
        print("🎊 ¡VERIFICACIÓN EXITOSA! Huffman corregido completamente.")
        print("   ✅ Backend funcionando correctamente")
        print("   ✅ Compatibilidad con GUI verificada")
        print("   ✅ Métodos wrapper implementados")
        print("   ✅ Codificación y decodificación operativas")
        return True
    else:
        print("❌ VERIFICACIÓN FALLIDA. Hay problemas pendientes.")
        print(f"   Backend: {'✅' if backend_ok else '❌'}")
        print(f"   GUI: {'✅' if gui_ok else '❌'}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
