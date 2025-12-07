import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from package.models.cachorro import Cachorro

cachorro_teste = Cachorro(
    nome = "Susy",
    raca = "poodle",
    idade = 18,
    peso = 23.1
)

print (f"\nAnimal cadrastado: \n{cachorro_teste.exibir_info()}")
print (f"Custo banho: R$ {cachorro_teste.calcular_banho_tosa()}")
print (f"Custo consulta: R$ {cachorro_teste.calcular_consulta()}\n")

"""
RETORNARÁ:
Animal cadrastado: 
Nome: Susy  |  Espécie: cachorro  
Raça: poodle  |  Idade: 18 anos 
Risco Veterinário: ALTO (idoso, prioridade no atendimento)
Custo banho: R$ 70.5
Custo consulta: R$ 130.0
"""