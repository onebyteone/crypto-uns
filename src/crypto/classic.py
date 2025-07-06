"""
📚 Criptografía Clásica - CryptoUNS
=================================

Implementación de algoritmos de criptografía clásica:
- Cifrado César
- Cifrado Vigenère
- Cifrado Playfair
- Método de Kasiski

Autor: CryptoUNS Team
Fecha: 06 de julio, 2025
Versión: 1.0.0
"""

import re
from typing import Optional, Tuple, List, Dict

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

# ===== CIFRADO CÉSAR =====
class CaesarCipher:
    """
    Implementación del cifrado César
    
    El cifrado César es un tipo de cifrado por sustitución en el que cada letra
    del texto plano es reemplazada por una letra que se encuentra un número
    fijo de posiciones más adelante en el alfabeto.
    """
    
    def __init__(self, alphabet: str = DEFAULT_ALPHABET):
        """
        Inicializar cifrado César
        
        Args:
            alphabet (str): Alfabeto a utilizar (por defecto inglés)
        """
        self.alphabet = alphabet.upper()
        self.alphabet_size = len(self.alphabet)
    
    def validate_key(self, key: int) -> bool:
        """
        Validar clave del cifrado César
        
        Args:
            key (int): Clave de desplazamiento
            
        Returns:
            bool: True si la clave es válida, False en caso contrario
        """
        return isinstance(key, int)
    
    def encrypt(self, plaintext: str, key: int) -> str:
        """
        Cifrar texto usando el cifrado César
        
        Args:
            plaintext (str): Texto plano a cifrar
            key (int): Clave de desplazamiento
            
        Returns:
            str: Texto cifrado
            
        Raises:
            InvalidKeyError: Si la clave no es válida
            InvalidInputError: Si el texto de entrada está vacío
        """
        # Validar entrada
        if not plaintext:
            raise InvalidInputError("El texto no puede estar vacío", "text")
        
        if not self.validate_key(key):
            raise InvalidKeyError(
                f"La clave debe ser un número entero",
                "caesar",
                {"provided_key": key}
            )
        
        # Normalizar clave al rango del alfabeto
        key = key % self.alphabet_size
        
        # Cifrar texto
        ciphertext = ""
        for char in plaintext.upper():
            if char in self.alphabet:
                # Encontrar posición en el alfabeto
                old_pos = self.alphabet.index(char)
                # Aplicar desplazamiento con módulo
                new_pos = (old_pos + key) % self.alphabet_size
                # Agregar carácter cifrado
                ciphertext += self.alphabet[new_pos]
            else:
                # Mantener caracteres que no están en el alfabeto
                ciphertext += char
        
        return ciphertext
    
    def decrypt(self, ciphertext: str, key: int) -> str:
        """
        Descifrar texto usando el cifrado César
        
        Args:
            ciphertext (str): Texto cifrado a descifrar
            key (int): Clave de desplazamiento (1-25)
            
        Returns:
            str: Texto plano
            
        Raises:
            InvalidKeyError: Si la clave no es válida
            InvalidInputError: Si el texto de entrada está vacío
        """
        # Validar entrada
        if not ciphertext:
            raise InvalidInputError("El texto no puede estar vacío", "text")
        
        if not self.validate_key(key):
            raise InvalidKeyError(
                f"La clave debe ser un número entero",
                "caesar",
                {"provided_key": key}
            )
        
        # Descifrar usando desplazamiento negativo
        return self.encrypt(ciphertext, -key)
    
    def brute_force_attack(self, ciphertext: str) -> List[Tuple[str, int]]:
        """
        Ataque de fuerza bruta al cifrado César
        
        Args:
            ciphertext (str): Texto cifrado
            
        Returns:
            List[Tuple[str, int]]: Lista de (texto_descifrado, clave)
        """
        results = []
        for key in range(self.alphabet_size):
            try:
                decrypted = self.decrypt(ciphertext, key)
                results.append((decrypted, key))
            except Exception:
                continue
        return results
    
    def frequency_analysis(self, text: str) -> Dict[str, float]:
        """
        Análisis de frecuencia de caracteres
        
        Args:
            text (str): Texto a analizar
            
        Returns:
            Dict[str, float]: Diccionario con frecuencias de caracteres
        """
        text = text.upper()
        char_count = {}
        total_chars = 0
        
        # Contar caracteres del alfabeto
        for char in text:
            if char in self.alphabet:
                char_count[char] = char_count.get(char, 0) + 1
                total_chars += 1
        
        # Calcular frecuencias (devolver conteos en lugar de porcentajes)
        frequencies = {}
        for char in self.alphabet:
            count = char_count.get(char, 0)
            frequencies[char] = count
        
        return frequencies

