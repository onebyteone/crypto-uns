"""
🎨 Configuración de Temas - CryptoUNS
===================================

Archivo que contiene la configuración de temas visuales para la interfaz
gráfica usando ttkbootstrap.

Autor: CryptoUNS Team
Fecha: 06 de julio, 2025
Versión: 1.0.0
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from typing import Dict, List, Tuple, Optional

# ===== CONFIGURACIÓN DE TEMAS =====
class CryptoThemes:
    """Clase para gestionar temas del sistema CryptoUNS"""
    
    # Tema principal por defecto
    DEFAULT_THEME = "darkly"
    
    # Temas disponibles
    AVAILABLE_THEMES = {
        "darkly": {
            "name": "Darkly",
            "description": "Tema oscuro moderno",
            "type": "dark",
            "colors": {
                "primary": "#375a7f",
                "secondary": "#444",
                "success": "#00bc8c",
                "info": "#3498db",
                "warning": "#f39c12",
                "danger": "#e74c3c",
                "light": "#adb5bd",
                "dark": "#303030"
            }
        },
        "flatly": {
            "name": "Flatly",
            "description": "Tema claro plano",
            "type": "light",
            "colors": {
                "primary": "#2C3E50",
                "secondary": "#95a5a6",
                "success": "#18BC9C",
                "info": "#3498DB",
                "warning": "#F39C12",
                "danger": "#E74C3C",
                "light": "#ecf0f1",
                "dark": "#2C3E50"
            }
        },
        "pulse": {
            "name": "Pulse",
            "description": "Tema púrpura vibrante",
            "type": "light",
            "colors": {
                "primary": "#593196",
                "secondary": "#A991D4",
                "success": "#13B955",
                "info": "#009BDC",
                "warning": "#EBA31D",
                "danger": "#FC3939",
                "light": "#f8f9fa",
                "dark": "#2C3E50"
            }
        },
        "solar": {
            "name": "Solar",
            "description": "Tema solar oscuro",
            "type": "dark",
            "colors": {
                "primary": "#b58900",
                "secondary": "#6c757d",
                "success": "#859900",
                "info": "#268bd2",
                "warning": "#cb4b16",
                "danger": "#dc322f",
                "light": "#fdf6e3",
                "dark": "#002b36"
            }
        },
        "cyborg": {
            "name": "Cyborg",
            "description": "Tema cibernético",
            "type": "dark",
            "colors": {
                "primary": "#2A9FD6",
                "secondary": "#555",
                "success": "#77B300",
                "info": "#9933CC",
                "warning": "#FF8800",
                "danger": "#CC0000",
                "light": "#222",
                "dark": "#080808"
            }
        },
        "superhero": {
            "name": "Superhero",
            "description": "Tema superhéroe",
            "type": "dark",
            "colors": {
                "primary": "#DF691A",
                "secondary": "#5A5A5A",
                "success": "#5CB85C",
                "info": "#5BC0DE",
                "warning": "#F0AD4E",
                "danger": "#D9534F",
                "light": "#4E5D6C",
                "dark": "#2B3E50"
            }
        },
        "vapor": {
            "name": "Vapor",
            "description": "Tema vapor wave",
            "type": "dark",
            "colors": {
                "primary": "#ea00d9",
                "secondary": "#6c757d",
                "success": "#0abdc6",
                "info": "#711c91",
                "warning": "#f39c12",
                "danger": "#e74c3c",
                "light": "#f8f9fa",
                "dark": "#190229"
            }
        },
        "litera": {
            "name": "Litera",
            "description": "Tema clásico literario",
            "type": "light",
            "colors": {
                "primary": "#4582EC",
                "secondary": "#6C757D",
                "success": "#02B875",
                "info": "#17A2B8",
                "warning": "#F8B500",
                "danger": "#D63384",
                "light": "#F8F9FA",
                "dark": "#212529"
            }
        }
    }
    
    @classmethod
    def get_theme_list(cls) -> List[str]:
        """Obtener lista de temas disponibles"""
        return list(cls.AVAILABLE_THEMES.keys())
    
    @classmethod
    def get_theme_info(cls, theme_name: str) -> Dict:
        """Obtener información de un tema específico"""
        return cls.AVAILABLE_THEMES.get(theme_name, cls.AVAILABLE_THEMES[cls.DEFAULT_THEME])
    
    @classmethod
    def is_dark_theme(cls, theme_name: str) -> bool:
        """Verificar si un tema es oscuro"""
        theme_info = cls.get_theme_info(theme_name)
        return theme_info.get("type", "light") == "dark"
    
    @classmethod
    def get_theme_colors(cls, theme_name: str) -> Dict[str, str]:
        """Obtener colores de un tema específico"""
        theme_info = cls.get_theme_info(theme_name)
        return theme_info.get("colors", {})

# ===== CONFIGURACIÓN DE ESTILOS PERSONALIZADOS =====
class CustomStyles:
    """Estilos personalizados para componentes específicos"""
    
    @staticmethod
    def configure_crypto_styles(style: ttk.Style):
        """Configurar estilos específicos para CryptoUNS"""
        
        # Estilo para títulos principales
        style.configure(
            "CryptoTitle.TLabel",
            font=("Segoe UI", 18, "bold"),
            foreground="#2C3E50"
        )
        
        # Estilo para subtítulos
        style.configure(
            "CryptoSubtitle.TLabel",
            font=("Segoe UI", 14, "bold"),
            foreground="#34495E"
        )
        
        # Estilo para texto monoespaciado
        style.configure(
            "CryptoMono.TText",
            font=("Consolas", 11),
            selectbackground="#3498DB",
            selectforeground="white"
        )
        
        # Estilo para botones principales
        style.configure(
            "CryptoPrimary.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=(15, 8)
        )
        
        # Estilo para botones secundarios
        style.configure(
            "CryptoSecondary.TButton",
            font=("Segoe UI", 10),
            padding=(10, 5)
        )
        
        # Estilo para frames principales
        style.configure(
            "CryptoFrame.TFrame",
            relief="solid",
            borderwidth=1
        )
        
        # Estilo para labels de estado
        style.configure(
            "CryptoStatus.TLabel",
            font=("Segoe UI", 10),
            foreground="#7F8C8D"
        )
        
        # Estilo para entries con validación
        style.configure(
            "CryptoEntry.TEntry",
            font=("Segoe UI", 11),
            padding=(5, 3)
        )
        
        # Estilo para spinbox
        style.configure(
            "CryptoSpinbox.TSpinbox",
            font=("Segoe UI", 11),
            padding=(5, 3)
        )

# ===== CONFIGURACIÓN DE ICONOS =====
class IconConfig:
    """Configuración de iconos para la interfaz"""
    
    # Iconos emoji para botones
    ICONS = {
        "encrypt": "🔒",
        "decrypt": "🔓",
        "generate": "⚙️",
        "copy": "📋",
        "paste": "📄",
        "clear": "🗑️",
        "save": "💾",
        "load": "📁",
        "help": "❓",
        "info": "ℹ️",
        "warning": "⚠️",
        "error": "❌",
        "success": "✅",
        "analyze": "🔍",
        "verify": "✔️",
        "compress": "📦",
        "decompress": "📤",
        "key": "🔑",
        "lock": "🔐",
        "unlock": "🔓",
        "shield": "🛡️",
        "gear": "⚙️",
        "tools": "🛠️",
        "crypto": "🔐",
        "hash": "#️⃣",
        "signature": "✍️",
        "blockchain": "⛓️",
        "huffman": "🌳",
        "matrix": "📊",
        "algorithm": "🧮",
        "classic": "📚",
        "modern": "🔬",
        "rsa": "🔢",
        "des": "🎯",
        "caesar": "👑",
        "vigenere": "🔤",
        "playfair": "🎲",
        "about": "📄",
        "exit": "🚪",
        "back": "⬅️",
        "next": "➡️",
        "up": "⬆️",
        "down": "⬇️",
        "left": "⬅️",
        "right": "➡️"
    }
    
    @classmethod
    def get_icon(cls, name: str) -> str:
        """Obtener icono por nombre"""
        return cls.ICONS.get(name, "")

# ===== CONFIGURACIÓN DE COLORES PERSONALIZADOS =====
class CryptoColors:
    """Colores personalizados para CryptoUNS"""
    
    # Colores principales
    PRIMARY = "#2C3E50"
    SECONDARY = "#34495E"
    ACCENT = "#3498DB"
    
    # Colores de estado
    SUCCESS = "#27AE60"
    WARNING = "#F39C12"
    ERROR = "#E74C3C"
    INFO = "#3498DB"
    
    # Colores de fondo
    BACKGROUND_LIGHT = "#ECF0F1"
    BACKGROUND_DARK = "#2C3E50"
    
    # Colores de texto
    TEXT_LIGHT = "#2C3E50"
    TEXT_DARK = "#FFFFFF"
    TEXT_MUTED = "#7F8C8D"
    
    # Colores de componentes
    BUTTON_PRIMARY = "#3498DB"
    BUTTON_SECONDARY = "#95A5A6"
    BUTTON_SUCCESS = "#27AE60"
    BUTTON_DANGER = "#E74C3C"
    
    # Colores de validación
    VALID = "#27AE60"
    INVALID = "#E74C3C"
    NEUTRAL = "#95A5A6"
    
    @classmethod
    def get_color_scheme(cls, theme_type: str = "light") -> Dict[str, str]:
        """Obtener esquema de colores según tipo de tema"""
        if theme_type == "dark":
            return {
                "background": cls.BACKGROUND_DARK,
                "text": cls.TEXT_DARK,
                "primary": cls.PRIMARY,
                "secondary": cls.SECONDARY,
                "accent": cls.ACCENT
            }
        else:
            return {
                "background": cls.BACKGROUND_LIGHT,
                "text": cls.TEXT_LIGHT,
                "primary": cls.PRIMARY,
                "secondary": cls.SECONDARY,
                "accent": cls.ACCENT
            }

# ===== CLASE PRINCIPAL DE GESTIÓN DE TEMAS =====
class ThemeManager:
    """Gestor principal de temas para CryptoUNS"""
    
    def __init__(self):
        self.current_theme = CryptoThemes.DEFAULT_THEME
        self.style = None
        self.root = None
    
    def initialize_theme(self, root, theme_name: str = None):
        """Inicializar tema de la aplicación"""
        if theme_name is None:
            theme_name = self.current_theme
        
        # Crear la aplicación con el tema
        self.root = root
        self.style = ttk.Style(theme=theme_name)
        
        # Configurar estilos personalizados
        CustomStyles.configure_crypto_styles(self.style)
        
        # Actualizar tema actual
        self.current_theme = theme_name
        
        return self.style
    
    def change_theme(self, theme_name: str):
        """Cambiar tema de la aplicación"""
        if theme_name in CryptoThemes.get_theme_list():
            self.style.theme_use(theme_name)
            self.current_theme = theme_name
            
            # Reconfigurar estilos personalizados
            CustomStyles.configure_crypto_styles(self.style)
            
            return True
        return False
    
    def get_current_theme(self) -> str:
        """Obtener tema actual"""
        return self.current_theme
    
    def get_theme_info(self) -> Dict:
        """Obtener información del tema actual"""
        return CryptoThemes.get_theme_info(self.current_theme)
    
    def is_dark_theme(self) -> bool:
        """Verificar si el tema actual es oscuro"""
        return CryptoThemes.is_dark_theme(self.current_theme)
    
    def get_theme_colors(self) -> Dict[str, str]:
        """Obtener colores del tema actual"""
        return CryptoThemes.get_theme_colors(self.current_theme)

# ===== FUNCIONES AUXILIARES =====
def create_themed_window(title: str = "CryptoUNS", theme: str = None) -> Tuple[ttk.Window, ThemeManager]:
    """Crear ventana con tema aplicado"""
    if theme is None:
        theme = CryptoThemes.DEFAULT_THEME
    
    # Crear ventana principal
    root = ttk.Window(title=title, themename=theme)
    
    # Crear gestor de temas
    theme_manager = ThemeManager()
    theme_manager.initialize_theme(root, theme)
    
    return root, theme_manager

def apply_crypto_styling(widget, style_name: str = None):
    """Aplicar estilo personalizado a un widget"""
    if style_name and hasattr(widget, 'configure'):
        widget.configure(style=style_name)

# ===== EXPORTAR COMPONENTES =====
__all__ = [
    'CryptoThemes',
    'CustomStyles',
    'IconConfig',
    'CryptoColors',
    'ThemeManager',
    'create_themed_window',
    'apply_crypto_styling'
]
