# 🔗 Guía de Uso: Pantalla de Blockchain

## Descripción General

La pantalla de Blockchain del sistema CryptoUNS es una implementación educativa que demuestra los conceptos fundamentales de la tecnología blockchain, incluyendo:

- **Cadena de bloques**: Una secuencia de bloques enlazados criptográficamente
- **Integridad de datos**: Verificación de que los datos no han sido alterados
- **Prueba de trabajo**: Algoritmo de consenso que requiere esfuerzo computacional
- **Detección de alteraciones**: Identificación automática de bloques modificados

## Elementos de la Interfaz

### Panel Izquierdo - Controles

#### 1. **Campo de Datos del Bloque**
- **Ubicación**: Parte superior del panel izquierdo
- **Función**: Ingrese aquí los datos que desea almacenar en el nuevo bloque
- **Ejemplo**: "Transacción #1", "Datos importantes", "Registro de evento"

#### 2. **Botón "➕ Agregar Bloque"**
- **Color**: Verde (Success)
- **Función**: Crear y agregar un nuevo bloque a la cadena
- **Requisito**: Debe haber texto en el campo de datos

#### 3. **Botón "🔍 Verificar Integridad"**
- **Color**: Azul (Info)
- **Función**: Verificar que toda la cadena de bloques sea válida
- **Resultado**: Muestra si la cadena es íntegra o ha sido alterada

#### 4. **Botón "⚠️ Simular Alteración"**
- **Color**: Amarillo (Warning)
- **Función**: Altera deliberadamente un bloque para demostrar la detección
- **Propósito**: Educativo - mostrar cómo se detectan las alteraciones

#### 5. **Botón "🗑️ Limpiar Cadena"**
- **Color**: Rojo (Danger)
- **Función**: Reiniciar la blockchain, eliminando todos los bloques

#### 6. **Panel de Información**
- **Bloques**: Número total de bloques en la cadena
- **Último hash**: Primeros 20 caracteres del hash del último bloque

### Panel Derecho - Visualización

#### 7. **Tabla de Bloques**
- **Índice**: Número secuencial del bloque (0, 1, 2, ...)
- **Datos**: Contenido almacenado en el bloque (truncado a 30 caracteres)
- **Hash**: Hash SHA-256 del bloque (truncado a 20 caracteres)
- **Hash Anterior**: Hash del bloque previo (truncado a 20 caracteres)
- **Timestamp**: Fecha y hora de creación del bloque
- **Válido**: ✅ si el bloque es válido, ❌ si está alterado

#### 8. **Área de Resultados**
- **Ubicación**: Parte inferior del panel derecho
- **Función**: Mostrar resultados de verificación de integridad

## Flujo de Uso Paso a Paso

### 🚀 Paso 1: Iniciando con Blockchain

1. **Acceder a la pantalla**: Haga clic en "Blockchain" en el menú principal
2. **Observar el estado inicial**: La cadena comienza con el "Bloque Génesis" (índice 0)
3. **Revisar la información**: El panel muestra "Bloques: 1"

### 📝 Paso 2: Agregar Nuevos Bloques

1. **Escribir datos**: En el campo "Datos del bloque", ingrese:
   ```
   Primera transacción
   ```

2. **Agregar el bloque**: Haga clic en "➕ Agregar Bloque"

3. **Observar el resultado**:
   - Aparece un nuevo bloque (índice 1) en la tabla
   - El campo de datos se limpia automáticamente
   - La información muestra "Bloques: 2"
   - Se muestra un mensaje de éxito

4. **Agregar más bloques** (repita para comprender mejor):
   ```
   Segunda transacción
   ```
   ```
   Registro de evento importante
   ```

### 🔍 Paso 3: Verificar Integridad

1. **Ejecutar verificación**: Haga clic en "🔍 Verificar Integridad"

2. **Leer el resultado** (en el área de resultados):
   ```
   ✅ La cadena de bloques es válida e íntegra
   ```

3. **Observar la tabla**:
   - Todos los bloques muestran ✅ en la columna "Válido"
   - Los hashes están correctamente enlazados

### ⚠️ Paso 4: Simular Alteración (Demostración Educativa)

1. **Alterar un bloque**: Haga clic en "⚠️ Simular Alteración"

2. **Observar los cambios**:
   - El bloque índice 1 cambia sus datos a "DATOS ALTERADOS"
   - El hash del bloque no se recalcula (simulando alteración maliciosa)
   - Se muestra un mensaje informativo

3. **Verificar nuevamente**: Haga clic en "🔍 Verificar Integridad"

4. **Analizar el resultado**:
   ```
   ❌ La cadena de bloques ha sido alterada o es inválida
   ```

