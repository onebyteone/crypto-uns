from src.crypto.classic import KasiskiAnalysis

# Probar el análisis de Kasiski
analyzer = KasiskiAnalysis()
# Texto que sabemos que tiene repeticiones
text = 'THEQUICKBROWNFOXJUMPSOVERTHEQUICKBROWNFOXJUMPSOVER'
result = analyzer.analyze(text)
print('Análisis de Kasiski:')
print(f'Repeticiones encontradas: {len(result["repetitions"])}')
for rep in result['repetitions'][:3]:  # Mostrar las primeras 3
    print(f'  Secuencia: {rep["sequence"]}')
    print(f'  Posiciones: {rep["positions"]}')
    print(f'  Distancias: {rep["distances"]}')
    print()
