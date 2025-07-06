# 🔐 Sistema Criptográfico: CryptoUNS
## Especificación del Proyecto Final - Segunda Unidad

### 📋 **INFORMACIÓN GENERAL**

**Curso:** Seguridad Informática IX Ciclo  
**Producto:** Software de Criptografía Integral  
**Duración:** 4 semanas  
**Modalidad:** Proyecto individual/grupal  
**Stack Tecnológico:** Python + ttkbootstrap  

---

## 🎯 **OBJETIVO GENERAL**

Desarrollar una aplicación de escritorio que integre todos los métodos criptográficos estudiados en la segunda unidad, proporcionando una interfaz gráfica moderna, funcional y educativa que permita cifrar, descifrar, y analizar diferentes técnicas criptográficas.

---

## 📊 **ENTREGABLES**

### 1. **Software Ejecutable**
- ✅ Aplicación de escritorio funcional
- ✅ Interfaz gráfica moderna con ttkbootstrap
- ✅ Compatibilidad multiplataforma (Windows, macOS, Linux)

### 2. **Manual de Usuario**
- ✅ Documento PDF profesional
- ✅ Guía de instalación y uso
- ✅ Ejemplos prácticos por cada método
- ✅ Capturas de pantalla

### 3. **Código Fuente**
- ✅ Código limpio y comentado
- ✅ Estructura modular
- ✅ Documentación técnica

---

## 🔧 **STACK TECNOLÓGICO**

### **Core Technologies**
```python
# requirements.txt
ttkbootstrap==1.10.1
pillow==10.0.0
pyperclip==1.8.2
cryptography==41.0.0
```

### **Herramientas de Desarrollo**
- **Python:** 3.9+
- **IDE:** VS Code / PyCharm
- **Packaging:** PyInstaller
- **Testing:** pytest (opcional)

---

## 🏗️ **ARQUITECTURA DEL PROYECTO**

### **Estructura de Carpetas**
```
📁 CryptoUNS/
├── 🐍 main.py                 # Punto de entrada
├── 📁 src/
│   ├── 🎨 gui/                # Interfaz gráfica
│   │   ├── __init__.py
│   │   ├── main_window.py     # Ventana principal
│   │   ├── classic_crypto.py  # Pantallas criptografía clásica
│   │   ├── modern_crypto.py   # Pantallas criptografía moderna
│   │   ├── tools_gui.py       # Herramientas adicionales
│   │   └── components.py      # Componentes reutilizables
│   ├── 🔐 crypto/             # Algoritmos criptográficos
│   │   ├── __init__.py
│   │   ├── classic.py         # César, Vigenère, Playfair
│   │   ├── modern.py          # RSA, Hash, DES
│   │   ├── tools.py           # Huffman, Kasiski, Blockchain
│   │   └── utils.py           # Funciones auxiliares
│   ├── 🛠️ utils/              # Utilidades generales
│   │   ├── __init__.py
│   │   ├── file_manager.py    # Manejo de archivos
│   │   ├── validators.py      # Validaciones
│   │   └── constants.py       # Constantes
│   └── 📊 data/               # Datos y configuración
│       ├── config.py          # Configuración de la app
│       └── themes.py          # Temas personalizados
├── 📁 assets/
│   ├── 🖼️ icons/             # Iconos SVG/PNG
│   ├── 🎨 images/            # Imágenes de la aplicación
│   └── 📋 templates/         # Plantillas de documentos
├── 📁 docs/
│   ├── 📖 Manual_Usuario.md
│   ├── 🔧 Manual_Tecnico.md
│   ├── 📸 screenshots/
│   └── 📋 ejemplos/
├── 📁 tests/                  # Pruebas unitarias
│   ├── test_classic.py
│   ├── test_modern.py
│   └── test_tools.py
├── 📦 dist/                   # Ejecutables generados
├── 📄 requirements.txt
├── 📄 README.md
└── 📄 setup.py
```

