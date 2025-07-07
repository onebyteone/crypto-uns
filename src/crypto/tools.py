"""
🛠️ Herramientas Adicionales - CryptoUNS
======================================

Implementación de herramientas adicionales:
- Codificación Huffman
- Simulador Blockchain
- Verificador de Integridad

Autor: CryptoUNS Team
Fecha: 06 de julio, 2025
Versión: 1.0.0
"""

import heapq
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Optional, Any
import json
import hashlib
import time
import os

# Importar constantes y excepciones
try:
    from ..utils.constants import *
    from ..utils.exceptions import *
except ImportError:
    # Importación absoluta para cuando se ejecuta directamente
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from utils.constants import *
    from utils.exceptions import *

# ===== CODIFICACIÓN HUFFMAN =====
class Node:
    """Nodo para el árbol de Huffman"""
    
    def __init__(self, char: Optional[str] = None, freq: int = 0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
    
    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanCoding:
    """
    Implementación de la codificación Huffman
    
    La codificación Huffman es un algoritmo de compresión sin pérdida
    que asigna códigos más cortos a caracteres más frecuentes.
    """
    
    def __init__(self):
        """Inicializar codificador Huffman"""
        self.root = None
        self.codes = {}
        self.reverse_codes = {}
    
    def build_frequency_table(self, text: str) -> Dict[str, int]:
        """
        Construir tabla de frecuencias
        
        Args:
            text (str): Texto a analizar
            
        Returns:
            Dict[str, int]: Tabla de frecuencias
        """
        return dict(Counter(text))
    
    def build_heap(self, frequency: Dict[str, int]) -> List[Node]:
        """
        Construir heap mínimo para el árbol
        
        Args:
            frequency (Dict[str, int]): Tabla de frecuencias
            
        Returns:
            List[Node]: Heap de nodos
        """
        heap = []
        for char, freq in frequency.items():
            node = Node(char, freq)
            heapq.heappush(heap, node)
        return heap
    
    def build_tree(self, heap: List[Node]) -> Node:
        """
        Construir árbol de Huffman
        
        Args:
            heap (List[Node]): Heap de nodos
            
        Returns:
            Node: Raíz del árbol
        """
        if len(heap) == 1:
            # Caso especial: solo un carácter
            root = Node(freq=heap[0].freq)
            root.left = heap[0]
            return root
        
        while len(heap) > 1:
            # Tomar los dos nodos con menor frecuencia
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            
            # Crear nodo padre
            parent = Node(freq=left.freq + right.freq, left=left, right=right)
            heapq.heappush(heap, parent)
        
        return heap[0]
    
    def build_codes(self, root: Node) -> Dict[str, str]:
        """
        Construir códigos de Huffman
        
        Args:
            root (Node): Raíz del árbol
            
        Returns:
            Dict[str, str]: Diccionario de códigos
        """
        if not root:
            return {}
        
        codes = {}
        
        def dfs(node: Node, code: str):
            if node.char is not None:
                # Nodo hoja
                codes[node.char] = code if code else "0"  # Caso especial para un solo carácter
            else:
                # Nodo interno
                if node.left:
                    dfs(node.left, code + "0")
                if node.right:
                    dfs(node.right, code + "1")
        
        dfs(root, "")
        return codes
    
    def encode(self, text: str) -> Tuple[str, Dict[str, str], Node]:
        """
        Codificar texto usando Huffman
        
        Args:
            text (str): Texto a codificar
            
        Returns:
            Tuple[str, Dict[str, str], Node]: (texto_codificado, códigos, árbol)
        """
        if not text:
            raise InvalidInputError("El texto no puede estar vacío")
        
        # Construir tabla de frecuencias
        frequency = self.build_frequency_table(text)
        
        # Construir heap
        heap = self.build_heap(frequency)
        
        # Construir árbol
        self.root = self.build_tree(heap)
        
        # Construir códigos
        self.codes = self.build_codes(self.root)
        self.reverse_codes = {v: k for k, v in self.codes.items()}
        
        # Codificar texto
        encoded_text = ""
        for char in text:
            encoded_text += self.codes[char]
        
        return encoded_text, self.codes, self.root
    
    def decode(self, encoded_text: str, root: Optional[Node] = None) -> str:
        """
        Decodificar texto usando Huffman
        
        Args:
            encoded_text (str): Texto codificado
            root (Optional[Node]): Raíz del árbol (opcional)
            
        Returns:
            str: Texto decodificado
        """
        if not encoded_text:
            return ""
        
        if root is None:
            root = self.root
        
        if not root:
            raise InvalidInputError("No hay árbol de Huffman disponible")
        
        decoded_text = ""
        current_node = root
        
        for bit in encoded_text:
            if bit == "0":
                current_node = current_node.left
            elif bit == "1":
                current_node = current_node.right
            else:
                raise InvalidInputError(f"Bit inválido en texto codificado: {bit}")
            
            # Si llegamos a una hoja
            if current_node.char is not None:
                decoded_text += current_node.char
                current_node = root
        
        return decoded_text
    
    def get_compression_stats(self, original_text: str, encoded_text: str) -> Dict[str, Any]:
        """
        Obtener estadísticas de compresión
        
        Args:
            original_text (str): Texto original
            encoded_text (str): Texto codificado
            
        Returns:
            Dict[str, Any]: Estadísticas de compresión
        """
        original_bits = len(original_text) * 8  # Asumiendo ASCII
        encoded_bits = len(encoded_text)
        
        compression_ratio = encoded_bits / original_bits if original_bits > 0 else 0
        space_saved = original_bits - encoded_bits
        space_saved_percent = (space_saved / original_bits * 100) if original_bits > 0 else 0
        
        return {
            "original_length": len(original_text),
            "original_bits": original_bits,
            "encoded_length": len(encoded_text),
            "encoded_bits": encoded_bits,
            "compression_ratio": compression_ratio,
            "space_saved": space_saved,
            "space_saved_percent": space_saved_percent,
            "codes": self.codes
        }
    
    def visualize_tree(self, node: Optional[Node] = None, prefix: str = "", is_last: bool = True) -> str:
        """
        Visualizar árbol de Huffman
        
        Args:
            node (Optional[Node]): Nodo actual
            prefix (str): Prefijo para la visualización
            is_last (bool): Si es el último nodo
            
        Returns:
            str: Representación visual del árbol
        """
        if node is None:
            node = self.root
        
        if not node:
            return "Árbol vacío"
        
        result = ""
        
        # Agregar nodo actual
        result += prefix
        result += "└── " if is_last else "├── "
        
        if node.char is not None:
            result += f"'{node.char}' ({node.freq})\\n"
        else:
            result += f"[{node.freq}]\\n"
        
        # Agregar hijos
        children = []
        if node.left:
            children.append(node.left)
        if node.right:
            children.append(node.right)
        
        for i, child in enumerate(children):
            is_last_child = (i == len(children) - 1)
            new_prefix = prefix + ("    " if is_last else "│   ")
            result += self.visualize_tree(child, new_prefix, is_last_child)
        
        return result
    
    def encode_for_gui(self, text: str) -> Dict[str, Any]:
        """
        Codificar texto para la GUI con formato específico
        
        Args:
            text (str): Texto a codificar
            
        Returns:
            Dict[str, Any]: Datos formateados para la GUI
        """
        # Codificar con el método original
        encoded_text, codes, tree = self.encode(text)
        
        # Obtener estadísticas
        stats = self.get_compression_stats(text, encoded_text)
        
        # Obtener frecuencias
        frequencies = self.build_frequency_table(text)
        
        # Visualizar árbol
        tree_visualization = self.visualize_tree(tree)
        
        return {
            'encoded': encoded_text,
            'codes': codes,
            'tree': tree,
            'frequencies': frequencies,
            'tree_visualization': tree_visualization,
            'original_size': len(text) * 8,  # bits
            'compressed_size': len(encoded_text),  # bits
            'compression_ratio': (len(encoded_text) / (len(text) * 8)) * 100,
            'space_saved': ((len(text) * 8 - len(encoded_text)) / (len(text) * 8)) * 100
        }
    
    def decode_for_gui(self, encoded_text: str, codes: Dict[str, str]) -> str:
        """
        Decodificar texto para la GUI
        
        Args:
            encoded_text (str): Texto codificado
            codes (Dict[str, str]): Diccionario de códigos
            
        Returns:
            str: Texto decodificado
        """
        # Usar el método de decodificación original
        return self.decode(encoded_text, self.root)

# ===== SIMULADOR BLOCKCHAIN =====
class Block:
    """Bloque individual de la blockchain"""
    
    def __init__(self, index: int, data: str, previous_hash: str, timestamp: Optional[float] = None):
        """
        Inicializar bloque
        
        Args:
            index (int): Índice del bloque
            data (str): Datos del bloque
            previous_hash (str): Hash del bloque anterior
            timestamp (Optional[float]): Timestamp del bloque
        """
        self.index = index
        self.data = data
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """
        Calcular hash del bloque
        
        Returns:
            str: Hash SHA-256 del bloque
        """
        block_string = f"{self.index}{self.data}{self.previous_hash}{self.timestamp}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int = 4):
        """
        Minar bloque con prueba de trabajo
        
        Args:
            difficulty (int): Dificultad de minado (número de ceros iniciales)
        """
        target = "0" * difficulty
        
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir bloque a diccionario"""
        return {
            "index": self.index,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "hash": self.hash
        }

class Blockchain:
    """
    Simulador de Blockchain
    
    Implementa una blockchain básica con prueba de trabajo
    """
    
    def __init__(self, difficulty: int = 4):
        """
        Inicializar blockchain
        
        Args:
            difficulty (int): Dificultad de minado
        """
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions = []
        self.mining_reward = 10
    
    def create_genesis_block(self) -> Block:
        """
        Crear bloque génesis
        
        Returns:
            Block: Primer bloque de la cadena
        """
        return Block(0, "Genesis Block", "0")
    
    def get_latest_block(self) -> Block:
        """
        Obtener último bloque
        
        Returns:
            Block: Último bloque de la cadena
        """
        return self.chain[-1]
    
    def add_block(self, data: str) -> Block:
        """
        Agregar nuevo bloque a la cadena
        
        Args:
            data (str): Datos del bloque
            
        Returns:
            Block: Bloque añadido
        """
        if not data:
            raise InvalidInputError("Los datos del bloque no pueden estar vacíos")
        
        previous_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            data=data,
            previous_hash=previous_block.hash
        )
        
        # Minar bloque
        new_block.mine_block(self.difficulty)
        
        # Validar antes de agregar
        if self.is_valid_new_block(new_block, previous_block):
            self.chain.append(new_block)
            return new_block
        else:
            raise ValidationError("El bloque no es válido")
    
    def is_block_valid(self, block: Block) -> bool:
        """
        Validar un bloque individual
        
        Args:
            block (Block): Bloque a validar
            
        Returns:
            bool: True si el bloque es válido
        """
        # Verificar que el hash del bloque sea correcto
        if block.hash != block.calculate_hash():
            return False
        
        # El bloque génesis no necesita prueba de trabajo
        if block.index == 0:
            return True
        
        # Verificar prueba de trabajo para otros bloques
        if hasattr(self, 'difficulty') and self.difficulty > 0:
            if not block.hash.startswith("0" * self.difficulty):
                return False
        
        return True
    
    def is_valid_new_block(self, new_block: Block, previous_block: Block) -> bool:
        """
        Validar nuevo bloque
        
        Args:
            new_block (Block): Nuevo bloque
            previous_block (Block): Bloque anterior
            
        Returns:
            bool: True si es válido
        """
        # Verificar índice
        if new_block.index != previous_block.index + 1:
            return False
        
        # Verificar hash anterior
        if new_block.previous_hash != previous_block.hash:
            return False
        
        # Verificar hash del bloque
        if new_block.hash != new_block.calculate_hash():
            return False
        
        # Verificar prueba de trabajo
        if not new_block.hash.startswith("0" * self.difficulty):
            return False
        
        return True
    
    def is_chain_valid(self) -> bool:
        """
        Validar toda la cadena
        
        Returns:
            bool: True si la cadena es válida
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Verificar hash del bloque actual
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Verificar enlace con bloque anterior
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def tamper_block(self, index: int, new_data: str):
        """
        Simular alteración de un bloque (para demostración)
        
        Args:
            index (int): Índice del bloque a alterar
            new_data (str): Nuevos datos
        """
        if 0 <= index < len(self.chain):
            self.chain[index].data = new_data
            # No recalcular hash para simular alteración
    
    def detect_tampering(self) -> List[int]:
        """
        Detectar bloques alterados
        
        Returns:
            List[int]: Lista de índices de bloques alterados
        """
        tampered_blocks = []
        
        for i, block in enumerate(self.chain):
            expected_hash = block.calculate_hash()
            if block.hash != expected_hash:
                tampered_blocks.append(i)
        
        return tampered_blocks
    
    def get_chain_info(self) -> Dict[str, Any]:
        """
        Obtener información de la cadena
        
        Returns:
            Dict[str, Any]: Información de la blockchain
        """
        return {
            "length": len(self.chain),
            "difficulty": self.difficulty,
            "is_valid": self.is_chain_valid(),
            "latest_block": self.get_latest_block().to_dict(),
            "tampered_blocks": self.detect_tampering()
        }
    
    def to_json(self) -> str:
        """
        Exportar blockchain a JSON
        
        Returns:
            str: Representación JSON de la blockchain
        """
        chain_data = [block.to_dict() for block in self.chain]
        return json.dumps(chain_data, indent=2)

# ===== VERIFICADOR DE INTEGRIDAD =====
class IntegrityVerifier:
    """
    Verificador de integridad para archivos y texto
    """
    
    def __init__(self):
        """Inicializar verificador"""
        pass
    
    def calculate_file_hash(self, file_path: str, algorithm: str = "sha256") -> str:
        """
        Calcular hash de un archivo
        
        Args:
            file_path (str): Ruta del archivo
            algorithm (str): Algoritmo de hash
            
        Returns:
            str: Hash del archivo
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        
        if algorithm.lower() not in ["sha256", "sha1", "md5"]:
            raise InvalidInputError(f"Algoritmo no soportado: {algorithm}")
        
        hash_func = getattr(hashlib, algorithm.lower())()
        
        try:
            with open(file_path, 'rb') as f:
                # Leer archivo en chunks para archivos grandes
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_func.update(chunk)
            
            return hash_func.hexdigest()
        
        except Exception as e:
            raise FileError(f"Error al leer archivo: {str(e)}")
    
    def calculate_text_hash(self, text: str, algorithm: str = "sha256") -> str:
        """
        Calcular hash de un texto
        
        Args:
            text (str): Texto a hashear
            algorithm (str): Algoritmo de hash
            
        Returns:
            str: Hash del texto
        """
        if algorithm.lower() not in ["sha256", "sha1", "md5"]:
            raise InvalidInputError(f"Algoritmo no soportado: {algorithm}")
        
        hash_func = getattr(hashlib, algorithm.lower())()
        hash_func.update(text.encode('utf-8'))
        
        return hash_func.hexdigest()
    
    def verify_file_integrity(self, file_path: str, expected_hash: str, algorithm: str = "sha256") -> Dict[str, Any]:
        """
        Verificar integridad de un archivo
        
        Args:
            file_path (str): Ruta del archivo
            expected_hash (str): Hash esperado
            algorithm (str): Algoritmo de hash
            
        Returns:
            Dict[str, Any]: Resultado de la verificación
        """
        try:
            calculated_hash = self.calculate_file_hash(file_path, algorithm)
            is_valid = calculated_hash.lower() == expected_hash.lower()
            
            return {
                "file_path": file_path,
                "algorithm": algorithm,
                "expected_hash": expected_hash.lower(),
                "calculated_hash": calculated_hash.lower(),
                "is_valid": is_valid,
                "file_size": os.path.getsize(file_path),
                "timestamp": time.time()
            }
        
        except Exception as e:
            return {
                "file_path": file_path,
                "algorithm": algorithm,
                "expected_hash": expected_hash.lower(),
                "calculated_hash": None,
                "is_valid": False,
                "error": str(e),
                "timestamp": time.time()
            }
    
    def verify_text_integrity(self, text: str, expected_hash: str, algorithm: str = "sha256") -> Dict[str, Any]:
        """
        Verificar integridad de un texto
        
        Args:
            text (str): Texto a verificar
            expected_hash (str): Hash esperado
            algorithm (str): Algoritmo de hash
            
        Returns:
            Dict[str, Any]: Resultado de la verificación
        """
        try:
            calculated_hash = self.calculate_text_hash(text, algorithm)
            is_valid = calculated_hash.lower() == expected_hash.lower()
            
            return {
                "text_length": len(text),
                "algorithm": algorithm,
                "expected_hash": expected_hash.lower(),
                "calculated_hash": calculated_hash.lower(),
                "is_valid": is_valid,
                "timestamp": time.time()
            }
        
        except Exception as e:
            return {
                "text_length": len(text),
                "algorithm": algorithm,
                "expected_hash": expected_hash.lower(),
                "calculated_hash": None,
                "is_valid": False,
                "error": str(e),
                "timestamp": time.time()
            }
    
    def compare_files(self, file1_path: str, file2_path: str, algorithm: str = "sha256") -> Dict[str, Any]:
        """
        Comparar dos archivos
        
        Args:
            file1_path (str): Ruta del primer archivo
            file2_path (str): Ruta del segundo archivo
            algorithm (str): Algoritmo de hash
            
        Returns:
            Dict[str, Any]: Resultado de la comparación
        """
        try:
            hash1 = self.calculate_file_hash(file1_path, algorithm)
            hash2 = self.calculate_file_hash(file2_path, algorithm)
            
            return {
                "file1": {
                    "path": file1_path,
                    "hash": hash1,
                    "size": os.path.getsize(file1_path)
                },
                "file2": {
                    "path": file2_path,
                    "hash": hash2,
                    "size": os.path.getsize(file2_path)
                },
                "algorithm": algorithm,
                "are_identical": hash1.lower() == hash2.lower(),
                "timestamp": time.time()
            }
        
        except Exception as e:
            return {
                "file1": {"path": file1_path},
                "file2": {"path": file2_path},
                "algorithm": algorithm,
                "are_identical": False,
                "error": str(e),
                "timestamp": time.time()
            }
    
    def generate_integrity_report(self, items: List[Dict[str, str]], algorithm: str = "sha256") -> Dict[str, Any]:
        """
        Generar reporte de integridad para múltiples elementos
        
        Args:
            items (List[Dict[str, str]]): Lista de elementos a verificar
            algorithm (str): Algoritmo de hash
            
        Returns:
            Dict[str, Any]: Reporte completo
        """
        report = {
            "algorithm": algorithm,
            "timestamp": time.time(),
            "results": [],
            "summary": {
                "total": len(items),
                "valid": 0,
                "invalid": 0,
                "errors": 0
            }
        }
        
        for item in items:
            if "file_path" in item:
                # Verificar archivo
                result = self.verify_file_integrity(item["file_path"], item["expected_hash"], algorithm)
            elif "text" in item:
                # Verificar texto
                result = self.verify_text_integrity(item["text"], item["expected_hash"], algorithm)
            else:
                result = {"error": "Tipo de elemento no soportado"}
            
            report["results"].append(result)
            
            # Actualizar resumen
            if "error" in result:
                report["summary"]["errors"] += 1
            elif result.get("is_valid", False):
                report["summary"]["valid"] += 1
            else:
                report["summary"]["invalid"] += 1
        
        return report

# ===== EXPORTAR CLASES =====
__all__ = [
    'HuffmanCoding',
    'Blockchain',
    'Block',
    'IntegrityVerifier'
]
