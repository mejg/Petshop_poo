from abc import ABC, abstractmethod

class Pessoa(ABC):

    def __init__(self, nome, cpf, telefone):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone

    @abstractmethod
    def exibir_tipo(self):
        pass
    
    @abstractmethod
    def exibir_dados(self):
        pass
    
    def __str__(self):
        return f'Nome: {self.nome}, CPF: {self.cpf}'
    
   
    
   