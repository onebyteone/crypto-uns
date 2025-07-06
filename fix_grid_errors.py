#!/usr/bin/env python3
"""Script para corregir errores de grid en main_window.py"""

def fix_grid_errors():
    file_path = 'src/gui/main_window.py'
    
    # Leer el archivo
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Líneas específicas que necesitan corrección (basado en grep)
    lines_to_fix = [348, 508, 747, 969, 1219, 1517, 1762, 2053, 2407]
    
    # Hacer las correcciones
    corrected_count = 0
    for line_num in lines_to_fix:
        if line_num <= len(lines):
            # Convertir a índice 0-based
            idx = line_num - 1
            
            # Verificar si la línea contiene el error
            if 'main_frame.grid(row=2, column=0, sticky="nsew", fill="both", expand=True)' in lines[idx]:
                lines[idx] = lines[idx].replace(
                    'main_frame.grid(row=2, column=0, sticky="nsew", fill="both", expand=True)',
                    'main_frame.grid(row=2, column=0, sticky="nsew")'
                )
                corrected_count += 1
                print(f"Corregida línea {line_num}")
    
    # Escribir el archivo corregido
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"Total de líneas corregidas: {corrected_count}")
    return corrected_count

if __name__ == "__main__":
    fix_grid_errors()
