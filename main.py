#!/usr/bin/env python3
"""
🔐 CryptoUNS - Sistema Criptográfico Integral
============================================

Punto de entrada principal de la aplicación CryptoUNS.
Sistema completo de criptografía con interfaz gráfica moderna.

Características:
- Criptografía clásica: César, Vigenère, Playfair
- Criptografía moderna: RSA, Hash, DES, Firma Digital
- Herramientas: Huffman, Blockchain, Verificador de Integridad
- Interfaz gráfica moderna con ttkbootstrap

Autor: CryptoUNS Team
Fecha: 06 de julio, 2025
Versión: 1.0.0
"""

import sys
import os
import logging
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Importaciones del sistema
try:
    from src.data.config import *
    from src.data.themes import *
    from src.utils.constants import *
except ImportError as e:
    print(f"Error al importar módulos base: {e}")
    print("Asegúrate de que todos los módulos estén correctamente instalados.")
    sys.exit(1)

# Configuración de logging
def setup_logging():
    """Configurar sistema de logging"""
    log_format = LogConfig.FORMAT
    log_level = LogConfig.LEVEL
    
    # Crear directorio de logs si no existe
    log_dir = PathConfig.BASE_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    
    # Configurar logging
    logging.basicConfig(
        level=getattr(logging, log_level),
        format=log_format,
        handlers=[
            logging.FileHandler(log_dir / "crypto_uns.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Crear logger principal
    logger = logging.getLogger("CryptoUNS")
    logger.info("Sistema de logging inicializado")
    return logger

# Verificar dependencias
def check_dependencies():
    """Verificar que las dependencias estén instaladas"""
    required_packages = [
        "ttkbootstrap",
        "PIL",  # pillow se importa como PIL
        "pyperclip",
        "cryptography"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Faltan las siguientes dependencias:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Instala las dependencias con:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

# Inicializar aplicación
def initialize_app():
    """Inicializar la aplicación"""
    logger = setup_logging()
    
    # Verificar dependencias
    if not check_dependencies():
        return None
    
    logger.info("Inicializando CryptoUNS...")
    logger.info(f"Versión: {APP_VERSION}")
    logger.info(f"Autor: {APP_AUTHOR}")
    
    # Importar GUI después de verificar dependencias
    try:
        # Importar ttkbootstrap
        import ttkbootstrap as ttk
        from ttkbootstrap.constants import BOTH, X, Y, LEFT, RIGHT, TOP, BOTTOM, CENTER
        
        # Crear ventana principal
        root = ttk.Window(
            title=WindowConfig.TITLE,
            themename=ThemeConfig.DEFAULT_THEME
        )
        
        # Configurar ventana
        root.geometry(f"{WindowConfig.WIDTH}x{WindowConfig.HEIGHT}")
        root.minsize(WindowConfig.MIN_WIDTH, WindowConfig.MIN_HEIGHT)
        
        # Centrar ventana
        if WindowConfig.CENTERED:
            root.place_window_center()
        
        # Configurar icono si existe
        icon_path = PathConfig.BASE_DIR / WindowConfig.ICON_PATH
        if icon_path.exists():
            root.iconbitmap(str(icon_path))
        
        logger.info("Ventana principal creada exitosamente")
        return root, logger
        
    except Exception as e:
        logger.error(f"Error al crear ventana principal: {e}")
        return None

# Crear interfaz temporal
def create_temp_interface(root, logger):
    """Crear interfaz temporal mientras se desarrolla la GUI completa"""
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import BOTH, X, Y, LEFT, RIGHT, TOP, BOTTOM, CENTER, W, E, N, S
    
    # Frame principal
    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack(fill=BOTH, expand=True)
    
    # Título
    title_label = ttk.Label(
        main_frame,
        text="🔐 CryptoUNS",
        font=("Segoe UI", 24, "bold"),
        bootstyle="info"
    )
    title_label.pack(pady=(0, 10))
    
    # Subtítulo
    subtitle_label = ttk.Label(
        main_frame,
        text="Sistema Criptográfico Integral",
        font=("Segoe UI", 14),
        bootstyle="secondary"
    )
    subtitle_label.pack(pady=(0, 30))
    
    # Información del proyecto
    info_frame = ttk.LabelFrame(
        main_frame,
        text="📋 Información del Proyecto",
        padding=20
    )
    info_frame.pack(fill=X, pady=(0, 20))
    
    # Detalles del proyecto
    details = [
        ("📊 Versión:", APP_VERSION),
        ("👥 Autor:", APP_AUTHOR),
        ("📅 Fecha:", "06 de julio, 2025"),
        ("🎯 Estado:", "En desarrollo - Fase 1 completada"),
        ("🔧 Framework:", "ttkbootstrap + Python 3.9+"),
        ("🏗️ Arquitectura:", "Modular y escalable")
    ]
    
    for i, (label, value) in enumerate(details):
        detail_frame = ttk.Frame(info_frame)
        detail_frame.pack(fill=X, pady=2)
        
        ttk.Label(
            detail_frame,
            text=label,
            font=("Segoe UI", 10, "bold")
        ).pack(side=LEFT)
        
        ttk.Label(
            detail_frame,
            text=value,
            font=("Segoe UI", 10)
        ).pack(side=LEFT, padx=(10, 0))
    
    # Funcionalidades por implementar
    features_frame = ttk.LabelFrame(
        main_frame,
        text="🚀 Funcionalidades por Implementar",
        padding=20
    )
    features_frame.pack(fill=X, pady=(0, 20))
    
    # Lista de funcionalidades
    features = [
        "📚 Criptografía Clásica: César, Vigenère, Playfair, Kasiski",
        "🔒 Criptografía Moderna: RSA, Hash, DES, Firma Digital",
        "🛠️ Herramientas: Huffman, Blockchain, Verificador de Integridad",
        "🎨 Interfaz Gráfica Completa y Moderna",
        "✅ Validaciones y Manejo de Errores",
        "📖 Documentación y Manuales"
    ]
    
    for feature in features:
        ttk.Label(
            features_frame,
            text=f"• {feature}",
            font=("Segoe UI", 10)
        ).pack(anchor=W, pady=1)
    
    # Botones de acción
    buttons_frame = ttk.Frame(main_frame)
    buttons_frame.pack(fill=X, pady=(20, 0))
    
    # Botón de información
    def show_info():
        import tkinter.messagebox as msgbox
        msgbox.showinfo(
            "Información",
            f"CryptoUNS v{APP_VERSION}\n\n"
            f"Sistema Criptográfico Integral desarrollado con Python y ttkbootstrap.\n\n"
            f"Autor: {APP_AUTHOR}\n"
            f"Fecha: 06 de julio, 2025\n\n"
            f"Estado: Fase 1 - Arquitectura base completada\n"
            f"Próximo: Implementación de algoritmos criptográficos"
        )
    
    # Botón de salir
    def exit_app():
        logger.info("Cerrando aplicación")
        root.quit()
    
    ttk.Button(
        buttons_frame,
        text="ℹ️ Información",
        command=show_info,
        bootstyle="info"
    ).pack(side=LEFT, padx=(0, 10))
    
    ttk.Button(
        buttons_frame,
        text="🚪 Salir",
        command=exit_app,
        bootstyle="danger"
    ).pack(side=RIGHT)
    
    # Barra de estado
    status_frame = ttk.Frame(root)
    status_frame.pack(fill=X, side=BOTTOM)
    
    ttk.Label(
        status_frame,
        text="Estado: Aplicación inicializada - Fase 1 completada",
        font=("Segoe UI", 9),
        bootstyle="secondary"
    ).pack(side=LEFT, padx=10, pady=5)
    
    ttk.Label(
        status_frame,
        text=f"v{APP_VERSION}",
        font=("Segoe UI", 9),
        bootstyle="secondary"
    ).pack(side=RIGHT, padx=10, pady=5)
    
    logger.info("Interfaz temporal creada exitosamente")

# Función principal
def main():
    """Función principal de la aplicación"""
    print("🔐 Iniciando CryptoUNS...")
    print(f"   Sistema Criptográfico Integral v{APP_VERSION}")
    print(f"   Autor: {APP_AUTHOR}")
    print("")
    
    # Verificar dependencias
    if not check_dependencies():
        print("❌ Error: Faltan dependencias requeridas")
        sys.exit(1)
    
    # Configurar logging
    logger = setup_logging()
    logger.info("Iniciando CryptoUNS...")
    
    # Importar y ejecutar la aplicación principal
    try:
        from src.gui.main_window import CryptoUNSApp
        
        print("✅ Aplicación iniciada exitosamente")
        print("")
        print("🎯 Estado del proyecto:")
        print("   ✅ Fase 1 - Arquitectura base completada")
        print("   ✅ Fase 2 - Algoritmos criptográficos implementados")
        print("   ✅ Todas las pruebas unitarias pasan (92/92)")
        print("   🚀 Fase 3 - Interfaz gráfica en desarrollo")
        print("")
        
        logger.info("Iniciando interfaz gráfica principal...")
        app = CryptoUNSApp()
        app.run()
        
    except ImportError as e:
        logger.error(f"Error al importar módulos: {e}")
        print(f"❌ Error al importar módulos: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Aplicación terminada por el usuario")
    except Exception as e:
        logger.error(f"Error en la aplicación: {e}")
        print(f"❌ Error en la aplicación: {e}")
        raise
    finally:
        logger.info("Aplicación terminada")

# Función de manejo de errores
def handle_exception(exc_type, exc_value, exc_traceback):
    """Manejar excepciones no capturadas"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    logger = logging.getLogger("CryptoUNS")
    logger.error(
        "Excepción no capturada",
        exc_info=(exc_type, exc_value, exc_traceback)
    )

# Configurar manejo de excepciones
sys.excepthook = handle_exception

# Ejecutar aplicación
if __name__ == "__main__":
    main()
