import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from package.models.cliente import Cliente
from package.models.gato import Gato

cliente_teste = Cliente(
    nome = "Jéssica Guimarães",
    cpf = "000.111.222-33",
    telefone = "4002-8922"
)

print(f"\nPessoa cadastrada: \n{cliente_teste.exibir_dados()}")
print(f"Exibir tipo: {cliente_teste.exibir_tipo()} ")

gato_teste = Gato("Aurora", "Siamês", 5, 4.5)
cliente_teste.adicionar_animal(gato_teste)

gato2 = Gato("Preguicinha", "Indefinida", 13, 12)
cliente_teste.adicionar_animal(gato2)

print("\n2. Animais do Cliente:")
print(cliente_teste.listar_animais())
