import sys
import os
from abc import ABC, abstractmethod
from typing import Tuple, Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

class Animal(ABC):

    def __init__(self, nome: str, raca: str, especie: str, idade: int, peso: float, dono_cpf: str = None, db_id: any = None):
        
        self.nome = nome
        self.raca = raca
        self.especie = especie
        self.idade = idade
        self.peso = peso
        
        self.dono_cpf = dono_cpf 
        self.db_id = db_id       
    
    def to_db(self) -> Tuple[str, str, str, int, float, str]:

        return (self.nome, self.raca, self.especie, self.idade, self.peso, self.dono_cpf)

    @staticmethod
    def from_db(dados_sql: Tuple[Any, ...]) -> 'Animal':
    
        raise NotImplementedError("A reconstrução do objeto deve ser feita nas classes Cachorro ou Gato.")
        
    
    @abstractmethod
    def necessidade_veterinaria(self) -> str:
        pass

    @abstractmethod
    def calcular_consulta(self) -> float:
        pass

    @abstractmethod
    def calcular_banho_tosa(self) -> float:
        pass

    def exibir_info(self) -> str:

        return (f"Nome: {self.nome} | Espécie: {self.especie} | ID_BD: {self.db_id if self.db_id else 'Novo'}\n"
                f"Raça: {self.raca} | Idade: {self.idade} anos | Peso: {self.peso} kg")
    
    def __str__(self) -> str:
        return f"Nome: {self.nome} ({self.especie})"


