from typing import Any, Tuple
from package.models.animal import Animal


class Gato(Animal):
    def __init__(self, nome: str, raca: str, idade: int, peso: float, dono_cpf: str = None, db_id: Any = None):
        super().__init__(nome, raca, "Gato", idade, peso, dono_cpf, db_id)
        self.db_id = None

    @staticmethod
    def from_db(dados_tuple: Tuple[Any, ...]) -> 'Gato': 
        db_id, nome, raca, especie, idade, peso, dono_cpf = dados_tuple
        gato = Gato(nome, raca, idade, peso, dono_cpf)
        gato.db_id = db_id
        return gato
    

    def necessidade_veterinaria(self):
        
        if self.peso > 7.0 and self.idade >= 12:
            return f"ALTO (sobrepeso/idoso)"
        if self.idade >= 12:
            return f"ALTO (idoso, prioridade no atendimento)"
        if self.peso > 7.0:
            return f"MÉDIO (risco de sobrepeso/mobilidade)"
        
        else:
            return "BAIXO (rotina)"
        
    def calcular_banho_tosa(self):
        custo = 40 
        if self.idade >= 12:
            custo += 20
        if self.peso >= 7.0:
            custo += 30
        return custo
    
    def calcular_consulta(self):
        custo = 100
        if self.idade >= 12:
            custo += 20
        if self.peso >= 7.0:
            custo += 30
        return custo

    def exibir_info(self):
        risco = self.necessidade_veterinaria()
        info_base = super().exibir_info()
        return (f"{info_base} \n"
                f"Risco Veterinário: {risco}")

     