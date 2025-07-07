# 🔧 Scripts de Utilidad

Esta carpeta contiene scripts útiles para el mantenimiento y operación del proyecto CryptoUNS.

## 📁 Contenido

### 🧹 clean_project.py
Script de limpieza automática que elimina:
- Archivos cache de Python (`__pycache__`, `*.pyc`)
- Directorios de build y distribución
- Archivos temporales de pruebas
- Logs antiguos (mantiene solo los 5 más recientes)

**Uso:**
```bash
python scripts/clean_project.py
```

### 🔍 verify_*.py
Scripts de verificación para diferentes componentes:
- `verify_blockchain.py`: Verifica la implementación del blockchain
- `verify_contrast.py`: Verifica la funcionalidad de contraste
- `verify_huffman.py`: Verifica la implementación de Huffman
- `verify_system.py`: Verificación general del sistema

### 🛠️ fix_grid_errors.py
Script para corrección de errores específicos de la interfaz gráfica.

## 🚀 Ejecución

Todos los scripts se ejecutan desde la raíz del proyecto:

```bash
# Limpieza del proyecto
python scripts/clean_project.py

# Verificación del sistema
python scripts/verify_system.py

# Verificación específica
python scripts/verify_blockchain.py
```

## 📋 Mantenimiento

Se recomienda ejecutar `clean_project.py` regularmente para mantener el proyecto optimizado y libre de archivos innecesarios.
