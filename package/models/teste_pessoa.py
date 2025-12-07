# Este teste prova que não podemos instanciar a classe abstrata Pessoa
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from package.models.pessoa import Pessoa

print("--- Teste de Abstração: Classe Pessoa ---")
try:
    # Tentar criar um objeto Pessoa genérico (DEVE FALHAR)
    pessoa_teste = Pessoa("Maria", "999.999.999-99", "123")
except TypeError as e:
    # A captura deste erro prova que a Abstração funcionou
    print(f"Não foi possível instanciar a classe Pessoa (Abstrata).")
    print(f"Erro esperado: {e}")
except Exception as e:
    print(f"Falha inesperada: {e}")