# ===== CIFRADO VIGENÈRE =====
class VigenereCipher:
    """
    Implementación del cifrado Vigenère
    
    El cifrado Vigenère es un cifrado polialfabético que utiliza una clave
    de texto para determinar el desplazamiento de cada letra.
    """
    
    def __init__(self, alphabet: str = DEFAULT_ALPHABET):
        """
        Inicializar cifrado Vigenère
        
        Args:
            alphabet (str): Alfabeto a utilizar (por defecto inglés)
        """
        self.alphabet = alphabet.upper()
        self.alphabet_size = len(self.alphabet)
    
    def validate_key(self, key: str) -> bool:
        """
        Validar clave del cifrado Vigenère
        
        Args:
            key (str): Clave alfabética
            
        Returns:
            bool: True si la clave es válida, False en caso contrario
        """
        if not isinstance(key, str) or len(key) < 1:
            return False
        
        # Verificar que todos los caracteres estén en el alfabeto
        return all(char.upper() in self.alphabet for char in key)
    
    def prepare_key(self, key: str, text_length: int) -> str:
        """
        Preparar clave repitiéndola para que coincida con la longitud del texto
        
        Args:
            key (str): Clave original
            text_length (int): Longitud del texto
            
        Returns:
            str: Clave preparada
        """
        key = key.upper()
        prepared_key = ""
        key_index = 0
        
        for _ in range(text_length):
            prepared_key += key[key_index % len(key)]
            key_index += 1
        
        return prepared_key
    
    def encrypt(self, plaintext: str, key: str) -> str:
        """
        Cifrar texto usando el cifrado Vigenère
        
        Args:
            plaintext (str): Texto plano a cifrar
            key (str): Clave alfabética
            
        Returns:
            str: Texto cifrado
            
        Raises:
            InvalidKeyError: Si la clave no es válida
            InvalidInputError: Si el texto de entrada está vacío
        """
        # Validar entrada
        if not plaintext:
            raise InvalidInputError("El texto no puede estar vacío", "text")
        
        if not self.validate_key(key):
            raise InvalidKeyError(
                f"La clave debe ser alfabética y tener al menos 1 carácter",
                "vigenere",
                {"provided_key": key}
            )
        
        # Preparar texto y clave
        plaintext = plaintext.upper()
        alphabet_chars = [char for char in plaintext if char in self.alphabet]
        prepared_key = self.prepare_key(key, len(alphabet_chars))
        
        # Cifrar
        ciphertext = ""
        key_index = 0
        
        for char in plaintext:
            if char in self.alphabet:
                # Obtener posiciones
                char_pos = self.alphabet.index(char)
                key_pos = self.alphabet.index(prepared_key[key_index])
                
                # Aplicar cifrado Vigenère
                new_pos = (char_pos + key_pos) % self.alphabet_size
                ciphertext += self.alphabet[new_pos]
                key_index += 1
            else:
                # Mantener caracteres que no están en el alfabeto
                ciphertext += char
        
        return ciphertext
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """
        Descifrar texto usando el cifrado Vigenère
        
        Args:
            ciphertext (str): Texto cifrado a descifrar
            key (str): Clave alfabética
            
        Returns:
            str: Texto plano
            
        Raises:
            InvalidKeyError: Si la clave no es válida
            InvalidInputError: Si el texto de entrada está vacío
        """
        # Validar entrada
        if not ciphertext:
            raise InvalidInputError("El texto no puede estar vacío", "text")
        
        if not self.validate_key(key):
            raise InvalidKeyError(
                f"La clave debe ser alfabética y tener al menos {VIGENERE_MIN_KEY_LENGTH} caracteres",
                "vigenere",
                {"min_length": VIGENERE_MIN_KEY_LENGTH, "provided_key": key}
            )
        
        # Preparar texto y clave
        ciphertext = ciphertext.upper()
        alphabet_chars = [char for char in ciphertext if char in self.alphabet]
        prepared_key = self.prepare_key(key, len(alphabet_chars))
        
        # Descifrar
        plaintext = ""
        key_index = 0
        
        for char in ciphertext:
            if char in self.alphabet:
                # Obtener posiciones
                char_pos = self.alphabet.index(char)
                key_pos = self.alphabet.index(prepared_key[key_index])
                
                # Aplicar descifrado Vigenère
                new_pos = (char_pos - key_pos) % self.alphabet_size
                plaintext += self.alphabet[new_pos]
                key_index += 1
            else:
                # Mantener caracteres que no están en el alfabeto
                plaintext += char
        
        return plaintext
    
    def get_key_length_candidates(self, ciphertext: str, max_length: int = 20) -> List[int]:
        """
        Obtener candidatos para la longitud de la clave usando índice de coincidencia
        
        Args:
            ciphertext (str): Texto cifrado
            max_length (int): Longitud máxima a probar
            
        Returns:
            List[int]: Lista de longitudes candidatas ordenadas por probabilidad
        """
        ciphertext = ''.join(char for char in ciphertext.upper() if char in self.alphabet)
        ic_scores = []
        
        for length in range(1, min(max_length + 1, len(ciphertext) // 2)):
            # Dividir en grupos según la longitud de clave candidata
            groups = [''] * length
            for i, char in enumerate(ciphertext):
                groups[i % length] += char
            
            # Calcular índice de coincidencia promedio
            total_ic = 0
            for group in groups:
                if len(group) > 1:
                    ic = self._calculate_index_of_coincidence(group)
                    total_ic += ic
            
            avg_ic = total_ic / length if length > 0 else 0
            ic_scores.append((length, avg_ic))
        
        # Ordenar por índice de coincidencia (más alto = más probable)
        ic_scores.sort(key=lambda x: x[1], reverse=True)
        return [length for length, _ in ic_scores[:5]]  # Top 5 candidatos
    
    def _calculate_index_of_coincidence(self, text: str) -> float:
        """
        Calcular índice de coincidencia de un texto
        
        Args:
            text (str): Texto a analizar
            
        Returns:
            float: Índice de coincidencia
        """
        if len(text) <= 1:
            return 0
        
        # Contar frecuencias
        freq = {}
        for char in text:
            freq[char] = freq.get(char, 0) + 1
        
        # Calcular IC
        n = len(text)
        ic = sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))
        return ic
    
    def generate_key(self, length: int) -> str:
        """
        Generar una clave aleatoria para Vigenère
        
        Args:
            length (int): Longitud de la clave
            
        Returns:
            str: Clave generada
        """
        import random
        return ''.join(random.choice(self.alphabet) for _ in range(length))
    
    def encrypt_autokey(self, plaintext: str, key: str) -> str:
        """
        Cifrar texto usando Vigenère con autoclave
        
        Args:
            plaintext (str): Texto plano a cifrar
            key (str): Clave inicial
            
        Returns:
            str: Texto cifrado
        """
        if not self.validate_key(key):
            raise InvalidKeyError("La clave debe ser alfabética", "vigenere")
        
        plaintext = plaintext.upper()
        key = key.upper()
        
        # Crear clave extendida con el texto plano
        alphabet_chars = [char for char in plaintext if char in self.alphabet]
        extended_key = key + ''.join(alphabet_chars)
        
        # Cifrar usando la clave extendida
        ciphertext = ""
        key_index = 0
        
        for char in plaintext:
            if char in self.alphabet:
                char_index = self.alphabet.index(char)
                key_char_index = self.alphabet.index(extended_key[key_index % len(extended_key)])
                cipher_index = (char_index + key_char_index) % self.alphabet_size
                ciphertext += self.alphabet[cipher_index]
                key_index += 1
            else:
                ciphertext += char
        
        return ciphertext
    
    def decrypt_autokey(self, ciphertext: str, key: str) -> str:
        """
        Descifrar texto usando Vigenère con autoclave
        
        Args:
            ciphertext (str): Texto cifrado
            key (str): Clave inicial
            
        Returns:
            str: Texto descifrado
        """
        if not self.validate_key(key):
            raise InvalidKeyError("La clave debe ser alfabética", "vigenere")
        
        ciphertext = ciphertext.upper()
        key = key.upper()
        
        plaintext = ""
        key_chars = list(key)
        
        for char in ciphertext:
            if char in self.alphabet:
                char_index = self.alphabet.index(char)
                key_char_index = self.alphabet.index(key_chars[0])
                plain_index = (char_index - key_char_index) % self.alphabet_size
                plain_char = self.alphabet[plain_index]
                plaintext += plain_char
                
                # Actualizar clave con el carácter descifrado
                key_chars = key_chars[1:] + [plain_char]
            else:
                plaintext += char
        
        return plaintext
    
    def find_repetitions(self, text: str, min_length: int = 3) -> List[Dict]:
        """
        Buscar repeticiones en el texto para análisis de Kasiski
        
        Args:
            text (str): Texto a analizar
            min_length (int): Longitud mínima de repetición
            
        Returns:
            List[Dict]: Lista de repeticiones encontradas
        """
        # Delegar al análisis de Kasiski
        kasiski = KasiskiAnalysis()
        return kasiski.find_repetitions(text, min_length)

