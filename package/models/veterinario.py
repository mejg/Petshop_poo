import sys
import os
from typing import List, Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from package.models.pessoa import Pessoa

class Veterinario(Pessoa):

    def __init__(self, nome: str, cpf: str, telefone: str, crm: str, especialidade: str):
        super().__init__(nome, cpf, telefone)
        self.crm = crm
        self.especialidade = especialidade
        self.atendimentos: List[Any] = []

    def adicionar_atendimento(self, atendimento: Any):

        self.atendimentos.append(atendimento)
    
    def exibir_tipo(self):
        return "Veterinário"
    
    def exibir_dados(self):
   
        return (f"Nome: {self.nome} | Tipo: {self.exibir_tipo()}\n"
               f"CRM: {self.crm}   | Especialidade: {self.especialidade}\n"
               f"Telefone: {self.telefone}")
    

    def to_db(self) -> tuple:

        return (self.crm, self.nome, self.especialidade, self.telefone)

    @staticmethod
    def from_db(dados_sql: tuple) -> 'Veterinario':

        crm, nome, especialidade, telefone = dados_sql
        