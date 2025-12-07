import sqlite3
import json
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_file='petshop.db'):
        self.db_file = db_file
        self.criar_tabelas()
    
    def criar_tabelas(self):

        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                cpf TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                telefone TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS veterinarios (
                crm TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                cpf TEXT,
                telefone TEXT,
                especialidade TEXT
            )
        ''')
        
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
    
    def insert_cliente(self, cliente):

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
  
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT cpf, nome, telefone FROM clientes')
        clientes = cursor.fetchall()
        conn.close()
        return clientes
    
  
    def insert_veterinario(self, veterinario):

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

        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT crm, nome, especialidade, telefone FROM veterinarios')
        vets = cursor.fetchall()
        conn.close()
        return vets
    
    def insert_animal(self, animal):

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

        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome, raca, especie, idade, peso, cpf_dono FROM animais WHERE cpf_dono = ?', (cpf,))
        animais = cursor.fetchall()
        conn.close()
        return animais
    
    def insert_atendimento(self, atendimento):

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

        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT id, cpf_cliente, crm_veterinario, id_animal, servicos, procedimentos, data_agendada, custo_total FROM atendimentos')
        atendimentos = cursor.fetchall()
        conn.close()
        return atendimentos
    
    def update_atendimento_procedimentos(self, atendimento_id, procedimentos, novo_custo):

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
        
    def export_clientes_to_json(self, filename= 'clientes.json'):

        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute('SELECT cpf, nome, telefone FROM clientes')
        rows = cur.fetchall()
        clientes = [{"cpf": r[0], "nome": r[1], "telefone": r[2]} for r in rows]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(clientes, f, ensure_ascii=False, indent=2)
        return filename
    
    def export_veterinarios_to_json(self, filename= 'veterinarios.json'):

        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute('SELECT crm, nome, cpf, telefone, especialidade FROM veterinarios')
        rows = cur.fetchall()
        veterinarios = [{"crm": r[0], "nome": r[1], "cpf": r[2], "telefone": r[3], "especialidade": r[4]} for r in rows]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(veterinarios, f, ensure_ascii=False, indent=2)
        return filename
    
    def export_animais_to_json(self, filename= 'animais.json'):
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute('SELECT id, nome, raca, especie, idade, peso, cpf_dono FROM animais')
        rows = cur.fetchall()
        animais = [{"id": r[0], "nome": r[1], "raca": r[2], "especie": r[3], "idade": r[4], "peso": r[5], "cpf_dono": r[6]} for r in rows]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(animais, f, ensure_ascii=False, indent=2)
        return filename
    
    def export_atendimentos_to_json(self, filename= 'atendimentos.json'):
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute('SELECT id, cpf_cliente, crm_veterinario, id_animal, servicos, procedimentos, data_agendada, custo_total FROM atendimentos')
        rows = cur.fetchall()
        atendimentos = []
        for r in rows:
            atendimentos.append({
                "id": r[0],
                "cpf_cliente": r[1],
                "crm_veterinario": r[2],
                "id_animal": r[3],
                "servicos": json.loads(r[4]),
                "procedimentos": json.loads(r[5]) if r[5] else [],
                "data_agendada": r[6],
                "custo_total": r[7]
            })
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(atendimentos, f, ensure_ascii=False, indent=2)
        return filename
    
    def export_all_to_json(self, directory='exports'):
        Path(directory).mkdir(parents=True, exist_ok=True)
        clientes_file = self.export_clientes_to_json(str(Path(directory) / 'clientes.json'))
        veterinarios_file = self.export_veterinarios_to_json(str(Path(directory) / 'veterinarios.json'))
        animais_file = self.export_animais_to_json(str(Path(directory) / 'animais.json'))
        atendimentos_file = self.export_atendimentos_to_json(str(Path(directory) / 'atendimentos.json'))
        return {
            "clientes": clientes_file,
            "veterinarios": veterinarios_file,
            "animais": animais_file,
            "atendimentos": atendimentos_file
        }