# ===== CIFRADO PLAYFAIR =====
class PlayfairCipher:
    """
    Implementación del cifrado Playfair
    
    El cifrado Playfair es un cifrado digráfico que utiliza una matriz 5x5
    para cifrar pares de letras.
    """
    
    def __init__(self):
        """Inicializar cifrado Playfair"""
        self.alphabet = PLAYFAIR_ALPHABET  # Sin J
        self.matrix = []
        self.char_positions = {}
    
    def validate_key(self, key: str) -> bool:
        """
        Validar clave del cifrado Playfair
        
        Args:
            key (str): Clave alfabética
            
        Returns:
            bool: True si la clave es válida, False en caso contrario
        """
        if not isinstance(key, str) or len(key) == 0:
            return False
        
        # Verificar que todos los caracteres estén en el alfabeto Playfair
        return all(char.upper() in self.alphabet for char in key)
    
    def create_matrix(self, key: str) -> List[List[str]]:
        """
        Crear matriz 5x5 para el cifrado Playfair
        
        Args:
            key (str): Clave para generar la matriz
            
        Returns:
            List[List[str]]: Matriz 5x5
        """
        # Preparar clave sin duplicados
        key = key.upper()
        used_chars = set()
        key_chars = []
        
        for char in key:
            if char in self.alphabet and char not in used_chars:
                key_chars.append(char)
                used_chars.add(char)
        
        # Agregar resto del alfabeto
        for char in self.alphabet:
            if char not in used_chars:
                key_chars.append(char)
        
        # Crear matriz 5x5
        matrix = []
        self.char_positions = {}
        
        for i in range(PLAYFAIR_MATRIX_SIZE):
            row = []
            for j in range(PLAYFAIR_MATRIX_SIZE):
                char = key_chars[i * PLAYFAIR_MATRIX_SIZE + j]
                row.append(char)
                self.char_positions[char] = (i, j)
            matrix.append(row)
        
        self.matrix = matrix
        return matrix
    
    def prepare_text(self, text: str) -> str:
        """
        Preparar texto para cifrado Playfair
        
        Args:
            text (str): Texto a preparar
            
        Returns:
            str: Texto preparado
        """
        # Convertir a mayúsculas y reemplazar J por I
        text = text.upper().replace('J', 'I')
        
        # Filtrar solo caracteres del alfabeto
        filtered_text = ''.join(char for char in text if char in self.alphabet)
        
        # Separar letras duplicadas con X
        prepared = ""
        i = 0
        while i < len(filtered_text):
            char1 = filtered_text[i]
            prepared += char1
            
            # Si hay un siguiente carácter y es igual al actual, insertar X
            if i + 1 < len(filtered_text) and filtered_text[i + 1] == char1:
                prepared += PLAYFAIR_SUBSTITUTE_CHAR
            
            i += 1
        
        # Asegurar que la longitud sea par
        if len(prepared) % 2 != 0:
            prepared += PLAYFAIR_SUBSTITUTE_CHAR
        
        return prepared
    
    def encrypt_pair(self, char1: str, char2: str) -> str:
        """
        Cifrar un par de caracteres
        
        Args:
            char1 (str): Primer carácter
            char2 (str): Segundo carácter
            
        Returns:
            str: Par cifrado
        """
        row1, col1 = self.char_positions[char1]
        row2, col2 = self.char_positions[char2]
        
        if row1 == row2:
            # Misma fila: mover a la derecha
            new_col1 = (col1 + 1) % PLAYFAIR_MATRIX_SIZE
            new_col2 = (col2 + 1) % PLAYFAIR_MATRIX_SIZE
            return self.matrix[row1][new_col1] + self.matrix[row2][new_col2]
        elif col1 == col2:
            # Misma columna: mover hacia abajo
            new_row1 = (row1 + 1) % PLAYFAIR_MATRIX_SIZE
            new_row2 = (row2 + 1) % PLAYFAIR_MATRIX_SIZE
            return self.matrix[new_row1][col1] + self.matrix[new_row2][col2]
        else:
            # Rectángulo: intercambiar columnas
            return self.matrix[row1][col2] + self.matrix[row2][col1]
    
    def decrypt_pair(self, char1: str, char2: str) -> str:
        """
        Descifrar un par de caracteres
        
        Args:
            char1 (str): Primer carácter cifrado
            char2 (str): Segundo carácter cifrado
            
        Returns:
            str: Par descifrado
        """
        row1, col1 = self.char_positions[char1]
        row2, col2 = self.char_positions[char2]
        
        if row1 == row2:
            # Misma fila: mover a la izquierda
            new_col1 = (col1 - 1) % PLAYFAIR_MATRIX_SIZE
            new_col2 = (col2 - 1) % PLAYFAIR_MATRIX_SIZE
            return self.matrix[row1][new_col1] + self.matrix[row2][new_col2]
        elif col1 == col2:
            # Misma columna: mover hacia arriba
            new_row1 = (row1 - 1) % PLAYFAIR_MATRIX_SIZE
            new_row2 = (row2 - 1) % PLAYFAIR_MATRIX_SIZE
            return self.matrix[new_row1][col1] + self.matrix[new_row2][col2]
        else:
            # Rectángulo: intercambiar columnas
            return self.matrix[row1][col2] + self.matrix[row2][col1]
    
    def encrypt(self, plaintext: str, key: str) -> str:
        """
        Cifrar texto usando el cifrado Playfair
        
        Args:
            plaintext (str): Texto plano a cifrar
            key (str): Clave alfabética
            
        Returns:
            str: Texto cifrado
            
        Raises:
            InvalidKeyError: Si la clave no es válida
            InvalidInputError: Si el texto de entrada está vacío
        """
        # Validar entrada
        if not plaintext:
            raise InvalidInputError("El texto no puede estar vacío", "text")
        
        if not self.validate_key(key):
            raise InvalidKeyError(
                "La clave debe contener solo letras del alfabeto inglés (sin J)",
                "playfair",
                {"provided_key": key}
            )
        
        # Crear matriz y preparar texto
        self.create_matrix(key)
        prepared_text = self.prepare_text(plaintext)
        
        # Cifrar por pares
        ciphertext = ""
        for i in range(0, len(prepared_text), 2):
            if i + 1 < len(prepared_text):
                char1 = prepared_text[i]
                char2 = prepared_text[i + 1]
                ciphertext += self.encrypt_pair(char1, char2)
        
        return ciphertext
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """
        Descifrar texto usando el cifrado Playfair
        
        Args:
            ciphertext (str): Texto cifrado a descifrar
            key (str): Clave alfabética
            
        Returns:
            str: Texto plano
            
        Raises:
            InvalidKeyError: Si la clave no es válida
            InvalidInputError: Si el texto de entrada está vacío
        """
        # Validar entrada
        if not ciphertext:
            raise InvalidInputError("El texto no puede estar vacío", "text")
        
        if not self.validate_key(key):
            raise InvalidKeyError(
                "La clave debe contener solo letras del alfabeto inglés (sin J)",
                "playfair",
                {"provided_key": key}
            )
        
        # Crear matriz
        self.create_matrix(key)
        
        # Preparar texto cifrado
        ciphertext = ciphertext.upper().replace('J', 'I')
        filtered_ciphertext = ''.join(char for char in ciphertext if char in self.alphabet)
        
        # Descifrar por pares
        plaintext = ""
        for i in range(0, len(filtered_ciphertext), 2):
            if i + 1 < len(filtered_ciphertext):
                char1 = filtered_ciphertext[i]
                char2 = filtered_ciphertext[i + 1]
                plaintext += self.decrypt_pair(char1, char2)
        
        return plaintext
    
    def get_matrix_display(self) -> str:
        """
        Obtener representación visual de la matriz
        
        Returns:
            str: Matriz formateada para mostrar
        """
        if not self.matrix:
            return "No hay matriz generada"
        
        display = "Matriz Playfair 5x5:\\n"
        display += "+" + "-" * 11 + "+\\n"
        
        for row in self.matrix:
            display += "| " + " ".join(row) + " |\\n"
        
        display += "+" + "-" * 11 + "+"
        return display
    
    def generate_key(self, length: int) -> str:
        """
        Generar una clave aleatoria para Playfair
        
        Args:
            length (int): Longitud de la clave
            
        Returns:
            str: Clave generada
        """
        import random
        return ''.join(random.choice(PLAYFAIR_ALPHABET) for _ in range(length))

