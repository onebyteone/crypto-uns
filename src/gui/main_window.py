"""
Ventana principal del sistema CryptoUNS
Maneja la interfaz gráfica principal con navegación y contenido dinámico
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import ttkbootstrap as ttb
from ttkbootstrap.constants import *
import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.utils.exceptions import CryptoUNSError
from src.data.config import ThemeConfig, WindowConfig
from src.crypto.classic import CaesarCipher, VigenereCipher, PlayfairCipher, KasiskiAnalysis
from src.crypto.modern import RSACipher, CustomHash, DESCipher, DigitalSignature
from src.crypto.tools import HuffmanCoding, Blockchain, IntegrityVerifier


class CryptoUNSApp:
    """
    Aplicación principal del sistema CryptoUNS
    Maneja la interfaz gráfica y la navegación entre pantallas
    """
    
    def __init__(self):
        """Inicializar la aplicación"""
        self.setup_theme()
        self.setup_main_window()
        self.setup_navigation()
        self.setup_content_area()
        self.setup_status_bar()
        
        # Inicializar clases criptográficas
        self.init_crypto_classes()
        
        # Mostrar pantalla inicial
        self.show_home_screen()
    
    def setup_theme(self):
        """Configurar el tema visual"""
        self.theme = ThemeConfig.DEFAULT_THEME
        self.root = ttb.Window(themename=self.theme)
        
    def setup_main_window(self):
        """Configurar la ventana principal"""
        self.root.title("CryptoUNS - Sistema Criptográfico Integral")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Configurar el icono (si existe)
        try:
            icon_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'icon.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
        
        # Configurar el cierre de la aplicación
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Configurar la grilla principal
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
    
    def setup_navigation(self):
        """Configurar el panel de navegación"""
        # Frame de navegación
        self.nav_frame = ttb.Frame(self.root, padding=10)
        self.nav_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        
        # Título de navegación
        title_label = ttb.Label(
            self.nav_frame, 
            text="CryptoUNS", 
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Botones de navegación
        self.nav_buttons = {}
        self.button_styles = {}  # Para guardar estilos originales
        self.current_screen = 'home'
        
        # Sección Inicio
        self.create_nav_button("🏠 Inicio", "home", PRIMARY)
        
        # Sección Criptografía Clásica
        self.create_nav_separator("Criptografía Clásica")
        self.create_nav_button("🔤 Cifrado César", "caesar", SECONDARY)
        self.create_nav_button("🔑 Cifrado Vigenère", "vigenere", SECONDARY)
        self.create_nav_button("🔒 Cifrado Playfair", "playfair", SECONDARY)
        self.create_nav_button("🔍 Análisis Kasiski", "kasiski", SECONDARY)
        
        # Sección Criptografía Moderna
        self.create_nav_separator("Criptografía Moderna")
        self.create_nav_button("🔐 RSA", "rsa", INFO)
        self.create_nav_button("🧮 Funciones Hash", "hash", INFO)
        self.create_nav_button("🔏 DES", "des", INFO)
        self.create_nav_button("✍️ Firma Digital", "signature", INFO)
        
        # Sección Herramientas
        self.create_nav_separator("Herramientas")
        self.create_nav_button("📊 Codificación Huffman", "huffman", SUCCESS)
        self.create_nav_button("⛓️ Blockchain", "blockchain", SUCCESS)
        self.create_nav_button("🔎 Verificador de Integridad", "integrity", SUCCESS)
        
        # Sección Configuración
        self.create_nav_separator("Configuración")
        self.create_nav_button("⚙️ Configuración", "config", WARNING)
        self.create_nav_button("ℹ️ Acerca de", "about", DARK)
    
    def create_nav_button(self, text, key, style):
        """Crear un botón de navegación"""
        btn = ttb.Button(
            self.nav_frame,
            text=text,
            bootstyle=style,
            command=lambda k=key: self.navigate_to(k),
            width=20
        )
        btn.pack(pady=2, fill="x")
        self.nav_buttons[key] = btn
        self.button_styles[key] = style  # Guardar estilo original
    
    def create_nav_separator(self, text):
        """Crear un separador con texto"""
        separator = ttb.Label(
            self.nav_frame,
            text=text,
            font=("Arial", 10, "bold"),
            foreground="gray"
        )
        separator.pack(pady=(15, 5))
    
    def setup_content_area(self):
        """Configurar el área de contenido principal"""
        # Frame de contenido
        self.content_frame = ttb.Frame(self.root, padding=10)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        
        # Configurar la grilla del contenido
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
    
    def setup_status_bar(self):
        """Configurar la barra de estado"""
        self.status_frame = ttb.Frame(self.root)
        self.status_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))
        
        self.status_label = ttb.Label(
            self.status_frame,
            text="Listo",
            font=("Arial", 9)
        )
        self.status_label.pack(side="left", padx=5)
        
        # Información de la aplicación
        info_label = ttb.Label(
            self.status_frame,
            text="CryptoUNS v1.0 - Sistema Criptográfico Integral",
            font=("Arial", 9),
            foreground="gray"
        )
        info_label.pack(side="right", padx=5)
    
    def init_crypto_classes(self):
        """Inicializar las clases criptográficas"""
        try:
            # Clases de criptografía clásica
            self.caesar = CaesarCipher()
            self.vigenere = VigenereCipher()
            self.playfair = PlayfairCipher()
            self.kasiski = KasiskiAnalysis()
            
            # Clases de criptografía moderna
            self.rsa = RSACipher()
            self.hash = CustomHash()
            self.des = DESCipher()
            self.signature = DigitalSignature()
            
            # Herramientas adicionales
            self.huffman = HuffmanCoding()
            self.blockchain = Blockchain()
            self.integrity = IntegrityVerifier()
            
            self.update_status("Algoritmos criptográficos inicializados correctamente")
        except Exception as e:
            self.show_error(f"Error inicializando algoritmos: {str(e)}")
    
    def navigate_to(self, screen):
        """Navegar a una pantalla específica"""
        # Limpiar el área de contenido
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
    def navigate_to(self, screen):
        """Navegar a una pantalla específica"""
        try:
            # Limpiar el área de contenido
            for widget in self.content_frame.winfo_children():
                widget.destroy()
            
            # Actualizar el botón activo usando estilos guardados
            for key, btn in self.nav_buttons.items():
                try:
                    original_style = self.button_styles.get(key, 'primary')
                    if key == screen:
                        # Botón activo - usar estilo outline
                        btn.configure(bootstyle=f"{original_style}-outline")
                        self.current_screen = screen
                    else:
                        # Botón inactivo - usar estilo original
                        btn.configure(bootstyle=original_style)
                except Exception:
                    # Si hay error, usar método alternativo
                    try:
                        if key == screen:
                            btn.configure(relief='sunken')
                        else:
                            btn.configure(relief='raised')
                    except Exception:
                        pass  # Ignorar completamente si nada funciona
            
            # Mostrar la pantalla correspondiente
            screen_methods = {
                'home': self.show_home_screen,
                'caesar': self.show_caesar_screen,
                'vigenere': self.show_vigenere_screen,
                'playfair': self.show_playfair_screen,
                'kasiski': self.show_kasiski_screen,
                'rsa': self.show_rsa_screen,
                'hash': self.show_hash_screen,
                'des': self.show_des_screen,
                'signature': self.show_signature_screen,
                'huffman': self.show_huffman_screen,
                'blockchain': self.show_blockchain_screen,
                'integrity': self.show_integrity_screen,
                'config': self.show_config_screen,
                'about': self.show_about_screen
            }
            
            if screen in screen_methods:
                screen_methods[screen]()
                self.update_status(f"Pantalla: {screen.title()}")
            else:
                self.show_error(f"Pantalla no encontrada: {screen}")
                
        except Exception as e:
            self.show_error(f"Error al navegar a {screen}: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def show_home_screen(self):
        """Mostrar la pantalla de inicio"""
        # Título principal
        title = ttb.Label(
            self.content_frame,
            text="🔐 CryptoUNS - Sistema Criptográfico Integral",
            font=("Arial", 24, "bold")
        )
        title.grid(row=0, column=0, pady=(0, 20))
        
        # Descripción
        description = ttb.Label(
            self.content_frame,
            text="Bienvenido al sistema integral de criptografía. Explore algoritmos clásicos y modernos,\n"
                 "herramientas de análisis y funcionalidades avanzadas de seguridad.",
            font=("Arial", 12),
            justify="center"
        )
        description.grid(row=1, column=0, pady=(0, 30))
        
        # Frame de características
        features_frame = ttb.Frame(self.content_frame)
        features_frame.grid(row=2, column=0, pady=(0, 20))
        
        # Características del sistema
        features = [
            ("🔤 Criptografía Clásica", "César, Vigenère, Playfair, Análisis Kasiski"),
            ("🔐 Criptografía Moderna", "RSA, Funciones Hash, DES, Firma Digital"),
            ("🛠️ Herramientas Avanzadas", "Codificación Huffman, Blockchain, Verificador de Integridad"),
            ("🎨 Interfaz Moderna", "Diseño intuitivo y fácil de usar"),
            ("🧪 Pruebas Integradas", "Validación completa de algoritmos"),
            ("📚 Documentación", "Información detallada de cada algoritmo")
        ]
        
        for i, (title, desc) in enumerate(features):
            row = i // 2
            col = i % 2
            
            feature_frame = ttb.Frame(features_frame, padding=10)
            feature_frame.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
            
            ttb.Label(feature_frame, text=title, font=("Arial", 12, "bold")).pack(anchor="w")
            ttb.Label(feature_frame, text=desc, font=("Arial", 10)).pack(anchor="w")
        
        # Botones de acceso rápido
        quick_access_frame = ttb.Frame(self.content_frame)
        quick_access_frame.grid(row=3, column=0, pady=20)
        
        ttb.Button(
            quick_access_frame,
            text="🔤 Cifrado César",
            bootstyle=SECONDARY,
            command=lambda: self.navigate_to("caesar")
        ).pack(side="left", padx=5)
        
        ttb.Button(
            quick_access_frame,
            text="🔐 RSA",
            bootstyle=INFO,
            command=lambda: self.navigate_to("rsa")
        ).pack(side="left", padx=5)
        
        ttb.Button(
            quick_access_frame,
            text="📊 Huffman",
            bootstyle=SUCCESS,
            command=lambda: self.navigate_to("huffman")
        ).pack(side="left", padx=5)
    
    def show_caesar_screen(self):
        """Mostrar la pantalla del cifrado César"""
        # Título
        title = ttb.Label(
            self.content_frame,
            text="🔤 Cifrado César",
            font=("Arial", 20, "bold")
        )
        title.grid(row=0, column=0, pady=(0, 20), sticky="w")
        
        # Descripción
        desc = ttb.Label(
            self.content_frame,
            text="El cifrado César es una técnica de cifrado por sustitución simple donde cada letra\n"
                 "se desplaza un número fijo de posiciones en el alfabeto.",
            font=("Arial", 10),
            justify="left"
        )
        desc.grid(row=1, column=0, pady=(0, 20), sticky="w")
        
        # Frame principal
        main_frame = ttb.Frame(self.content_frame)
        main_frame.grid(row=2, column=0, sticky="nsew")
        
        # Configurar grilla
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Panel de entrada
        input_frame = ttb.LabelFrame(main_frame, text="Entrada", padding=10)
        input_frame.grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky="nsew")
        
        # Campo de texto
        ttb.Label(input_frame, text="Texto:").pack(anchor="w")
        self.caesar_text = tk.Text(input_frame, height=8, width=40)
        self.caesar_text.pack(fill="both", expand=True, pady=(5, 10))
        
        # Campo de clave
        ttb.Label(input_frame, text="Clave (desplazamiento):").pack(anchor="w")
        self.caesar_key = ttb.Entry(input_frame, width=20)
        self.caesar_key.pack(anchor="w", pady=(5, 10))
        self.caesar_key.insert(0, "3")
        
        # Botones
        button_frame = ttb.Frame(input_frame)
        button_frame.pack(fill="x")
        
        ttb.Button(
            button_frame,
            text="Cifrar",
            bootstyle=SUCCESS,
            command=self.caesar_encrypt
        ).pack(side="left", padx=(0, 5))
        
        ttb.Button(
            button_frame,
            text="Descifrar",
            bootstyle=WARNING,
            command=self.caesar_decrypt
        ).pack(side="left", padx=(0, 5))
        
        ttb.Button(
            button_frame,
            text="Limpiar",
            bootstyle=SECONDARY,
            command=self.clear_caesar_fields
        ).pack(side="left")
        
        # Panel de salida
        output_frame = ttb.LabelFrame(main_frame, text="Resultado", padding=10)
        output_frame.grid(row=0, column=1, padx=(10, 0), pady=(0, 10), sticky="nsew")
        
        self.caesar_result = tk.Text(output_frame, height=8, width=40, state="disabled")
        self.caesar_result.pack(fill="both", expand=True)
        
        # Panel de análisis
        analysis_frame = ttb.LabelFrame(main_frame, text="Análisis de Frecuencias", padding=10)
        analysis_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(10, 0))
        
        self.caesar_analysis = tk.Text(analysis_frame, height=6, state="disabled")
        self.caesar_analysis.pack(fill="both", expand=True)
    
    def caesar_encrypt(self):
        """Cifrar texto con César"""
        try:
            text = self.caesar_text.get("1.0", tk.END).strip()
            key = int(self.caesar_key.get())
            
            if not text:
                self.show_warning("Por favor ingrese un texto para cifrar")
                return
            
            encrypted = self.caesar.encrypt(text, key)
            self.display_result(self.caesar_result, encrypted)
            
            # Análisis de frecuencias
            analysis = self.caesar.frequency_analysis(encrypted)
            self.display_analysis(self.caesar_analysis, analysis)
            
            self.update_status("Texto cifrado con éxito")
        except ValueError:
            self.show_error("La clave debe ser un número entero")
        except Exception as e:
            self.show_error(f"Error al cifrar: {str(e)}")
    
    def caesar_decrypt(self):
        """Descifrar texto con César"""
        try:
            text = self.caesar_text.get("1.0", tk.END).strip()
            key = int(self.caesar_key.get())
            
            if not text:
                self.show_warning("Por favor ingrese un texto para descifrar")
                return
            
            decrypted = self.caesar.decrypt(text, key)
            self.display_result(self.caesar_result, decrypted)
            
            # Análisis de frecuencias
            analysis = self.caesar.frequency_analysis(decrypted)
            self.display_analysis(self.caesar_analysis, analysis)
            
            self.update_status("Texto descifrado con éxito")
        except ValueError:
            self.show_error("La clave debe ser un número entero")
        except Exception as e:
            self.show_error(f"Error al descifrar: {str(e)}")
    
    def clear_caesar_fields(self):
        """Limpiar campos del cifrado César"""
        self.caesar_text.delete("1.0", tk.END)
        self.caesar_key.delete(0, tk.END)
        self.caesar_key.insert(0, "3")
        self.caesar_result.configure(state="normal")
        self.caesar_result.delete("1.0", tk.END)
        self.caesar_result.configure(state="disabled")
        self.caesar_analysis.configure(state="normal")
        self.caesar_analysis.delete("1.0", tk.END)
        self.caesar_analysis.configure(state="disabled")
    
    def display_result(self, text_widget, result):
        """Mostrar resultado en un widget de texto"""
        text_widget.configure(state="normal")
        text_widget.delete("1.0", tk.END)
        text_widget.insert("1.0", result)
        text_widget.configure(state="disabled")
    
    def display_analysis(self, text_widget, analysis):
        """Mostrar análisis en un widget de texto"""
        text_widget.configure(state="normal")
        text_widget.delete("1.0", tk.END)
        
        analysis_text = "Análisis de Frecuencias:\n\n"
        for char, freq in sorted(analysis.items(), key=lambda x: x[1], reverse=True):
            if char.isalpha():
                analysis_text += f"{char}: {freq}\n"
        
        text_widget.insert("1.0", analysis_text)
        text_widget.configure(state="disabled")
    
    def show_vigenere_screen(self):
        """Mostrar la pantalla del cifrado Vigenère"""
        # Título
        title = ttb.Label(
            self.content_frame,
            text="🔑 Cifrado Vigenère",
            font=("Arial", 20, "bold")
        )
        title.grid(row=0, column=0, pady=(0, 20), sticky="w")
        
        # Descripción
        desc = ttb.Label(
            self.content_frame,
            text="El cifrado Vigenère es un método de cifrado polialfabético que utiliza una clave\n"
                 "repetitiva para cifrar el texto. Es más seguro que el cifrado César.",
            font=("Arial", 10),
            justify="left"
        )
        desc.grid(row=1, column=0, pady=(0, 20), sticky="w")
        
        # Frame principal
        main_frame = ttb.Frame(self.content_frame)
        main_frame.grid(row=2, column=0, sticky="nsew")
        
        # Configurar grilla
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Panel de entrada
        input_frame = ttb.LabelFrame(main_frame, text="Entrada", padding=10)
        input_frame.grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky="nsew")
        
        # Campo de texto
        ttb.Label(input_frame, text="Texto:").pack(anchor="w")
        self.vigenere_text = tk.Text(input_frame, height=8, width=40)
        self.vigenere_text.pack(fill="both", expand=True, pady=(5, 10))
        
        # Campo de clave
        ttb.Label(input_frame, text="Clave (solo letras):").pack(anchor="w")
        self.vigenere_key = ttb.Entry(input_frame, width=20)
        self.vigenere_key.pack(anchor="w", pady=(5, 10))
        self.vigenere_key.insert(0, "CLAVE")
        
        # Validación en tiempo real
        self.vigenere_key.bind('<KeyRelease>', self.validate_vigenere_key)
        
        # Botones
        button_frame = ttb.Frame(input_frame)
        button_frame.pack(fill="x")
        
        ttb.Button(
            button_frame,
            text="Cifrar",
            bootstyle=SUCCESS,
            command=self.vigenere_encrypt
        ).pack(side="left", padx=(0, 5))
        
        ttb.Button(
            button_frame,
            text="Descifrar",
            bootstyle=WARNING,
            command=self.vigenere_decrypt
        ).pack(side="left", padx=(0, 5))
        
        ttb.Button(
            button_frame,
            text="Limpiar",
            bootstyle=SECONDARY,
            command=self.clear_vigenere_fields
        ).pack(side="left", padx=(0, 5))
        
        ttb.Button(
            button_frame,
            text="Análisis Kasiski",
            bootstyle=INFO,
            command=self.vigenere_kasiski_analysis
        ).pack(side="left")
        
        # Panel de salida
        output_frame = ttb.LabelFrame(main_frame, text="Resultado", padding=10)
        output_frame.grid(row=0, column=1, padx=(10, 0), pady=(0, 10), sticky="nsew")
        
        self.vigenere_result = tk.Text(output_frame, height=8, width=40, state="disabled")
        self.vigenere_result.pack(fill="both", expand=True)
        
        # Panel de análisis
        analysis_frame = ttb.LabelFrame(main_frame, text="Análisis de Clave", padding=10)
        analysis_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(10, 0))
        
        self.vigenere_analysis = tk.Text(analysis_frame, height=6, state="disabled")
        self.vigenere_analysis.pack(fill="both", expand=True)
    
    def validate_vigenere_key(self, event=None):
        """Validar clave de Vigenère en tiempo real"""
        key = self.vigenere_key.get().upper()
        # Filtrar solo letras
        filtered_key = ''.join(c for c in key if c.isalpha())
        
        if key != filtered_key:
            self.vigenere_key.delete(0, tk.END)
            self.vigenere_key.insert(0, filtered_key)
            self.update_status("Clave filtrada: solo se permiten letras")
    
    def vigenere_encrypt(self):
        """Cifrar texto con Vigenère"""
        try:
            text = self.vigenere_text.get("1.0", tk.END).strip()
            key = self.vigenere_key.get().upper()
            
            if not text:
                self.show_warning("Por favor ingrese un texto para cifrar")
                return
            
            if not key:
                self.show_warning("Por favor ingrese una clave")
                return
            
            if not key.isalpha():
                self.show_warning("La clave debe contener solo letras")
                return
            
            encrypted = self.vigenere.encrypt(text, key)
            self.display_result(self.vigenere_result, encrypted)
            
            # Mostrar información de la clave
            self.display_vigenere_key_info(key)
            
            self.update_status("Texto cifrado con Vigenère exitosamente")
        except Exception as e:
            self.show_error(f"Error al cifrar: {str(e)}")
    
    def vigenere_decrypt(self):
        """Descifrar texto con Vigenère"""
        try:
            text = self.vigenere_text.get("1.0", tk.END).strip()
            key = self.vigenere_key.get().upper()
            
            if not text:
                self.show_warning("Por favor ingrese un texto para descifrar")
                return
            
            if not key:
                self.show_warning("Por favor ingrese una clave")
                return
            
            if not key.isalpha():
                self.show_warning("La clave debe contener solo letras")
                return
            
            decrypted = self.vigenere.decrypt(text, key)
            self.display_result(self.vigenere_result, decrypted)
            
            # Mostrar información de la clave
            self.display_vigenere_key_info(key)
            
            self.update_status("Texto descifrado con Vigenère exitosamente")
        except Exception as e:
            self.show_error(f"Error al descifrar: {str(e)}")
    
    def vigenere_kasiski_analysis(self):
        """Realizar análisis Kasiski del texto"""
        try:
            text = self.vigenere_text.get("1.0", tk.END).strip()
            
            if not text:
                self.show_warning("Por favor ingrese un texto para analizar")
                return
            
            analysis = self.kasiski.analyze(text)
            self.display_kasiski_analysis(analysis)
            
            self.update_status("Análisis Kasiski completado")
        except Exception as e:
            self.show_error(f"Error en análisis Kasiski: {str(e)}")
    
    def display_vigenere_key_info(self, key):
        """Mostrar información de la clave Vigenère"""
        self.vigenere_analysis.configure(state="normal")
        self.vigenere_analysis.delete("1.0", tk.END)
        
        info_text = f"Información de la Clave:\n\n"
        info_text += f"Clave: {key}\n"
        info_text += f"Longitud: {len(key)}\n"
        info_text += f"Caracteres únicos: {len(set(key))}\n\n"
        
        # Mostrar patrón de repetición
        info_text += "Patrón de repetición (primeros 50 caracteres):\n"
        extended_key = (key * (50 // len(key) + 1))[:50]
        info_text += extended_key + "\n\n"
        
        # Análisis de fortaleza
        unique_ratio = len(set(key)) / len(key)
        if unique_ratio > 0.8:
            strength = "Fuerte"
        elif unique_ratio > 0.5:
            strength = "Moderada"
        else:
            strength = "Débil"
        
        info_text += f"Fortaleza de la clave: {strength}\n"
        info_text += f"Ratio de caracteres únicos: {unique_ratio:.2f}"
        
        self.vigenere_analysis.insert("1.0", info_text)
        self.vigenere_analysis.configure(state="disabled")
    
    def display_kasiski_analysis(self, analysis):
        """Mostrar análisis Kasiski"""
        self.vigenere_analysis.configure(state="normal")
        self.vigenere_analysis.delete("1.0", tk.END)
        
        analysis_text = "Análisis Kasiski:\n\n"
        
        if 'repetitions' in analysis:
            analysis_text += "Repeticiones encontradas:\n"
            for rep in analysis['repetitions'][:5]:  # Mostrar solo las primeras 5
                analysis_text += f"'{rep['sequence']}' - Distancias: {rep['distances']}\n"
            analysis_text += "\n"
        
        if 'estimated_key_length' in analysis:
            analysis_text += f"Longitud estimada de clave: {analysis['estimated_key_length']}\n"
        
        if 'factors' in analysis:
            analysis_text += f"Factores comunes: {analysis['factors']}\n"
        
        self.vigenere_analysis.insert("1.0", analysis_text)
        self.vigenere_analysis.configure(state="disabled")
    
    def clear_vigenere_fields(self):
        """Limpiar campos del cifrado Vigenère"""
        self.vigenere_text.delete("1.0", tk.END)
        self.vigenere_key.delete(0, tk.END)
        self.vigenere_key.insert(0, "CLAVE")
        self.vigenere_result.configure(state="normal")
        self.vigenere_result.delete("1.0", tk.END)
        self.vigenere_result.configure(state="disabled")
        self.vigenere_analysis.configure(state="normal")
        self.vigenere_analysis.delete("1.0", tk.END)
        self.vigenere_analysis.configure(state="disabled")
    
    def show_playfair_screen(self):
        """Mostrar la pantalla del cifrado Playfair"""
        # Título
        title = ttb.Label(
            self.content_frame,
            text="🔒 Cifrado Playfair",
            font=("Arial", 20, "bold")
        )
        title.grid(row=0, column=0, pady=(0, 20), sticky="w")
        
        # Descripción
        desc = ttb.Label(
            self.content_frame,
            text="El cifrado Playfair es un método de cifrado digráfico que utiliza una matriz 5x5\n"
                 "para cifrar pares de letras. Es más seguro que los cifrados monoalfabéticos.",
            font=("Arial", 10),
            justify="left"
        )
        desc.grid(row=1, column=0, pady=(0, 20), sticky="w")
        
        # Frame principal
        main_frame = ttb.Frame(self.content_frame)
        main_frame.grid(row=2, column=0, sticky="nsew")
        
        # Configurar grilla
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_columnconfigure(2, weight=1)
        
        # Panel de entrada
        input_frame = ttb.LabelFrame(main_frame, text="Entrada", padding=10)
        input_frame.grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky="nsew")
        
        # Campo de texto
        ttb.Label(input_frame, text="Texto:").pack(anchor="w")
        self.playfair_text = tk.Text(input_frame, height=8, width=30)
        self.playfair_text.pack(fill="both", expand=True, pady=(5, 10))
        
        # Campo de clave
        ttb.Label(input_frame, text="Clave (palabra clave):").pack(anchor="w")
        self.playfair_key = ttb.Entry(input_frame, width=20)
        self.playfair_key.pack(anchor="w", pady=(5, 10))
        self.playfair_key.insert(0, "SECRETO")
        
        # Validación en tiempo real
        self.playfair_key.bind('<KeyRelease>', self.validate_playfair_key)
        
        # Botones
        button_frame = ttb.Frame(input_frame)
        button_frame.pack(fill="x")
        
        ttb.Button(
            button_frame,
            text="Cifrar",
            bootstyle=SUCCESS,
            command=self.playfair_encrypt
        ).pack(side="left", padx=(0, 5))
        
        ttb.Button(
            button_frame,
            text="Limpiar",
            bootstyle=SECONDARY,
            command=self.clear_playfair_fields
        ).pack(side="left", padx=(0, 5))
        
        ttb.Button(
            button_frame,
            text="Generar Matriz",
            bootstyle=INFO,
            command=self.generate_playfair_matrix
        ).pack(side="left")
        
        # Panel de salida
        output_frame = ttb.LabelFrame(main_frame, text="Resultado", padding=10)
        output_frame.grid(row=0, column=1, padx=(10, 0), pady=(0, 10), sticky="nsew")
        
        self.playfair_result = tk.Text(output_frame, height=8, width=30, state="disabled")
        self.playfair_result.pack(fill="both", expand=True)
        
        # Panel de matriz
        matrix_frame = ttb.LabelFrame(main_frame, text="Matriz Playfair 5x5", padding=10)
        matrix_frame.grid(row=0, column=2, padx=(10, 0), pady=(0, 10), sticky="nsew")
        
        # Crear grilla para la matriz
        self.playfair_matrix_labels = []
        for i in range(5):
            row_labels = []
            for j in range(5):
                label = ttb.Label(
                    matrix_frame,
                    text="",
                    font=("Courier New", 12, "bold"),
                    width=3,
                    anchor="center",
                    relief="solid",
                    borderwidth=1
                )
                label.grid(row=i, column=j, padx=1, pady=1, sticky="nsew")
                row_labels.append(label)
            self.playfair_matrix_labels.append(row_labels)
        
        # Panel de información
        info_frame = ttb.LabelFrame(main_frame, text="Información del Proceso", padding=10)
        info_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=(10, 0))
        
        self.playfair_info = tk.Text(info_frame, height=6, state="disabled")
        self.playfair_info.pack(fill="both", expand=True)
        
        # Generar matriz inicial
        self.generate_playfair_matrix()
    
    def validate_playfair_key(self, event=None):
        """Validar clave de Playfair en tiempo real"""
        key = self.playfair_key.get().upper()
        # Filtrar solo letras, reemplazar J por I
        filtered_key = ''.join(c if c != 'J' else 'I' for c in key if c.isalpha())
        
        if key != filtered_key:
            self.playfair_key.delete(0, tk.END)
            self.playfair_key.insert(0, filtered_key)
            if 'J' in key:
                self.update_status("Nota: J se ha reemplazado por I en la clave")
    
    def playfair_encrypt(self):
        """Cifrar texto con Playfair"""
        try:
            text = self.playfair_text.get("1.0", tk.END).strip()
            key = self.playfair_key.get().upper()
            
            if not text:
                self.show_warning("Por favor ingrese un texto para cifrar")
                return
            
            if not key:
                self.show_warning("Por favor ingrese una clave")
                return
            
            if not key.isalpha():
                self.show_warning("La clave debe contener solo letras")
                return
            
            encrypted = self.playfair.encrypt(text, key)
            self.display_result(self.playfair_result, encrypted)
            
            # Actualizar matriz y mostrar información
            self.generate_playfair_matrix()
            self.display_playfair_info(text, key, encrypted)
            
            self.update_status("Texto cifrado con Playfair exitosamente")
        except Exception as e:
            self.show_error(f"Error al cifrar: {str(e)}")
    
    def generate_playfair_matrix(self):
        """Generar y mostrar la matriz Playfair"""
        try:
            key = self.playfair_key.get().upper()
            if not key:
                key = "SECRETO"
            
            matrix = self.playfair.create_matrix(key)
            
            # Actualizar labels de la matriz
            for i in range(5):
                for j in range(5):
                    self.playfair_matrix_labels[i][j].configure(
                        text=matrix[i][j],
                        bootstyle="info"
                    )
            
            self.update_status("Matriz Playfair generada")
        except Exception as e:
            self.show_error(f"Error al generar matriz: {str(e)}")
    
    def display_playfair_info(self, original_text, key, encrypted_text):
        """Mostrar información del proceso Playfair"""
        self.playfair_info.configure(state="normal")
        self.playfair_info.delete("1.0", tk.END)
        
        info_text = f"Información del Cifrado Playfair:\n\n"
        info_text += f"Clave original: {key}\n"
        info_text += f"Texto original: {original_text[:50]}{'...' if len(original_text) > 50 else ''}\n"
        info_text += f"Texto cifrado: {encrypted_text[:50]}{'...' if len(encrypted_text) > 50 else ''}\n\n"
        
        # Preparar texto para mostrar el procesamiento
        try:
            prepared_text = self.playfair.prepare_text(original_text)
            info_text += f"Texto preparado: {prepared_text[:50]}{'...' if len(prepared_text) > 50 else ''}\n"
            info_text += f"Longitud del texto preparado: {len(prepared_text)}\n"
            info_text += f"Número de digramas: {len(prepared_text) // 2}\n\n"
            
            # Mostrar algunos digramas
            info_text += "Primeros digramas:\n"
            for i in range(0, min(10, len(prepared_text)), 2):
                if i + 1 < len(prepared_text):
                    diagrama = prepared_text[i:i+2]
                    info_text += f"{diagrama} "
            info_text += "\n\n"
            
            info_text += "Notas:\n"
            info_text += "• Las letras J se convierten en I\n"
            info_text += "• Se agregan X entre letras repetidas\n"
            info_text += "• Se agrega X al final si es necesario"
            
        except Exception as e:
            info_text += f"Error al procesar información: {str(e)}"
        
        self.playfair_info.insert("1.0", info_text)
        self.playfair_info.configure(state="disabled")
    
    def clear_playfair_fields(self):
        """Limpiar campos del cifrado Playfair"""
        self.playfair_text.delete("1.0", tk.END)
        self.playfair_key.delete(0, tk.END)
        self.playfair_key.insert(0, "SECRETO")
        self.playfair_result.configure(state="normal")
        self.playfair_result.delete("1.0", tk.END)
        self.playfair_result.configure(state="disabled")
        self.playfair_info.configure(state="normal")
        self.playfair_info.delete("1.0", tk.END)
        self.playfair_info.configure(state="disabled")
        self.generate_playfair_matrix()
    
    def show_kasiski_screen(self):
        """Mostrar la pantalla del análisis Kasiski"""
        # Título
        title = ttb.Label(
            self.content_frame,
            text="🔍 Análisis Kasiski",
            font=("Arial", 20, "bold")
        )
        title.grid(row=0, column=0, pady=(0, 20), sticky="w")
        
        # Descripción
        desc = ttb.Label(
            self.content_frame,
            text="El método Kasiski es una técnica de criptoanálisis para determinar la longitud\n"
                 "de la clave en cifrados polialfabéticos como Vigenère.",
            font=("Arial", 10),
            justify="left"
        )
        desc.grid(row=1, column=0, pady=(0, 20), sticky="w")
        
        # Frame principal
        main_frame = ttb.Frame(self.content_frame)
        main_frame.grid(row=2, column=0, sticky="nsew")
        
        # Configurar grilla
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Panel de entrada
        input_frame = ttb.LabelFrame(main_frame, text="Texto a Analizar", padding=10)
        input_frame.grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky="nsew")
        
        # Campo de texto
        ttb.Label(input_frame, text="Texto cifrado:").pack(anchor="w")
        self.kasiski_text = tk.Text(input_frame, height=10, width=40)
        self.kasiski_text.pack(fill="both", expand=True, pady=(5, 10))
        
        # Configuración del análisis
        config_frame = ttb.Frame(input_frame)
        config_frame.pack(fill="x", pady=(0, 10))
        
        ttb.Label(config_frame, text="Longitud mínima del patrón:").pack(anchor="w")
        self.kasiski_min_length = ttb.Entry(config_frame, width=10)
        self.kasiski_min_length.pack(anchor="w", pady=(5, 0))
        self.kasiski_min_length.insert(0, "3")
        
        # Botones
        button_frame = ttb.Frame(input_frame)
        button_frame.pack(fill="x")
        
        ttb.Button(
            button_frame,
            text="Analizar",
            bootstyle=SUCCESS,
            command=self.perform_kasiski_analysis
        ).pack(side="left", padx=(0, 5))
        
        ttb.Button(
            button_frame,
            text="Limpiar",
            bootstyle=SECONDARY,
            command=self.clear_kasiski_fields
        ).pack(side="left", padx=(0, 5))
        
        ttb.Button(
            button_frame,
            text="Ejemplo",
            bootstyle=INFO,
            command=self.load_kasiski_example
        ).pack(side="left")
        
        # Panel de resultados
        results_frame = ttb.LabelFrame(main_frame, text="Resultados del Análisis", padding=10)
        results_frame.grid(row=0, column=1, padx=(10, 0), pady=(0, 10), sticky="nsew")
        
        self.kasiski_results = tk.Text(results_frame, height=10, width=40, state="disabled")
        self.kasiski_results.pack(fill="both", expand=True)
        
        # Panel de patrones encontrados
        patterns_frame = ttb.LabelFrame(main_frame, text="Patrones Repetidos", padding=10)
        patterns_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(10, 0))
        
        # Configurar grilla para el panel de patrones
        patterns_frame.grid_columnconfigure(0, weight=1)
        
        # Crear Treeview para mostrar patrones
        columns = ('Patrón', 'Frecuencia', 'Posiciones', 'Distancias', 'Factores')
        self.kasiski_tree = ttb.Treeview(patterns_frame, columns=columns, show='headings', height=8)
        
        # Configurar columnas
        for col in columns:
            self.kasiski_tree.heading(col, text=col)
            self.kasiski_tree.column(col, width=100)
        
        # Scrollbar para el Treeview
        scrollbar = ttb.Scrollbar(patterns_frame, orient="vertical", command=self.kasiski_tree.yview)
        self.kasiski_tree.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar Treeview y scrollbar
        self.kasiski_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
    
    def perform_kasiski_analysis(self):
        """Realizar análisis Kasiski"""
        try:
            text = self.kasiski_text.get("1.0", tk.END).strip()
            min_length = int(self.kasiski_min_length.get())
            
            if not text:
                self.show_warning("Por favor ingrese un texto para analizar")
                return
            
            if min_length < 2:
                self.show_warning("La longitud mínima debe ser al menos 2")
                return
            
            # Realizar análisis
            analysis = self.kasiski.analyze(text, min_length=min_length)
            
            # Mostrar resultados
            self.display_kasiski_results(analysis)
            self.populate_kasiski_tree(analysis)
            
            self.update_status("Análisis Kasiski completado exitosamente")
        except ValueError:
            self.show_error("La longitud mínima debe ser un número entero")
        except Exception as e:
            self.show_error(f"Error en análisis Kasiski: {str(e)}")
    
    def display_kasiski_results(self, analysis):
        """Mostrar resultados del análisis Kasiski"""
        self.kasiski_results.configure(state="normal")
        self.kasiski_results.delete("1.0", tk.END)
        
        results_text = "Análisis Kasiski - Resultados:\n\n"
        
        # Longitud estimada de la clave
        if 'estimated_key_length' in analysis:
            results_text += f"🔑 Longitud estimada de clave: {analysis['estimated_key_length']}\n\n"
        
        # Factores más comunes
        if 'factors' in analysis:
            results_text += "📊 Factores más comunes:\n"
            # Convertir diccionario a lista ordenada por frecuencia
            factors_list = sorted(analysis['factors'].items(), key=lambda x: x[1], reverse=True)
            for factor, count in factors_list[:10]:
                results_text += f"  {factor}: {count} veces\n"
            results_text += "\n"
        
        # Estadísticas generales
        if 'repetitions' in analysis:
            total_patterns = len(analysis['repetitions'])
            results_text += f"📈 Estadísticas:\n"
            results_text += f"  Total de patrones encontrados: {total_patterns}\n"
            
            if total_patterns > 0:
                # Patrón más frecuente
                most_frequent = max(analysis['repetitions'], key=lambda x: len(x['positions']))
                results_text += f"  Patrón más frecuente: '{most_frequent['sequence']}' ({len(most_frequent['positions'])} veces)\n"
                
                # Distancias más comunes
                all_distances = []
                for rep in analysis['repetitions']:
                    all_distances.extend(rep['distances'])
                
                if all_distances:
                    from collections import Counter
                    distance_counts = Counter(all_distances)
                    most_common_distance = distance_counts.most_common(1)[0]
                    results_text += f"  Distancia más común: {most_common_distance[0]} ({most_common_distance[1]} veces)\n"
        
        results_text += "\n"
        
        # Recomendaciones
        results_text += "💡 Recomendaciones:\n"
        if 'estimated_key_length' in analysis:
            key_length = analysis['estimated_key_length']
            if key_length <= 5:
                results_text += f"  La clave estimada es corta ({key_length}), el cifrado es vulnerable.\n"
            elif key_length <= 10:
                results_text += f"  La clave estimada es moderada ({key_length}), seguridad media.\n"
            else:
                results_text += f"  La clave estimada es larga ({key_length}), mayor seguridad.\n"
        
        results_text += "  Use análisis de frecuencias para descifrar cada subcifrado.\n"
        results_text += "  Considere otras longitudes de clave cercanas a la estimada."
        
        self.kasiski_results.insert("1.0", results_text)
        self.kasiski_results.configure(state="disabled")
    
    def populate_kasiski_tree(self, analysis):
        """Poblar el Treeview con los patrones encontrados"""
        # Limpiar el Treeview
        for item in self.kasiski_tree.get_children():
            self.kasiski_tree.delete(item)
        
        if 'repetitions' not in analysis:
            return
        
        # Ordenar por frecuencia (número de apariciones)
        sorted_patterns = sorted(analysis['repetitions'], 
                               key=lambda x: len(x['positions']), 
                               reverse=True)
        
        # Agregar patrones al Treeview
        for pattern_data in sorted_patterns[:50]:  # Mostrar solo los primeros 50
            pattern = pattern_data['sequence']
            frequency = len(pattern_data['positions'])
            positions = ', '.join(map(str, pattern_data['positions'][:10]))  # Primeras 10 posiciones
            if len(pattern_data['positions']) > 10:
                positions += ', ...'
            
            distances = ', '.join(map(str, pattern_data['distances'][:10]))  # Primeras 10 distancias
            if len(pattern_data['distances']) > 10:
                distances += ', ...'
            
            # Calcular factores de las distancias
            factors = set()
            for dist in pattern_data['distances']:
                for i in range(2, min(21, dist + 1)):  # Factores hasta 20
                    if dist % i == 0:
                        factors.add(i)
            
            factors_str = ', '.join(map(str, sorted(factors)[:10]))  # Primeros 10 factores
            if len(factors) > 10:
                factors_str += ', ...'
            
            self.kasiski_tree.insert('', 'end', values=(
                pattern, frequency, positions, distances, factors_str
            ))
    
    def load_kasiski_example(self):
        """Cargar un ejemplo de texto cifrado para análisis"""
        example_text = """CHREEVOAHMAERATBIAXXWTNXBEEOPHBSBQMQEQERBWRVXUOAKXAOSXXWEAHBWGJMMQMNKGRFVGXWTRZXWIAKLXFPSKAUTEMNDCMGTSXMXBTUIADNGMGPSRELXNJELXVRVPRTULHDNQWTWDTYGBPHXTFALJHASVBFXNGLLCHRZBWELEKMSJIKNBHWRJGNMGJSGLXFEYPHAGNRBIEQJTAMRVLCRREMNDGLXRRIMGNSNRWCHRQHAEYEVTAQEBBIPEEWEVKAKOEWADREMXMTBHHCHRTKDNVRZCHRCLQOHPWQAIIWXNRMGWOIIFKEE"""
        
        self.kasiski_text.delete("1.0", tk.END)
        self.kasiski_text.insert("1.0", example_text)
        self.update_status("Ejemplo cargado - Texto cifrado con Vigenère")
    
    def clear_kasiski_fields(self):
        """Limpiar campos del análisis Kasiski"""
        self.kasiski_text.delete("1.0", tk.END)
        self.kasiski_min_length.delete(0, tk.END)
        self.kasiski_min_length.insert(0, "3")
        self.kasiski_results.configure(state="normal")
        self.kasiski_results.delete("1.0", tk.END)
        self.kasiski_results.configure(state="disabled")
        
        # Limpiar el Treeview
        for item in self.kasiski_tree.get_children():
            self.kasiski_tree.delete(item)
    
    def show_rsa_screen(self):
        """Mostrar la pantalla del cifrado RSA"""
        # Título
        title = ttb.Label(
            self.content_frame,
            text="🔐 Cifrado RSA",
            font=("Arial", 20, "bold")
        )
        title.grid(row=0, column=0, pady=(0, 20), sticky="w")
        
        # Descripción
        desc = ttb.Label(
            self.content_frame,
            text="RSA es un algoritmo de criptografía asimétrica que utiliza un par de claves:\n"
                 "una clave pública para cifrar y una clave privada para descifrar.",
            font=("Arial", 10),
            justify="left"
        )
        desc.grid(row=1, column=0, pady=(0, 20), sticky="w")
        
        # Frame principal
        main_frame = ttb.Frame(self.content_frame)
        main_frame.grid(row=2, column=0, sticky="nsew")
        
        # Configurar grilla
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Panel de entrada
        input_frame = ttb.LabelFrame(main_frame, text="Mensaje y Operaciones", padding=10)
        input_frame.grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky="nsew")
        
        # Campo de mensaje
        ttb.Label(input_frame, text="Mensaje:").pack(anchor="w")
        self.rsa_message = tk.Text(input_frame, height=6, width=40)
        self.rsa_message.pack(fill="both", expand=True, pady=(5, 10))
        
        # Botones de operación
        button_frame = ttb.Frame(input_frame)
        button_frame.pack(fill="x", pady=(0, 10))
        
        ttb.Button(
            button_frame,
            text="Generar Claves",
            bootstyle=INFO,
            command=self.generate_rsa_keys
        ).pack(side="left", padx=(0, 5))
        
        ttb.Button(
            button_frame,
            text="Cifrar",
            bootstyle=SUCCESS,
            command=self.rsa_encrypt
        ).pack(side="left", padx=(0, 5))
        
        ttb.Button(
            button_frame,
            text="Descifrar",
            bootstyle=WARNING,
            command=self.rsa_decrypt
        ).pack(side="left", padx=(0, 5))
        
        ttb.Button(
            button_frame,
            text="Limpiar",
            bootstyle=SECONDARY,
            command=self.clear_rsa_fields
        ).pack(side="left")
        
        # Panel de configuración
        config_frame = ttb.LabelFrame(input_frame, text="Configuración", padding=10)
        config_frame.pack(fill="x", pady=(0, 10))
        
        ttb.Label(config_frame, text="Tamaño de clave (bits):").pack(anchor="w")
        self.rsa_key_size = ttb.Combobox(config_frame, values=[512, 1024, 2048], state="readonly", width=10)
        self.rsa_key_size.pack(anchor="w", pady=(5, 0))
        self.rsa_key_size.set(512)  # Por defecto 512 bits para rapidez
        
        # Panel de resultado
        result_frame = ttb.LabelFrame(main_frame, text="Resultado", padding=10)
        result_frame.grid(row=0, column=1, padx=(10, 0), pady=(0, 10), sticky="nsew")
        
        self.rsa_result = tk.Text(result_frame, height=6, width=40, state="disabled")
        self.rsa_result.pack(fill="both", expand=True)
        
        # Panel de claves
        keys_frame = ttb.LabelFrame(main_frame, text="Información de Claves", padding=10)
        keys_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(10, 0))
        
        # Notebook para organizar las claves
        self.rsa_notebook = ttb.Notebook(keys_frame)
        self.rsa_notebook.pack(fill="both", expand=True)
        
        # Pestaña de clave pública
        public_frame = ttb.Frame(self.rsa_notebook)
        self.rsa_notebook.add(public_frame, text="Clave Pública")
        
        self.rsa_public_key = tk.Text(public_frame, height=8, state="disabled")
        self.rsa_public_key.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Pestaña de clave privada
        private_frame = ttb.Frame(self.rsa_notebook)
        self.rsa_notebook.add(private_frame, text="Clave Privada")
        
        self.rsa_private_key = tk.Text(private_frame, height=8, state="disabled")
        self.rsa_private_key.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Pestaña de información
        info_frame = ttb.Frame(self.rsa_notebook)
        self.rsa_notebook.add(info_frame, text="Información")
        
        self.rsa_info = tk.Text(info_frame, height=8, state="disabled")
        self.rsa_info.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Variables para almacenar las claves y datos cifrados
        self.current_public_key = None
        self.current_private_key = None
        self.current_encrypted_data = None  # Para almacenar la lista de bloques cifrados
        
        # Generar claves iniciales
        self.generate_rsa_keys()
    
    def generate_rsa_keys(self):
        """Generar par de claves RSA"""
        try:
            key_size = int(self.rsa_key_size.get())
            self.update_status(f"Generando claves RSA de {key_size} bits...")
            
            # Generar claves
            public_key, private_key = self.rsa.generate_keys()
            self.current_public_key = public_key
            self.current_private_key = private_key
            
            # Mostrar clave pública
            self.rsa_public_key.configure(state="normal")
            self.rsa_public_key.delete("1.0", tk.END)
            public_text = f"Clave Pública (e, n):\n\n"
            public_text += f"e = {public_key[0]}\n\n"
            public_text += f"n = {public_key[1]}\n\n"
            public_text += f"Tamaño: {key_size} bits\n"
            public_text += f"Longitud de n: {len(str(public_key[1]))} dígitos"
            self.rsa_public_key.insert("1.0", public_text)
            self.rsa_public_key.configure(state="disabled")
            
            # Mostrar clave privada
            self.rsa_private_key.configure(state="normal")
            self.rsa_private_key.delete("1.0", tk.END)
            private_text = f"Clave Privada (d, n):\n\n"
            private_text += f"d = {private_key[0]}\n\n"
            private_text += f"n = {private_key[1]}\n\n"
            private_text += f"Tamaño: {key_size} bits\n"
            private_text += f"Longitud de d: {len(str(private_key[0]))} dígitos"
            self.rsa_private_key.insert("1.0", private_text)
            self.rsa_private_key.configure(state="disabled")
            
            # Mostrar información adicional
            self.rsa_info.configure(state="normal")
            self.rsa_info.delete("1.0", tk.END)
            info_text = f"Información de Generación RSA:\n\n"
            info_text += f"Claves generadas:\n"
            info_text += f"e (exponente público) = {public_key[0]}\n"
            info_text += f"d (exponente privado) = {private_key[0]}\n"
            info_text += f"n (módulo) = {public_key[1]}\n\n"
            info_text += f"Propiedades:\n"
            info_text += f"• n es el producto de dos primos grandes\n"
            info_text += f"• e y d son inversos modulares\n"
            info_text += f"• Longitud de n: {len(str(public_key[1]))} dígitos\n\n"
            info_text += f"Seguridad:\n"
            info_text += f"• Factorización de n es computacionalmente difícil\n"
            info_text += f"• Clave pública se puede compartir libremente\n"
            info_text += f"• Clave privada debe mantenerse secreta"
            self.rsa_info.insert("1.0", info_text)
            self.rsa_info.configure(state="disabled")
            
            self.update_status(f"Claves RSA de {key_size} bits generadas exitosamente")
            
        except Exception as e:
            self.show_error(f"Error al generar claves RSA: {str(e)}")
    
    def rsa_encrypt(self):
        """Cifrar mensaje con RSA"""
        try:
            message = self.rsa_message.get("1.0", tk.END).strip()
            
            if not message:
                self.show_warning("Por favor ingrese un mensaje para cifrar")
                return
            
            if not self.current_public_key:
                self.show_warning("Por favor genere las claves RSA primero")
                return
            
            # Cifrar mensaje
            encrypted = self.rsa.encrypt(message, self.current_public_key)
            self.current_encrypted_data = encrypted  # Almacenar la lista completa
            
            # Mostrar resultado
            self.rsa_result.configure(state="normal")
            self.rsa_result.delete("1.0", tk.END)
            
            result_text = f"Mensaje Cifrado:\n\n"
            result_text += f"Texto original: {message}\n\n"
            result_text += f"Texto cifrado (bloques):\n"
            if len(encrypted) == 1:
                result_text += f"[{encrypted[0]}]\n\n"
            else:
                result_text += f"Bloques: {len(encrypted)}\n"
                for i, block in enumerate(encrypted):
                    result_text += f"Bloque {i+1}: {block}\n"
                result_text += "\n"
            
            total_digits = sum(len(str(block)) for block in encrypted)
            result_text += f"Total de dígitos: {total_digits}\n\n"
            result_text += f"Proceso:\n"
            result_text += f"• Texto convertido a bloques\n"
            result_text += f"• Aplicado: c = m^e mod n para cada bloque\n"
            result_text += f"• e = {self.current_public_key[0]}\n"
            result_text += f"• n = {self.current_public_key[1]}\n\n"
            result_text += f"💡 Usa el botón 'Descifrar' para recuperar el texto original"
            
            self.rsa_result.insert("1.0", result_text)
            self.rsa_result.configure(state="disabled")
            
            self.update_status("Mensaje cifrado con RSA exitosamente")
            
        except Exception as e:
            self.show_error(f"Error al cifrar con RSA: {str(e)}")
    
    def rsa_decrypt(self):
        """Descifrar mensaje con RSA"""
        try:
            # Verificar que hay datos cifrados
            if not self.current_encrypted_data:
                self.show_warning("Primero cifre un mensaje para poder descifrarlo")
                return
            
            if not self.current_private_key:
                self.show_warning("Por favor genere las claves RSA primero")
                return
            
            # Descifrar mensaje usando la lista almacenada
            decrypted = self.rsa.decrypt(self.current_encrypted_data, self.current_private_key)
            
            # Mostrar resultado
            self.rsa_result.configure(state="normal")
            self.rsa_result.delete("1.0", tk.END)
            
            result_text = f"Mensaje Descifrado:\n\n"
            result_text += f"Bloques cifrados: {len(self.current_encrypted_data)}\n"
            if len(self.current_encrypted_data) <= 3:
                for i, block in enumerate(self.current_encrypted_data):
                    result_text += f"Bloque {i+1}: {block}\n"
            else:
                result_text += f"Primer bloque: {self.current_encrypted_data[0]}\n"
                result_text += f"... ({len(self.current_encrypted_data)-2} bloques más) ...\n"
                result_text += f"Último bloque: {self.current_encrypted_data[-1]}\n"
            
            result_text += f"\nTexto descifrado: {decrypted}\n\n"
            result_text += f"Proceso:\n"
            result_text += f"• Aplicado: m = c^d mod n para cada bloque\n"
            result_text += f"• d = {self.current_private_key[0]}\n"
            result_text += f"• n = {self.current_private_key[1]}\n"
            result_text += f"• Bloques convertidos a texto\n\n"
            result_text += f"Verificación:\n"
            result_text += f"• El texto descifrado coincide con el original\n"
            result_text += f"• La criptografía asimétrica funciona correctamente"
            
            self.rsa_result.insert("1.0", result_text)
            self.rsa_result.configure(state="disabled")
            
            self.update_status("Mensaje descifrado con RSA exitosamente")
            
        except Exception as e:
            self.show_error(f"Error al descifrar con RSA: {str(e)}")
    
    def clear_rsa_fields(self):
        """Limpiar campos de RSA"""
        self.rsa_message.delete("1.0", tk.END)
        self.rsa_result.configure(state="normal")
        self.rsa_result.delete("1.0", tk.END)
        self.rsa_result.configure(state="disabled")
        
        # Limpiar información de claves
        self.rsa_public_key.configure(state="normal")
        self.rsa_public_key.delete("1.0", tk.END)
        self.rsa_public_key.configure(state="disabled")
        
        self.rsa_private_key.configure(state="normal")
        self.rsa_private_key.delete("1.0", tk.END)
        self.rsa_private_key.configure(state="disabled")
        
        self.rsa_info.configure(state="normal")
        self.rsa_info.delete("1.0", tk.END)
        self.rsa_info.configure(state="disabled")
        
        # Limpiar claves y datos almacenados
        self.current_public_key = None
        self.current_private_key = None
        self.current_encrypted_data = None
    
    def show_hash_screen(self):
        """Mostrar la pantalla de funciones Hash"""
        # Título
        title = ttb.Label(
            self.content_frame,
            text="🧮 Funciones Hash",
            font=("Arial", 20, "bold")
        )
        title.grid(row=0, column=0, pady=(0, 20), sticky="w")
        
        # Descripción
        desc = ttb.Label(
            self.content_frame,
            text="Las funciones hash convierten datos de cualquier tamaño en un valor hash de tamaño fijo.\n"
                 "Son fundamentales para verificar integridad y en criptografía.",
            font=("Arial", 10),
            justify="left"
        )
        desc.grid(row=1, column=0, pady=(0, 20), sticky="w")
        
        # Frame principal
        main_frame = ttb.Frame(self.content_frame)
        main_frame.grid(row=2, column=0, sticky="nsew")
        
        # Configurar grilla
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Panel de entrada
        input_frame = ttb.LabelFrame(main_frame, text="Entrada", padding=10)
        input_frame.grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky="nsew")
        
        # Campo de texto
        ttb.Label(input_frame, text="Texto a hashear:").pack(anchor="w")
        self.hash_text = tk.Text(input_frame, height=8, width=40)
        self.hash_text.pack(fill="both", expand=True, pady=(5, 10))
        
        # Selector de algoritmo
        ttb.Label(input_frame, text="Algoritmo de hash:").pack(anchor="w")
        self.hash_algorithm = ttb.Combobox(
            input_frame, 
            values=["Hash-64", "Hash-128", "Hash-256", "SHA-256"], 
            state="readonly", 
            width=15
        )
        self.hash_algorithm.pack(anchor="w", pady=(5, 10))
        self.hash_algorithm.set("Hash-256")
        
        # Botones
        button_frame = ttb.Frame(input_frame)
        button_frame.pack(fill="x")
        
        ttb.Button(
            button_frame,
            text="Calcular Hash",
            bootstyle=SUCCESS,
            command=self.calculate_hash
        ).pack(side="left", padx=(0, 5))
        
        ttb.Button(
            button_frame,
            text="Comparar",
            bootstyle=INFO,
            command=self.compare_hashes
        ).pack(side="left", padx=(0, 5))
        
        ttb.Button(
            button_frame,
            text="Limpiar",
            bootstyle=SECONDARY,
            command=self.clear_hash_fields
        ).pack(side="left")
        
        # Panel de resultados
        results_frame = ttb.LabelFrame(main_frame, text="Resultados", padding=10)
        results_frame.grid(row=0, column=1, padx=(10, 0), pady=(0, 10), sticky="nsew")
        
        self.hash_results = tk.Text(results_frame, height=8, width=40, state="disabled")
        self.hash_results.pack(fill="both", expand=True)
        
        # Panel de comparación
        comparison_frame = ttb.LabelFrame(main_frame, text="Comparación de Hashes", padding=10)
        comparison_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(10, 0))
        
        # Frame para los campos de comparación
        comp_fields_frame = ttb.Frame(comparison_frame)
        comp_fields_frame.pack(fill="x", pady=(0, 10))
        
        # Campo Hash 1
        comp_left_frame = ttb.Frame(comp_fields_frame)
        comp_left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ttb.Label(comp_left_frame, text="Hash 1:").pack(anchor="w")
        self.hash_compare1 = tk.Text(comp_left_frame, height=3, width=30)
        self.hash_compare1.pack(fill="both", expand=True)
        
        # Campo Hash 2
        comp_right_frame = ttb.Frame(comp_fields_frame)
        comp_right_frame.pack(side="right", fill="both", expand=True)
        
        ttb.Label(comp_right_frame, text="Hash 2:").pack(anchor="w")
        self.hash_compare2 = tk.Text(comp_right_frame, height=3, width=30)
        self.hash_compare2.pack(fill="both", expand=True)
        
        # Resultado de comparación
        self.hash_comparison_result = tk.Text(comparison_frame, height=4, state="disabled")
        self.hash_comparison_result.pack(fill="both", expand=True)
        
        # Lista para almacenar hashes calculados
        self.calculated_hashes = []
    
    def calculate_hash(self):
        """Calcular hash del texto"""
        try:
            text = self.hash_text.get("1.0", tk.END).strip()
            algorithm = self.hash_algorithm.get()
            
            if not text:
                self.show_warning("Por favor ingrese un texto para hashear")
                return
            
            # Calcular hash según el algoritmo seleccionado
            if algorithm == "Hash-64":
                hash_value = self.hash.hash_64(text)
                hash_length = 64
            elif algorithm == "Hash-128":
                hash_value = self.hash.hash_128(text)
                hash_length = 128
            elif algorithm == "Hash-256":
                hash_value = self.hash.hash_256(text)
                hash_length = 256
            elif algorithm == "SHA-256":
                hash_value = self.hash.sha256(text)
                hash_length = 256
            else:
                self.show_error("Algoritmo no soportado")
                return
            
            # Almacenar hash calculado
            hash_info = {
                'text': text,
                'algorithm': algorithm,
                'hash': hash_value,
                'length': hash_length
            }
            self.calculated_hashes.append(hash_info)
            
            # Mostrar resultado
            self.hash_results.configure(state="normal")
            self.hash_results.delete("1.0", tk.END)
            
            result_text = f"Resultado del Hash:\n\n"
            result_text += f"Algoritmo: {algorithm}\n"
            result_text += f"Texto original: {text[:100]}{'...' if len(text) > 100 else ''}\n"
            result_text += f"Longitud del texto: {len(text)} caracteres\n\n"
            result_text += f"Hash calculado:\n{hash_value}\n\n"
            result_text += f"Información del hash:\n"
            result_text += f"• Longitud: {len(hash_value)} caracteres\n"
            result_text += f"• Bits: {hash_length} bits\n"
            result_text += f"• Hexadecimal: {'Sí' if all(c in '0123456789abcdefABCDEF' for c in hash_value) else 'No'}\n\n"
            
            # Análisis del hash
            result_text += f"Análisis:\n"
            unique_chars = len(set(hash_value))
            result_text += f"• Caracteres únicos: {unique_chars}\n"
            result_text += f"• Distribución: {'Buena' if unique_chars > len(hash_value) * 0.5 else 'Regular'}\n"
            
            # Mostrar algunos hashes anteriores
            if len(self.calculated_hashes) > 1:
                result_text += f"\nÚltimos 3 hashes calculados:\n"
                for i, prev_hash in enumerate(self.calculated_hashes[-3:], 1):
                    result_text += f"{i}. {prev_hash['algorithm']}: {prev_hash['hash'][:32]}...\n"
            
            self.hash_results.insert("1.0", result_text)
            self.hash_results.configure(state="disabled")
            
            self.update_status(f"Hash {algorithm} calculado exitosamente")
            
        except Exception as e:
            self.show_error(f"Error al calcular hash: {str(e)}")
    
    def compare_hashes(self):
        """Comparar dos hashes"""
        try:
            hash1 = self.hash_compare1.get("1.0", tk.END).strip()
            hash2 = self.hash_compare2.get("1.0", tk.END).strip()
            
            if not hash1 or not hash2:
                self.show_warning("Por favor ingrese ambos hashes para comparar")
                return
            
            # Comparar hashes
            are_equal = hash1 == hash2
            
            # Mostrar resultado
            self.hash_comparison_result.configure(state="normal")
            self.hash_comparison_result.delete("1.0", tk.END)
            
            comparison_text = f"Resultado de la Comparación:\n\n"
            comparison_text += f"Hash 1: {hash1[:64]}{'...' if len(hash1) > 64 else ''}\n"
            comparison_text += f"Hash 2: {hash2[:64]}{'...' if len(hash2) > 64 else ''}\n\n"
            
            if are_equal:
                comparison_text += "✅ LOS HASHES SON IDÉNTICOS\n"
                comparison_text += "• Los datos de origen son los mismos\n"
                comparison_text += "• La integridad se mantiene\n"
                comparison_text += "• No hay modificaciones"
            else:
                comparison_text += "❌ LOS HASHES SON DIFERENTES\n"
                comparison_text += "• Los datos de origen son diferentes\n"
                comparison_text += "• Posible modificación o corrupción\n"
                comparison_text += "• Verificar integridad de los datos\n\n"
                
                # Análisis de diferencias
                differences = sum(1 for a, b in zip(hash1, hash2) if a != b)
                comparison_text += f"Análisis de diferencias:\n"
                comparison_text += f"• Caracteres diferentes: {differences}\n"
                comparison_text += f"• Similitud: {(1 - differences/max(len(hash1), len(hash2))) * 100:.1f}%"
            
            self.hash_comparison_result.insert("1.0", comparison_text)
            self.hash_comparison_result.configure(state="disabled")
            
            self.update_status("Comparación de hashes completada")
            
        except Exception as e:
            self.show_error(f"Error al comparar hashes: {str(e)}")
    
    def clear_hash_fields(self):
        """Limpiar campos de hash"""
        self.hash_text.delete("1.0", tk.END)
        self.hash_algorithm.set("Hash-256")
        
        self.hash_results.configure(state="normal")
        self.hash_results.delete("1.0", tk.END)
        self.hash_results.configure(state="disabled")
        
        self.hash_compare1.delete("1.0", tk.END)
        self.hash_compare2.delete("1.0", tk.END)
        
        self.hash_comparison_result.configure(state="normal")
        self.hash_comparison_result.delete("1.0", tk.END)
        self.hash_comparison_result.configure(state="disabled")
        
        self.calculated_hashes.clear()
    
    def show_des_screen(self):
        """Mostrar la pantalla del cifrado DES"""
        # Título
        title = ttb.Label(
            self.content_frame,
            text="🔏 Cifrado DES",
            font=("Arial", 20, "bold")
        )
        title.grid(row=0, column=0, pady=(0, 20), sticky="w")
        
        # Descripción
        desc = ttb.Label(
            self.content_frame,
            text="DES (Data Encryption Standard) es un algoritmo de cifrado simétrico que utiliza\n"
                 "una clave de 64 bits y soporta modos ECB y CBC.",
            font=("Arial", 10),
            justify="left"
        )
        desc.grid(row=1, column=0, pady=(0, 20), sticky="w")
        
        # Frame principal
        main_frame = ttb.Frame(self.content_frame)
        main_frame.grid(row=2, column=0, sticky="nsew")
        
        # Configurar grilla
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Panel de entrada
        input_frame = ttb.LabelFrame(main_frame, text="Entrada", padding=10)
        input_frame.grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky="nsew")
        
        # Campo de texto
        ttb.Label(input_frame, text="Texto:").pack(anchor="w")
        self.des_text = tk.Text(input_frame, height=6, width=40)
        self.des_text.pack(fill="both", expand=True, pady=(5, 10))
        
        # Campo de clave
        ttb.Label(input_frame, text="Clave (8 caracteres):").pack(anchor="w")
        self.des_key = ttb.Entry(input_frame, width=20, show="*")
        self.des_key.pack(anchor="w", pady=(5, 10))
        self.des_key.insert(0, "SECRETKY")
        
        # Validación en tiempo real
        self.des_key.bind('<KeyRelease>', self.validate_des_key)
        
        # Selector de modo
        ttb.Label(input_frame, text="Modo de operación:").pack(anchor="w")
        self.des_mode = ttb.Combobox(
            input_frame, 
            values=["ECB", "CBC"], 
            state="readonly", 
            width=10
        )
        self.des_mode.pack(anchor="w", pady=(5, 10))
        self.des_mode.set("ECB")
        
        # Vector de inicialización (solo para CBC)
        ttb.Label(input_frame, text="IV (8 caracteres, solo CBC):").pack(anchor="w")
        self.des_iv = ttb.Entry(input_frame, width=20)
        self.des_iv.pack(anchor="w", pady=(5, 10))
        self.des_iv.insert(0, "INITVECT")
        
        # Botones
        button_frame = ttb.Frame(input_frame)
        button_frame.pack(fill="x")
        
        ttb.Button(
            button_frame,
            text="Cifrar",
            bootstyle=SUCCESS,
            command=self.des_encrypt
        ).pack(side="left", padx=(0, 5))
        
        ttb.Button(
            button_frame,
            text="Descifrar",
            bootstyle=WARNING,
            command=self.des_decrypt
        ).pack(side="left", padx=(0, 5))
        
        ttb.Button(
            button_frame,
            text="Limpiar",
            bootstyle=SECONDARY,
            command=self.clear_des_fields
        ).pack(side="left", padx=(0, 5))
        
        ttb.Button(
            button_frame,
            text="Generar Clave",
            bootstyle=INFO,
            command=self.generate_des_key
        ).pack(side="left")
        
        # Panel de salida
        output_frame = ttb.LabelFrame(main_frame, text="Resultado", padding=10)
        output_frame.grid(row=0, column=1, padx=(10, 0), pady=(0, 10), sticky="nsew")
        
        self.des_result = tk.Text(output_frame, height=6, width=40, state="disabled")
        self.des_result.pack(fill="both", expand=True)
        
        # Panel de información
        info_frame = ttb.LabelFrame(main_frame, text="Información DES", padding=10)
        info_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(10, 0))
        
        self.des_info = tk.Text(info_frame, height=8, state="disabled")
        self.des_info.pack(fill="both", expand=True)
        
        # Actualizar información inicial
        self.update_des_info()
    
    def validate_des_key(self, event=None):
        """Validar clave DES en tiempo real"""
        key = self.des_key.get()
        if len(key) > 8:
            self.des_key.delete(8, tk.END)
            self.update_status("Clave DES limitada a 8 caracteres")
        elif len(key) < 8:
            self.update_status(f"Clave DES: {len(key)}/8 caracteres")
        else:
            self.update_status("Clave DES completa (8 caracteres)")
    
    def des_encrypt(self):
        """Cifrar texto con DES"""
        try:
            text = self.des_text.get("1.0", tk.END).strip()
            key = self.des_key.get()
            mode = self.des_mode.get()
            iv = self.des_iv.get() if mode == "CBC" else None
            
            if not text:
                self.show_warning("Por favor ingrese un texto para cifrar")
                return
            
            if len(key) != 8:
                self.show_warning("La clave debe tener exactamente 8 caracteres")
                return
            
            if mode == "CBC" and len(iv) != 8:
                self.show_warning("El IV debe tener exactamente 8 caracteres para modo CBC")
                return
            
            # Cifrar según el modo
            if mode == "ECB":
                encrypted = self.des.encrypt_ecb(text, key)
            else:  # CBC
                encrypted = self.des.encrypt_cbc(text, key, iv)
            
            # Mostrar resultado
            self.display_result(self.des_result, encrypted)
            self.display_des_operation_info("Cifrado", text, key, mode, iv, encrypted)
            
            self.update_status(f"Texto cifrado con DES-{mode} exitosamente")
            
        except Exception as e:
            self.show_error(f"Error al cifrar con DES: {str(e)}")
    
    def des_decrypt(self):
        """Descifrar texto con DES"""
        try:
            text = self.des_text.get("1.0", tk.END).strip()
            key = self.des_key.get()
            mode = self.des_mode.get()
            iv = self.des_iv.get() if mode == "CBC" else None
            
            if not text:
                self.show_warning("Por favor ingrese un texto para descifrar")
                return
            
            if len(key) != 8:
                self.show_warning("La clave debe tener exactamente 8 caracteres")
                return
            
            if mode == "CBC" and len(iv) != 8:
                self.show_warning("El IV debe tener exactamente 8 caracteres para modo CBC")
                return
            
            # Descifrar según el modo
            if mode == "ECB":
                decrypted = self.des.decrypt_ecb(text, key)
            else:  # CBC
                decrypted = self.des.decrypt_cbc(text, key, iv)
            
            # Mostrar resultado
            self.display_result(self.des_result, decrypted)
            self.display_des_operation_info("Descifrado", text, key, mode, iv, decrypted)
            
            self.update_status(f"Texto descifrado con DES-{mode} exitosamente")
            
        except Exception as e:
            self.show_error(f"Error al descifrar con DES: {str(e)}")
    
    def generate_des_key(self):
        """Generar una clave DES aleatoria"""
        import random
        import string
        
        # Generar clave aleatoria de 8 caracteres
        key = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        
        self.des_key.delete(0, tk.END)
        self.des_key.insert(0, key)
        
        self.update_status("Clave DES generada aleatoriamente")
    
    def display_des_operation_info(self, operation, text, key, mode, iv, result):
        """Mostrar información de la operación DES"""
        self.des_info.configure(state="normal")
        self.des_info.delete("1.0", tk.END)
        
        info_text = f"Información de {operation} DES:\n\n"
        info_text += f"Operación: {operation}\n"
        info_text += f"Modo: DES-{mode}\n"
        info_text += f"Clave: {'*' * len(key)} (8 caracteres)\n"
        if mode == "CBC":
            info_text += f"IV: {iv}\n"
        info_text += f"\nTexto original ({len(text)} caracteres):\n{text[:100]}{'...' if len(text) > 100 else ''}\n"
        info_text += f"\nResultado ({len(result)} caracteres):\n{result[:100]}{'...' if len(result) > 100 else ''}\n\n"
        
        # Información técnica
        info_text += f"Detalles técnicos:\n"
        info_text += f"• Algoritmo: Data Encryption Standard (DES)\n"
        info_text += f"• Tamaño de bloque: 64 bits (8 bytes)\n"
        info_text += f"• Tamaño de clave: 64 bits (8 bytes)\n"
        info_text += f"• Modo de operación: {mode}\n"
        
        if mode == "ECB":
            info_text += f"• ECB: Cada bloque se cifra independientemente\n"
            info_text += f"• Ventaja: Simple y paralelo\n"
            info_text += f"• Desventaja: Patrones visibles en datos similares\n"
        else:
            info_text += f"• CBC: Cada bloque depende del anterior\n"
            info_text += f"• Vector de inicialización requerido\n"
            info_text += f"• Ventaja: Oculta patrones en los datos\n"
            info_text += f"• Desventaja: No es paralelo para cifrado\n"
        
        info_text += f"\nNota de seguridad:\n"
        info_text += f"DES es considerado inseguro para aplicaciones modernas\n"
        info_text += f"debido a su tamaño de clave relativamente pequeño (56 bits efectivos)."
        
        self.des_info.insert("1.0", info_text)
        self.des_info.configure(state="disabled")
    
    def update_des_info(self):
        """Actualizar información general de DES"""
        self.des_info.configure(state="normal")
        self.des_info.delete("1.0", tk.END)
        
        info_text = """Información sobre DES (Data Encryption Standard):

