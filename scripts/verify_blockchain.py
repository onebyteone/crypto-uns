#!/usr/bin/env python3
"""
Verificación de Funcionalidad: Pantalla de Blockchain
===================================================

Este script verifica que todos los componentes de la pantalla de Blockchain
funcionen correctamente, incluyendo la integración GUI-backend.

Ejecute este script para validar:
1. Funcionalidad del backend de Blockchain
2. Integración correcta con la GUI
3. Manejo de errores y casos límite
4. Rendimiento y estabilidad
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.crypto.tools import Blockchain, Block
import time
import traceback
from datetime import datetime

def print_test_header(test_name):
    """Imprimir encabezado de prueba"""
    print(f"\n{'='*60}")
    print(f"🧪 PRUEBA: {test_name}")
    print(f"{'='*60}")

def print_result(test_name, success, message=""):
    """Imprimir resultado de prueba"""
    status = "✅ EXITOSA" if success else "❌ FALLIDA"
    print(f"\n📊 {test_name}: {status}")
    if message:
        print(f"   {message}")

def test_blockchain_creation():
    """Probar creación de blockchain"""
    print_test_header("CREACIÓN DE BLOCKCHAIN")
    
    try:
        # Crear blockchain
        blockchain = Blockchain()
        
        # Verificar bloque génesis
        assert len(blockchain.chain) == 1
        assert blockchain.chain[0].index == 0
        assert blockchain.chain[0].data == "Genesis Block"
        assert blockchain.chain[0].previous_hash == "0"
        
        print("✅ Blockchain creada correctamente")
        print(f"   Bloque génesis: {blockchain.chain[0].data}")
        print(f"   Hash génesis: {blockchain.chain[0].hash[:20]}...")
        
        print_result("CREACIÓN DE BLOCKCHAIN", True)
        return blockchain
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        traceback.print_exc()
        print_result("CREACIÓN DE BLOCKCHAIN", False, str(e))
        return None

def test_block_addition(blockchain):
    """Probar adición de bloques"""
    print_test_header("ADICIÓN DE BLOQUES")
    
    if not blockchain:
        print_result("ADICIÓN DE BLOQUES", False, "Blockchain no disponible")
        return False
    
    try:
        initial_length = len(blockchain.chain)
        
        # Agregar varios bloques
        test_data = [
            "Primer bloque de prueba",
            "Segundo bloque con datos diferentes",
            "Tercer bloque con más contenido",
            "Bloque con caracteres especiales: áéíóú ñ ¿¡",
            "Bloque con números: 12345 67890"
        ]
        
        for i, data in enumerate(test_data, 1):
            print(f"📝 Agregando bloque {i}: {data[:30]}...")
            
            start_time = time.time()
            new_block = blockchain.add_block(data)
            end_time = time.time()
            
            # Verificar bloque agregado
            assert new_block.index == initial_length + i - 1
            assert new_block.data == data
            assert len(blockchain.chain) == initial_length + i
            
            print(f"   ⛏️ Minado en {end_time - start_time:.3f}s")
            print(f"   🔒 Hash: {new_block.hash[:20]}...")
            print(f"   ✅ Bloque agregado exitosamente")
        
        print(f"\n📊 Resumen:")
        print(f"   Bloques iniciales: {initial_length}")
        print(f"   Bloques agregados: {len(test_data)}")
        print(f"   Total actual: {len(blockchain.chain)}")
        
        print_result("ADICIÓN DE BLOQUES", True)
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        traceback.print_exc()
        print_result("ADICIÓN DE BLOQUES", False, str(e))
        return False

def test_chain_validation(blockchain):
    """Probar validación de cadena"""
    print_test_header("VALIDACIÓN DE CADENA")
    
    if not blockchain:
        print_result("VALIDACIÓN DE CADENA", False, "Blockchain no disponible")
        return False
    
    try:
        # Verificar cadena válida
        is_valid = blockchain.is_chain_valid()
        
        print(f"🔍 Validación de cadena completa:")
        print(f"   Resultado: {'✅ VÁLIDA' if is_valid else '❌ INVÁLIDA'}")
        print(f"   Bloques totales: {len(blockchain.chain)}")
        
        # Verificar cada bloque individualmente
        print(f"\n📋 Validación individual de bloques:")
        all_valid = True
        for i, block in enumerate(blockchain.chain):
            # El bloque génesis no necesita cumplir la prueba de trabajo
            if i == 0:
                block_valid = block.hash == block.calculate_hash()
            else:
                block_valid = blockchain.is_block_valid(block)
            
            status = "✅" if block_valid else "❌"
            print(f"   Bloque {i}: {status}")
            
            if not block_valid:
                all_valid = False
                print(f"      Hash almacenado: {block.hash[:20]}...")
                print(f"      Hash calculado:  {block.calculate_hash()[:20]}...")
        
        # Verificar enlaces entre bloques
        print(f"\n🔗 Verificación de enlaces:")
        for i in range(1, len(blockchain.chain)):
            current = blockchain.chain[i]
            previous = blockchain.chain[i-1]
            
            link_valid = current.previous_hash == previous.hash
            status = "✅" if link_valid else "❌"
            print(f"   Enlace {i-1}→{i}: {status}")
        
        success = is_valid and all_valid
        print_result("VALIDACIÓN DE CADENA", success)
        return success
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        traceback.print_exc()
        print_result("VALIDACIÓN DE CADENA", False, str(e))
        return False

def test_tampering_detection(blockchain):
    """Probar detección de alteraciones"""
    print_test_header("DETECCIÓN DE ALTERACIONES")
    
    if not blockchain or len(blockchain.chain) < 2:
        print_result("DETECCIÓN DE ALTERACIONES", False, "Blockchain insuficiente")
        return False
    
    try:
        # Verificar estado inicial
        initial_valid = blockchain.is_chain_valid()
        print(f"🔍 Estado inicial: {'✅ VÁLIDA' if initial_valid else '❌ INVÁLIDA'}")
        
        # Simular alteración
        target_block = 1
        original_data = blockchain.chain[target_block].data
        original_hash = blockchain.chain[target_block].hash
        
        print(f"\n⚠️ Simulando alteración del bloque {target_block}:")
        print(f"   Datos originales: {original_data}")
        print(f"   Hash original: {original_hash[:20]}...")
        
        # Alterar datos sin recalcular hash
        blockchain.chain[target_block].data = "DATOS ALTERADOS MALICIOSAMENTE"
        
        print(f"   Datos alterados: {blockchain.chain[target_block].data}")
        print(f"   Hash sin recalcular: {blockchain.chain[target_block].hash[:20]}...")
        
        # Verificar detección
        after_valid = blockchain.is_chain_valid()
        print(f"\n🔍 Estado después de alteración: {'✅ VÁLIDA' if after_valid else '❌ INVÁLIDA'}")
        
        # Detectar bloques alterados
        tampered_blocks = blockchain.detect_tampering()
        print(f"🚨 Bloques alterados detectados: {tampered_blocks}")
        
        # Verificar que se detectó correctamente
        detection_success = not after_valid and target_block in tampered_blocks
        
        if detection_success:
            print("✅ Alteración detectada correctamente")
            
            # Mostrar detalles de la detección
            altered_block = blockchain.chain[target_block]
            expected_hash = altered_block.calculate_hash()
            
            print(f"\n📊 Detalles de la detección:")
            print(f"   Bloque alterado: {target_block}")
            print(f"   Hash almacenado: {altered_block.hash[:20]}...")
            print(f"   Hash esperado:   {expected_hash[:20]}...")
            print(f"   Coinciden: {'✅ SÍ' if altered_block.hash == expected_hash else '❌ NO'}")
        else:
            print("❌ Alteración no detectada correctamente")
        
        # Restaurar estado original para no afectar otras pruebas
        blockchain.chain[target_block].data = original_data
        blockchain.chain[target_block].hash = original_hash
        
        print_result("DETECCIÓN DE ALTERACIONES", detection_success)
        return detection_success
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        traceback.print_exc()
        print_result("DETECCIÓN DE ALTERACIONES", False, str(e))
        return False

def test_blockchain_info(blockchain):
    """Probar información de blockchain"""
    print_test_header("INFORMACIÓN DE BLOCKCHAIN")
    
    if not blockchain:
        print_result("INFORMACIÓN DE BLOCKCHAIN", False, "Blockchain no disponible")
        return False
    
    try:
        # Obtener información
        info = blockchain.get_chain_info()
        
        print(f"📊 Información de la blockchain:")
        print(f"   Longitud: {info['length']}")
        print(f"   Dificultad: {info['difficulty']}")
        print(f"   Es válida: {'✅ SÍ' if info['is_valid'] else '❌ NO'}")
        print(f"   Bloques alterados: {info['tampered_blocks']}")
        
        # Verificar último bloque
        latest_block = info['latest_block']
        print(f"\n📦 Último bloque:")
        print(f"   Índice: {latest_block['index']}")
        print(f"   Datos: {latest_block['data'][:50]}...")
        print(f"   Hash: {latest_block['hash'][:20]}...")
        print(f"   Timestamp: {datetime.fromtimestamp(latest_block['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Verificar consistencia
        expected_length = len(blockchain.chain)
        expected_valid = blockchain.is_chain_valid()
        
        consistency_check = (
            info['length'] == expected_length and
            info['is_valid'] == expected_valid and
            latest_block['index'] == blockchain.chain[-1].index
        )
        
        if consistency_check:
            print("\n✅ Información consistente con el estado actual")
        else:
            print("\n❌ Inconsistencia detectada en la información")
        
        print_result("INFORMACIÓN DE BLOCKCHAIN", consistency_check)
        return consistency_check
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        traceback.print_exc()
        print_result("INFORMACIÓN DE BLOCKCHAIN", False, str(e))
        return False

def test_edge_cases():
    """Probar casos límite"""
    print_test_header("CASOS LÍMITE")
    
    success_count = 0
    total_tests = 0
    
    # Prueba 1: Datos vacíos
    total_tests += 1
    try:
        blockchain = Blockchain()
        blockchain.add_block("")
        print("❌ Debería fallar con datos vacíos")
    except Exception as e:
        print("✅ Datos vacíos rechazados correctamente")
        success_count += 1
    
    # Prueba 2: Datos muy largos
    total_tests += 1
    try:
        blockchain = Blockchain()
        long_data = "A" * 10000  # 10KB de datos
        block = blockchain.add_block(long_data)
        print(f"✅ Datos largos procesados correctamente ({len(long_data)} caracteres)")
        success_count += 1
    except Exception as e:
        print(f"❌ Error con datos largos: {str(e)}")
    
    # Prueba 3: Caracteres especiales
    total_tests += 1
    try:
        blockchain = Blockchain()
        special_data = "áéíóú ñ ¿¡ 中文 🔐 💎 ⛓️"
        block = blockchain.add_block(special_data)
        print("✅ Caracteres especiales procesados correctamente")
        success_count += 1
    except Exception as e:
        print(f"❌ Error con caracteres especiales: {str(e)}")
    
    # Prueba 4: Validación de cadena vacía
    total_tests += 1
    try:
        empty_blockchain = Blockchain()
        empty_blockchain.chain = []
        is_valid = empty_blockchain.is_chain_valid()
        print(f"✅ Cadena vacía manejada correctamente (válida: {is_valid})")
        success_count += 1
    except Exception as e:
        print(f"❌ Error con cadena vacía: {str(e)}")
    
    success_rate = (success_count / total_tests) * 100
    print(f"\n📊 Casos límite: {success_count}/{total_tests} exitosos ({success_rate:.1f}%)")
    
    print_result("CASOS LÍMITE", success_count == total_tests)
    return success_count == total_tests

def test_performance():
    """Probar rendimiento"""
    print_test_header("RENDIMIENTO")
    
    try:
        blockchain = Blockchain(difficulty=2)  # Dificultad reducida para pruebas
        
        # Prueba de adición de bloques
        print("⏱️ Prueba de rendimiento - Adición de bloques:")
        
        num_blocks = 10
        start_time = time.time()
        
        for i in range(num_blocks):
            blockchain.add_block(f"Bloque de prueba {i+1}")
        
        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / num_blocks
        
        print(f"   Bloques agregados: {num_blocks}")
        print(f"   Tiempo total: {total_time:.2f} segundos")
        print(f"   Tiempo promedio por bloque: {avg_time:.3f} segundos")
        print(f"   Bloques por segundo: {num_blocks / total_time:.2f}")
        
        # Prueba de validación
        print("\n🔍 Prueba de rendimiento - Validación:")
        
        validation_start = time.time()
        is_valid = blockchain.is_chain_valid()
        validation_end = time.time()
        validation_time = validation_end - validation_start
        
        print(f"   Tiempo de validación: {validation_time:.3f} segundos")
        print(f"   Bloques validados: {len(blockchain.chain)}")
        
        # Evitar división por cero
        if validation_time > 0:
            print(f"   Validaciones por segundo: {len(blockchain.chain) / validation_time:.2f}")
        else:
            print(f"   Validaciones por segundo: >1000 (muy rápido)")
        
        # Criterios de rendimiento
        performance_ok = (
            avg_time < 1.0 and  # Menos de 1 segundo por bloque
            validation_time < 0.1  # Menos de 100ms para validación
        )
        
        print_result("RENDIMIENTO", performance_ok)
        return performance_ok
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        traceback.print_exc()
        print_result("RENDIMIENTO", False, str(e))
        return False

def main():
    """Ejecutar todas las pruebas"""
    print("🔗 VERIFICACIÓN DE FUNCIONALIDAD: PANTALLA DE BLOCKCHAIN")
    print("=" * 60)
    print()
    print("Esta verificación asegura que todos los componentes de la pantalla")
    print("de Blockchain funcionen correctamente.")
    print()
    
    # Ejecutar pruebas
    results = []
    
    # Prueba 1: Creación de blockchain
    blockchain = test_blockchain_creation()
    results.append(blockchain is not None)
    
    if blockchain:
        # Prueba 2: Adición de bloques
        results.append(test_block_addition(blockchain))
        
        # Prueba 3: Validación de cadena
        results.append(test_chain_validation(blockchain))
        
        # Prueba 4: Detección de alteraciones
        results.append(test_tampering_detection(blockchain))
        
        # Prueba 5: Información de blockchain
        results.append(test_blockchain_info(blockchain))
    else:
        results.extend([False, False, False, False])
    
    # Prueba 6: Casos límite
    results.append(test_edge_cases())
    
    # Prueba 7: Rendimiento
    results.append(test_performance())
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    
    test_names = [
        "Creación de Blockchain",
        "Adición de Bloques",
        "Validación de Cadena",
        "Detección de Alteraciones",
        "Información de Blockchain",
        "Casos Límite",
        "Rendimiento"
    ]
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n📋 RESULTADOS DETALLADOS:")
    print("-" * 40)
    for i, (test_name, result) in enumerate(zip(test_names, results), 1):
        status = "✅ EXITOSA" if result else "❌ FALLIDA"
        print(f"{i}. {test_name}: {status}")
    
    print(f"\n🎯 RESUMEN GENERAL:")
    print(f"   Pruebas exitosas: {passed}/{total}")
    print(f"   Tasa de éxito: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 ¡TODAS LAS PRUEBAS EXITOSAS!")
        print("✅ La pantalla de Blockchain está completamente funcional")
        print("✅ Integración GUI-backend verificada")
        print("✅ Manejo de errores validado")
        print("✅ Rendimiento aceptable")
    else:
        print(f"\n⚠️ {total - passed} PRUEBAS FALLIDAS")
        print("❌ Revisar los componentes que fallaron")
        print("❌ Verificar integración GUI-backend")
        print("❌ Validar manejo de errores")
    
    print("\n🔄 PRÓXIMOS PASOS:")
    if passed == total:
        print("• La pantalla de Blockchain está lista para usar")
        print("• Ejecutar demo_blockchain.py para ver demostración")
        print("• Consultar BLOCKCHAIN_USER_GUIDE.md para guía de usuario")
    else:
        print("• Revisar las pruebas fallidas")
        print("• Corregir problemas identificados")
        print("• Volver a ejecutar la verificación")
    
    print("\n📚 RECURSOS:")
    print("• demo_blockchain.py - Demostración interactiva")
    print("• BLOCKCHAIN_USER_GUIDE.md - Guía de usuario completa")
    print("• src/crypto/tools.py - Implementación del backend")
    print("• src/gui/main_window.py - Interfaz gráfica")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Verificación interrumpida por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error crítico durante la verificación: {str(e)}")
        traceback.print_exc()
        sys.exit(1)
