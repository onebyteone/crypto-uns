#!/usr/bin/env python3
"""
Script de limpieza automática para el proyecto CryptoUNS
Elimina archivos temporales, cache y otros archivos innecesarios
"""

import os
import shutil
import glob
from pathlib import Path

def clean_project():
    """
    Limpia el proyecto eliminando archivos temporales y cache
    """
    project_root = Path(__file__).parent
    
    print("🧹 Iniciando limpieza del proyecto CryptoUNS...")
    
    # Patrones de archivos a eliminar
    patterns_to_remove = [
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/*.pyd",
        "**/.pytest_cache",
        "**/build",
        "**/dist",
        "**/*.egg-info",
        "**/.coverage",
        "**/htmlcov",
        "**/.tox",
        "**/.cache",
        "**/temp_*",
        "**/*.tmp",
        "**/*.temp",
        "**/test_file.txt"
    ]
    
    files_removed = 0
    dirs_removed = 0
    
    # Eliminar archivos y directorios según patrones
    for pattern in patterns_to_remove:
        matches = glob.glob(str(project_root / pattern), recursive=True)
        for match in matches:
            path = Path(match)
            try:
                if path.is_file():
                    path.unlink()
                    files_removed += 1
                    print(f"  ❌ Eliminado archivo: {path.relative_to(project_root)}")
                elif path.is_dir():
                    shutil.rmtree(path)
                    dirs_removed += 1
                    print(f"  🗂️ Eliminado directorio: {path.relative_to(project_root)}")
            except Exception as e:
                print(f"  ⚠️ Error al eliminar {path}: {e}")
    
    # Limpiar logs antiguos (mantener solo los 5 más recientes)
    logs_dir = project_root / "logs"
    if logs_dir.exists():
        log_files = list(logs_dir.glob("*.log"))
        if len(log_files) > 5:
            log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            for log_file in log_files[5:]:
                try:
                    log_file.unlink()
                    files_removed += 1
                    print(f"  📄 Eliminado log antiguo: {log_file.name}")
                except Exception as e:
                    print(f"  ⚠️ Error al eliminar {log_file}: {e}")
    
    print(f"\n✅ Limpieza completada:")
    print(f"  📁 Directorios eliminados: {dirs_removed}")
    print(f"  📄 Archivos eliminados: {files_removed}")
    print(f"  🎯 Proyecto limpio y optimizado")

if __name__ == "__main__":
    clean_project()
