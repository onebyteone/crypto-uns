#!/usr/bin/env python3
"""
Demostración Práctica: Pantalla de Blockchain
============================================

Este script demuestra cómo usar la pantalla de Blockchain en CryptoUNS
paso a paso, mostrando cada funcionalidad y concepto importante.

Ejecute este script para ver una demostración completa de:
1. Creación de bloques
2. Verificación de integridad
3. Simulación de alteraciones
4. Detección de problemas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.crypto.tools import Blockchain, Block
import time
from datetime import datetime

def print_separator(title=""):
    """Imprimir separador visual"""
    print("\n" + "="*60)
    if title:
        print(f"  {title}")
        print("="*60)
    print()

def print_block_info(block, index=None):
    """Mostrar información detallada de un bloque"""
    if index is not None:
        print(f"📦 BLOQUE {index}")
        print("-" * 40)
    
    print(f"Índice: {block.index}")
    print(f"Datos: {block.data}")
    print(f"Hash: {block.hash}")
    print(f"Hash Anterior: {block.previous_hash}")
    print(f"Timestamp: {datetime.fromtimestamp(block.timestamp).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Nonce: {block.nonce}")
    print()

def print_chain_status(blockchain):
    """Mostrar estado actual de la cadena"""
    print(f"📊 ESTADO DE LA CADENA")
    print("-" * 40)
    print(f"Número de bloques: {len(blockchain.chain)}")
    print(f"Dificultad: {blockchain.difficulty}")
    print(f"Cadena válida: {'✅ SÍ' if blockchain.is_chain_valid() else '❌ NO'}")
    
    if blockchain.chain:
        último_hash = blockchain.chain[-1].hash
        print(f"Último hash: {último_hash[:20]}...")
    
    bloques_alterados = blockchain.detect_tampering()
    if bloques_alterados:
        print(f"⚠️ Bloques alterados: {bloques_alterados}")
    else:
        print("✅ No se detectaron alteraciones")
    print()

def main():
    """Demostración principal"""
    print("🔗 DEMOSTRACIÓN: PANTALLA DE BLOCKCHAIN")
    print("=====================================")
    print()
    print("Esta demostración muestra cómo funciona la pantalla de Blockchain")
    print("y los conceptos fundamentales de la tecnología blockchain.")
    print()
    
    # Crear nueva blockchain
    print_separator("PASO 1: INICIALIZACIÓN")
    
    print("🚀 Creando nueva blockchain...")
    blockchain = Blockchain(difficulty=2)  # Dificultad reducida para demo
    print("✅ Blockchain creada con bloque génesis")
    print()
    
    # Mostrar estado inicial
    print_chain_status(blockchain)
    print_block_info(blockchain.chain[0], 0)
    
    input("Presione Enter para continuar...")
    
    # Agregar bloques
    print_separator("PASO 2: AGREGANDO BLOQUES")
    
    bloques_demo = [
        "Primera transacción - Alice paga 10 BTC a Bob",
        "Segunda transacción - Bob paga 5 BTC a Charlie",
        "Registro de evento - Nuevo usuario registrado",
        "Tercera transacción - Charlie paga 3 BTC a David",
        "Actualización del sistema - Versión 2.0 desplegada"
    ]
    
    for i, datos in enumerate(bloques_demo[:3], 1):  # Solo primeros 3 para demo
        print(f"📝 Agregando bloque {i}...")
        print(f"   Datos: {datos}")
        
        # Simular el proceso de minado
        start_time = time.time()
        nuevo_bloque = blockchain.add_block(datos)
        end_time = time.time()
        
        print(f"   ⛏️  Minado completado en {end_time - start_time:.2f} segundos")
        print(f"   🔒 Hash generado: {nuevo_bloque.hash[:20]}...")
        print(f"   ✅ Bloque agregado exitosamente")
        print()
    
    print_chain_status(blockchain)
    
    # Mostrar todos los bloques
    print("📋 TODOS LOS BLOQUES EN LA CADENA:")
    print("-" * 40)
    for i, bloque in enumerate(blockchain.chain):
        print(f"{i}. {bloque.data[:40]}... | Hash: {bloque.hash[:16]}...")
    print()
    
    input("Presione Enter para continuar...")
    
    # Verificar integridad
    print_separator("PASO 3: VERIFICACIÓN DE INTEGRIDAD")
    
    print("🔍 Verificando integridad de la cadena...")
    es_valida = blockchain.is_chain_valid()
    
    if es_valida:
        print("✅ RESULTADO: La cadena de bloques es válida e íntegra")
        print("   • Todos los hashes son correctos")
        print("   • Todos los enlaces están intactos")
        print("   • No se detectaron alteraciones")
    else:
        print("❌ RESULTADO: La cadena de bloques ha sido alterada")
    
    print()
    print("📊 VALIDACIÓN INDIVIDUAL DE BLOQUES:")
    print("-" * 40)
    for i, bloque in enumerate(blockchain.chain):
        es_valido = blockchain.is_block_valid(bloque)
        estado = "✅ VÁLIDO" if es_valido else "❌ INVÁLIDO"
        print(f"Bloque {i}: {estado}")
    
    print()
    input("Presione Enter para continuar...")
    
    # Simular alteración
    print_separator("PASO 4: SIMULACIÓN DE ALTERACIÓN")
    
    print("⚠️ SIMULANDO ALTERACIÓN MALICIOSA...")
    print("   (Esto es solo para demostración educativa)")
    print()
    
    if len(blockchain.chain) > 1:
        bloque_objetivo = 1
        datos_originales = blockchain.chain[bloque_objetivo].data
        
        print(f"🎯 Objetivo: Bloque {bloque_objetivo}")
        print(f"   Datos originales: {datos_originales}")
        print()
        
        # Alterar los datos (sin recalcular el hash)
        print("🔧 Alterando datos del bloque...")
        blockchain.chain[bloque_objetivo].data = "DATOS ALTERADOS MALICIOSAMENTE"
        
        print(f"   Datos alterados: {blockchain.chain[bloque_objetivo].data}")
        print("   ⚠️ NOTA: El hash NO se recalculó (simulando alteración maliciosa)")
        print()
        
        # Verificar nuevamente
        print("🔍 Verificando integridad después de la alteración...")
        es_valida_alterada = blockchain.is_chain_valid()
        
        if not es_valida_alterada:
            print("❌ RESULTADO: Alteración detectada exitosamente")
            print("   • El sistema detectó la inconsistencia")
            print("   • La integridad de la cadena se ha comprometido")
        else:
            print("⚠️ RESULTADO: No se detectó alteración (error)")
        
        print()
        print("📊 VALIDACIÓN DESPUÉS DE ALTERACIÓN:")
        print("-" * 40)
        for i, bloque in enumerate(blockchain.chain):
            es_valido = blockchain.is_block_valid(bloque)
            estado = "✅ VÁLIDO" if es_valido else "❌ INVÁLIDO"
            print(f"Bloque {i}: {estado}")
            
            if not es_valido and i == bloque_objetivo:
                hash_esperado = bloque.calculate_hash()
                print(f"   Hash almacenado: {bloque.hash[:20]}...")
                print(f"   Hash calculado:  {hash_esperado[:20]}...")
                print(f"   ❌ Los hashes no coinciden")
        
        print()
        
        # Detectar bloques alterados
        bloques_alterados = blockchain.detect_tampering()
        if bloques_alterados:
            print(f"🚨 BLOQUES ALTERADOS DETECTADOS: {bloques_alterados}")
        
    else:
        print("⚠️ Se necesitan al menos 2 bloques para demostrar alteración")
    
    print()
    input("Presione Enter para continuar...")
    
    # Conceptos importantes
    print_separator("PASO 5: CONCEPTOS IMPORTANTES")
    
    print("💡 CONCEPTOS CLAVE DEMOSTRADOS:")
    print("-" * 40)
    print("1. 🔗 ENLACE CRIPTOGRÁFICO")
    print("   • Cada bloque contiene el hash del bloque anterior")
    print("   • Esto crea una cadena inmutable")
    print("   • Alterar un bloque rompe toda la cadena")
    print()
    
    print("2. 🛡️ INTEGRIDAD DE DATOS")
    print("   • El hash SHA-256 actúa como huella digital")
    print("   • Cualquier cambio produce un hash diferente")
    print("   • La verificación es automática e inmediata")
    print()
    
    print("3. ⛏️ PRUEBA DE TRABAJO")
    print("   • Requiere esfuerzo computacional para crear bloques")
    print("   • El 'nonce' se incrementa hasta encontrar hash válido")
    print("   • Previene spam y ataques maliciosos")
    print()
    
    print("4. 🔍 DETECCIÓN DE ALTERACIONES")
    print("   • Comparación automática de hashes")
    print("   • Identificación inmediata de inconsistencias")
    print("   • Garantía de integridad histórica")
    print()
    
    # Demostrar uso en GUI
    print_separator("APLICACIÓN EN LA GUI")
    
    print("🖥️ EN LA INTERFAZ GRÁFICA:")
    print("-" * 40)
    print("1. 📝 Campo 'Datos del bloque' → Ingrese texto")
    print("2. ➕ Botón 'Agregar Bloque' → Crea y mina nuevo bloque")
    print("3. 🔍 Botón 'Verificar Integridad' → Valida toda la cadena")
    print("4. ⚠️ Botón 'Simular Alteración' → Demuestra detección")
    print("5. 🗑️ Botón 'Limpiar Cadena' → Reinicia blockchain")
    print()
    
    print("📊 VISUALIZACIÓN EN TABLA:")
    print("-" * 40)
    print("• Índice: Posición del bloque en la cadena")
    print("• Datos: Contenido almacenado (truncado)")
    print("• Hash: Identificador único del bloque")
    print("• Hash Anterior: Enlace al bloque previo")
    print("• Timestamp: Fecha y hora de creación")
    print("• Válido: ✅ íntegro, ❌ alterado")
    print()
    
    # Casos de uso
    print_separator("CASOS DE USO EDUCATIVOS")
    
    print("🎓 PARA ESTUDIANTES:")
    print("-" * 40)
    print("• Crear cadenas de diferentes longitudes")
    print("• Experimentar con diferentes tipos de datos")
    print("• Observar cómo cambian los hashes")
    print("• Entender la inmutabilidad prácticamente")
    print()
    
    print("👨‍🏫 PARA EDUCADORES:")
    print("-" * 40)
    print("• Demostrar conceptos criptográficos")
    print("• Mostrar seguridad de blockchain")
    print("• Explicar prueba de trabajo")
    print("• Enseñar detección de alteraciones")
    print()
    
    print("👨‍💻 PARA DESARROLLADORES:")
    print("-" * 40)
    print("• Estudiar implementación de blockchain")
    print("• Entender algoritmos de hash")
    print("• Analizar estructuras de datos")
    print("• Experimentar con parámetros")
    print()
    
    print_separator("DEMOSTRACIÓN COMPLETADA")
    
    print("🎉 ¡DEMOSTRACIÓN COMPLETADA EXITOSAMENTE!")
    print()
    print("📚 RECURSOS ADICIONALES:")
    print("• BLOCKCHAIN_USER_GUIDE.md - Guía completa de usuario")
    print("• src/crypto/tools.py - Implementación del backend")
    print("• src/gui/main_window.py - Interfaz gráfica")
    print()
    print("🔄 PRÓXIMOS PASOS:")
    print("• Abra la aplicación CryptoUNS (main.py)")
    print("• Navegue a la pantalla de Blockchain")
    print("• Practique con los conocimientos adquiridos")
    print("• Experimente con diferentes escenarios")
    print()
    print("¡Gracias por usar CryptoUNS! 🚀")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Demostración interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la demostración: {str(e)}")
        import traceback
        traceback.print_exc()
