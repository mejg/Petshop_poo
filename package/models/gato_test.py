import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from package.models.gato import Gato

gato_teste = Gato(
    nome = "Mimi",
    raca = "Siamês",
    idade = 7,
    peso = 7.8
)

print (f"\nAnimal cadrastado: \n{gato_teste.exibir_info()}")
print (f"Custo banho: R$ {gato_teste.calcular_banho_tosa()}")
print (f"Custo consulta: R$ {gato_teste.calcular_consulta()}\n")

"""
RETONARÁ:
Animal cadrastado: 
Nome: Mimi  |  Espécie: gato  
Raça: Siamês  |  Idade: 7 anos 
Risco Veterinário: MÉDIO (risco de sobrepeso/mobilidade)
Custo banho: R$ 70
Custo consulta: R$ 130
"""