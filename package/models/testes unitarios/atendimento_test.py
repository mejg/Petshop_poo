import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from package.models.atendimento import Atendimento
from package.models.cliente import Cliente
from package.models.veterinario import Veterinario
from package.models.cachorro import Cachorro

cliente1 = Cliente("Reginaldo Guimarães", "000.111.222-33", "4002-8922")
cachorro = Cachorro("Aurora", "poodle", 11, 40.5)
veterinario1 = Veterinario("Isabelly Dantas", "000.000.000-00","4002-8922", "123456/DF", "Clinica geral")

atendimento = Atendimento(
    cliente = cliente1,
    animal = cachorro,
    veterinario = veterinario1, 
    servicos = ["consulta", "banho e tosa"],
    data_agendada = "16/10/2025 14:00"
)
atendimento.adicionar_procedimento("Corte unhas")
atendimento.adicionar_procedimento("Vacinação")

print(atendimento.exibir_resumo())