---

## 💻 **FUNCIONALIDADES REQUERIDAS**

### **📚 1. CRIPTOGRAFÍA CLÁSICA**

#### **A. Cifrado César**
- **Función:** Cifrado por sustitución monoalfabética
- **Entrada:** Texto plano + clave numérica (1-25)
- **Salida:** Texto cifrado/descifrado
- **Validaciones:** Clave válida, texto no vacío

#### **B. Cifrado Vigenère**
- **Función:** Cifrado polialfabético con clave repetida
- **Entrada:** Texto plano + clave alfabética
- **Salida:** Texto cifrado/descifrado
- **Validaciones:** Clave alfabética, longitud mínima

#### **C. Cifrado Playfair**
- **Función:** Cifrado digráfico con matriz 5x5
- **Entrada:** Texto plano + clave alfabética
- **Salida:** Texto cifrado
- **Características:** Manejo de caracteres duplicados

#### **D. Método de Kasiski**
- **Función:** Análisis para romper Vigenère
- **Entrada:** Texto cifrado con Vigenère
- **Salida:** Longitud probable de la clave
- **Características:** Búsqueda de patrones repetidos

### **🔒 2. CRIPTOGRAFÍA MODERNA**

#### **A. Algoritmo RSA**
- **Función:** Criptografía asimétrica
- **Características:**
  - Generación de claves (p, q, n, e, d)
  - Cifrado con clave pública
  - Descifrado con clave privada
  - Validación de números primos

#### **B. Funciones Hash**
- **Tipos:** Hash 64, 128, 256 bits + SHA-256
- **Función:** Generación de resúmenes criptográficos
- **Características:**
  - Efecto avalancha
  - Verificación de integridad
  - Comparación de hashes

#### **C. Cifrado DES**
- **Función:** Cifrado simétrico por bloques
- **Características:**
  - Modo ECB/CBC
  - Cifrado/descifrado
  - Validación de claves

#### **D. Firma Digital**
- **Función:** Autenticación y no repudio
- **Proceso:** Hash del mensaje + cifrado con clave privada
- **Verificación:** Descifrado con clave pública + comparación

### **🛠️ 3. HERRAMIENTAS ADICIONALES**

#### **A. Codificación Huffman**
- **Función:** Compresión de datos
- **Características:**
  - Generación de árbol de frecuencias
  - Codificación variable
  - Análisis de compresión

#### **B. Simulador de Blockchain**
- **Función:** Cadena de bloques básica
- **Características:**
  - Bloques con hash
  - Verificación de integridad
  - Detección de alteraciones

#### **C. Verificador de Integridad**
- **Función:** Comparación de archivos/textos
- **Método:** Comparación de hashes
- **Salida:** Confirmación de integridad

---

## 🎨 **ESPECIFICACIONES DE DISEÑO**

### **Tema Visual**
```python
# Configuración de ttkbootstrap
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Tema principal
THEME = "darkly"  # Alternativas: flatly, pulse, solar, cyborg

# Paleta de colores
COLORS = {
    'primary': '#007bff',
    'secondary': '#6c757d',
    'success': '#28a745',
    'warning': '#ffc107',
    'danger': '#dc3545',
    'info': '#17a2b8'
}
```

### **Estructura de la Interfaz**

#### **Ventana Principal**
```
┌─────────────────────────────────────────────────────────┐
│  🔐 CryptoUNS                             [−] [□] [×]  │
├─────────────────────────────────────────────────────────┤
│  [📚 Criptografía Clásica] [🔒 Criptografía Moderna]   │
│  [🛠️ Herramientas]        [ℹ️ Acerca de]              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│              Área de Contenido Dinámico                │
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │  Texto Entrada  │  │  Texto Salida   │              │
│  │                 │  │                 │              │
│  │                 │  │                 │              │
│  └─────────────────┘  └─────────────────┘              │
│                                                         │
│  [🔑 Clave: ________]  [⚙️ Configuración]              │
│                                                         │
│  [🔒 Cifrar] [🔓 Descifrar] [📋 Copiar] [🗑️ Limpiar]   │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  Estado: Listo                           v1.0.0        │
└─────────────────────────────────────────────────────────┘
```

