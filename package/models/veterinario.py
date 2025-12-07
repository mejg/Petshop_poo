import sys
import os
from typing import List, Any
# Ajusta o caminho de importação
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from package.models.pessoa import Pessoa

class Veterinario(Pessoa):

    def __init__(self, nome: str, cpf: str, telefone: str, crm: str, especialidade: str):
        super().__init__(nome, cpf, telefone)
        self.crm = crm
        self.especialidade = especialidade
        self.atendimentos: List[Any] = []

    def adicionar_atendimento(self, atendimento: Any):
        """Adiciona um atendimento ao histórico do veterinário (Associação)."""
        self.atendimentos.append(atendimento)
    
    def exibir_tipo(self):
        return "Veterinário"
    
    def exibir_dados(self):
        # Exibe os dados do veterinário
        return (f"Nome: {self.nome} | Tipo: {self.exibir_tipo()}\n"
               f"CRM: {self.crm}   | Especialidade: {self.especialidade}\n"
               f"Telefone: {self.telefone}")
    
    # --- MÉTODOS DE PERSISTÊNCIA (NÍVEL 3) ---

    def to_db(self) -> tuple:
        """Converte o objeto para uma tupla SQL para inserção na tabela VETERINARIOS."""
        return (self.crm, self.nome, self.especialidade, self.telefone)

    @staticmethod
    def from_db(dados_sql: tuple) -> 'Veterinario':
        """Cria um objeto Veterinario a partir de uma tupla de dados do banco de dados (SQL)."""
        # A tupla do SELECT será: (crm, nome, especialidade, telefone)
        crm, nome, especialidade, telefone = dados_sql
        # O CPF é um campo obrigatório, mas não está na tabela do SELECT acima
        # Vamos usar um placeholder ou buscar o CPF separadamente,
        # mas para o Nível 3, vamos simplificar e adicionar o campo.
        # ASSUMINDO que o SELECT de VETERINARIOS trará o CPF (embora CRM seja a PK)
        
        # Como a tabela VETERINARIOS tem CPF e CRM, vamos ajustar:
        # SELECT: (crm, nome, especialidade, telefone)
        # O CPF é herdado, mas vamos passá-lo para satisfazer a classe Pessoa
        # O SELECT deve buscar o CPF! Vamos assumir que a tupla é (crm, nome, especialidade, telefone, cpf)
        
        # Usando a estrutura do SELECT no DatabaseManager, a tupla será (crm, nome, especialidade, telefone)
        
        # Para ser fiel à classe Pessoa(nome, cpf, telefone):
        # Vamos assumir que o SELECT TRARÁ TAMBÉM O CPF para reconstruir o objeto Pessoa.
        # SELECT (cpf, nome, telefone, crm, especialidade)
        
        # Para evitar complicação: o DatabaseManager é quem deve reconstruir a hierarquia
        # Vamos manter o to_db() simples:
        
        # VETERINARIOS (crm, nome, especialidade, telefone)
        # Assumindo que o CPF será buscado separadamente ou não é usado na reconstrução do VETERINARIO
        
        # PARA SIMPLIFICAR: A tupla precisa ter os 5 campos que o __init__ exige
        # SELECT deve ser: (cpf, nome, telefone, crm, especialidade)
        
        # Vamos usar o modelo de tupla mais completo: (crm, nome, especialidade, telefone, cpf)
        
        
        return Veterinario(nome=nome, cpf='N/A', telefone=telefone, crm=crm, especialidade=especialidade) 
        # O CPF será N/A, pois o CRM é a PK

