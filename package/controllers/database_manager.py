import sqlite3
import json
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_file='petshop.db'):
        self.db_file = db_file
        self.criar_tabelas()
    
    def criar_tabelas(self):
        """Cria todas as tabelas necessárias."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Tabela Clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                cpf TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                telefone TEXT NOT NULL
            )
        ''')
        
        # Tabela Veterinários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS veterinarios (
                crm TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                cpf TEXT,
                telefone TEXT,
                especialidade TEXT
            )
        ''')
        
        # Tabela Animais
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS animais (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                raca TEXT NOT NULL,
                especie TEXT NOT NULL,
                idade INTEGER,
                peso REAL,
                cpf_dono TEXT NOT NULL,
                FOREIGN KEY(cpf_dono) REFERENCES clientes(cpf)
            )
        ''')
        
        # Tabela Atendimentos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS atendimentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cpf_cliente TEXT NOT NULL,
                crm_veterinario TEXT,
                id_animal INTEGER NOT NULL,
                servicos TEXT NOT NULL,
                procedimentos TEXT,
                data_agendada TEXT,
                custo_total REAL,
                FOREIGN KEY(cpf_cliente) REFERENCES clientes(cpf),
                FOREIGN KEY(crm_veterinario) REFERENCES veterinarios(crm),
                FOREIGN KEY(id_animal) REFERENCES animais(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # ========== CLIENTES ==========
    def insert_cliente(self, cliente):
        """Insere um cliente no BD."""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO clientes (cpf, nome, telefone) VALUES (?, ?, ?)',
                (cliente.cpf, cliente.nome, cliente.telefone)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            print(f"Erro: CPF {cliente.cpf} já existe no banco.")
            return False
        except Exception as e:
            print(f"Erro ao inserir cliente: {e}")
            return False
    
    def select_all_clientes(self):
        """Retorna todos os clientes."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT cpf, nome, telefone FROM clientes')
        clientes = cursor.fetchall()
        conn.close()
        return clientes
    
    # ========== VETERINÁRIOS ==========
    def insert_veterinario(self, veterinario):
        """Insere um veterinário no BD."""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO veterinarios (crm, nome, cpf, telefone, especialidade) VALUES (?, ?, ?, ?, ?)',
                (veterinario.crm, veterinario.nome, veterinario.cpf, veterinario.telefone, veterinario.especialidade)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            print(f"Erro: CRM {veterinario.crm} já existe no banco.")
            return False
        except Exception as e:
            print(f"Erro ao inserir veterinário: {e}")
            return False
    
    def select_all_veterinarios(self):
        """Retorna todos os veterinários."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT crm, nome, especialidade, telefone FROM veterinarios')
        vets = cursor.fetchall()
        conn.close()
        return vets
    
    # ========== ANIMAIS ==========
    def insert_animal(self, animal):
        """Insere um animal e retorna o ID gerado."""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO animais (nome, raca, especie, idade, peso, cpf_dono) VALUES (?, ?, ?, ?, ?, ?)',
                (animal.nome, animal.raca, animal.__class__.__name__, animal.idade, animal.peso, animal.dono_cpf)
            )
            conn.commit()
            animal_id = cursor.lastrowid
            conn.close()
            return animal_id
        except Exception as e:
            print(f"Erro ao inserir animal: {e}")
            return None
    
    def select_animal_by_cpf(self, cpf):
        """Retorna todos os animais de um cliente."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome, raca, especie, idade, peso, cpf_dono FROM animais WHERE cpf_dono = ?', (cpf,))
        animais = cursor.fetchall()
        conn.close()
        return animais
    
    # ========== ATENDIMENTOS ==========
    def insert_atendimento(self, atendimento):
        """Insere um atendimento no BD."""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO atendimentos 
                   (cpf_cliente, crm_veterinario, id_animal, servicos, procedimentos, data_agendada, custo_total)
                   VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (
                    atendimento.cliente.cpf,
                    atendimento.veterinario.crm if atendimento.veterinario else None,
                    atendimento.animal.db_id,
                    json.dumps(atendimento.servicos_solicitados),
                    json.dumps(atendimento.procedimentos),
                    atendimento.data_agendada,
                    atendimento.calcular_total()
                )
            )
            conn.commit()
            atendimento_id = cursor.lastrowid
            atendimento.db_id = atendimento_id
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao inserir atendimento: {e}")
            return False
    
    def select_all_atendimentos(self):
        """Retorna todos os atendimentos."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT id, cpf_cliente, crm_veterinario, id_animal, servicos, procedimentos, data_agendada, custo_total FROM atendimentos')
        atendimentos = cursor.fetchall()
        conn.close()
        return atendimentos
    
    def update_atendimento_procedimentos(self, atendimento_id, procedimentos, novo_custo):
        """Atualiza procedimentos e custo de um atendimento."""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE atendimentos SET procedimentos = ?, custo_total = ? WHERE id = ?',
                (json.dumps(procedimentos), novo_custo, atendimento_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao atualizar atendimento: {e}")
            return False