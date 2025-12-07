import sys
import os
from typing import List, TYPE_CHECKING, Tuple, Any

# Ajusta o caminho de importação
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

if TYPE_CHECKING:
    from package.models.animal import Animal

# Herda da classe Pessoa
from .pessoa import Pessoa

class Cliente(Pessoa):
    """
    Classe Cliente (Herda de Pessoa).
    Adiciona a funcionalidade de possuir uma lista de animais.
    """
    def __init__(self, nome: str, cpf: str, telefone: str, **kwargs):
        # Kwargs permite aceitar ID do banco de dados (BD) sem quebrar o construtor
        super().__init__(nome, cpf, telefone)
        self.animais: List["Animal"] = []
        
        # Adicionando a persistência (opcional no construtor)
        self.db_id = kwargs.get('db_id') 

    # --- MÉTODOS DE PERSISTÊNCIA ---
    
    def to_db(self) -> Tuple[str, str, str]:
        """Converte o objeto Cliente em uma tupla para inserção SQL."""
        return (self.cpf, self.nome, self.telefone)

    # --- Métodos de POO (Mantidos) ---
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
        
        # List Comprehension para pegar as informações de cada animal
        detalhe_animais = [a.exibir_info() for a in self.animais]
        
        # O join formata a lista para ser exibida em várias linhas
        return f" Animais do cliente {self.nome}:\n - " + "\n - ".join(detalhe_animais)
    