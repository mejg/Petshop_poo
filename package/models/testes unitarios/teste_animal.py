# Este teste prova que não podemos instanciar a classe abstrata Pessoa
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from package.models.animal import Animal

print("--- Teste de Abstração: Classe Animal ---")
try:
    # Tentar criar um objeto (DEVE FALHAR)
    animal_teste = Animal("Mimi", "indefinida", "123", "5", "5.0")
except TypeError as e:
    # A captura deste erro prova que a Abstração funcionou
    print(f"Não foi possível instanciar a classe Animal (Abstrata).")
    print(f"Erro esperado: {e}")
except Exception as e:
    print(f"Falha inesperada: {e}")
