#!/usr/bin/env python3
"""
Prueba rápida de funcionalidad de Firma Digital
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_signature_functionality():
    """Probar la funcionalidad de firma digital"""
    try:
        from crypto.modern import DigitalSignature
        
        print("🔐 Probando funcionalidad de Firma Digital...")
        
        # Crear instancia
        ds = DigitalSignature()
        
        # Generar claves
        public_key, private_key = ds.generate_keys(512)  # Tamaño pequeño para rapidez
        print(f"✅ Claves generadas exitosamente")
        
        # Firmar mensaje
        message = "Mensaje de prueba para verificar contraste"
        signature = ds.sign_message(message, private_key)
        print(f"✅ Mensaje firmado exitosamente")
        
        # Verificar firma válida
        is_valid = ds.verify_signature(message, signature, public_key)
        print(f"✅ Verificación (válida): {is_valid}")
        
        # Verificar con mensaje modificado
        modified_message = "Mensaje MODIFICADO para verificar contraste"
        is_invalid = ds.verify_signature(modified_message, signature, public_key)
        print(f"✅ Verificación (inválida): {is_invalid}")
        
        if is_valid and not is_invalid:
            print("🎊 Funcionalidad de Firma Digital verificada exitosamente!")
            return True
        else:
            print("❌ Error en la verificación de firma")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_signature_functionality()
    print(f"\n{'✅ PRUEBA EXITOSA' if success else '❌ PRUEBA FALLIDA'}")