### **Componentes UI**

#### **Campos de Entrada**
- **Texto:** Área de texto con scroll
- **Clave:** Campo de entrada con validación
- **Configuración:** Controles específicos por método

#### **Botones de Acción**
- **Cifrar/Descifrar:** Acciones principales
- **Generar:** Para claves RSA o matrices
- **Copiar:** Al clipboard
- **Limpiar:** Resetear campos
- **Ayuda:** Información contextual

#### **Área de Resultados**
- **Texto formateado:** Monospace para códigos
- **Estadísticas:** Información adicional
- **Validaciones:** Mensajes de error/éxito

---

## ⚙️ **FUNCIONALIDADES TÉCNICAS**

### **1. Validaciones**
```python
# Ejemplos de validaciones requeridas
def validate_caesar_key(key):
    """Validar clave César (1-25)"""
    return 1 <= key <= 25

def validate_vigenere_key(key):
    """Validar clave Vigenère (solo letras)"""
    return key.isalpha() and len(key) >= 2

def validate_rsa_primes(p, q):
    """Validar números primos para RSA"""
    return is_prime(p) and is_prime(q) and p != q
```

### **2. Manejo de Errores**
```python
# Sistema de manejo de errores
class CryptoError(Exception):
    """Excepción base para errores criptográficos"""
    pass

class InvalidKeyError(CryptoError):
    """Error de clave inválida"""
    pass

class InvalidInputError(CryptoError):
    """Error de entrada inválida"""
    pass
```

### **3. Utilidades**
```python
# Funciones auxiliares
def copy_to_clipboard(text):
    """Copiar texto al clipboard"""
    pyperclip.copy(text)

def save_to_file(content, filename):
    """Guardar contenido en archivo"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def load_from_file(filename):
    """Cargar contenido desde archivo"""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()
```

---

## 📋 **CRITERIOS DE EVALUACIÓN**

| **Criterio** | **Peso** | **Descripción** | **Puntuación** |
|--------------|----------|-----------------|----------------|
| **Funcionalidad** | 40% | Todos los métodos criptográficos funcionan correctamente | 8 pts |
| **Interfaz de Usuario** | 25% | UI moderna, intuitiva y responsiva | 5 pts |
| **Manual de Usuario** | 20% | Documentación completa y clara | 4 pts |
| **Calidad del Código** | 10% | Estructura, comentarios, buenas prácticas | 2 pts |
| **Características Adicionales** | 5% | Funcionalidades extra o innovadoras | 1 pt |
| **TOTAL** | **100%** | | **20 pts** |

### **Criterios Específicos de Funcionalidad**

#### **Criptografía Clásica (2 pts)**
- ✅ César: Cifrado/descifrado funcional
- ✅ Vigenère: Cifrado/descifrado funcional
- ✅ Playfair: Cifrado funcional
- ✅ Kasiski: Análisis básico

#### **Criptografía Moderna (4 pts)**
- ✅ RSA: Generación de claves y cifrado/descifrado
- ✅ Hash: Múltiples algoritmos funcionando
- ✅ DES: Cifrado simétrico básico
- ✅ Firma Digital: Proceso completo

#### **Herramientas (2 pts)**
- ✅ Huffman: Compresión básica
- ✅ Blockchain: Simulador funcional
- ✅ Verificación: Comparación de hashes

---

## 🚀 **CARACTERÍSTICAS ADICIONALES (BONUS)**

### **Funcionalidades Opcionales (+0.5 pts c/u)**

#### **🔧 Gestión Avanzada**
- **Gestor de Claves:** Guardar/cargar claves RSA
- **Historial:** Registro de operaciones
- **Exportar/Importar:** Archivos de configuración

