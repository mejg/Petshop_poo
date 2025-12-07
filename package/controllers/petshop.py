import sys
import os
import json
from typing import Dict, Any, List

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from package.models.cliente import Cliente
from package.models.veterinario import Veterinario
from package.models.cachorro import Cachorro
from package.models.gato import Gato
from package.models.atendimento import Atendimento

from package.controllers.database_manager import DatabaseManager

class PetShopController:
    def __init__(self):

        self.db_manager = DatabaseManager()
        
        self.clientes = []
        self.veterinarios = []
        self.animais = []
        self.atendimentos = []

        self._load_data_from_db()

        self.opcoes_listagem: Dict[str, Any] = {
             '1': self.listar_clientes,
             '2': self.listar_veterinarios,
             '3': self.listar_animais,
             '4': self.listar_atendimentos,
             '5': lambda: True
        }
        
        self.opcoes: Dict[str, Any] = {
            '1': self.menu_cadastros,
            '2': self.menu_agendar_servicos,
            '3': self.listar_dados,
            '4': self.sair
        }

        self.opcoes_cadastros: Dict[str, Any] = {
            '1': self.cadastrar_cliente,
            '2': self.cadastrar_veterinario,
            '3': self.cadastrar_animal,
            '4': lambda: True
        }
        
        self.opcoes_agendamento: Dict[str, Any] = {
            '1': self.agendar_consulta,
            '2': self.agendar_banho_tosa,
            '3': self.adicionar_procedimento_extra,
            '4': lambda: True
        }

    def _load_data_from_db(self):

        print("\n[BD] Carregando dados do disco...")
        
        self.clientes.clear()
        self.veterinarios.clear()
        self.animais.clear()
        self.atendimentos.clear()
        
        clientes_data = self.db_manager.select_all_clientes()
        
        for cpf, nome, telefone in clientes_data:

            cliente = Cliente(nome, cpf, telefone) 
            self.clientes.append(cliente)
            
            animais_data = self.db_manager.select_animal_by_cpf(cpf)
            for db_id, nome_a, raca, especie, idade, peso, dono_cpf in animais_data:

                if especie == 'Cachorro':
                    animal = Cachorro.from_db((db_id, nome_a, raca, especie, idade, peso, dono_cpf))
                elif especie == 'Gato':
                    animal = Gato.from_db((db_id, nome_a, raca, especie, idade, peso, dono_cpf))
                else:
                    continue 
                
                self.animais.append(animal)
                cliente.adicionar_animal(animal) 
        
        vets_data = self.db_manager.select_all_veterinarios()
        for crm, nome, especialidade, telefone in vets_data:

            vet = Veterinario(nome, 'N/A', telefone, crm, especialidade)
            self.veterinarios.append(vet)


        atendimentos_data = self.db_manager.select_all_atendimentos()
        for id_at, cliente_cpf, vet_crm, animal_id, servicos_json, procedimentos_json, data_agendada, custo_total in atendimentos_data:
            

            cliente = self.encontrar_objeto(self.clientes, 'cpf', cliente_cpf)
            veterinario = self.encontrar_objeto(self.veterinarios, 'crm', vet_crm) if vet_crm else None
            animal = self.encontrar_objeto(self.animais, 'db_id', animal_id)
            
            if cliente and animal:
                atendimento = Atendimento(
                    cliente=cliente,
                    animal=animal,
                    veterinario=veterinario,
                    servicos=json.loads(servicos_json),
                    data_agendada=data_agendada,
                    db_id=id_at 
                )
                atendimento.procedimentos = json.loads(procedimentos_json)
                self.atendimentos.append(atendimento)
                if veterinario:
                    veterinario.adicionar_atendimento(atendimento)
        

    def validar_numero(self, prompt: str, tipo: type = float):
        while True:
            try:
                valor = input(prompt)
                return tipo(valor)
            except ValueError:
                print("ERRO DE VALIDAÇÃO: Por favor insira apenas números.")

    def validar_vazio(self, prompt: str):
        while True:
            valor = input(prompt).strip()
            if valor:
                return valor
            print("ERRO DE VALIDAÇÃO: Este campo não pode ficar vazio.")

    def _normalize_cpf(self, cpf: str) -> str:
        if cpf is None:
            return cpf
        return ''.join(ch for ch in cpf if ch.isdigit())

    def encontrar_objeto(self, lista: list, atributo: str, valor: str):
        for obj in lista:
            # Normaliza CPF ao comparar para evitar diferenças de formatação
            if atributo == 'cpf':
                obj_cpf = getattr(obj, atributo, None)
                if obj_cpf is not None and valor is not None:
                    if self._normalize_cpf(obj_cpf) == self._normalize_cpf(valor):
                        return obj
            else:
                if getattr(obj, atributo, None) == valor:
                    return obj
        return None
    
    def menu_principal(self):
        output = True
        while output:
            print("\n -------- PET SHOP -------")
            print("1. Cadastros (Clientes, Veterinários, Animais)")
            print("2. Agendar Serviço (Consulta, Banho/Tosa)")
            print("3. Listar Dados")
            print("4. Sair")
            escolha = input("Escolha uma opção: ")

            acao = self.opcoes.get(escolha, self.default)
            output = acao()

    def menu_cadastros(self):
        while True:
            print("\n ------ MENU CADASTROS ------")
            print("1. Cadastrar Cliente")
            print("2. Cadastrar Veterinário")
            print("3. Cadastrar Animal")
            print("4. Voltar ao Menu Principal")
            escolha = input("Escolha uma opção: ")
            acao = self.opcoes_cadastros.get(escolha)
            
            if acao:
                if escolha == '4':
                    return True
                acao()
            else:
                self.default()
    
    def menu_agendar_servicos(self):

        while True:
            print("\n ------- AGENDAR SERVIÇOS -------")
            print("1. Agendar Consulta")
            print("2. Agendar Banho e Tosa")
            print("3. Adicionar Procedimento Extra (a um atendimento existente)")
            print("4. Voltar ao Menu Principal")
            escolha = input("Escolha uma opção: ")

            acao = self.opcoes_agendamento.get(escolha)
            
            if acao:
                if escolha == '4':
                    return True 
                acao()
            else:
                self.default()

    def cadastrar_cliente(self):
        print("\n ------- NOVO CLIENTE (Persistência SQL) ------- ")
        nome = self.validar_vazio("Nome do Cliente: ")
        cpf_raw = self.validar_vazio("CPF: ")
        cpf = self._normalize_cpf(cpf_raw)
        telefone = self.validar_vazio("Telefone: ")

        novo_cliente = Cliente(nome, cpf, telefone)
        
        if self.db_manager.insert_cliente(novo_cliente):
            self.clientes.append(novo_cliente)
            self.db_manager.export_all_to_json()
            print(f"\nSucesso! Cliente '{nome}' cadastrado e SALVO.")
        else:
            print("\nERRO: Falha ao salvar no banco de dados. Cliente pode já existir.")

    def cadastrar_veterinario(self):
        print("\n ------- NOVO VETERINÁRIO (Persistência SQL) -------")
        nome = self.validar_vazio("Nome do Veterinário: ")
        cpf_raw = self.validar_vazio("CPF: ")
        cpf = self._normalize_cpf(cpf_raw)
        telefone = self.validar_vazio("Telefone: ")
        crm = self.validar_vazio("CRM: ")
        especialidade = self.validar_vazio("Especialidade: ")

        novo_vet = Veterinario(nome, cpf, telefone, crm, especialidade)

        if self.db_manager.insert_veterinario(novo_vet):
            self.veterinarios.append(novo_vet)
            self.db_manager.export_all_to_json()
            print(f"\nSucesso! Veterinário '{nome}' cadastrado e SALVO.")
        else:
            print("\nERRO: Falha ao salvar no banco de dados. CRM pode já existir.")

    def cadastrar_animal(self):
        print("\n ------- NOVO ANIMAL (Persistência SQL) -------")
        nome = self.validar_vazio("Nome do animal: ")
        raca = self.validar_vazio("Raça: ")
        especie_input = self.validar_vazio("Espécie (Cachorro/Gato): ").strip().lower()
        especie = especie_input.capitalize()
        idade = self.validar_numero("Idade: ", int)
        peso = self.validar_numero("Peso (kg): ", float)
        cpf_dono_raw = self.validar_vazio("CPF do dono: ")
        cpf_dono = self._normalize_cpf(cpf_dono_raw)

        cliente_dono = self.encontrar_objeto(self.clientes, 'cpf', cpf_dono)

        if not cliente_dono:
            print("Cliente não encontrado na memória. Cadastre-o primeiro.")
            return

        if especie == 'Cachorro':
            novo_animal = Cachorro(nome, raca, idade, peso, dono_cpf=cpf_dono)
        elif especie == 'Gato':
            novo_animal = Gato(nome, raca, idade, peso, dono_cpf=cpf_dono)
        else:
            print("Espécie inválida. Apenas Cachorro ou Gato. \nTente novamente.")
            return

 
        animal_id = self.db_manager.insert_animal(novo_animal)

        if animal_id:
            novo_animal.db_id = animal_id 
            self.animais.append(novo_animal)
            cliente_dono.adicionar_animal(novo_animal)
            print(f"\nSucesso! Animal '{nome}' cadastrado e SALVO no BD (ID: {animal_id}).")
        else:
            print("\nERRO: Falha ao salvar o Animal no Banco de Dados.")


    def _obter_dados_agendamento(self, servico_tipo: str) -> Dict[str, Any] | None:
 
        if not self.clientes or not self.animais:
            print("\nERRO: Cadastre pelo menos 1 Cliente e 1 Animal antes de agendar.")
            return None

        cpf_cliente = self.validar_vazio("CPF do Cliente: ")
        cliente_dono = self.encontrar_objeto(self.clientes, 'cpf', cpf_cliente)
        if not cliente_dono:
            print("Cliente não encontrado. Operação cancelada.")
            return None
        
        if not cliente_dono.animais:
            print("Cliente não possui animais cadastrados.")
            return None

        print("\nAnimais do Cliente:")
        for i, animal in enumerate(cliente_dono.animais):

            print(f"{i+1}. {animal.nome} ({animal.raca}) - Risco: {animal.necessidade_veterinaria()}")
            
        escolha_animal = self.validar_numero("Escolha o número do animal: ", int)
        if escolha_animal < 1 or escolha_animal > len(cliente_dono.animais):
            print("Escolha inválida. Operação cancelada.")
            return None
        animal_selecionado = cliente_dono.animais[escolha_animal - 1]

        data_agendada = self.validar_vazio(f"Data do {servico_tipo} (DD/MM/AAAA): ")
        hora_agendada = self.validar_vazio(f"Hora do {servico_tipo} (HH:MM): ")
        
        return {
            'cliente': cliente_dono,
            'animal': animal_selecionado,
            'data_agendada': f"{data_agendada} {hora_agendada}"
        }

    def agendar_consulta(self):
        dados = self._obter_dados_agendamento("Consulta")
        if not dados:
            return True

        crm_vet = self.validar_vazio("CRM do Veterinário responsável: ")
        veterinario_responsavel = self.encontrar_objeto(self.veterinarios, 'crm', crm_vet)
        if not veterinario_responsavel:
            print("Veterinário não encontrado. Operação cancelada.")
            return True

        novo_atendimento = Atendimento(
            cliente=dados['cliente'], 
            animal=dados['animal'], 
            veterinario=veterinario_responsavel, 
            servicos=["Consulta"], 
            data_agendada=dados['data_agendada']
        )
        
        if self.db_manager.insert_atendimento(novo_atendimento):

            self.atendimentos.append(novo_atendimento)
            veterinario_responsavel.adicionar_atendimento(novo_atendimento)
            self.db_manager.export_all_to_json()
            print("\nConsulta agendada e SALVA com sucesso!")
            print(novo_atendimento.exibir_resumo())
        else:
            print("\nERRO: Falha ao salvar atendimento no Banco de Dados.")
        return True 

    def agendar_banho_tosa(self):
        dados = self._obter_dados_agendamento("Banho e Tosa")
        if not dados:
            return True

        servicos_beleza_raw = self.validar_vazio("Serviço de Beleza (Ex: 'Banho', 'Tosa', ou 'Ambos'): ").lower()
        
        servicos_solicitados = []
        if 'banho' in servicos_beleza_raw:
            servicos_solicitados.append('Banho')
        if 'tosa' in servicos_beleza_raw or 'ambos' in servicos_beleza_raw:
            servicos_solicitados.append('Tosa')
            
        if not servicos_solicitados:
            print("Serviço inválido. Operação cancelada.")
            return True

        novo_atendimento = Atendimento(
            cliente=dados['cliente'], 
            animal=dados['animal'], 
            veterinario=None, 
            servicos=servicos_solicitados, 
            data_agendada=dados['data_agendada']
        )
        
        if self.db_manager.insert_atendimento(novo_atendimento):
            self.atendimentos.append(novo_atendimento)
            self.db_manager.export_all_to_json()
            print("\nBanho e Tosa agendado e SALVO com sucesso!")
            print(novo_atendimento.exibir_resumo())
        else:
            print("\nERRO: Falha ao salvar atendimento no Banco de Dados.")
        return True

    def adicionar_procedimento_extra(self):
        print("\n --- Adicionar Procedimento Extra ---")
        
        if not self.atendimentos:
            print("Nenhum atendimento registrado para adicionar extras.")
            return True
            
        print("\nAtendimentos Registrados:")

        for i, at in enumerate(self.atendimentos):
            print(f"{i+1}. {at.animal.nome} - Dono: {at.cliente.nome} ({at.data_agendada})")
        
        escolha_atendimento = self.validar_numero("Escolha o número do atendimento para modificar: ", int)
        if escolha_atendimento < 1 or escolha_atendimento > len(self.atendimentos):
            print("Escolha inválida.")
            return True
            
        atendimento_selecionado = self.atendimentos[escolha_atendimento - 1]
        
        procedimento = self.validar_vazio("Descrição do Procedimento Extra: ")
        atendimento_selecionado.adicionar_procedimento(procedimento)
        
        novo_custo = atendimento_selecionado.calcular_total()
        
        if self.db_manager.update_atendimento_procedimentos(atendimento_selecionado.db_id, atendimento_selecionado.procedimentos, novo_custo):
            print(f"\nProcedimento adicionado e CUSTO ATUALIZADO no BD!")
            print("Novo Resumo:")
            print(atendimento_selecionado.exibir_resumo())
        else:
            print("ERRO: Falha ao atualizar o procedimento no Banco de Dados.")

        return True
    
    def listar_dados(self):

        while True:
            print("\n--- Menu de Listagem ---")
            print("1. Listar Clientes")
            print("2. Listar Veterinários")
            print("3. Listar Animais")
            print("4. Listar Atendimentos")
            print("5. Voltar ao Menu Principal")
            escolha = input("Escolha uma opção: ")
            
            acao = self.opcoes_listagem.get(escolha)
            if acao:
                if escolha == '5':
                    return True
                acao()
            else:
                self.default()
    
    def listar_clientes(self):
        print("\n--- Listagem de Clientes ---")
        if not self.clientes:
            print("Nenhum cliente cadastrado.")
            return
        for i, cliente in enumerate(self.clientes):
            print(f"\n{i+1}. {cliente.exibir_dados()}")
            print(cliente.listar_animais())

    def listar_veterinarios(self):
        print("\n--- Listagem de Veterinários ---")
        if not self.veterinarios:
            print("Nenhum veterinário cadastrado.")
            return
        for i, vet in enumerate(self.veterinarios):
            print(f"\n{i+1}. {vet.exibir_dados()}")
            print(f"   Atendimentos Registrados: {len(vet.atendimentos)}")
    
    def listar_animais(self):
        print("\n--- Listagem de Animais ---")
        if not self.animais:
            print("Nenhum animal cadastrado.")
            return
        for i, animal in enumerate(self.animais):
            print(f"\n{i+1}. {animal.exibir_info()}")

    def listar_atendimentos(self):
        print("\n--- Histórico de Atendimentos ---")
        if not self.atendimentos:
            print("Nenhum atendimento agendado.")
            return
        for i, atendimento in enumerate(self.atendimentos):
            print(f"\n--- ATENDIMENTO #{i+1} ---")
            print(atendimento.exibir_resumo())

    def default(self):

        print("Opção inválida. Tente novamente.")
        return True

    def sair(self):

        print("\nSaindo do sistema. Até logo!")
        return False
        for i, atendimento in enumerate(self.atendimentos):
            print(f"\n--- ATENDIMENTO #{i+1} ---")
            print(atendimento.exibir_resumo())

    def exportar_dados(self):
        arquivos = self.db_manager.export_all_to_json('.', 'backup')
        print("[EXPORT] Arquivos gerados:", arquivos)
        return True