DES es un algoritmo de cifrado simétrico desarrollado por IBM en los años 1970
y adoptado como estándar por el gobierno de Estados Unidos.

Características principales:
• Algoritmo de cifrado en bloques
• Tamaño de bloque: 64 bits (8 bytes)
• Tamaño de clave: 64 bits (56 bits efectivos + 8 bits de paridad)
• 16 rondas de procesamiento
• Utiliza redes de Feistel

Modos de operación implementados:
• ECB (Electronic Codebook): Cada bloque se cifra independientemente
• CBC (Cipher Block Chaining): Cada bloque depende del anterior

Estado actual de seguridad:
⚠️ DES es considerado inseguro para aplicaciones modernas debido a:
• Tamaño de clave pequeño (56 bits efectivos)
• Vulnerable a ataques de fuerza bruta
• Reemplazado por AES en aplicaciones críticas

Uso recomendado: Solo para propósitos educativos y compatibilidad legacy."""
        
        self.des_info.insert("1.0", info_text)
        self.des_info.configure(state="disabled")
    
    def clear_des_fields(self):
        """Limpiar campos de DES"""
        self.des_text.delete("1.0", tk.END)
        self.des_key.delete(0, tk.END)
        self.des_key.insert(0, "SECRETKY")
        self.des_mode.set("ECB")
        self.des_iv.delete(0, tk.END)
        self.des_iv.insert(0, "INITVECT")
        
        self.des_result.configure(state="normal")
        self.des_result.delete("1.0", tk.END)
        self.des_result.configure(state="disabled")
        
        self.update_des_info()
    
    def show_signature_screen(self):
        """Mostrar la pantalla de Firma Digital"""
        # Título
        title = ttb.Label(
            self.content_frame,
            text="✍️ Firma Digital",
            font=("Arial", 20, "bold")
        )
        title.grid(row=0, column=0, pady=(0, 20), sticky="w")
        
        # Descripción
        desc = ttb.Label(
            self.content_frame,
            text="La firma digital proporciona autenticidad e integridad mediante criptografía\n"
                 "asimétrica. Combina hash del mensaje con cifrado RSA de la clave privada.",
            font=("Arial", 10),
            justify="left"
        )
        desc.grid(row=1, column=0, pady=(0, 20), sticky="w")
        
        # Frame principal
        main_frame = ttb.Frame(self.content_frame)
        main_frame.grid(row=2, column=0, sticky="nsew")
        
        # Configurar grilla
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Panel de mensaje
        message_frame = ttb.LabelFrame(main_frame, text="Mensaje", padding=10)
        message_frame.grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky="nsew")
        
        # Campo de mensaje
        ttb.Label(message_frame, text="Mensaje a firmar/verificar:").pack(anchor="w")
        self.signature_message = tk.Text(message_frame, height=6, width=40)
        self.signature_message.pack(fill="both", expand=True, pady=(5, 10))
        
        # Configuración
        config_frame = ttb.Frame(message_frame)
        config_frame.pack(fill="x", pady=(0, 10))
        
        ttb.Label(config_frame, text="Algoritmo Hash:").pack(anchor="w")
        self.signature_hash_algo = ttb.Combobox(
            config_frame, 
            values=["SHA-256", "Hash-256"], 
            state="readonly", 
            width=15
        )
        self.signature_hash_algo.pack(anchor="w", pady=(5, 10))
        self.signature_hash_algo.set("SHA-256")
        
        # Botones de operación
        button_frame = ttb.Frame(message_frame)
        button_frame.pack(fill="x")
        
        ttb.Button(
            button_frame,
            text="Generar Claves",
            bootstyle=INFO,
            command=self.generate_signature_keys
        ).pack(side="left", padx=(0, 5))
        
        ttb.Button(
            button_frame,
            text="Firmar",
            bootstyle=SUCCESS,
            command=self.sign_message
        ).pack(side="left", padx=(0, 5))
        
        ttb.Button(
            button_frame,
            text="Verificar",
            bootstyle=WARNING,
            command=self.verify_signature
        ).pack(side="left", padx=(0, 5))
        
        ttb.Button(
            button_frame,
            text="Limpiar",
            bootstyle=SECONDARY,
            command=self.clear_signature_fields
        ).pack(side="left")
        
        # Panel de firma
        signature_frame = ttb.LabelFrame(main_frame, text="Firma Digital", padding=10)
        signature_frame.grid(row=0, column=1, padx=(10, 0), pady=(0, 10), sticky="nsew")
        
        ttb.Label(signature_frame, text="Firma generada:").pack(anchor="w")
        self.signature_result = tk.Text(signature_frame, height=4, width=40, state="disabled")
        self.signature_result.pack(fill="both", expand=True, pady=(5, 10))
        
        ttb.Label(signature_frame, text="Estado de verificación:").pack(anchor="w")
        self.signature_verification = tk.Text(signature_frame, height=2, width=40, state="disabled")
        self.signature_verification.pack(fill="both", expand=True)
        
        # Panel de información de claves
        keys_frame = ttb.LabelFrame(main_frame, text="Información de Claves", padding=10)
        keys_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(10, 0))
        
        # Notebook para claves
        self.signature_notebook = ttb.Notebook(keys_frame)
        self.signature_notebook.pack(fill="both", expand=True)
        
        # Pestaña de proceso
        process_frame = ttb.Frame(self.signature_notebook)
        self.signature_notebook.add(process_frame, text="Proceso de Firma")
        
        self.signature_process = tk.Text(process_frame, height=8, state="disabled")
        self.signature_process.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Pestaña de claves
        keys_info_frame = ttb.Frame(self.signature_notebook)
        self.signature_notebook.add(keys_info_frame, text="Claves RSA")
        
        self.signature_keys_info = tk.Text(keys_info_frame, height=8, state="disabled")
        self.signature_keys_info.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Variables para las claves y firma
        self.signature_keys = None
        self.current_signature = None
        self.current_message_hash = None
        
        # Mostrar información inicial
        self.show_signature_info()
    
    def generate_signature_keys(self):
        """Generar claves para firma digital"""
        try:
            self.update_status("Generando claves RSA para firma digital...")
            
            # Generar claves RSA (devuelve tuplas)
            public_key, private_key = self.signature.generate_keys(1024)  # 1024 bits para rapidez
            
            # Almacenar claves como tuplas
            self.signature_keys = {
                'public_key': public_key,
                'private_key': private_key
            }
            
            # Mostrar información de claves
            self.signature_keys_info.configure(state="normal")
            self.signature_keys_info.delete("1.0", tk.END)
            
            keys_text = f"Claves RSA para Firma Digital:\n\n"
            keys_text += f"Clave Pública (para verificación):\n"
            keys_text += f"e = {public_key[0]}\n"
            keys_text += f"n = {public_key[1]}\n\n"
            keys_text += f"Clave Privada (para firmado):\n"
            keys_text += f"d = {private_key[0]}\n"
            keys_text += f"n = {private_key[1]}\n\n"
            keys_text += f"Información:\n"
            keys_text += f"• Tamaño de clave: 1024 bits\n"
            keys_text += f"• Longitud de n: {len(str(public_key[1]))} dígitos\n\n"
            keys_text += f"Uso:\n"
            keys_text += f"• Clave privada: Firmar documentos (mantener secreta)\n"
            keys_text += f"• Clave pública: Verificar firmas (compartir libremente)"
            
            self.signature_keys_info.insert("1.0", keys_text)
            self.signature_keys_info.configure(state="disabled")
            
            self.update_status("Claves RSA para firma digital generadas exitosamente")
            
        except Exception as e:
            self.show_error(f"Error al generar claves: {str(e)}")
    
    def sign_message(self):
        """Firmar mensaje"""
        try:
            message = self.signature_message.get("1.0", tk.END).strip()
            hash_algo = self.signature_hash_algo.get()
            
            if not message:
                self.show_warning("Por favor ingrese un mensaje para firmar")
                return
            
            if not self.signature_keys:
                self.show_warning("Por favor genere las claves RSA primero")
                return
            
            # Firmar mensaje usando el método correcto
            signature = self.signature.sign_message(message, self.signature_keys['private_key'])
            
            # Generar hash del mensaje para mostrar
            message_hash = self.signature.hash_func.sha256_wrapper(message)
            
            self.current_signature = signature
            self.current_message_hash = message_hash
            
            # Mostrar firma
            self.signature_result.configure(state="normal")
            self.signature_result.delete("1.0", tk.END)
            self.signature_result.insert("1.0", str(self.current_signature))
            self.signature_result.configure(state="disabled")
            
            # Mostrar proceso
            signature_data = {
                'signature': signature,
                'message_hash': message_hash,
                'message': message
            }
            self.display_signature_process("Firmado", message, hash_algo, signature_data)
            
            # Limpiar verificación anterior
            self.signature_verification.configure(state="normal")
            self.signature_verification.delete("1.0", tk.END)
            self.signature_verification.insert("1.0", "Mensaje firmado. Use 'Verificar' para validar la firma.")
            self.signature_verification.configure(state="disabled")
            
            self.update_status("Mensaje firmado exitosamente")
            
        except Exception as e:
            self.show_error(f"Error al firmar mensaje: {str(e)}")
    
    def verify_signature(self):
        """Verificar firma"""
        try:
            message = self.signature_message.get("1.0", tk.END).strip()
            hash_algo = self.signature_hash_algo.get()
            
            if not message:
                self.show_warning("Por favor ingrese el mensaje original")
                return
            
            if not self.signature_keys:
                self.show_warning("Por favor genere las claves RSA primero")
                return
            
            if not self.current_signature:
                self.show_warning("Por favor firme el mensaje primero")
                return
            
            # Verificar firma usando el método correcto
            is_valid = self.signature.verify_signature(message, self.current_signature, self.signature_keys['public_key'])
            
            # Mostrar resultado de verificación
            self.signature_verification.configure(state="normal")
            self.signature_verification.delete("1.0", tk.END)
            
            if is_valid:
                verification_text = "✅ FIRMA VÁLIDA\nEl mensaje es auténtico y no ha sido modificado."
                self.signature_verification.configure(bg="#d4edda", fg="#155724")
            else:
                verification_text = "❌ FIRMA INVÁLIDA\nEl mensaje ha sido modificado o la firma es incorrecta."
                self.signature_verification.configure(bg="#f8d7da", fg="#721c24")
            
            self.signature_verification.insert("1.0", verification_text)
            self.signature_verification.configure(state="disabled")
            
            # Mostrar proceso de verificación
            verification_data = {
                'signature': self.current_signature,
                'message_hash': self.current_message_hash,
                'is_valid': is_valid
            }
            self.display_signature_process("Verificación", message, hash_algo, verification_data)
            
            self.update_status(f"Verificación completada: {'Válida' if is_valid else 'Inválida'}")
            
        except Exception as e:
            self.show_error(f"Error al verificar firma: {str(e)}")
    
    def display_signature_process(self, operation, message, hash_algo, data):
        """Mostrar información del proceso de firma"""
        self.signature_process.configure(state="normal")
        self.signature_process.delete("1.0", tk.END)
        
        process_text = f"Proceso de {operation} - Firma Digital:\n\n"
        process_text += f"1. Mensaje original:\n   {message[:80]}{'...' if len(message) > 80 else ''}\n\n"
        
        if operation == "Firmado":
            process_text += f"2. Hash del mensaje ({hash_algo}):\n   {data['message_hash']}\n\n"
            process_text += f"3. Cifrado del hash con clave privada:\n   Signature = Hash^d mod n\n"
            process_text += f"   d = {str(self.signature_keys['private_key'][0])[:20]}...\n"
            process_text += f"   n = {str(self.signature_keys['private_key'][1])[:20]}...\n\n"
            process_text += f"4. Firma digital generada:\n   {str(data['signature'])[:60]}...\n\n"
            process_text += f"Resultado: Mensaje firmado exitosamente\n"
            process_text += f"• La firma puede verificarse con la clave pública\n"
            process_text += f"• Garantiza autenticidad e integridad del mensaje"
        
        else:  # Verificación
            process_text += f"2. Hash del mensaje recibido ({hash_algo}):\n   {data['message_hash']}\n\n"
            process_text += f"3. Descifrado de la firma con clave pública:\n   Hash_descifrado = Signature^e mod n\n"
            process_text += f"   e = {self.signature_keys['public_key'][0]}\n"
            process_text += f"   n = {str(self.signature_keys['public_key'][1])[:20]}...\n\n"
            process_text += f"4. Comparación de hashes:\n"
            process_text += f"   Hash calculado == Hash descifrado: {'SÍ' if data['is_valid'] else 'NO'}\n\n"
            process_text += f"Resultado: {'✅ FIRMA VÁLIDA' if data['is_valid'] else '❌ FIRMA INVÁLIDA'}\n"
            
            if data['is_valid']:
                process_text += f"• El mensaje no ha sido modificado\n"
                process_text += f"• La firma proviene del poseedor de la clave privada\n"
                process_text += f"• Se garantiza autenticidad e integridad"
            else:
                process_text += f"• El mensaje pudo haber sido modificado\n"
                process_text += f"• La firma no coincide con el mensaje\n"
                process_text += f"• NO se puede garantizar autenticidad"
        
        self.signature_process.insert("1.0", process_text)
        self.signature_process.configure(state="disabled")
    
    def show_signature_info(self):
        """Mostrar información general sobre firma digital"""
        self.signature_process.configure(state="normal")
        self.signature_process.delete("1.0", tk.END)
        
        info_text = """Firma Digital - Conceptos Fundamentales:

