# 🔐 CryptoUNS - Sistema Criptográfico Integral

Sistema completo de criptografía con interfaz gráfica moderna desarrollado en Python con ttkbootstrap.

## 📋 Descripción

CryptoUNS es un sistema integral que implementa múltiples algoritmos criptográficos clásicos y modernos, junto con herramientas adicionales de análisis y seguridad, todo ello en una interfaz gráfica moderna e intuitiva.

## ✨ Características

### 📚 Criptografía Clásica
- **Cifrado César**: Cifrado por sustitución monoalfabética
- **Cifrado Vigenère**: Cifrado polialfabético con clave repetida
- **Cifrado Playfair**: Cifrado digráfico con matriz 5x5
- **Método de Kasiski**: Análisis para romper Vigenère

### 🔒 Criptografía Moderna
- **Algoritmo RSA**: Criptografía asimétrica completa
- **Funciones Hash**: SHA-256 y algoritmos personalizados
- **Cifrado DES**: Cifrado simétrico por bloques
- **Firma Digital**: Autenticación y no repudio

### 🛠️ Herramientas Adicionales
- **Codificación Huffman**: Compresión de datos
- **Simulador Blockchain**: Cadena de bloques básica
- **Verificador de Integridad**: Comparación de archivos/textos

## 🏗️ Arquitectura

```
📁 CryptoUNS/
├── 🐍 main.py                 # Punto de entrada
├── 📁 src/
│   ├── 🎨 gui/                # Interfaz gráfica
│   ├── 🔐 crypto/             # Algoritmos criptográficos
│   ├── 🛠️ utils/              # Utilidades generales
│   └── 📊 data/               # Configuración y datos
├── 📁 assets/                 # Recursos gráficos
├── 📁 docs/                   # Documentación
├── 📁 tests/                  # Pruebas unitarias
└── 📁 dist/                   # Ejecutables
```

## 🚀 Instalación

### Requisitos del Sistema
- **Python**: 3.9 o superior
- **Sistema Operativo**: Windows 10+, macOS 10.14+, Linux Ubuntu 18.04+
- **RAM**: 4GB mínimo
- **Espacio en disco**: 500MB

### Instalación Rápida

1. **Clonar el repositorio**:
```bash
git clone https://github.com/onebyteone/crypto-uns.git
cd crypto-uns
```

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Ejecutar la aplicación**:
```bash
python main.py
```

### Dependencias Principales
- `ttkbootstrap==1.10.1` - Interfaz gráfica moderna
- `pillow==10.0.0` - Manejo de imágenes
- `pyperclip==1.8.2` - Funcionalidades de clipboard
- `cryptography==41.0.0` - Criptografía moderna
- `numpy==1.24.3` - Operaciones matemáticas

## 🎯 Estado del Proyecto

### ✅ Fase 1 - Arquitectura Base (COMPLETADA)
- [x] Estructura de carpetas creada
- [x] Dependencias configuradas  
- [x] Configuración base implementada
- [x] Tema visual configurado
- [x] Punto de entrada funcional
- [x] Sistema de logging
- [x] Manejo de excepciones

### ✅ Fase 2 - Algoritmos Criptográficos (COMPLETADA)
- [x] Criptografía clásica implementada
- [x] Criptografía moderna implementada
- [x] Herramientas adicionales implementadas
- [x] 92/92 pruebas unitarias creadas y pasando

### ✅ Fase 3 - Interfaz Gráfica (COMPLETADA)
- [x] Ventana principal diseñada
- [x] 12 pantallas específicas creadas
- [x] Navegación implementada
- [x] Backend integrado con frontend
- [x] Manejo robusto de errores

### 🚀 Próximas Fases

#### 🔧 Fase 4 - Funcionalidades Avanzadas
- [ ] Funcionalidades de clipboard
- [ ] Manejo avanzado de archivos
- [ ] Validaciones mejoradas
- [ ] Características UX (tooltips, ayuda)
- [ ] Optimizaciones de rendimiento

## 🛠️ Desarrollo

### Estructura de Desarrollo
- **Lenguaje**: Python 3.9+
- **Framework GUI**: ttkbootstrap
- **Testing**: pytest
- **Empaquetado**: PyInstaller
- **Documentación**: Markdown

### Configuración de Desarrollo

1. **Crear entorno virtual**:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

2. **Instalar dependencias de desarrollo**:
```bash
pip install -r requirements.txt
```

3. **Ejecutar en modo desarrollo**:
```bash
python main.py
```

### Testing
```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar pruebas específicas
pytest tests/test_classic.py
pytest tests/test_modern.py
pytest tests/test_tools.py
```

## 📊 Métricas Actuales

- **Progreso General**: 15% (Fase 1 completada)
- **Líneas de Código**: ~1,500
- **Archivos Creados**: 15
- **Dependencias**: 8 principales
- **Funcionalidades**: 0/13 algoritmos implementados

## 🎨 Capturas de Pantalla

### Interfaz Principal (Temporal)
![Interfaz Principal](docs/screenshots/main_window.png)

*Nota: Las capturas se agregarán conforme se desarrolle la interfaz completa.*

## 📖 Documentación

- [Manual de Usuario](docs/Manual_Usuario.md) *(En desarrollo)*
- [Manual Técnico](docs/Manual_Tecnico.md) *(En desarrollo)*
- [Guía de Instalación](docs/instalacion.md) *(En desarrollo)*
- [Roadmap Detallado](ROADMAP.md) *(Completado)*

## 🤝 Contribución

### Cómo Contribuir
1. Fork del repositorio
2. Crear rama para nueva característica
3. Implementar cambios con pruebas
4. Enviar Pull Request

### Estándares de Código
- Seguir PEP 8
- Documentar funciones y clases
- Incluir pruebas unitarias
- Comentarios en español

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## 👥 Equipo

**CryptoUNS Team**
- Desarrollo: GitHub Copilot Assistant
- Arquitectura: Diseño modular y escalable
- Testing: Pruebas unitarias completas
- Documentación: Manuales técnicos y de usuario

## 📞 Contacto y Soporte

- **GitHub**: [https://github.com/onebyteone/crypto-uns](https://github.com/onebyteone/crypto-uns)
- **Issues**: Reportar bugs y solicitar características
- **Email**: crypto@uns.edu.ar

## 🔄 Historial de Versiones

### v1.0.0 (06 de julio, 2025) - Fase 1
- ✅ Arquitectura base implementada
- ✅ Estructura de proyecto creada
- ✅ Configuración inicial
- ✅ Interfaz temporal funcional
- ✅ Sistema de logging
- ✅ Manejo de excepciones

### Próximas Versiones
- **v1.1.0**: Algoritmos criptográficos básicos
- **v1.2.0**: Interfaz gráfica completa
- **v1.3.0**: Funcionalidades avanzadas
- **v2.0.0**: Versión final con todas las características

## 🎊 Agradecimientos

Agradecemos al curso de Seguridad Informática IX Ciclo por la oportunidad de desarrollar este proyecto integral de criptografía.

---

**CryptoUNS v1.0.0** - Sistema Criptográfico Integral  
*Desarrollado con ❤️ y Python*

## 🚀 Inicio Rápido

```bash
# Clonar e instalar
git clone https://github.com/onebyteone/crypto-uns.git
cd crypto-uns
pip install -r requirements.txt

# Ejecutar
python main.py
```

¡Disfruta explorando el mundo de la criptografía con CryptoUNS! 🔐