# ===== MÉTODO DE KASISKI =====
class KasiskiAnalysis:
    """
    Implementación del Método de Kasiski para criptoanálisis de Vigenère
    
    El método de Kasiski es una técnica de criptoanálisis que busca secuencias
    repetidas en un texto cifrado para determinar la longitud de la clave.
    """
    
    def __init__(self, min_sequence_length: int = 3, max_sequence_length: int = 6):
        """
        Inicializar análisis de Kasiski
        
        Args:
            min_sequence_length (int): Longitud mínima de secuencia a buscar
            max_sequence_length (int): Longitud máxima de secuencia a buscar
        """
        self.min_sequence_length = min_sequence_length
        self.max_sequence_length = max_sequence_length
    
    def find_repetitions(self, text: str, min_length: int = 3) -> List[Dict]:
        """
        Encontrar secuencias repetidas en el texto
        
        Args:
            text (str): Texto cifrado a analizar
            min_length (int): Longitud mínima de secuencia
            
        Returns:
            List[Dict]: Lista de diccionarios con información de repeticiones
        """
        if not text:
            return []
            
        text = text.upper().replace(" ", "")
        repetitions = []
        
        # Buscar secuencias de diferentes longitudes
        for length in range(min_length, min(len(text) // 2 + 1, self.max_sequence_length + 1)):
            sequences = {}
            
            # Extraer todas las secuencias de la longitud especificada
            for i in range(len(text) - length + 1):
                sequence = text[i:i + length]
                
                if sequence not in sequences:
                    sequences[sequence] = []
                sequences[sequence].append(i)
            
            # Filtrar secuencias que aparecen más de una vez
            for sequence, positions in sequences.items():
                if len(positions) > 1:
                    repetitions.append({
                        'sequence': sequence,
                        'positions': positions,
                        'length': length,
                        'occurrences': len(positions)
                    })
        
        # Ordenar por número de ocurrencias y longitud
        repetitions.sort(key=lambda x: (x['occurrences'], x['length']), reverse=True)
        return repetitions
    
    def calculate_distances(self, repetitions: List[Dict]) -> List[int]:
        """
        Calcular distancias entre repeticiones
        
        Args:
            repetitions (List[Dict]): Lista de repeticiones encontradas
            
        Returns:
            List[int]: Lista de distancias entre repeticiones
        """
        distances = []
        
        for rep in repetitions:
            positions = rep['positions']
            for i in range(len(positions)):
                for j in range(i + 1, len(positions)):
                    distance = positions[j] - positions[i]
                    distances.append(distance)
        
        return sorted(list(set(distances)))
    
    def find_common_factors(self, distances: List[int]) -> Dict[int, int]:
        """
        Encontrar factores comunes de las distancias
        
        Args:
            distances (List[int]): Lista de distancias
            
        Returns:
            Dict[int, int]: Diccionario con factores y sus frecuencias
        """
        factor_count = {}
        
        for distance in distances:
            factors = self._get_factors(distance)
            for factor in factors:
                if factor > 1:  # Excluir factor 1
                    factor_count[factor] = factor_count.get(factor, 0) + 1
        
        # Ordenar por frecuencia
        sorted_factors = dict(sorted(factor_count.items(), key=lambda x: x[1], reverse=True))
        return sorted_factors
    
    def _get_factors(self, n: int) -> List[int]:
        """
        Obtener todos los factores de un número
        
        Args:
            n (int): Número a factorizar
            
        Returns:
            List[int]: Lista de factores
        """
        factors = []
        for i in range(1, int(n**0.5) + 1):
            if n % i == 0:
                factors.append(i)
                if i != n // i:
                    factors.append(n // i)
        return sorted(factors)
    
    def estimate_key_length(self, ciphertext: str, max_key_length: int = 20) -> List[Tuple[int, float]]:
        """
        Estimar la longitud de la clave usando el método de Kasiski
        
        Args:
            ciphertext (str): Texto cifrado
            max_key_length (int): Longitud máxima de clave a considerar
            
        Returns:
            List[Tuple[int, float]]: Lista de tuplas (longitud, puntuación)
        """
        if not ciphertext:
            return []
        
        # Encontrar repeticiones
        repetitions = self.find_repetitions(ciphertext)
        
        if not repetitions:
            return []
        
        # Calcular distancias
        distances = self.calculate_distances(repetitions)
        
        if not distances:
            return []
        
        # Encontrar factores comunes
        factors = self.find_common_factors(distances)
        
        # Calcular puntuaciones para cada longitud posible
        key_length_scores = []
        for length in range(2, max_key_length + 1):
            score = factors.get(length, 0)
            if score > 0:
                key_length_scores.append((length, score))
        
        # Ordenar por puntuación
        key_length_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Normalizar puntuaciones
        if key_length_scores:
            max_score = key_length_scores[0][1]
            normalized_scores = [(length, score / max_score) for length, score in key_length_scores]
            return normalized_scores
        
        return []
    
    def analyze(self, ciphertext: str) -> Dict:
        """
        Realizar análisis completo de Kasiski
        
        Args:
            ciphertext (str): Texto cifrado a analizar
            
        Returns:
            Dict: Diccionario con resultados del análisis
        """
        if not ciphertext:
            raise InvalidInputError("El texto cifrado no puede estar vacío")
        
        # Limpiar texto
        clean_text = ciphertext.upper().replace(" ", "")
        
        # Encontrar repeticiones
        repetitions = self.find_repetitions(clean_text)
        
        # Calcular distancias
        distances = self.calculate_distances(repetitions)
        
        # Encontrar factores comunes
        factors = self.find_common_factors(distances)
        
        # Estimar longitud de clave
        key_length_estimates = self.estimate_key_length(clean_text)
        
        # Preparar resultado
        result = {
            'text_length': len(clean_text),
            'repetitions': repetitions[:10],  # Top 10 repeticiones
            'distances': distances[:20],  # Top 20 distancias
            'factors': factors,
            'key_length_estimates': key_length_estimates[:10],  # Top 10 estimaciones
            'analysis_summary': {
                'total_repetitions': len(repetitions),
                'total_distances': len(distances),
                'total_factors': len(factors),
                'recommended_key_length': key_length_estimates[0][0] if key_length_estimates else None
            }
        }
        
        return result
    
    def generate_report(self, analysis_result: Dict) -> str:
        """
        Generar reporte legible del análisis
        
        Args:
            analysis_result (Dict): Resultado del análisis
            
        Returns:
            str: Reporte formateado
        """
        report = []
        report.append("=" * 60)
        report.append("📊 ANÁLISIS DE KASISKI - REPORTE")
        report.append("=" * 60)
        
        # Información general
        report.append(f"Longitud del texto: {analysis_result['text_length']}")
        report.append(f"Repeticiones encontradas: {analysis_result['analysis_summary']['total_repetitions']}")
        report.append(f"Distancias calculadas: {analysis_result['analysis_summary']['total_distances']}")
        report.append(f"Factores identificados: {analysis_result['analysis_summary']['total_factors']}")
        
        # Longitud de clave recomendada
        recommended = analysis_result['analysis_summary']['recommended_key_length']
        if recommended:
            report.append(f"\\n🎯 Longitud de clave recomendada: {recommended}")
        
        # Top repeticiones
        report.append("\\n🔍 Repeticiones más frecuentes:")
        for rep in analysis_result['repetitions'][:5]:
            report.append(f"  '{rep['sequence']}' -> {rep['occurrences']} veces en posiciones {rep['positions']}")
        
        # Top estimaciones de longitud
        report.append("\\n📏 Estimaciones de longitud de clave:")
        for length, score in analysis_result['key_length_estimates'][:5]:
            report.append(f"  Longitud {length}: {score:.2f}")
        
        # Factores más comunes
        report.append("\\n🔢 Factores más comunes:")
        for factor, count in list(analysis_result['factors'].items())[:5]:
            report.append(f"  {factor}: {count} ocurrencias")
        
        report.append("=" * 60)
        
        return "\\n".join(report)

# ===== EXPORTAR CLASES =====
__all__ = [
    'CaesarCipher',
    'VigenereCipher', 
    'PlayfairCipher',
    'KasiskiAnalysis'
]
