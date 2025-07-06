"""
Demo del proceso completo de RSA en CryptoUNS
"""
from src.crypto.modern import RSACipher

def demo_rsa_completo():
    print("🔐 DEMOSTRACIÓN COMPLETA DE RSA")
    print("=" * 50)
    
    # Crear instancia de RSA
    rsa = RSACipher()
    
    # 1. Generar claves
    print("1️⃣ Generando claves RSA...")
    public_key, private_key = rsa.generate_keys()
    print(f"   Clave pública: (e={public_key[0]}, n={str(public_key[1])[:50]}...)")
    print(f"   Clave privada: (d={str(private_key[0])[:50]}..., n={str(private_key[1])[:50]}...)")
    print()
    
    # 2. Mensaje original
    mensaje = "HELLO WORLD"
    print(f"2️⃣ Mensaje original: '{mensaje}'")
    
    # 3. Conversión a números
    numeros = [ord(c) for c in mensaje]
    print(f"   Códigos ASCII: {numeros}")
    numero_completo = int(''.join(f"{ord(c):03d}" for c in mensaje))
    print(f"   Número completo: {numero_completo}")
    print()
    
    # 4. Cifrado
    print("3️⃣ Proceso de cifrado...")
    cifrado = rsa.encrypt(mensaje, public_key)
    print(f"   Aplicando: c = m^e mod n")
    print(f"   Resultado cifrado: {cifrado}")
    print(f"   Longitud del número cifrado: {len(str(cifrado))} dígitos")
    print()
    
    # 5. Descifrado
    print("4️⃣ Proceso de descifrado...")
    descifrado = rsa.decrypt(cifrado, private_key)
    print(f"   Aplicando: m = c^d mod n")
    print(f"   Resultado descifrado: '{descifrado}'")
    print()
    
    # 6. Verificación
    print("5️⃣ Verificación:")
    if mensaje == descifrado:
        print("   ✅ ¡Cifrado y descifrado exitoso!")
    else:
        print("   ❌ Error en el proceso")
    
    print("\n" + "=" * 50)
    print("💡 CONCLUSIÓN:")
    print("RSA convierte texto → números → cifra → descifra → texto")
    print("Los números cifrados son la representación segura del mensaje.")

if __name__ == "__main__":
    demo_rsa_completo()
