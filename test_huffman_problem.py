#!/usr/bin/env python3
"""
Script para simular el problema exacto de Huffman
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from crypto.tools import HuffmanCoding

def simulate_gui_problem():
    """Simular el problema exacto de la GUI"""
    print("🔍 Simulando el problema de la GUI con Huffman...")
    
    # Simular el texto que aparece en la captura de pantalla
    input_text = "HOLA MUNDO"
    print(f"Texto de entrada: '{input_text}'")
    
    # Crear instancia de Huffman
    hc = HuffmanCoding()
    
    # Paso 1: Codificar
    print("\n1. Codificando...")
    encoded_data = hc.encode_for_gui(input_text)
    print(f"   Código binario: {encoded_data['encoded'][:30]}...")
    print(f"   Tamaño original: {encoded_data['original_size']} bits")
    print(f"   Tamaño comprimido: {encoded_data['compressed_size']} bits")
    
    # Paso 2: Decodificar
    print("\n2. Decodificando...")
    decoded_text = hc.decode_for_gui(encoded_data['encoded'], encoded_data['codes'])
    print(f"   Texto decodificado: '{decoded_text}'")
    print(f"   Longitud original: {len(input_text)}")
    print(f"   Longitud decodificada: {len(decoded_text)}")
    
    # Verificación
    is_correct = decoded_text == input_text
    print(f"\n3. Verificación:")
    print(f"   Textos iguales: {is_correct}")
    print(f"   Original: {repr(input_text)}")
    print(f"   Decodificado: {repr(decoded_text)}")
    
    if not is_correct:
        print("\n❌ PROBLEMA DETECTADO:")
        print(f"   El texto decodificado no coincide con el original")
        print(f"   Diferencias:")
        for i, (a, b) in enumerate(zip(input_text, decoded_text)):
            if a != b:
                print(f"   Posición {i}: '{a}' != '{b}'")
    else:
        print("\n✅ Funcionamiento correcto")
    
    # Verificar qué se muestra en el resultado
    print(f"\n4. Simulando el resultado que se muestra:")
    result_text = f"Texto Decodificado:\n\n"
    result_text += f"{decoded_text}\n\n"
    result_text += f"Verificación:\n"
    result_text += f"• Decodificación {'✅ CORRECTA' if is_correct else '❌ INCORRECTA'}\n"
    result_text += f"• Longitud original: {len(input_text)} caracteres\n"
    result_text += f"• Longitud decodificada: {len(decoded_text)} caracteres\n"
    
    print("   Resultado que debería mostrarse:")
    print("   " + "="*50)
    print("   " + result_text.replace("\n", "\n   "))
    print("   " + "="*50)

if __name__ == "__main__":
    simulate_gui_problem()
