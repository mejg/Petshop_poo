import sys
import os

sys.path.insert (0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from package.models.veterinario import Veterinario

veterninario_teste = Veterinario(
    nome = "Karollyna Lima",
    cpf = "000.111.222-33",
    telefone = "61 9209-1388",
    crm = "123456/DF",
    especialidade = "Clínica geral"
)

print (f"\nPessoa cadastrada:\n {veterninario_teste.exibir_dados()}") 
print (f"Exibir tipo: {veterninario_teste.exibir_tipo()}")

"""
RETORNARÁ:

Pessoa cadastrada:
 Nome: Karollyna Lima
CRM: 123456/DF   | Especialidade: Clínica geral
Exibir tipo: Veterinário
"""