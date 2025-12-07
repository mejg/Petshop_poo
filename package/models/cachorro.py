from typing import Any, Tuple
from package.models.animal import Animal


class Cachorro(Animal):
    def __init__(self, nome: str, raca: str, idade: int, peso: float, dono_cpf: str = None, db_id: Any = None):
        super().__init__(nome, raca, "Cachorro", idade, peso, dono_cpf, db_id)
        self.db_id = None

    @staticmethod
    def from_db(dados_tuple: Tuple[Any, ...]) -> 'Cachorro':

        db_id, nome, raca, especie, idade, peso, dono_cpf = dados_tuple
        cachorro = Cachorro(nome, raca, idade, peso, dono_cpf)
        cachorro.db_id = db_id
        return cachorro

    def necessidade_veterinaria(self):
        if self.peso > 40.00 and self.idade >= 10:
            return f"ALTO (sobrepeso/idoso)"
        if self.idade >= 10:
            return f"ALTO (idoso, prioridade no atendimento)"
        if self.peso > 40.00:
            return f"MÉDIO (risco de sobrepeso/mobilidade)"
        else:
            return "BAIXO (rotina)"
    
    def validar_necessidade_veterinaria(self):
        return self.necessidade_veterinaria()
        
    def calcular_banho_tosa(self):
        custo = 50.0  
        if self.idade >= 10:
            custo += 20.50

        if self.peso > 40.0 and self.idade >= 10:
            custo += 60.99  

        elif self.peso >= 40:
            custo += 40.39 
            
        return custo
      
    def calcular_consulta(self):
        custo = 100.0 
        
        if self.idade >= 10:
            custo += 30.0  

        if self.peso >= 40:
            custo += 50.0  
            
        return custo  
    
    def exibir_info(self):
        risco = self.necessidade_veterinaria()
        info_base = super().exibir_info()
        return (f"{info_base} \n"
                f"Risco Veterinário: {risco}")