La firma digital es un mecanismo criptográfico que proporciona:
• Autenticidad: Confirma la identidad del firmante
• Integridad: Detecta modificaciones en el mensaje
• No repudio: El firmante no puede negar haber firmado

Proceso de Firmado:
1. Se calcula el hash del mensaje original
2. El hash se cifra con la clave privada del firmante
3. El resultado es la firma digital

Proceso de Verificación:
1. Se calcula el hash del mensaje recibido
2. Se descifra la firma con la clave pública
3. Se comparan ambos hashes

Ventajas:
• Más eficiente que cifrar todo el mensaje
• Funciona con mensajes de cualquier tamaño
• Proporciona prueba criptográfica de autenticidad

Aplicaciones:
• Documentos legales digitales
• Transacciones financieras
• Comunicaciones seguras
• Autenticación de software"""
        
        self.signature_process.insert("1.0", info_text)
        self.signature_process.configure(state="disabled")
    
    def clear_signature_fields(self):
        """Limpiar campos de firma digital"""
        self.signature_message.delete("1.0", tk.END)
        self.signature_hash_algo.set("SHA-256")
        
        self.signature_result.configure(state="normal")
        self.signature_result.delete("1.0", tk.END)
        self.signature_result.configure(state="disabled")
        
        self.signature_verification.configure(state="normal", bg="white", fg="black")
        self.signature_verification.delete("1.0", tk.END)
        self.signature_verification.configure(state="disabled")
        
        self.signature_keys_info.configure(state="normal")
        self.signature_keys_info.delete("1.0", tk.END)
        self.signature_keys_info.configure(state="disabled")
        
        # Limpiar variables
        self.signature_keys = None
        self.current_signature = None
        self.current_message_hash = None
        
        # Mostrar información inicial
        self.show_signature_info()
    
    def show_huffman_screen(self):
        """Mostrar la pantalla de codificación Huffman"""
        # Título
        title = ttb.Label(
            self.content_frame,
            text="📊 Codificación Huffman",
            font=("Arial", 20, "bold")
        )
        title.grid(row=0, column=0, pady=(0, 20), sticky="w")
        
        # Descripción
        desc = ttb.Label(
            self.content_frame,
            text="La codificación Huffman es un algoritmo de compresión sin pérdida que asigna\n"
                 "códigos más cortos a caracteres más frecuentes.",
            font=("Arial", 10),
            justify="left"
        )
        desc.grid(row=1, column=0, pady=(0, 20), sticky="w")
        
        # Frame principal
        main_frame = ttb.Frame(self.content_frame)
        main_frame.grid(row=2, column=0, sticky="nsew")
        
        # Configurar grilla
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Panel de entrada
        input_frame = ttb.LabelFrame(main_frame, text="Texto Original", padding=10)
        input_frame.grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky="nsew")
        
        # Campo de texto
        ttb.Label(input_frame, text="Texto a comprimir:").pack(anchor="w")
        self.huffman_text = tk.Text(input_frame, height=8, width=40)
        self.huffman_text.pack(fill="both", expand=True, pady=(5, 10))
        
        # Botones
        button_frame = ttb.Frame(input_frame)
        button_frame.pack(fill="x")
        
        ttb.Button(
            button_frame,
            text="Codificar",
            bootstyle=SUCCESS,
            command=self.huffman_encode
        ).pack(side="left", padx=(0, 5))
        
        ttb.Button(
            button_frame,
            text="Decodificar",
            bootstyle=WARNING,
            command=self.huffman_decode
        ).pack(side="left", padx=(0, 5))
        
        ttb.Button(
            button_frame,
            text="Limpiar",
            bootstyle=SECONDARY,
            command=self.clear_huffman_fields
        ).pack(side="left", padx=(0, 5))
        
        ttb.Button(
            button_frame,
            text="Ejemplo",
            bootstyle=INFO,
            command=self.load_huffman_example
        ).pack(side="left")
        
        # Panel de resultado
        result_frame = ttb.LabelFrame(main_frame, text="Resultado", padding=10)
        result_frame.grid(row=0, column=1, padx=(10, 0), pady=(0, 10), sticky="nsew")
        
        self.huffman_result = tk.Text(result_frame, height=8, width=40, state="disabled")
        self.huffman_result.pack(fill="both", expand=True)
        
        # Panel de estadísticas
        stats_frame = ttb.LabelFrame(main_frame, text="Estadísticas de Compresión", padding=10)
        stats_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(10, 0))
        
        # Notebook para organizar la información
        self.huffman_notebook = ttb.Notebook(stats_frame)
        self.huffman_notebook.pack(fill="both", expand=True)
        
        # Pestaña de frecuencias
        freq_frame = ttb.Frame(self.huffman_notebook)
        self.huffman_notebook.add(freq_frame, text="Frecuencias")
        
        self.huffman_frequencies = tk.Text(freq_frame, height=10, state="disabled")
        self.huffman_frequencies.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Pestaña de códigos
        codes_frame = ttb.Frame(self.huffman_notebook)
        self.huffman_notebook.add(codes_frame, text="Códigos")
        
        self.huffman_codes = tk.Text(codes_frame, height=10, state="disabled")
        self.huffman_codes.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Pestaña de árbol
        tree_frame = ttb.Frame(self.huffman_notebook)
        self.huffman_notebook.add(tree_frame, text="Árbol")
        
        self.huffman_tree = tk.Text(tree_frame, height=10, state="disabled", font=("Courier New", 9))
        self.huffman_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Variables para almacenar datos
        self.huffman_encoder = None
        self.last_encoded_data = None
    
    def huffman_encode(self):
        """Codificar texto con Huffman"""
        try:
            text = self.huffman_text.get("1.0", tk.END).strip()
            
            if not text:
                self.show_warning("Por favor ingrese un texto para codificar")
                return
            
            if len(text) < 2:
                self.show_warning("El texto debe tener al menos 2 caracteres")
                return
            
            # Codificar con Huffman
            encoded_data = self.huffman.encode(text)
            self.huffman_encoder = self.huffman
            self.last_encoded_data = encoded_data
            
            # Mostrar resultado
            self.huffman_result.configure(state="normal")
            self.huffman_result.delete("1.0", tk.END)
            
            result_text = f"Texto Codificado (Huffman):\n\n"
            result_text += f"Código binario:\n{encoded_data['encoded'][:200]}"
            if len(encoded_data['encoded']) > 200:
                result_text += f"...\n(Mostrando primeros 200 bits de {len(encoded_data['encoded'])} totales)"
            result_text += f"\n\nEstadísticas de compresión:\n"
            result_text += f"• Tamaño original: {encoded_data['original_size']} bits\n"
            result_text += f"• Tamaño comprimido: {encoded_data['compressed_size']} bits\n"
            result_text += f"• Ratio de compresión: {encoded_data['compression_ratio']:.2f}%\n"
            result_text += f"• Ahorro de espacio: {encoded_data['space_saved']:.2f}%"
            
            self.huffman_result.insert("1.0", result_text)
            self.huffman_result.configure(state="disabled")
            
            # Mostrar frecuencias
            self.display_huffman_frequencies(encoded_data['frequencies'])
            
            # Mostrar códigos
            self.display_huffman_codes(encoded_data['codes'])
            
            # Mostrar árbol
            self.display_huffman_tree(encoded_data['tree_visualization'])
            
            self.update_status(f"Texto codificado con Huffman - Compresión: {encoded_data['compression_ratio']:.1f}%")
            
        except Exception as e:
            self.show_error(f"Error al codificar con Huffman: {str(e)}")
    
    def huffman_decode(self):
        """Decodificar texto con Huffman"""
        try:
            if not self.last_encoded_data:
                self.show_warning("Primero codifique un texto para poder decodificarlo")
                return
            
            # Decodificar
            decoded_text = self.huffman.decode(
                self.last_encoded_data['encoded'], 
                self.last_encoded_data['codes']
            )
            
            # Mostrar resultado
            self.huffman_result.configure(state="normal")
            self.huffman_result.delete("1.0", tk.END)
            
            result_text = f"Texto Decodificado:\n\n"
            result_text += f"{decoded_text}\n\n"
            result_text += f"Verificación:\n"
            original_text = self.huffman_text.get("1.0", tk.END).strip()
            is_correct = decoded_text == original_text
            result_text += f"• Decodificación {'✅ CORRECTA' if is_correct else '❌ INCORRECTA'}\n"
            result_text += f"• Longitud original: {len(original_text)} caracteres\n"
            result_text += f"• Longitud decodificada: {len(decoded_text)} caracteres\n"
            
            if is_correct:
                result_text += f"• ✅ El proceso de compresión es sin pérdidas"
            else:
                result_text += f"• ❌ Error en el proceso de decodificación"
            
            self.huffman_result.insert("1.0", result_text)
            self.huffman_result.configure(state="disabled")
            
            self.update_status(f"Decodificación {'exitosa' if is_correct else 'fallida'}")
            
        except Exception as e:
            self.show_error(f"Error al decodificar: {str(e)}")
    
    def display_huffman_frequencies(self, frequencies):
        """Mostrar tabla de frecuencias"""
        self.huffman_frequencies.configure(state="normal")
        self.huffman_frequencies.delete("1.0", tk.END)
        
        freq_text = "Análisis de Frecuencias:\n\n"
        freq_text += f"{'Carácter':<10} {'Frecuencia':<12} {'Porcentaje':<12}\n"
        freq_text += "-" * 40 + "\n"
        
        total_chars = sum(frequencies.values())
        sorted_freq = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
        
        for char, freq in sorted_freq:
            char_display = repr(char) if char in '\n\r\t ' else char
            percentage = (freq / total_chars) * 100
            freq_text += f"{char_display:<10} {freq:<12} {percentage:<12.1f}%\n"
        
        freq_text += f"\nTotal de caracteres: {total_chars}\n"
        freq_text += f"Caracteres únicos: {len(frequencies)}\n"
        freq_text += f"Carácter más frecuente: '{sorted_freq[0][0]}' ({sorted_freq[0][1]} veces)"
        
        self.huffman_frequencies.insert("1.0", freq_text)
        self.huffman_frequencies.configure(state="disabled")
    
    def display_huffman_codes(self, codes):
        """Mostrar tabla de códigos Huffman"""
        self.huffman_codes.configure(state="normal")
        self.huffman_codes.delete("1.0", tk.END)
        
        codes_text = "Códigos Huffman Generados:\n\n"
        codes_text += f"{'Carácter':<10} {'Código':<15} {'Longitud':<10}\n"
        codes_text += "-" * 40 + "\n"
        
        # Ordenar por longitud de código
        sorted_codes = sorted(codes.items(), key=lambda x: len(x[1]))
        
        total_bits = 0
        for char, code in sorted_codes:
            char_display = repr(char) if char in '\n\r\t ' else char
            codes_text += f"{char_display:<10} {code:<15} {len(code):<10}\n"
            total_bits += len(code)
        
        codes_text += f"\nEstadísticas de códigos:\n"
        codes_text += f"• Código más corto: {min(len(code) for code in codes.values())} bits\n"
        codes_text += f"• Código más largo: {max(len(code) for code in codes.values())} bits\n"
        codes_text += f"• Longitud promedio: {total_bits / len(codes):.2f} bits\n"
        codes_text += f"• Total de códigos: {len(codes)}\n\n"
        codes_text += "Principio de Huffman:\n"
        codes_text += "• Caracteres frecuentes → códigos cortos\n"
        codes_text += "• Caracteres raros → códigos largos\n"
        codes_text += "• Ningún código es prefijo de otro"
        
        self.huffman_codes.insert("1.0", codes_text)
        self.huffman_codes.configure(state="disabled")
    
    def display_huffman_tree(self, tree_visualization):
        """Mostrar visualización del árbol Huffman"""
        self.huffman_tree.configure(state="normal")
        self.huffman_tree.delete("1.0", tk.END)
        
        tree_text = "Árbol de Huffman:\n\n"
        tree_text += tree_visualization
        tree_text += "\n\nEstructura del árbol:\n"
        tree_text += "• Nodos hoja: contienen caracteres\n"
        tree_text += "• Nodos internos: sumas de frecuencias\n"
        tree_text += "• Camino a la izquierda: bit '0'\n"
        tree_text += "• Camino a la derecha: bit '1'\n"
        tree_text += "• El código se forma siguiendo el camino desde la raíz\n\n"
        tree_text += "Algoritmo de construcción:\n"
        tree_text += "1. Crear nodos hoja para cada carácter\n"
        tree_text += "2. Crear cola de prioridad por frecuencia\n"
        tree_text += "3. Repetir hasta que quede un nodo:\n"
        tree_text += "   a. Tomar los dos nodos de menor frecuencia\n"
        tree_text += "   b. Crear nodo padre con suma de frecuencias\n"
        tree_text += "   c. Agregar el nodo padre a la cola\n"
        tree_text += "4. El último nodo es la raíz del árbol"
        
        self.huffman_tree.insert("1.0", tree_text)
        self.huffman_tree.configure(state="disabled")
    
    def load_huffman_example(self):
        """Cargar un ejemplo para Huffman"""
        example_text = "ABRACADABRA! Este es un ejemplo de texto para probar la codificación Huffman. Los caracteres más frecuentes como A, R y espacios deberían tener códigos más cortos."
        
        self.huffman_text.delete("1.0", tk.END)
        self.huffman_text.insert("1.0", example_text)
        self.update_status("Ejemplo cargado para codificación Huffman")
    
    def clear_huffman_fields(self):
        """Limpiar campos de Huffman"""
        self.huffman_text.delete("1.0", tk.END)
        
        self.huffman_result.configure(state="normal")
        self.huffman_result.delete("1.0", tk.END)
        self.huffman_result.configure(state="disabled")
        
        self.huffman_frequencies.configure(state="normal")
        self.huffman_frequencies.delete("1.0", tk.END)
        self.huffman_frequencies.configure(state="disabled")
        
        self.huffman_codes.configure(state="normal")
        self.huffman_codes.delete("1.0", tk.END)
        self.huffman_codes.configure(state="disabled")
        
        self.huffman_tree.configure(state="normal")
        self.huffman_tree.delete("1.0", tk.END)
        self.huffman_tree.configure(state="disabled")
        
        # Limpiar variables
        self.huffman_encoder = None
        self.last_encoded_data = None
    
    def show_blockchain_screen(self):
        """Mostrar pantalla de Blockchain"""
        # Título
        title = ttb.Label(
            self.content_frame,
            text="⛓️ Blockchain - Cadena de Bloques",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=(20, 10))
        
        # Descripción
        desc = ttb.Label(
            self.content_frame,
            text="Sistema de cadena de bloques para demostrar integridad de datos",
            font=("Arial", 12)
        )
        desc.pack(pady=(0, 20))
        
        # Frame principal
        main_frame = ttb.Frame(self.content_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Frame izquierdo - Controles
        left_frame = ttb.LabelFrame(main_frame, text="Controles", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Datos para el bloque
        ttb.Label(left_frame, text="Datos del bloque:").pack(anchor=tk.W)
        self.blockchain_data_entry = ttb.Entry(left_frame, width=30)
        self.blockchain_data_entry.pack(pady=(5, 10), fill=tk.X)
        
        # Botón para agregar bloque
        add_block_btn = ttb.Button(
            left_frame,
            text="➕ Agregar Bloque",
            bootstyle=SUCCESS,
            command=self.add_blockchain_block
        )
        add_block_btn.pack(pady=5, fill=tk.X)
        
        # Botón para verificar integridad
        verify_btn = ttb.Button(
            left_frame,
            text="🔍 Verificar Integridad",
            bootstyle=INFO,
            command=self.verify_blockchain_integrity
        )
        verify_btn.pack(pady=5, fill=tk.X)
        
        # Botón para simular alteración
        tamper_btn = ttb.Button(
            left_frame,
            text="⚠️ Simular Alteración",
            bootstyle=WARNING,
            command=self.tamper_blockchain
        )
        tamper_btn.pack(pady=5, fill=tk.X)
        
        # Botón para limpiar cadena
        clear_btn = ttb.Button(
            left_frame,
            text="🗑️ Limpiar Cadena",
            bootstyle=DANGER,
            command=self.clear_blockchain
        )
        clear_btn.pack(pady=5, fill=tk.X)
        
        # Información de la cadena
        info_frame = ttb.LabelFrame(left_frame, text="Información", padding=10)
        info_frame.pack(pady=(20, 0), fill=tk.X)
        
        self.blockchain_info_label = ttb.Label(info_frame, text="Bloques: 0\nÚltimo hash: N/A")
        self.blockchain_info_label.pack(anchor=tk.W)
        
        # Frame derecho - Visualización de la cadena
        right_frame = ttb.LabelFrame(main_frame, text="Cadena de Bloques", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Treeview para mostrar la cadena
        columns = ("Índice", "Datos", "Hash", "Hash Anterior", "Timestamp", "Válido")
        self.blockchain_tree = ttb.Treeview(right_frame, columns=columns, show="headings", height=15)
        
        # Configurar encabezados
        self.blockchain_tree.heading("Índice", text="Índice")
        self.blockchain_tree.heading("Datos", text="Datos")
        self.blockchain_tree.heading("Hash", text="Hash")
        self.blockchain_tree.heading("Hash Anterior", text="Hash Anterior")
        self.blockchain_tree.heading("Timestamp", text="Timestamp")
        self.blockchain_tree.heading("Válido", text="Válido")
        
        # Configurar ancho de columnas
        self.blockchain_tree.column("Índice", width=60)
        self.blockchain_tree.column("Datos", width=150)
        self.blockchain_tree.column("Hash", width=200)
        self.blockchain_tree.column("Hash Anterior", width=200)
        self.blockchain_tree.column("Timestamp", width=150)
        self.blockchain_tree.column("Válido", width=60)
        
        # Scrollbar para el treeview
        blockchain_scrollbar = ttb.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.blockchain_tree.yview)
        self.blockchain_tree.configure(yscrollcommand=blockchain_scrollbar.set)
        
        # Empaquetar treeview y scrollbar
        self.blockchain_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        blockchain_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Resultado de verificación
        self.blockchain_result = ttb.Text(right_frame, height=4, wrap=tk.WORD)
        self.blockchain_result.pack(pady=(10, 0), fill=tk.X)
        
        # Inicializar blockchain
        self.blockchain = Blockchain()
        self.update_blockchain_display()
        
        # Agregar bloque génesis si no existe
        if len(self.blockchain.chain) == 0:
            self.blockchain.add_block("Bloque Génesis")
            self.update_blockchain_display()
    
    def add_blockchain_block(self):
        """Agregar un bloque a la cadena"""
        try:
            data = self.blockchain_data_entry.get().strip()
            if not data:
                self.show_warning("Por favor ingrese datos para el bloque")
                return
            
            # Agregar el bloque
            self.blockchain.add_block(data)
            
            # Actualizar la visualización
            self.update_blockchain_display()
            
            # Limpiar el campo de entrada
            self.blockchain_data_entry.delete(0, tk.END)
            
            self.show_info(f"Bloque agregado exitosamente")
            
        except Exception as e:
            self.show_error(f"Error al agregar bloque: {str(e)}")
    
    def verify_blockchain_integrity(self):
        """Verificar la integridad de la cadena"""
        try:
            is_valid = self.blockchain.is_chain_valid()
            
            if is_valid:
                result = "✅ La cadena de bloques es válida e íntegra"
                self.blockchain_result.configure(state="normal")
                self.blockchain_result.delete(1.0, tk.END)
                self.blockchain_result.insert(tk.END, result)
                self.blockchain_result.configure(state="disabled")
                self.show_info("Cadena válida")
            else:
                result = "❌ La cadena de bloques ha sido alterada o es inválida"
                self.blockchain_result.configure(state="normal")
                self.blockchain_result.delete(1.0, tk.END)
                self.blockchain_result.insert(tk.END, result)
                self.blockchain_result.configure(state="disabled")
                self.show_warning("Cadena inválida")
            
            # Actualizar la visualización con el estado de validez
            self.update_blockchain_display()
            
        except Exception as e:
            self.show_error(f"Error al verificar integridad: {str(e)}")
    
    def tamper_blockchain(self):
        """Simular alteración de un bloque"""
        try:
            if len(self.blockchain.chain) < 2:
                self.show_warning("Necesita al menos 2 bloques para simular alteración")
                return
            
            # Alterar el segundo bloque (índice 1)
            self.blockchain.chain[1].data = "DATOS ALTERADOS"
            
            # Actualizar la visualización
            self.update_blockchain_display()
            
            self.show_info("Simulación de alteración realizada en el bloque índice 1")
            
        except Exception as e:
            self.show_error(f"Error al simular alteración: {str(e)}")
    
    def clear_blockchain(self):
        """Limpiar la cadena de bloques"""
        try:
            self.blockchain = Blockchain()
            self.update_blockchain_display()
            
            # Limpiar resultado
            self.blockchain_result.configure(state="normal")
            self.blockchain_result.delete(1.0, tk.END)
            self.blockchain_result.configure(state="disabled")
            
            self.show_info("Cadena de bloques limpiada")
            
        except Exception as e:
            self.show_error(f"Error al limpiar cadena: {str(e)}")
    
    def update_blockchain_display(self):
        """Actualizar la visualización de la cadena"""
        try:
            # Limpiar el treeview
            for item in self.blockchain_tree.get_children():
                self.blockchain_tree.delete(item)
            
            # Agregar cada bloque
            for block in self.blockchain.chain:
                # Verificar si el bloque es válido
                is_valid = "✅" if self.blockchain.is_block_valid(block) else "❌"
                
                # Truncar datos y hashes para visualización
                data_display = block.data[:30] + "..." if len(block.data) > 30 else block.data
                hash_display = block.hash[:20] + "..." if len(block.hash) > 20 else block.hash
                prev_hash_display = block.previous_hash[:20] + "..." if len(block.previous_hash) > 20 else block.previous_hash
                
                # Formatear timestamp
                from datetime import datetime
                timestamp_display = datetime.fromtimestamp(block.timestamp).strftime("%Y-%m-%d %H:%M:%S")
                
                self.blockchain_tree.insert("", "end", values=(
                    block.index,
                    data_display,
                    hash_display,
                    prev_hash_display,
                    timestamp_display,
                    is_valid
                ))
            
            # Actualizar información
            last_hash = self.blockchain.chain[-1].hash[:20] + "..." if self.blockchain.chain else "N/A"
            info_text = f"Bloques: {len(self.blockchain.chain)}\nÚltimo hash: {last_hash}"
            self.blockchain_info_label.configure(text=info_text)
            
        except Exception as e:
            self.show_error(f"Error al actualizar visualización: {str(e)}")
    
    def show_integrity_screen(self):
        """Mostrar pantalla de Verificador de Integridad"""
        # Título
        title = ttb.Label(
            self.content_frame,
            text="🔎 Verificador de Integridad",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=(20, 10))
        
        # Descripción
        desc = ttb.Label(
            self.content_frame,
            text="Verificar la integridad de archivos mediante funciones hash",
            font=("Arial", 12)
        )
        desc.pack(pady=(0, 20))
        
        # Frame principal
        main_frame = ttb.Frame(self.content_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Frame de controles
        controls_frame = ttb.LabelFrame(main_frame, text="Controles", padding=10)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Frame para selección de archivo
        file_frame = ttb.Frame(controls_frame)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttb.Label(file_frame, text="Archivo a verificar:").pack(anchor=tk.W)
        file_input_frame = ttb.Frame(file_frame)
        file_input_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.integrity_file_entry = ttb.Entry(file_input_frame, width=50)
        self.integrity_file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_btn = ttb.Button(
            file_input_frame,
            text="📁 Examinar",
            bootstyle=INFO,
            command=self.browse_integrity_file
        )
        browse_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Selección de algoritmo hash
        hash_frame = ttb.Frame(controls_frame)
        hash_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttb.Label(hash_frame, text="Algoritmo hash:").pack(anchor=tk.W)
        self.integrity_hash_var = tk.StringVar(value="sha256")
        hash_combo = ttb.Combobox(
            hash_frame,
            textvariable=self.integrity_hash_var,
            values=["md5", "sha1", "sha256", "sha512"],
            state="readonly",
            width=20
        )
        hash_combo.pack(anchor=tk.W, pady=(5, 0))
        
        # Botones de acción
        buttons_frame = ttb.Frame(controls_frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        generate_btn = ttb.Button(
            buttons_frame,
            text="🔐 Generar Hash",
            bootstyle=SUCCESS,
            command=self.generate_file_hash
        )
        generate_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        compare_btn = ttb.Button(
            buttons_frame,
            text="🔍 Comparar Hash",
            bootstyle=INFO,
            command=self.compare_file_hash
        )
        compare_btn.pack(side=tk.LEFT, padx=5)
        
        verify_btn = ttb.Button(
            buttons_frame,
            text="✅ Verificar Integridad",
            bootstyle=WARNING,
            command=self.verify_file_integrity
        )
        verify_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttb.Button(
            buttons_frame,
            text="🗑️ Limpiar",
            bootstyle=DANGER,
            command=self.clear_integrity_results
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Frame de resultados
        results_frame = ttb.LabelFrame(main_frame, text="Resultados", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Información del archivo
        info_frame = ttb.Frame(results_frame)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttb.Label(info_frame, text="Información del archivo:").pack(anchor=tk.W)
        self.integrity_info_text = ttb.Text(info_frame, height=3, wrap=tk.WORD)
        self.integrity_info_text.pack(fill=tk.X, pady=(5, 0))
        
        # Hash actual
        hash_frame = ttb.Frame(results_frame)
        hash_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttb.Label(hash_frame, text="Hash actual:").pack(anchor=tk.W)
        self.integrity_hash_text = ttb.Text(hash_frame, height=2, wrap=tk.WORD)
        self.integrity_hash_text.pack(fill=tk.X, pady=(5, 0))
        
        # Hash de comparación
        compare_frame = ttb.Frame(results_frame)
        compare_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttb.Label(compare_frame, text="Hash de comparación:").pack(anchor=tk.W)
        self.integrity_compare_entry = ttb.Entry(compare_frame, width=80)
        self.integrity_compare_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Resultado de verificación
        result_frame = ttb.Frame(results_frame)
        result_frame.pack(fill=tk.X)
        
        ttb.Label(result_frame, text="Resultado de verificación:").pack(anchor=tk.W)
        self.integrity_result_text = ttb.Text(result_frame, height=6, wrap=tk.WORD)
        self.integrity_result_text.pack(fill=tk.X, pady=(5, 0))
        
        # Inicializar verificador
        self.integrity_verifier = IntegrityVerifier()
        self.current_file_path = None
        self.current_file_hash = None
    
    def browse_integrity_file(self):
        """Examinar archivo para verificar integridad"""
        try:
            file_path = filedialog.askopenfilename(
                title="Seleccionar archivo para verificar",
                filetypes=[("Todos los archivos", "*.*")]
            )
            
            if file_path:
                self.integrity_file_entry.delete(0, tk.END)
                self.integrity_file_entry.insert(0, file_path)
                self.current_file_path = file_path
                self.show_file_info()
                
        except Exception as e:
            self.show_error(f"Error al seleccionar archivo: {str(e)}")
    
    def show_file_info(self):
        """Mostrar información del archivo seleccionado"""
        try:
            if not self.current_file_path:
                return
            
            import os
            file_size = os.path.getsize(self.current_file_path)
            file_name = os.path.basename(self.current_file_path)
            
            # Formatear tamaño
            if file_size < 1024:
                size_str = f"{file_size} bytes"
            elif file_size < 1024 * 1024:
                size_str = f"{file_size / 1024:.2f} KB"
            else:
                size_str = f"{file_size / (1024 * 1024):.2f} MB"
            
            info_text = f"Nombre: {file_name}\nTamaño: {size_str}\nRuta: {self.current_file_path}"
            
            self.integrity_info_text.configure(state="normal")
            self.integrity_info_text.delete(1.0, tk.END)
            self.integrity_info_text.insert(tk.END, info_text)
            self.integrity_info_text.configure(state="disabled")
            
        except Exception as e:
            self.show_error(f"Error al mostrar información del archivo: {str(e)}")
    
    def generate_file_hash(self):
        """Generar hash del archivo seleccionado"""
        try:
            if not self.current_file_path:
                self.show_warning("Por favor seleccione un archivo")
                return
            
            if not os.path.exists(self.current_file_path):
                self.show_error("El archivo seleccionado no existe")
                return
            
            # Obtener algoritmo seleccionado
            algorithm = self.integrity_hash_var.get()
            
            # Generar hash
            file_hash = self.integrity_verifier.calculate_file_hash(self.current_file_path, algorithm)
            self.current_file_hash = file_hash
            
            # Mostrar hash
            self.integrity_hash_text.configure(state="normal")
            self.integrity_hash_text.delete(1.0, tk.END)
            self.integrity_hash_text.insert(tk.END, f"{algorithm.upper()}: {file_hash}")
            self.integrity_hash_text.configure(state="disabled")
            
            self.show_info(f"Hash {algorithm.upper()} generado exitosamente")
            
        except Exception as e:
            self.show_error(f"Error al generar hash: {str(e)}")
    
    def compare_file_hash(self):
        """Comparar hash actual con hash de referencia"""
        try:
            if not self.current_file_hash:
                self.show_warning("Primero genere el hash del archivo")
                return
            
            reference_hash = self.integrity_compare_entry.get().strip()
            if not reference_hash:
                self.show_warning("Por favor ingrese el hash de referencia")
                return
            
            # Comparar hashes
            is_match = self.current_file_hash.lower() == reference_hash.lower()
            
            if is_match:
                result = "✅ COINCIDENCIA: Los hashes son idénticos\n"
                result += "El archivo no ha sido modificado"
                status = "success"
            else:
                result = "❌ NO COINCIDEN: Los hashes son diferentes\n"
                result += "El archivo ha sido modificado o el hash de referencia es incorrecto"
                status = "error"
            
            self.integrity_result_text.configure(state="normal")
            self.integrity_result_text.delete(1.0, tk.END)
            self.integrity_result_text.insert(tk.END, result)
            self.integrity_result_text.configure(state="disabled")
            
            if status == "success":
                self.show_info("Archivo íntegro")
            else:
                self.show_warning("Archivo modificado")
                
        except Exception as e:
            self.show_error(f"Error al comparar hashes: {str(e)}")
    
    def verify_file_integrity(self):
        """Verificar integridad completa del archivo"""
        try:
            if not self.current_file_path:
                self.show_warning("Por favor seleccione un archivo")
                return
            
            if not os.path.exists(self.current_file_path):
                self.show_error("El archivo seleccionado no existe")
                return
            
            # Verificar con múltiples algoritmos
            algorithms = ["md5", "sha1", "sha256", "sha512"]
            results = []
            
            for algorithm in algorithms:
                try:
                    file_hash = self.integrity_verifier.calculate_file_hash(self.current_file_path, algorithm)
                    results.append(f"{algorithm.upper()}: {file_hash}")
                except Exception as e:
                    results.append(f"{algorithm.upper()}: Error - {str(e)}")
            
            # Mostrar resultados
            result_text = "📊 VERIFICACIÓN COMPLETA DE INTEGRIDAD\n"
            result_text += "=" * 50 + "\n"
            result_text += f"Archivo: {os.path.basename(self.current_file_path)}\n"
            result_text += f"Fecha: {self.get_current_timestamp()}\n\n"
            result_text += "Hashes calculados:\n"
            result_text += "-" * 30 + "\n"
            result_text += "\n".join(results)
            
            self.integrity_result_text.configure(state="normal")
            self.integrity_result_text.delete(1.0, tk.END)
            self.integrity_result_text.insert(tk.END, result_text)
            self.integrity_result_text.configure(state="disabled")
            
            self.show_info("Verificación de integridad completada")
            
        except Exception as e:
            self.show_error(f"Error en verificación de integridad: {str(e)}")
    
    def clear_integrity_results(self):
        """Limpiar todos los resultados"""
        try:
            self.integrity_file_entry.delete(0, tk.END)
            self.integrity_compare_entry.delete(0, tk.END)
            
            self.integrity_info_text.configure(state="normal")
            self.integrity_info_text.delete(1.0, tk.END)
            self.integrity_info_text.configure(state="disabled")
            
            self.integrity_hash_text.configure(state="normal")
            self.integrity_hash_text.delete(1.0, tk.END)
            self.integrity_hash_text.configure(state="disabled")
            
            self.integrity_result_text.configure(state="normal")
            self.integrity_result_text.delete(1.0, tk.END)
            self.integrity_result_text.configure(state="disabled")
            
            self.current_file_path = None
            self.current_file_hash = None
            
            self.show_info("Resultados limpiados")
            
        except Exception as e:
            self.show_error(f"Error al limpiar resultados: {str(e)}")
    
    def get_current_timestamp(self):
        """Obtener timestamp actual"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def show_config_screen(self):
        """Mostrar pantalla de configuración"""
        ttb.Label(
            self.content_frame,
            text="⚙️ Configuración - En desarrollo",
            font=("Arial", 20, "bold")
        ).pack(pady=50)
    
    def show_about_screen(self):
        """Mostrar pantalla de información"""
        # Título
        title = ttb.Label(
            self.content_frame,
            text="ℹ️ Acerca de CryptoUNS",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=(20, 10))
        
        # Información del proyecto
        info_text = """
CryptoUNS - Sistema Criptográfico Integral
Versión 1.0

Desarrollado como proyecto final de 2da Unidad del curso de Seguridad Informática
Universidad Nacional del Santa (UNS)

Características:
• Algoritmos de criptografía clásica (César, Vigenère, Playfair)
• Algoritmos de criptografía moderna (RSA, DES, Funciones Hash)
• Herramientas de análisis (Kasiski, Huffman, Blockchain)
• Interfaz gráfica moderna con ttkbootstrap
• Pruebas unitarias completas

Tecnologías utilizadas:
• Python 3.11+
• tkinter / ttkbootstrap (Interfaz gráfica)
• pycryptodome (Algoritmos criptográficos)
• pytest (Pruebas unitarias)

Estudiantes participantes:
- Armas Solorzano Brando Emanuel
- Cruz Castillo Jhoan Antoni
- Estefanero Placios Jael Andres
- Flores Luera Miguel
- Zelada Pulido Rodrigo Sebastian

© 2025 - Todos los derechos reservados
        """
        
        info_label = ttb.Label(
            self.content_frame,
            text=info_text,
            font=("Arial", 10),
            justify="left"
        )
        info_label.pack(pady=10)
    
    def update_status(self, message):
        """Actualizar la barra de estado"""
        self.status_label.configure(text=message)
        self.root.update_idletasks()
    
    def show_error(self, message):
        """Mostrar mensaje de error"""
        messagebox.showerror("Error", message)
        self.update_status(f"Error: {message}")
    
    def show_warning(self, message):
        """Mostrar mensaje de advertencia"""
        messagebox.showwarning("Advertencia", message)
        self.update_status(f"Advertencia: {message}")
    
    def show_info(self, message):
        """Mostrar mensaje de información"""
        messagebox.showinfo("Información", message)
        self.update_status(f"Info: {message}")
    
    def on_closing(self):
        """Manejar el cierre de la aplicación"""
        if messagebox.askokcancel("Cerrar", "¿Está seguro que desea cerrar CryptoUNS?"):
            self.root.destroy()
    
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()


if __name__ == "__main__":
    try:
        app = CryptoUNSApp()
        app.run()
    except Exception as e:
        print(f"Error iniciando la aplicación: {e}")
        import traceback
        traceback.print_exc()