5. **Examinar la tabla**:
   - El bloque alterado muestra ❌ en la columna "Válido"
   - Los bloques siguientes también pueden mostrar ❌ debido al efecto cascada

### 🗑️ Paso 5: Limpiar y Reiniciar

1. **Limpiar la cadena**: Haga clic en "🗑️ Limpiar Cadena"

2. **Verificar el reinicio**:
   - La tabla se vacía
   - La información muestra "Bloques: 0"
   - El área de resultados se limpia

## Conceptos Importantes Demostrados

### 🔗 Enlace Criptográfico
- Cada bloque contiene el hash del bloque anterior
- Esto crea una cadena inmutable de bloques
- Alterar un bloque rompe la cadena completa

### 🛡️ Integridad de Datos
- El hash SHA-256 actúa como una "huella digital" única
- Cualquier cambio en los datos produce un hash completamente diferente
- La verificación detecta automáticamente las alteraciones

### ⏰ Timestamp
- Cada bloque tiene una marca de tiempo
- Proporciona un registro cronológico de las transacciones
- Útil para auditorías y trazabilidad

### 🔍 Detección de Alteraciones
- El sistema compara el hash almacenado con el hash calculado
- Las discrepancias indican alteraciones
- La detección es inmediata y automática

## Casos de Uso Educativos

### 1. **Demostración de Inmutabilidad**
```
Agregar bloque → Verificar integridad → Simular alteración → Verificar nuevamente
```

### 2. **Comprensión del Enlace Criptográfico**
```
Observar cómo cada "Hash Anterior" coincide con el "Hash" del bloque previo
```

### 3. **Análisis de Integridad**
```
Comparar el estado antes y después de una alteración
```

### 4. **Construcción de Cadenas**
```
Agregar múltiples bloques para ver cómo crece la cadena
```

## Características Técnicas

### Algoritmo de Hash
- **SHA-256**: Función criptográfica estándar
- **Salida**: 64 caracteres hexadecimales
- **Seguridad**: Resistente a colisiones

### Prueba de Trabajo
- **Dificultad**: 4 (requiere 4 ceros iniciales en el hash)
- **Minado**: Automático al agregar bloques
- **Nonce**: Número variable para encontrar hash válido

### Validación
- **Verificación de hash**: Comparación con hash calculado
- **Verificación de enlace**: Hash anterior debe coincidir
- **Verificación de secuencia**: Índices consecutivos

## Mensajes del Sistema

### Éxito ✅
- "Bloque agregado exitosamente"
- "Cadena válida"
- "Cadena de bloques limpiada"

### Advertencias ⚠️
- "Por favor ingrese datos para el bloque"
- "Necesita al menos 2 bloques para simular alteración"
- "Cadena inválida"

### Información ℹ️
- "Simulación de alteración realizada en el bloque índice 1"

## Consejos de Uso

### Para Educadores
1. **Empezar simple**: Agregar solo 2-3 bloques inicialmente
2. **Explicar conceptos**: Mostrar cómo funciona el enlace criptográfico
3. **Demostrar alteraciones**: Usar la simulación para mostrar detección
4. **Comparar estados**: Mostrar antes/después de alteraciones

### Para Estudiantes
1. **Experimentar**: Probar diferentes tipos de datos
2. **Observar patrones**: Ver cómo cambian los hashes
3. **Entender la inmutabilidad**: Apreciar la seguridad del enlace
4. **Practicar verificación**: Usar el botón de verificación frecuentemente

### Para Desarrolladores
1. **Analizar implementación**: Revisar el código fuente
2. **Entender algoritmos**: Estudiar SHA-256 y prueba de trabajo
3. **Experimentar con parámetros**: Modificar dificultad de minado
4. **Implementar mejoras**: Agregar funcionalidades adicionales

## Solución de Problemas

### Problema: No se agrega el bloque
**Solución**: Verificar que el campo de datos no esté vacío

### Problema: La verificación siempre falla
**Solución**: Reiniciar la cadena con el botón "Limpiar Cadena"

### Problema: No se ve el efecto de la alteración
**Solución**: Agregar al menos 2 bloques antes de simular alteración

### Problema: Los hashes no se muestran completos
**Solución**: Esto es normal, se truncan para mejorar la visualización

## Extensiones Posibles

### Para Proyectos Avanzados
1. **Múltiples algoritmos de hash**
2. **Diferentes niveles de dificultad**
3. **Transacciones complejas**
4. **Visualización gráfica de la cadena**
5. **Exportación de datos**
6. **Comparación de cadenas**

---

Esta guía le proporcionará una comprensión completa de cómo usar la pantalla de Blockchain en CryptoUNS para aprender los conceptos fundamentales de la tecnología blockchain de manera práctica e interactiva.
