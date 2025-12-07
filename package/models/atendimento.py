from datetime import datetime
from typing import List, TYPE_CHECKING, Any 


if TYPE_CHECKING:
    from .cliente import Cliente
    from .veterinario import Veterinario
    from .animal import Animal

class Atendimento: 
    def __init__(self, cliente: "Cliente", animal: "Animal", veterinario: "Veterinario" = None, 
                 servicos: List[str] = None, data_agendada: str = None, hora_agendada: str = None, db_id: Any = None):
        
    
        self.cliente = cliente
        self.animal = animal
        self.veterinario = veterinario
        self.data_agendada = data_agendada
        self.hora_agendada = hora_agendada
        
        self.data_registro = datetime.now().strftime("%d/%m/%Y %H:%M:%S") 
        self.data_agendada = data_agendada

        self.servicos_solicitados = [s.lower() for s in servicos] if servicos else []
        self.procedimentos: List[str] = [] 
        self.db_id = db_id

    def adicionar_procedimento(self, procedimento: str):
        self.procedimentos.append(procedimento)

    def calcular_total(self):
        custo_total = 0.0

        if 'consulta' in self.servicos_solicitados:
            custo_total += self.animal.calcular_consulta()
        
        if 'banho' in self.servicos_solicitados or 'tosa' in self.servicos_solicitados or 'banho e tosa' in self.servicos_solicitados:
            custo_total += self.animal.calcular_banho_tosa()

        custo_total += 20.00 * len(self.procedimentos)

        return custo_total

    def exibir_resumo(self):
        total = self.calcular_total()
        
        procs_str = "\n - " + "\n - ".join(self.procedimentos) if self.procedimentos else "Nenhum procedimento extra."
        
        vet_nome = self.veterinario.nome if self.veterinario else "Não atribuído"
        vet_crm = getattr(self.veterinario, "crm", "N/A")

        return (
                f"--- AGENDAMENTO ----\n"
                f"DATA REGISTRO: {self.data_registro}   | DATA AGENDADA: {self.data_agendada}\n"
                f"DONO: {self.cliente.nome}   | CPF: {self.cliente.cpf}\n"
                f"ANIMAL: {self.animal.nome}   | ESPÉCIE: {self.animal.especie}   | RAÇA: {self.animal.raca}\n"
                f"VETERINÁRIO: {vet_nome}   | CRM: {vet_crm}\n"
                f"SERVIÇOS SOLICITADOS: {', '.join(self.servicos_solicitados).title()}\n"
                f"RISCO VETERINÁRIO: {self.animal.necessidade_veterinaria()}\n\n"
                f"PROCEDIMENTOS EXTRAS: {procs_str}\n"
                f"CUSTO TOTAL FINAL: R$ {total:.2f}\n"
                f"------------------------------------------------------"
        )