#### **🎨 Mejoras de UX**
- **Temas:** Modo claro/oscuro
- **Animaciones:** Transiciones suaves
- **Notificaciones:** Alertas de operaciones

#### **📊 Análisis Avanzado**
- **Estadísticas:** Frecuencia de caracteres
- **Benchmarking:** Tiempo de ejecución
- **Análisis de Fortaleza:** Evaluación de claves

#### **🌐 Integraciones**
- **Clipboard:** Detección automática
- **Arrastrar y Soltar:** Archivos de texto
- **Multiidioma:** Español/Inglés

---

## 📖 **MANUAL DE USUARIO**

### **Estructura del Manual**

#### **1. Introducción**
- Objetivo del software
- Requisitos del sistema
- Instalación y configuración

#### **2. Guía de Uso**
- Navegación por la interfaz
- Tutorial por cada método criptográfico
- Ejemplos prácticos paso a paso

#### **3. Métodos Criptográficos**
- **Criptografía Clásica:**
  - César: Teoría y práctica
  - Vigenère: Teoría y práctica
  - Playfair: Teoría y práctica
  - Kasiski: Análisis de texto
  
- **Criptografía Moderna:**
  - RSA: Generación de claves y uso
  - Hash: Verificación de integridad
  - DES: Cifrado simétrico
  - Firma Digital: Autenticación

#### **4. Herramientas Adicionales**
- Huffman: Compresión de datos
- Blockchain: Simulador básico
- Verificación: Control de integridad

#### **5. Solución de Problemas**
- Errores comunes y soluciones
- Preguntas frecuentes
- Contacto y soporte

#### **6. Anexos**
- Capturas de pantalla
- Ejemplos de uso
- Referencias bibliográficas

---

## 🔧 **GUÍA DE INSTALACIÓN**

### **Requisitos del Sistema**
- **Sistema Operativo:** Windows 10+, macOS 10.14+, Linux Ubuntu 18.04+
- **Python:** 3.9 o superior
- **RAM:** 4GB mínimo
- **Espacio en disco:** 500MB

### **Instalación para Desarrollo**
```bash
# 1. Clonar el repositorio
git clone https://github.com/onebyteone/crypto-uns.git
cd crypto-uns

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Ejecutar aplicación
python main.py
```

### **Instalación para Usuario Final**
```bash
# Opción 1: Ejecutable
# Descargar archivo .exe/.app/.deb desde releases
# Ejecutar directamente

# Opción 2: Desde código fuente
pip install ttkbootstrap pillow pyperclip
python main.py
```

---

## 🧪 **TESTING Y VALIDACIÓN**

### **Pruebas Unitarias**
```python
# Ejemplo de pruebas requeridas
def test_caesar_cipher():
    """Probar cifrado César"""
    result = caesar_cipher("HELLO", 3)
    assert result == "KHOOR"

def test_vigenere_cipher():
    """Probar cifrado Vigenère"""
    result = vigenere_cipher("HELLO", "KEY")
    assert result == "RIJVS"

def test_rsa_key_generation():
    """Probar generación de claves RSA"""
    public, private = generate_rsa_keys(61, 53)
    assert public is not None
    assert private is not None
```

### **Casos de Prueba**
| **Método** | **Entrada** | **Salida Esperada** | **Estado** |
|------------|-------------|---------------------|------------|
| César | "HELLO", 3 | "KHOOR" | ✅ |
| Vigenère | "HELLO", "KEY" | "RIJVS" | ✅ |
| RSA | p=61, q=53 | Claves válidas | ✅ |

---

## 📅 **CRONOGRAMA DE DESARROLLO**

### **Semana 1: Configuración y Backend**
- **Días 1-2:** Configuración del proyecto y estructura
- **Días 3-4:** Implementación de criptografía clásica
- **Días 5-7:** Implementación de criptografía moderna

