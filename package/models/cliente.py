import sys
import os
from typing import List, TYPE_CHECKING, Tuple, Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

if TYPE_CHECKING:
    from package.models.animal import Animal

from .pessoa import Pessoa

class Cliente(Pessoa):
   
    def __init__(self, nome: str, cpf: str, telefone: str, **kwargs):

        super().__init__(nome, cpf, telefone)
        self.animais: List["Animal"] = []
        
        self.db_id = kwargs.get('db_id') 

    
    def to_db(self) -> Tuple[str, str, str]:

        return (self.cpf, self.nome, self.telefone)

    def exibir_tipo(self) -> str:
        return "Cliente"
    
    def exibir_dados(self) -> str:
        return (
                f"Nome: {self.nome} | CPF: {self.cpf}\n"
                f"Telefone de contato: {self.telefone}"
        )
    
    def adicionar_animal(self, animal: "Animal"):
        self.animais.append(animal)
        print(f"Animal {animal.nome} adicionado ao cliente {self.nome}.")

    def listar_animais(self) -> str:
        if not self.animais:
            return f" O cliente {self.nome} não possui animais cadastrados."
        
        detalhe_animais = [a.exibir_info() for a in self.animais]
        
        return f" Animais do cliente {self.nome}:\n - " + "\n - ".join(detalhe_animais)
    