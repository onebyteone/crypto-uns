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
        
        # Actualizar el botón activo
        for key, btn in self.nav_buttons.items():
            if key == screen:
                btn.configure(bootstyle=f"{btn.cget('bootstyle')}-outline")
            else:
                style = btn.cget('bootstyle').replace('-outline', '')
                btn.configure(bootstyle=style)
        
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
        main_frame.grid(row=2, column=0, sticky="nsew", fill="both", expand=True)
        
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
        main_frame.grid(row=2, column=0, sticky="nsew", fill="both", expand=True)
        
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
                analysis_text += f"'{rep['pattern']}' - Distancias: {rep['distances']}\n"
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
        main_frame.grid(row=2, column=0, sticky="nsew", fill="both", expand=True)
        
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
            
            matrix = self.playfair.generate_matrix(key)
            
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
        main_frame.grid(row=2, column=0, sticky="nsew", fill="both", expand=True)
        
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
            for factor, count in analysis['factors'].most_common(10):
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
                results_text += f"  Patrón más frecuente: '{most_frequent['pattern']}' ({len(most_frequent['positions'])} veces)\n"
                
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
            pattern = pattern_data['pattern']
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
        main_frame.grid(row=2, column=0, sticky="nsew", fill="both", expand=True)
        
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
        
        # Variables para almacenar las claves
        self.current_public_key = None
        self.current_private_key = None
        
        # Generar claves iniciales
        self.generate_rsa_keys()
    
    def generate_rsa_keys(self):
        """Generar par de claves RSA"""
        try:
            key_size = int(self.rsa_key_size.get())
            self.update_status(f"Generando claves RSA de {key_size} bits...")
            
            # Generar claves
            keys = self.rsa.generate_keys(key_size)
            self.current_public_key = keys['public_key']
            self.current_private_key = keys['private_key']
            
            # Mostrar clave pública
            self.rsa_public_key.configure(state="normal")
            self.rsa_public_key.delete("1.0", tk.END)
            public_text = f"Clave Pública (n, e):\n\n"
            public_text += f"n = {keys['public_key']['n']}\n\n"
            public_text += f"e = {keys['public_key']['e']}\n\n"
            public_text += f"Tamaño: {key_size} bits\n"
            public_text += f"Longitud de n: {len(str(keys['public_key']['n']))} dígitos"
            self.rsa_public_key.insert("1.0", public_text)
            self.rsa_public_key.configure(state="disabled")
            
            # Mostrar clave privada
            self.rsa_private_key.configure(state="normal")
            self.rsa_private_key.delete("1.0", tk.END)
            private_text = f"Clave Privada (n, d):\n\n"
            private_text += f"n = {keys['private_key']['n']}\n\n"
            private_text += f"d = {keys['private_key']['d']}\n\n"
            private_text += f"Tamaño: {key_size} bits\n"
            private_text += f"Longitud de d: {len(str(keys['private_key']['d']))} dígitos"
            self.rsa_private_key.insert("1.0", private_text)
            self.rsa_private_key.configure(state="disabled")
            
            # Mostrar información adicional
            self.rsa_info.configure(state="normal")
            self.rsa_info.delete("1.0", tk.END)
            info_text = f"Información de Generación RSA:\n\n"
            info_text += f"Primos utilizados:\n"
            info_text += f"p = {keys['p']}\n"
            info_text += f"q = {keys['q']}\n\n"
            info_text += f"Cálculos:\n"
            info_text += f"n = p × q = {keys['public_key']['n']}\n"
            info_text += f"φ(n) = (p-1) × (q-1) = {keys['phi_n']}\n"
            info_text += f"e = {keys['public_key']['e']} (exponente público)\n"
            info_text += f"d = {keys['private_key']['d']} (exponente privado)\n\n"
            info_text += f"Verificación: (e × d) mod φ(n) = {(keys['public_key']['e'] * keys['private_key']['d']) % keys['phi_n']}\n\n"
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
            
            # Mostrar resultado
            self.rsa_result.configure(state="normal")
            self.rsa_result.delete("1.0", tk.END)
            
            result_text = f"Mensaje Cifrado:\n\n"
            result_text += f"Texto original: {message}\n\n"
            result_text += f"Texto cifrado (números):\n"
            result_text += f"{encrypted}\n\n"
            result_text += f"Longitud: {len(str(encrypted))} dígitos\n\n"
            result_text += f"Proceso:\n"
            result_text += f"• Texto convertido a números\n"
            result_text += f"• Aplicado: c = m^e mod n\n"
            result_text += f"• e = {self.current_public_key['e']}\n"
            result_text += f"• n = {self.current_public_key['n']}"
            
            self.rsa_result.insert("1.0", result_text)
            self.rsa_result.configure(state="disabled")
            
            self.update_status("Mensaje cifrado con RSA exitosamente")
            
        except Exception as e:
            self.show_error(f"Error al cifrar con RSA: {str(e)}")
    
    def rsa_decrypt(self):
        """Descifrar mensaje con RSA"""
        try:
            # Obtener el resultado cifrado actual
            current_result = self.rsa_result.get("1.0", tk.END).strip()
            
            if not current_result or "Texto cifrado (números):" not in current_result:
                self.show_warning("Primero cifre un mensaje para poder descifrarlo")
                return
            
            if not self.current_private_key:
                self.show_warning("Por favor genere las claves RSA primero")
                return
            
            # Extraer el número cifrado del resultado
            lines = current_result.split('\n')
            encrypted_number = None
            for i, line in enumerate(lines):
                if "Texto cifrado (números):" in line and i + 1 < len(lines):
                    try:
                        encrypted_number = int(lines[i + 1].strip())
                        break
                    except ValueError:
                        continue
            
            if encrypted_number is None:
                self.show_warning("No se encontró un mensaje cifrado válido")
                return
            
            # Descifrar mensaje
            decrypted = self.rsa.decrypt(encrypted_number, self.current_private_key)
            
            # Mostrar resultado
            self.rsa_result.configure(state="normal")
            self.rsa_result.delete("1.0", tk.END)
            
            result_text = f"Mensaje Descifrado:\n\n"
            result_text += f"Número cifrado: {encrypted_number}\n\n"
            result_text += f"Texto descifrado: {decrypted}\n\n"
            result_text += f"Proceso:\n"
            result_text += f"• Aplicado: m = c^d mod n\n"
            result_text += f"• d = {self.current_private_key['d']}\n"
            result_text += f"• n = {self.current_private_key['n']}\n"
            result_text += f"• Números convertidos a texto\n\n"
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
        
        # Limpiar claves almacenadas
        self.current_public_key = None
        self.current_private_key = None
    
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
        main_frame.grid(row=2, column=0, sticky="nsew", fill="both", expand=True)
        
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
        """Mostrar pantalla de DES (implementar después)"""
        ttb.Label(
            self.content_frame,
            text="🔏 DES - En desarrollo",
            font=("Arial", 20, "bold")
        ).pack(pady=50)
    
    def show_signature_screen(self):
        """Mostrar pantalla de Firma Digital (implementar después)"""
        ttb.Label(
            self.content_frame,
            text="✍️ Firma Digital - En desarrollo",
            font=("Arial", 20, "bold")
        ).pack(pady=50)
    
    def show_huffman_screen(self):
        """Mostrar pantalla de Huffman (implementar después)"""
        ttb.Label(
            self.content_frame,
            text="📊 Codificación Huffman - En desarrollo",
            font=("Arial", 20, "bold")
        ).pack(pady=50)
    
    def show_blockchain_screen(self):
        """Mostrar pantalla de Blockchain (implementar después)"""
        ttb.Label(
            self.content_frame,
            text="⛓️ Blockchain - En desarrollo",
            font=("Arial", 20, "bold")
        ).pack(pady=50)
    
    def show_integrity_screen(self):
        """Mostrar pantalla de Integridad (implementar después)"""
        ttb.Label(
            self.content_frame,
            text="🔎 Verificador de Integridad - En desarrollo",
            font=("Arial", 20, "bold")
        ).pack(pady=50)
    
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

Desarrollado como proyecto final de criptografía
Universidad Nacional del Sur (UNS)

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