### **Semana 2: Interfaz de Usuario**
- **Días 1-3:** Diseño de la interfaz principal
- **Días 4-5:** Implementación de pantallas específicas
- **Días 6-7:** Integración backend-frontend

### **Semana 3: Funcionalidades Avanzadas**
- **Días 1-3:** Herramientas adicionales
- **Días 4-5:** Validaciones y manejo de errores
- **Días 6-7:** Optimización y pulido

### **Semana 4: Documentación y Entrega**
- **Días 1-3:** Manual de usuario
- **Días 4-5:** Documentación técnica
- **Días 6-7:** Preparación de entrega final

---

## 🎯 **CHECKLIST DE ENTREGA**

### **Software**
- [ ] Aplicación ejecutable funcional
- [ ] Todos los métodos criptográficos implementados
- [ ] Interfaz gráfica completa y funcional
- [ ] Validaciones y manejo de errores
- [ ] Código fuente comentado y estructurado

### **Documentación**
- [ ] Manual de usuario completo (PDF)
- [ ] Capturas de pantalla de todas las funcionalidades
- [ ] Ejemplos de uso prácticos
- [ ] Guía de instalación
- [ ] README.md actualizado

### **Calidad**
- [ ] Código sin errores críticos
- [ ] Interfaz intuitiva y responsive
- [ ] Funcionalidades probadas
- [ ] Documentación clara y profesional
- [ ] Cumplimiento de todos los requerimientos

---

## 💡 **CONSEJOS PARA EL DESARROLLO**

### **Mejores Prácticas**
1. **Desarrollo Incremental:** Implementar funcionalidades una a una
2. **Testing Continuo:** Probar cada función antes de continuar
3. **Documentación:** Comentar código conforme se desarrolla
4. **Backup:** Versionar código regularmente
5. **UI/UX:** Priorizar experiencia del usuario

### **Recursos Útiles**
- **ttkbootstrap:** https://ttkbootstrap.readthedocs.io/
- **Python Crypto:** https://docs.python.org/3/library/crypto.html
- **PyInstaller:** https://pyinstaller.readthedocs.io/
- **Markdown:** https://guides.github.com/features/mastering-markdown/

### **Errores Comunes a Evitar**
- No validar entradas del usuario
- Hardcodear rutas de archivos
- No manejar excepciones
- Interfaz poco intuitiva
- Documentación incompleta

---

## 🏆 **CRITERIOS DE EXCELENCIA**

### **Para obtener calificación máxima:**
1. **Funcionalidad Completa:** Todos los métodos funcionan perfectamente
2. **Interfaz Excepcional:** UI moderna, intuitiva y atractiva
3. **Documentación Profesional:** Manual completo con ejemplos
4. **Código Limpio:** Estructura clara, comentarios, buenas prácticas
5. **Innovación:** Características adicionales creativas

### **Elementos Diferenciadores:**
- **Experiencia de Usuario:** Interfaz que "wow" al usuario
- **Robustez:** Manejo elegante de errores
- **Performance:** Operaciones rápidas y eficientes
- **Profesionalismo:** Presentación de calidad comercial

---

## 📋 **ENTREGA FINAL**

### **Criterios de Aceptación**
- ✅ Entrega completa y a tiempo
- ✅ Archivo ejecutable funcional
- ✅ Código fuente incluido
- ✅ Documentación completa
- ✅ Cumplimiento de todos los requerimientos

---

## 🎊 **¡ÉXITO EN SU PROYECTO!**

Este proyecto representa la culminación de sus conocimientos en criptografía. Demuestren su creatividad, habilidades técnicas y compromiso con la excelencia. ¡Esperamos ver aplicaciones innovadoras y profesionales!

---

*📝 Documento actualizado: 06 de julio, 2025*  
*🔗 Versión: 1.0.0*  
*👨‍🏫 Autor: Equipo docente Seguridad Informática*