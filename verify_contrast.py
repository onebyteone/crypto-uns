#!/usr/bin/env python3
"""
Script para verificar la mejora de contraste en la pantalla de Firma Digital.
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_contrast_values():
    """
    Verificar que los valores de contraste están configurados correctamente.
    """
    try:
        # Valores de contraste esperados
        expected_values = {
            'valid_bg': '#d4edda',
            'valid_fg': '#155724',
            'invalid_bg': '#f8d7da',
            'invalid_fg': '#721c24',
            'normal_bg': 'white',
            'normal_fg': 'black'
        }
        
        print("🎨 Verificando valores de contraste en Firma Digital...")
        
        # Leer el archivo de la GUI
        gui_file = os.path.join('src', 'gui', 'main_window.py')
        with open(gui_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar que los valores de contraste están presentes
        checks = [
            ('Fondo válido', expected_values['valid_bg'] in content),
            ('Texto válido', expected_values['valid_fg'] in content),
            ('Fondo inválido', expected_values['invalid_bg'] in content),
            ('Texto inválido', expected_values['invalid_fg'] in content),
            ('Fondo normal', 'bg="white", fg="black"' in content)
        ]
        
        print("\n📋 Resultados de verificación:")
        all_passed = True
        
        for check_name, result in checks:
            status = "✅" if result else "❌"
            print(f"  {status} {check_name}: {'CORRECTO' if result else 'FALTANTE'}")
            if not result:
                all_passed = False
        
        if all_passed:
            print("\n🎊 ¡Todos los valores de contraste están configurados correctamente!")
            return True
        else:
            print("\n⚠️  Algunos valores de contraste no están configurados correctamente.")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la verificación: {str(e)}")
        return False

def test_color_contrast_ratios():
    """
    Verificar que los ratios de contraste cumplen con WCAG 2.1 AA.
    """
    print("\n🔍 Verificando ratios de contraste (WCAG 2.1 AA)...")
    
    # Función para calcular luminancia
    def get_luminance(hex_color):
        """Calcular luminancia de un color hex"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Convertir a valores sRGB
        r, g, b = r/255.0, g/255.0, b/255.0
        
        # Aplicar función gamma
        def gamma_correct(c):
            if c <= 0.03928:
                return c / 12.92
            else:
                return ((c + 0.055) / 1.055) ** 2.4
        
        r, g, b = gamma_correct(r), gamma_correct(g), gamma_correct(b)
        
        # Calcular luminancia
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    # Función para calcular ratio de contraste
    def contrast_ratio(color1, color2):
        """Calcular ratio de contraste entre dos colores"""
        l1 = get_luminance(color1)
        l2 = get_luminance(color2)
        
        # Asegurar que l1 es el más brillante
        if l1 < l2:
            l1, l2 = l2, l1
        
        return (l1 + 0.05) / (l2 + 0.05)
    
    # Verificar contrastes
    contrasts = [
        ("Firma válida", "#d4edda", "#155724"),
        ("Firma inválida", "#f8d7da", "#721c24"),
        ("Estado normal", "white", "black")
    ]
    
    print("\n📊 Ratios de contraste:")
    all_compliant = True
    
    for name, bg, fg in contrasts:
        # Convertir colores nombrados
        if bg == "white":
            bg = "#ffffff"
        if fg == "black":
            fg = "#000000"
        
        ratio = contrast_ratio(bg, fg)
        compliant = ratio >= 4.5  # WCAG 2.1 AA estándar
        
        status = "✅" if compliant else "❌"
        compliance = "WCAG AA" if compliant else "NO CUMPLE"
        
        print(f"  {status} {name}: {ratio:.2f}:1 ({compliance})")
        
        if not compliant:
            all_compliant = False
    
    if all_compliant:
        print("\n🎊 ¡Todos los contrastes cumplen con WCAG 2.1 AA!")
        return True
    else:
        print("\n⚠️  Algunos contrastes no cumplen con WCAG 2.1 AA.")
        return False

def main():
    """Función principal de verificación"""
    print("🔍 VERIFICADOR DE CONTRASTE - FIRMA DIGITAL")
    print("=" * 50)
    
    # Verificar valores de contraste
    values_ok = test_contrast_values()
    
    # Verificar ratios de contraste
    ratios_ok = test_color_contrast_ratios()
    
    # Resultado final
    print("\n" + "=" * 50)
    if values_ok and ratios_ok:
        print("🎊 ¡VERIFICACIÓN EXITOSA! El contraste ha sido corregido correctamente.")
        print("   ✅ Valores de contraste configurados")
        print("   ✅ Ratios de contraste cumplen WCAG 2.1 AA")
        print("   ✅ Accesibilidad mejorada")
        return True
    else:
        print("❌ VERIFICACIÓN FALLIDA. Hay problemas con el contraste.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
