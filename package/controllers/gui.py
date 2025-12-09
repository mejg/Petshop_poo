import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from package.controllers.petshop import PetShopController

class PetShopGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🐾 PetShop - Sistema de Gerenciamento")
        self.root.geometry("1100x750")
        self.root.resizable(True, True)
        self.root.configure(bg='#0f172a')
        try:
            self.root.iconbitmap('petshop.ico')
        except:
            pass

        self.controller = PetShopController()
        self.define_estilos()
        self.criar_menu_principal()

    def define_estilos(self):
        self.cor_primaria = "#7c3aed"
        self.cor_secundaria = "#0ea5e9"
        self.cor_sucesso = "#10b981"
        self.cor_alerta = "#f59e0b"
        self.cor_erro = "#ef4444"
        self.cor_fundo = "#0f172a"
        self.cor_fundo_card = "#1e293b"
        self.cor_texto = "#f1f5f9"
        self.cor_texto_secundario = "#94a3b8"

        self.fonte_titulo = ("Segoe UI", 24, "bold")
        self.fonte_subtitulo = ("Segoe UI", 14, "bold")
        self.fonte_normal = ("Segoe UI", 11)
        self.fonte_botao = ("Segoe UI", 11, "bold")

        style = ttk.Style()
        try:
            style.theme_use('clam')
        except:
            pass

        style.configure('.', background=self.cor_fundo, foreground=self.cor_texto)
        style.map('Primario.TButton',
                 background=[('active', '#6d28d9'), ('pressed', '#5b21b6')])
        style.configure('TCombobox',
                       fieldbackground=self.cor_fundo_card,
                       background=self.cor_fundo_card,
                       foreground=self.cor_texto,
                       selectbackground=self.cor_primaria,
                       selectforeground=self.cor_texto,
                       borderwidth=1,
                       relief='solid')

    def criar_card(self, parent, texto, comando, cor, emoji, largura=300, altura=120):
        card = tk.Frame(parent,
                       bg=cor,
                       width=largura,
                       height=altura,
                       cursor='hand2',
                       relief='flat',
                       highlightthickness=0)

        def on_enter(e):
            card.configure(bg=self.clarear_cor(cor, 12))
            card.config(relief='solid', highlightbackground=self.clarear_cor(cor, 20))

        def on_leave(e):
            card.configure(bg=cor)
            card.config(relief='flat', highlightbackground=cor)

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        card.bind("<Button-1>", lambda e: comando())

        emoji_label = tk.Label(card, text=emoji,
                              font=("Segoe UI Emoji", 28),
                              bg=cor, fg='white')
        emoji_label.place(relx=0.15, rely=0.5, anchor='center')

        texto_label = tk.Label(card, text=texto,
                              font=self.fonte_botao,
                              bg=cor, fg='white',
                              wraplength=180,
                              justify='center')
        texto_label.place(relx=0.65, rely=0.5, anchor='center')

        seta = tk.Label(card, text="→",
                       font=("Segoe UI", 18, "bold"),
                       bg=cor, fg='white')
        seta.place(relx=0.92, rely=0.5, anchor='center')

        # animação simples: mudar cor da seta ao entrar
        def animar_seta_enter(e):
            seta.configure(fg=self.clarear_cor('ffffff', -80))
        def animar_seta_leave(e):
            seta.configure(fg='white')

        card.bind("<Enter>", lambda e: (on_enter(e), animar_seta_enter(e)))
        card.bind("<Leave>", lambda e: (on_leave(e), animar_seta_leave(e)))

        return card

    def criar_botao(self, parent, texto, comando, estilo="primario"):
        if estilo == "primario":
            bg = self.cor_primaria
            fg = 'white'
        elif estilo == "sucesso":
            bg = self.cor_sucesso
            fg = 'white'
        elif estilo == "erro":
            bg = self.cor_erro
            fg = 'white'
        else:
            bg = self.cor_fundo_card
            fg = self.cor_texto

        btn = tk.Button(parent, text=texto, command=comando,
                       font=self.fonte_botao,
                       bg=bg, fg=fg,
                       cursor='hand2',
                       relief='raised',
                       borderwidth=1,
                       padx=30, pady=12,
                       activebackground=self.clarear_cor(bg, 20),
                       activeforeground=fg)

        def on_enter(e):
            btn.configure(bg=self.clarear_cor(bg, 12))

        def on_leave(e):
            btn.configure(bg=bg)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn

    def criar_campo_entrada(self, parent, label_text):
        frame = tk.Frame(parent, bg=self.cor_fundo)

        label = tk.Label(frame, text=label_text,
                        font=("Segoe UI", 10, "bold"),
                        bg=self.cor_fundo,
                        fg=self.cor_texto_secundario)
        label.pack(anchor='w', padx=5)

        entrada = tk.Entry(frame,
                          font=self.fonte_normal,
                          bg=self.cor_fundo_card,
                          fg=self.cor_texto,
                          insertbackground=self.cor_primaria,
                          relief='flat',
                          borderwidth=2,
                          highlightthickness=2,
                          highlightbackground="#334155",
                          highlightcolor=self.cor_primaria)
        entrada.pack(fill='x', padx=5, pady=(0, 15), ipady=8)

        return frame, entrada

    def clarear_cor(self, cor, percentual):
        cor = cor.lstrip('#')
        r, g, b = tuple(int(cor[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, max(0, int(r * (1 + percentual/100))))
        g = min(255, max(0, int(g * (1 + percentual/100))))
        b = min(255, max(0, int(b * (1 + percentual/100))))
        return f'#{r:02x}{g:02x}{b:02x}'

    def limpar_janela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def criar_menu_principal(self):
        self.limpar_janela()
        main_frame = tk.Frame(self.root, bg=self.cor_fundo)
        main_frame.pack(fill=tk.BOTH, expand=True)
        header = tk.Frame(main_frame, bg=self.cor_fundo)
        header.pack(fill='x', padx=40, pady=(30, 10))
        titulo = tk.Label(header, text="🐾 PetCare Manager", font=self.fonte_titulo, bg=self.cor_fundo, fg='white')
        titulo.pack(side='left')
        subtitulo = tk.Label(header, text="Sistema de Gerenciamento Completo",
                             font=("Segoe UI", 12),
                             bg=self.cor_fundo,
                             fg=self.cor_texto_secundario)
        subtitulo.pack(side='left', padx=(15, 0), pady=(8, 0))

        container = tk.Frame(main_frame, bg=self.cor_fundo)
        container.pack(fill='both', expand=True, padx=40, pady=20)

        linha1 = tk.Frame(container, bg=self.cor_fundo)
        linha1.pack(fill='x', pady=(0, 20))

        cards1 = [
            ("Cadastros\nGerenciamento", self.menu_cadastros, self.cor_primaria, "📋"),
            ("Agendar\nServiços", self.menu_agendamento, self.cor_secundaria, "📅"),
            ("Listar\nDados", self.listar_dados_menu, self.cor_sucesso, "📊"),
        ]

        for texto, comando, cor, emoji in cards1:
            card = self.criar_card(linha1, texto, comando, cor, emoji)
            card.pack(side='left', expand=True, fill='both', padx=10)

        linha2 = tk.Frame(container, bg=self.cor_fundo)
        linha2.pack(fill='x')

        cards2 = [
            ("Ajuda e\nSuporte", lambda: messagebox.showinfo("Ajuda", "Sistema PetShop v1.0\n\nContato: suporte@petshop.com"), "#06b6d4", "❓"),
        ]

        for texto, comando, cor, emoji in cards2:
            card = self.criar_card(linha2, texto, comando, cor, emoji)
            card.pack(side='left', expand=True, fill='both', padx=10)

        footer = tk.Frame(main_frame, bg=self.cor_fundo)
        footer.pack(fill='x', padx=40, pady=(20, 30))
        btn_sair = self.criar_botao(footer, "🚪 Sair do Sistema", self.sair_app, "erro")
        btn_sair.pack(side='right')

        status_bar = tk.Frame(main_frame, bg='#1e293b', height=30)
        status_bar.pack(fill='x', side='bottom')
        status_text = tk.Label(status_bar,
                              text=f"🔵 Conectado | Clientes: {len(self.controller.clientes)} | Animais: {len(self.controller.animais)}",
                              font=("Segoe UI", 9),
                              bg='#1e293b',
                              fg=self.cor_texto_secundario)
        status_text.pack(side='left', padx=20)

    def menu_cadastros(self):
        self.limpar_janela()
        main_frame = tk.Frame(self.root, bg=self.cor_fundo)
        main_frame.pack(fill=tk.BOTH, expand=True)
        header = tk.Frame(main_frame, bg=self.cor_fundo)
        header.pack(fill='x', padx=40, pady=(30, 20))
        btn_voltar = self.criar_botao(header, "← Voltar", self.criar_menu_principal)
        btn_voltar.pack(side='left')
        titulo = tk.Label(header, text="📝 Cadastros", font=self.fonte_titulo, bg=self.cor_fundo, fg='white')
        titulo.pack(side='left', padx=(20, 0))

        container = tk.Frame(main_frame, bg=self.cor_fundo)
        container.pack(fill='both', expand=True, padx=40, pady=20)

        cards_frame = tk.Frame(container, bg=self.cor_fundo)
        cards_frame.pack(fill='both', expand=True)

        cadastros = [
            ("👤 Cliente", "Cadastrar novo cliente", self.cadastrar_cliente, self.cor_primaria),
            ("🩺 Veterinário", "Cadastrar novo profissional", self.cadastrar_veterinario, self.cor_secundaria),
            ("🐶 Animal", "Cadastrar novo animal", self.cadastrar_animal, self.cor_sucesso),
        ]

        for i, (emoji, descricao, comando, cor) in enumerate(cadastros):
            card = tk.Frame(cards_frame, bg=self.cor_fundo_card, relief='flat', borderwidth=0)
            card.grid(row=i//2, column=i%2, padx=15, pady=15, sticky='nsew')
            cards_frame.grid_columnconfigure(i%2, weight=1)
            emoji_label = tk.Label(card, text=emoji, font=("Segoe UI Emoji", 32), bg=self.cor_fundo_card, fg='white')
            emoji_label.pack(pady=(20, 10))
            titulo_card = tk.Label(card, text=descricao.split()[0], font=self.fonte_subtitulo, bg=self.cor_fundo_card, fg='white')
            titulo_card.pack()
            desc_label = tk.Label(card, text=descricao, font=("Segoe UI", 9), bg=self.cor_fundo_card, fg=self.cor_texto_secundario, wraplength=200)
            desc_label.pack(pady=(5, 20))
            btn = self.criar_botao(card, "Acessar →", comando)
            btn.pack(pady=(0, 20))

            def criar_hover(card):
                def on_enter(e):
                    card.configure(bg=self.clarear_cor(self.cor_fundo_card, 10))
                def on_leave(e):
                    card.configure(bg=self.cor_fundo_card)
                return on_enter, on_leave

            on_enter, on_leave = criar_hover(card)
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)

    def cadastrar_cliente(self):
        self.limpar_janela()
        main_frame = tk.Frame(self.root, bg=self.cor_fundo)
        main_frame.pack(fill=tk.BOTH, expand=True)
        header = tk.Frame(main_frame, bg=self.cor_fundo)
        header.pack(fill='x', padx=40, pady=(30, 20))
        btn_voltar = self.criar_botao(header, "← Voltar", self.menu_cadastros)
        btn_voltar.pack(side='left')
        titulo = tk.Label(header, text="👤 Novo Cliente", font=self.fonte_titulo, bg=self.cor_fundo, fg='white')
        titulo.pack(side='left', padx=(20, 0))

        card_form = tk.Frame(main_frame, bg=self.cor_fundo_card, relief='flat', borderwidth=0)
        card_form.pack(fill='both', expand=True, padx=40, pady=(0, 40))
        campos_frame = tk.Frame(card_form, bg=self.cor_fundo_card)
        campos_frame.pack(fill='both', expand=True, padx=40, pady=40)

        campos = [
            ("Nome Completo:", "nome"),
            ("CPF:", "cpf"),
            ("Telefone:", "telefone"),
        ]

        entradas = {}
        for label_text, var_name in campos:
            frame_campo, entrada = self.criar_campo_entrada(campos_frame, label_text)
            frame_campo.pack(fill='x', pady=5)
            entradas[var_name] = entrada

        btn_frame = tk.Frame(card_form, bg=self.cor_fundo_card)
        btn_frame.pack(fill='x', padx=40, pady=(0, 30))

        def salvar():
            try:
                nome = entradas['nome'].get().strip()
                cpf = entradas['cpf'].get().strip()
                telefone = entradas['telefone'].get().strip()
                if not nome or not cpf or not telefone:
                    messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                    return
                from package.models.cliente import Cliente
                novo_cliente = Cliente(nome, cpf, telefone)
                if self.controller.db_manager.insert_cliente(novo_cliente):
                    self.controller.clientes.append(novo_cliente)
                    self.controller.db_manager.export_all_to_json()
                    messagebox.showinfo("Sucesso", f"✅ Cliente '{nome}' cadastrado com sucesso!")
                    self.menu_cadastros()
                else:
                    messagebox.showerror("Erro", "❌ Falha ao salvar cliente. CPF pode já existir.")
            except Exception as e:
                messagebox.showerror("Erro", f"❌ Erro ao cadastrar: {str(e)}")

        btn_salvar = self.criar_botao(btn_frame, "💾 Salvar Cadastro", salvar, "sucesso")
        btn_salvar.pack(side='right', padx=(10,0))
        btn_cancelar = self.criar_botao(btn_frame, "✕ Cancelar", self.menu_cadastros, "erro")
        btn_cancelar.pack(side='right')

    def cadastrar_veterinario(self):
        self.limpar_janela()
        main_frame = tk.Frame(self.root, bg=self.cor_fundo)
        main_frame.pack(fill=tk.BOTH, expand=True)
        header = tk.Frame(main_frame, bg=self.cor_fundo)
        header.pack(fill='x', padx=40, pady=(30, 20))
        btn_voltar = self.criar_botao(header, "← Voltar", self.menu_cadastros)
        btn_voltar.pack(side='left')
        titulo = tk.Label(header, text="🩺 Novo Veterinário", font=self.fonte_titulo, bg=self.cor_fundo, fg='white')
        titulo.pack(side='left', padx=(20, 0))

        card_form = tk.Frame(main_frame, bg=self.cor_fundo_card, relief='flat', borderwidth=0)
        card_form.pack(fill='both', expand=True, padx=40, pady=(0, 40))
        campos_frame = tk.Frame(card_form, bg=self.cor_fundo_card)
        campos_frame.pack(fill='both', expand=True, padx=40, pady=40)

        campos = [
            ("Nome Completo:", "nome"),
            ("CPF:", "cpf"),
            ("Telefone:", "telefone"),
            ("CRM:", "crm"),
            ("Especialidade:", "especialidade"),
        ]

        entradas = {}
        for label_text, var_name in campos:
            frame_campo, entrada = self.criar_campo_entrada(campos_frame, label_text)
            frame_campo.pack(fill='x', pady=5)
            entradas[var_name] = entrada

        btn_frame = tk.Frame(card_form, bg=self.cor_fundo_card)
        btn_frame.pack(fill='x', padx=40, pady=(0, 30))

        def salvar_vet():
            try:
                nome = entradas['nome'].get().strip()
                cpf = entradas['cpf'].get().strip()
                telefone = entradas['telefone'].get().strip()
                crm = entradas['crm'].get().strip()
                especialidade = entradas['especialidade'].get().strip()
                if not all([nome, cpf, telefone, crm, especialidade]):
                    messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                    return
                from package.models.veterinario import Veterinario
                novo_vet = Veterinario(nome, cpf, telefone, crm, especialidade)
                if self.controller.db_manager.insert_veterinario(novo_vet):
                    self.controller.veterinarios.append(novo_vet)
                    self.controller.db_manager.export_all_to_json()
                    messagebox.showinfo("Sucesso", f"✅ Veterinário '{nome}' cadastrado com sucesso!")
                    self.menu_cadastros()
                else:
                    messagebox.showerror("Erro", "❌ Falha ao salvar. CRM pode já existir.")
            except Exception as e:
                messagebox.showerror("Erro", f"❌ Erro ao cadastrar: {str(e)}")

        btn_salvar = self.criar_botao(btn_frame, "💾 Salvar Veterinário", salvar_vet, "sucesso")
        btn_salvar.pack(side='right', padx=(10,0))
        btn_cancelar = self.criar_botao(btn_frame, "✕ Cancelar", self.menu_cadastros, "erro")
        btn_cancelar.pack(side='right')

    def cadastrar_animal(self):

        self.limpar_janela()
        main_frame = tk.Frame(self.root, bg=self.cor_fundo)
        main_frame.pack(fill=tk.BOTH, expand=True)
    
   
        header = tk.Frame(main_frame, bg=self.cor_fundo)
        header.pack(fill='x', padx=40, pady=(30, 20))
    
        btn_voltar = self.criar_botao(header, "← Voltar", self.menu_cadastros)
        btn_voltar.pack(side='left')
    
        titulo = tk.Label(header, text="🐶 Novo Animal", 
                        font=self.fonte_titulo, 
                        bg=self.cor_fundo, 
                        fg='white')
        titulo.pack(side='left', padx=(20, 0))
    
        
        container = tk.Frame(main_frame, bg=self.cor_fundo)
        container.pack(fill=tk.BOTH, expand=True, padx=40, pady=(0, 20))
    

        canvas = tk.Canvas(container, bg=self.cor_fundo, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.cor_fundo)
    
        scrollable_frame.bind(
                "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
    
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
    
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    
        card_form = tk.Frame(scrollable_frame, 
                            bg=self.cor_fundo_card, 
                            relief='flat', 
                            borderwidth=0)
        card_form.pack(fill='x', padx=0, pady=(0, 20))
    
    
        campos_frame = tk.Frame(card_form, bg=self.cor_fundo_card)
        campos_frame.pack(fill='x', padx=40, pady=40)
    
   
        campos = [
            ("Nome do Animal:", "nome"),
            ("Raça:", "raca"),
            ("Idade:", "idade"),
            ("Peso (kg):", "peso"),
            ("CPF do Dono:", "dono_cpf"),
        ]
    
        entradas = {}
        for label_text, var_name in campos:
            frame_campo, entrada = self.criar_campo_entrada(campos_frame, label_text)
            frame_campo.pack(fill='x', pady=8)
            entradas[var_name] = entrada
    
        especie_frame = tk.Frame(campos_frame, bg=self.cor_fundo_card)
        especie_frame.pack(fill='x', pady=8)
    
        especie_label = tk.Label(especie_frame, 
                                text="Espécie:", 
                                font=("Segoe UI", 10, "bold"), 
                                bg=self.cor_fundo_card, 
                                fg=self.cor_texto_secundario)
        especie_label.pack(anchor='w', padx=5)
    
        especie_var = tk.StringVar(value="Cachorro")
        especie_combo = ttk.Combobox(especie_frame, 
                                    textvariable=especie_var, 
                                    values=["Cachorro", "Gato"], 
                                    state='readonly', 
                                    font=self.fonte_normal, 
                                    height=10)
        especie_combo.pack(fill='x', padx=5, pady=(0, 15), ipady=8)
    
        btn_frame_container = tk.Frame(main_frame, bg=self.cor_fundo)
        btn_frame_container.pack(fill='x', side='bottom', padx=40, pady=(0, 30))
    
        btn_frame = tk.Frame(btn_frame_container, bg=self.cor_fundo)
        btn_frame.pack()

        def salvar_animal():
            try:
                nome = entradas['nome'].get().strip()
                raca = entradas['raca'].get().strip()
                idade = int(entradas['idade'].get().strip())
                peso = float(entradas['peso'].get().strip())
                dono_cpf = entradas['dono_cpf'].get().strip()
                especie = especie_var.get()
                if not all([nome, raca, dono_cpf]):
                    messagebox.showerror("Erro", "Preencha todos os campos!")
                    return
                from package.models.cachorro import Cachorro
                from package.models.gato import Gato
                cliente_dono = self.controller.encontrar_objeto(self.controller.clientes, 'cpf', dono_cpf)
                if not cliente_dono:
                    messagebox.showerror("Erro", "Cliente não encontrado!")
                    return
                if especie == "Cachorro":
                    novo_animal = Cachorro(nome, raca, idade, peso, dono_cpf)
                else:
                    novo_animal = Gato(nome, raca, idade, peso, dono_cpf)
                animal_id = self.controller.db_manager.insert_animal(novo_animal)
                if animal_id:
                    novo_animal.db_id = animal_id
                    self.controller.animais.append(novo_animal)
                    cliente_dono.adicionar_animal(novo_animal)
                    self.controller.db_manager.export_all_to_json()
                    messagebox.showinfo("Sucesso", f"✅ Animal '{nome}' cadastrado com sucesso!")
                    self.menu_cadastros()
                else:
                    messagebox.showerror("Erro", "❌ Falha ao salvar animal.")
            except ValueError:
                messagebox.showerror("Erro", "Idade e Peso devem ser números!")
            except Exception as e:
                messagebox.showerror("Erro", f"❌ Erro ao cadastrar: {str(e)}")

        btn_salvar = self.criar_botao(btn_frame, "💾 Salvar Animal", salvar_animal, "sucesso")
        btn_salvar.pack(side='right', padx=(10,0))
        btn_cancelar = self.criar_botao(btn_frame, "✕ Cancelar", self.menu_cadastros, "erro")
        btn_cancelar.pack(side='right')

    def menu_agendamento(self):
        self.limpar_janela()
        main_frame = tk.Frame(self.root, bg=self.cor_fundo)
        main_frame.pack(fill=tk.BOTH, expand=True)
        header = tk.Frame(main_frame, bg=self.cor_fundo)
        header.pack(fill='x', padx=40, pady=(30, 20))
        btn_voltar = self.criar_botao(header, "← Voltar", self.criar_menu_principal)
        btn_voltar.pack(side='left')
        titulo = tk.Label(header, text="📅 Agendamentos", font=self.fonte_titulo, bg=self.cor_fundo, fg='white')
        titulo.pack(side='left', padx=(20, 0))

        container = tk.Frame(main_frame, bg=self.cor_fundo)
        container.pack(fill='both', expand=True, padx=40, pady=20)
        cards_frame = tk.Frame(container, bg=self.cor_fundo)
        cards_frame.pack(fill='both', expand=True)

        agendamentos = [
            ("🩺 Consulta", "Agendar consulta veterinária", self.agendar_consulta, self.cor_primaria),
            ("🛁 Banho/Tosa", "Agendar serviços de estética", self.agendar_banho_tosa, self.cor_secundaria),
            ("➕ Procedimento", "Adicionar procedimento extra", self.adicionar_procedimento, self.cor_sucesso),
            ("📋 Histórico", "Ver histórico de atendimentos", lambda: self.listar_atendimentos_gui(), self.cor_alerta),
        ]

        for i, (emoji, descricao, comando, cor) in enumerate(agendamentos):
            card = tk.Frame(cards_frame, bg=self.cor_fundo_card, relief='flat', borderwidth=0)
            card.grid(row=i//2, column=i%2, padx=15, pady=15, sticky='nsew')
            cards_frame.grid_columnconfigure(i%2, weight=1)
            emoji_label = tk.Label(card, text=emoji, font=("Segoe UI Emoji", 32), bg=self.cor_fundo_card, fg='white')
            emoji_label.pack(pady=(20, 10))
            titulo_card = tk.Label(card, text=descricao.split()[0], font=self.fonte_subtitulo, bg=self.cor_fundo_card, fg='white')
            titulo_card.pack()
            desc_label = tk.Label(card, text=descricao, font=("Segoe UI", 9), bg=self.cor_fundo_card, fg=self.cor_texto_secundario, wraplength=200)
            desc_label.pack(pady=(5, 20))
            btn = self.criar_botao(card, "Agendar →", comando)
            btn.pack(pady=(0, 20))

    def agendar_consulta(self):
        self.limpar_janela()
        main_frame = tk.Frame(self.root, bg=self.cor_fundo)
        main_frame.pack(fill=tk.BOTH, expand=True)
        header = tk.Frame(main_frame, bg=self.cor_fundo)
        header.pack(fill='x', padx=40, pady=(30, 20))
        btn_voltar = self.criar_botao(header, "← Voltar", self.menu_agendamento)
        btn_voltar.pack(side='left')
        titulo = tk.Label(header, text="🩺 Nova Consulta", font=self.fonte_titulo, bg=self.cor_fundo, fg='white')
        titulo.pack(side='left', padx=(20, 0))

        card_form = tk.Frame(main_frame, bg=self.cor_fundo_card, relief='flat', borderwidth=0)
        card_form.pack(fill='both', expand=True, padx=40, pady=(0, 40))
        campos_frame = tk.Frame(card_form, bg=self.cor_fundo_card)
        campos_frame.pack(fill='both', expand=True, padx=40, pady=40)

        campos = [
            ("CPF do Cliente:", "cpf_cliente"),
            ("CRM do Veterinário:", "crm_vet"),
            ("ID do Animal:", "id_animal"),
            ("Data (DD/MM/AAAA):", "data"),
            ("Hora (HH:MM):", "hora"),
        ]

        entradas = {}
        for label_text, var_name in campos:
            frame_campo, entrada = self.criar_campo_entrada(campos_frame, label_text)
            frame_campo.pack(fill='x', pady=5)
            entradas[var_name] = entrada

        btn_frame = tk.Frame(card_form, bg=self.cor_fundo_card)
        btn_frame.pack(fill='x', padx=40, pady=(0, 30))

        def salvar_consulta():
            try:
                from package.models.atendimento import Atendimento
                cliente = self.controller.encontrar_objeto(self.controller.clientes, 'cpf', entradas['cpf_cliente'].get().strip())
                veterinario = self.controller.encontrar_objeto(self.controller.veterinarios, 'crm', entradas['crm_vet'].get().strip())
                animal = self.controller.encontrar_objeto(self.controller.animais, 'db_id', int(entradas['id_animal'].get().strip()))
                if not cliente or not veterinario or not animal:
                    messagebox.showerror("Erro", "Cliente, Veterinário ou Animal não encontrado!")
                    return
                data_agendada = f"{entradas['data'].get().strip()} {entradas['hora'].get().strip()}"
                novo_atendimento = Atendimento(cliente=cliente, animal=animal, veterinario=veterinario, servicos=["Consulta"], data_agendada=data_agendada)
                if self.controller.db_manager.insert_atendimento(novo_atendimento):
                    self.controller.atendimentos.append(novo_atendimento)
                    veterinario.adicionar_atendimento(novo_atendimento)
                    self.controller.db_manager.export_all_to_json()
                    messagebox.showinfo("Sucesso", "✅ Consulta agendada com sucesso!")
                    self.menu_agendamento()
                else:
                    messagebox.showerror("Erro", "❌ Falha ao salvar agendamento.")
            except Exception as e:
                messagebox.showerror("Erro", f"❌ Erro: {str(e)}")

        btn_salvar = self.criar_botao(btn_frame, "📅 Agendar Consulta", salvar_consulta, "sucesso")
        btn_salvar.pack(side='right', padx=(10, 0))
        btn_cancelar = self.criar_botao(btn_frame, "✕ Cancelar", self.menu_agendamento, "erro")
        btn_cancelar.pack(side='right')
        
    def agendar_banho_tosa(self):
        
        self.limpar_janela()
        main_frame = tk.Frame(self.root, bg=self.cor_fundo)
        main_frame.pack(fill=tk.BOTH, expand=True)
        header = tk.Frame(main_frame, bg=self.cor_fundo)
        header.pack(fill='x', padx=40, pady=(30, 20))
        bnt_voltar = self.criar_botao(header, "← Voltar", self.menu_agendamento)
        bnt_voltar.pack(side='left')
        titulo = tk.Label(header, text="🛁 Agendar Banho/Tosa", font=self.fonte_titulo, bg=self.cor_fundo, fg='white')
        titulo.pack(side='left', padx=(20, 0))
        
        card_form = tk.Frame(main_frame, bg=self.cor_fundo_card, relief='flat', borderwidth=0)
        card_form.pack(fill='both', expand=True, padx=40, pady=(0, 40))
        campos_frame = tk.Frame(card_form, bg=self.cor_fundo_card)  
        campos_frame.pack(fill='both', expand=True, padx=40, pady=40)
        
        campos = [
            ("CPF do Cliente:", "cpf_cliente"),
            ("ID do Animal:", "id_animal"),
            ("Data (DD/MM/AAAA):", "data"),
            ("Hora (HH:MM):", "hora"),
        ]
        
        entradas = {}
        for label_text, var_name in campos:
            frame_campo, entrada = self.criar_campo_entrada(campos_frame, label_text)
            frame_campo.pack(fill='x', pady=5)
            entradas[var_name] = entrada
        btn_frame = tk.Frame(card_form, bg=self.cor_fundo_card)
        btn_frame.pack(fill='x', padx=40, pady=(0, 30))
        
        def salvar_banho_tosa():
            try:
                from package.models.atendimento import Atendimento
                cliente = self.controller.encontrar_objeto(self.controller.clientes, 'cpf', entradas['cpf_cliente'].get().strip())
                animal = self.controller.encontrar_objeto(self.controller.animais, 'db_id', int(entradas['id_animal'].get().strip()))
                if not cliente or not animal:
                    messagebox.showerror("Erro", "Cliente ou Animal não encontrado!")
                    return
                data_agendada = f"{entradas['data'].get().strip()} {entradas['hora'].get().strip()}"
                novo_atendimento = Atendimento(cliente=cliente, animal=animal, veterinario=None, servicos=["Banho/Tosa"], data_agendada=data_agendada)
                if self.controller.db_manager.insert_atendimento(novo_atendimento):
                    self.controller.atendimentos.append(novo_atendimento)
                    self.controller.db_manager.export_all_to_json()
                    messagebox.showinfo("Sucesso", "✅ Banho/Tosa agendado com sucesso!")
                    self.menu_agendamento()
                else:
                    messagebox.showerror("Erro", "❌ Falha ao salvar agendamento.")
            except Exception as e:
                messagebox.showerror("Erro", f"❌ Erro: {str(e)}")
                
        btn_salvar = self.criar_botao(btn_frame, "📅 Agendar Banho e Tosa", salvar_banho_tosa, "sucesso")
        btn_salvar.pack(side='right', padx=(10, 0))
        btn_cancelar = self.criar_botao(btn_frame, "✕ Cancelar", self.menu_agendamento, "erro")
        btn_cancelar.pack(side='right')
        
    def adicionar_procedimento(self):
        
        self.limpar_janela()
        main_frame = tk.Frame(self.root, bg=self.cor_fundo)
        main_frame.pack(fill=tk.BOTH, expand=True)
        header = tk.Frame(main_frame, bg=self.cor_fundo)
        header.pack(fill='x', padx=40, pady=(30, 20))
        btn_voltar = self.criar_botao(header, "← Voltar", self.menu_agendamento)
        btn_voltar.pack(side='left')
        titulo = tk.Label(header, text="➕ Adicionar Procedimento", font=self.fonte_titulo, bg=self.cor_fundo, fg='white')
        titulo.pack(side='left', padx=(20, 0))
        
        card_form = tk.Frame(main_frame, bg=self.cor_fundo_card, relief='flat', borderwidth=0)
        card_form.pack(fill='both', expand=True, padx=40, pady=(0, 40))
        campos_frame = tk.Frame(card_form, bg=self.cor_fundo_card)
        campos_frame.pack(fill='both', expand=True, padx=40, pady=40)
        
        # Campos simplificados: Apenas o ID do serviço e a descrição
        campos = [
            ("ID do Atendimento Existente (Ex: 1, 2, 3):", "id_servico"), 
            ("Descrição do Novo Procedimento (Ex: Castração, Raio-X):", "descricao"),
        ]
        
        
        entradas = {}
        for label_text, var_name in campos:
            frame_campo, entrada = self.criar_campo_entrada(campos_frame, label_text)
            frame_campo.pack(fill='x', pady=5)
            entradas[var_name] = entrada
            
        btn_frame = tk.Frame(card_form, bg=self.cor_fundo_card)
        btn_frame.pack(fill='x', padx=40, pady=(0, 30))
        
        def salvar_procedimento():
            try:
                # 1. Coletar e validar dados
                id_servico_str = entradas['id_servico'].get().strip()
                descricao = entradas['descricao'].get().strip()
                
                if not id_servico_str or not descricao:
                    messagebox.showerror("Erro", "Preencha o ID do Atendimento e a Descrição do Procedimento.")
                    return
                
                atendimento_id = int(id_servico_str)
                
                # 2. Encontrar o objeto Atendimento na memória (Model)
                atendimento_existente = self.controller.encontrar_objeto(self.controller.atendimentos, 'db_id', atendimento_id)
                
                if not atendimento_existente:
                    messagebox.showerror("Erro", f"❌ Atendimento com ID {atendimento_id} não encontrado.")
                    return
                
                # 3. Executar a lógica de negócio no objeto (Model)
                atendimento_existente.adicionar_procedimento(descricao)
                novo_custo = atendimento_existente.calcular_total() # Recalcula o total
                
                # 4. Persistir a mudança no Banco de Dados
                # Usa o método correto da DatabaseManager que atualiza 'procedimentos' e 'custo_total'
                db_manager = self.controller.db_manager
                if db_manager.update_atendimento_procedimentos(atendimento_id, atendimento_existente.procedimentos, novo_custo):
                    db_manager.export_all_to_json() # Salva a exportação
                    messagebox.showinfo("Sucesso", f"✅ Procedimento adicionado! Novo Custo Total: R$ {novo_custo:.2f}!")
                    self.menu_agendamento()
                else:
                    messagebox.showerror("Erro", "❌ Falha ao atualizar o procedimento no Banco de Dados.")

            except ValueError:
                messagebox.showerror("Erro", "O ID do serviço deve ser um número inteiro!")
            except Exception as e:
                messagebox.showerror("Erro", f"❌ Erro ao adicionar procedimento: {str(e)}")
        
        btn_salvar = self.criar_botao(btn_frame, "➕ Adicionar Procedimento", salvar_procedimento, "sucesso")
        btn_salvar.pack(side='right', padx=(10, 0))
        btn_cancelar = self.criar_botao(btn_frame, "✕ Cancelar", self.menu_agendamento, "erro")
        btn_cancelar.pack(side='right')
        
    def listar_dados_menu(self):
        self.limpar_janela()
        main_frame = tk.Frame(self.root, bg=self.cor_fundo)
        main_frame.pack(fill=tk.BOTH, expand=True)
        header = tk.Frame(main_frame, bg=self.cor_fundo)
        header.pack(fill='x', padx=40, pady=(30, 20))
        btn_voltar = self.criar_botao(header, "← Voltar", self.criar_menu_principal)
        btn_voltar.pack(side='left')
        titulo = tk.Label(header, text="📊 Relatórios e Dados", font=self.fonte_titulo, bg=self.cor_fundo, fg='white')
        titulo.pack(side='left', padx=(20, 0))
        container = tk.Frame(main_frame, bg=self.cor_fundo)
        container.pack(fill='both', expand=True, padx=40, pady=20)
        cards_frame = tk.Frame(container, bg=self.cor_fundo)
        cards_frame.pack(fill='both', expand=True)

        relatorios = [
            ("👥 Clientes", f"{len(self.controller.clientes)} cadastrados", self.listar_clientes_gui, self.cor_primaria),
            ("🩺 Veterinários", f"{len(self.controller.veterinarios)} cadastrados", self.listar_veterinarios_gui, self.cor_secundaria),
            ("🐾 Animais", f"{len(self.controller.animais)} cadastrados", self.listar_animais_gui, self.cor_sucesso),
            ("📅 Atendimentos", f"{len(self.controller.atendimentos)} registrados", self.listar_atendimentos_gui, self.cor_alerta),
            ("📤 Exportar", "Exportar dados completos", lambda: messagebox.showinfo("Exportar", "Dados exportados automaticamente para JSON!"), "#06b6d4"),
        ]

        for i, (emoji, descricao, comando, cor) in enumerate(relatorios):
            row = i // 3
            col = i % 3
            card = tk.Frame(cards_frame, bg=self.cor_fundo_card, relief='flat', borderwidth=0)
            card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            cards_frame.grid_columnconfigure(col, weight=1)
            cards_frame.grid_rowconfigure(row, weight=1)
            gradient_frame = tk.Frame(card, bg=cor, height=5)
            gradient_frame.pack(fill='x')
            conteudo_frame = tk.Frame(card, bg=self.cor_fundo_card)
            conteudo_frame.pack(fill='both', expand=True, padx=20, pady=20)
            emoji_label = tk.Label(conteudo_frame, text=emoji, font=("Segoe UI Emoji", 24), bg=self.cor_fundo_card, fg='white')
            emoji_label.pack(anchor='w')
            titulo_card = tk.Label(conteudo_frame, text=descricao.split()[0], font=self.fonte_subtitulo, bg=self.cor_fundo_card, fg='white')
            titulo_card.pack(anchor='w', pady=(10, 5))
            desc_label = tk.Label(conteudo_frame, text=descricao, font=("Segoe UI", 9), bg=self.cor_fundo_card, fg=self.cor_texto_secundario)
            desc_label.pack(anchor='w')
            btn = self.criar_botao(conteudo_frame, "Visualizar →", comando)
            btn.pack(anchor='w', pady=(20, 0))

    def listar_clientes_gui(self):
        self.limpar_janela()
        main_frame = tk.Frame(self.root, bg=self.cor_fundo)
        main_frame.pack(fill=tk.BOTH, expand=True)
        header = tk.Frame(main_frame, bg=self.cor_fundo)
        header.pack(fill='x', padx=40, pady=(30, 20))
        btn_voltar = self.criar_botao(header, "← Voltar", self.listar_dados_menu)
        btn_voltar.pack(side='left')
        titulo = tk.Label(header, text="👥 Lista de Clientes", font=self.fonte_titulo, bg=self.cor_fundo, fg='white')
        titulo.pack(side='left', padx=(20, 0))
        pesquisa_frame = tk.Frame(main_frame, bg=self.cor_fundo)
        pesquisa_frame.pack(fill='x', padx=40, pady=(0, 20))
        pesquisa_entry = tk.Entry(pesquisa_frame, font=self.fonte_normal, bg=self.cor_fundo_card, fg=self.cor_texto, insertbackground=self.cor_primaria, relief='flat', borderwidth=0)
        pesquisa_entry.pack(side='left', fill='x', expand=True, padx=(0, 10), ipady=8)
        btn_pesquisa = self.criar_botao(pesquisa_frame, "🔍 Pesquisar", lambda: None)
        btn_pesquisa.pack(side='right')
        lista_container = tk.Frame(main_frame, bg=self.cor_fundo)
        lista_container.pack(fill='both', expand=True, padx=40, pady=(0, 30))
        cabecalho = tk.Frame(lista_container, bg=self.cor_fundo_card)
        cabecalho.pack(fill='x', pady=(0, 2))
        colunas = ["Nome", "CPF", "Telefone", "Animais"]
        larguras = [200, 120, 120, 80]
        for i, (coluna, largura) in enumerate(zip(colunas, larguras)):
            label = tk.Label(cabecalho, text=coluna, font=("Segoe UI", 10, "bold"), bg=self.cor_primaria, fg='white', padx=10, pady=10)
            label.grid(row=0, column=i, sticky='ew', padx=(1, 0))
            cabecalho.grid_columnconfigure(i, minsize=largura)

        lista_frame = tk.Frame(lista_container, bg=self.cor_fundo)
        lista_frame.pack(fill='both', expand=True)
        canvas = tk.Canvas(lista_frame, bg=self.cor_fundo, highlightthickness=0)
        scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.cor_fundo)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        if not self.controller.clientes:
            vazio_frame = tk.Frame(scrollable_frame, bg=self.cor_fundo_card, height=100)
            vazio_frame.pack(fill='x', pady=2)
            label_vazio = tk.Label(vazio_frame, text="Nenhum cliente cadastrado", font=self.fonte_normal, bg=self.cor_fundo_card, fg=self.cor_texto_secundario)
            label_vazio.pack(expand=True)
        else:
            for i, cliente in enumerate(self.controller.clientes):
                cor_fundo = self.cor_fundo_card if i % 2 == 0 else self.clarear_cor(self.cor_fundo_card, 5)
                linha = tk.Frame(scrollable_frame, bg=cor_fundo, height=60)
                linha.pack(fill='x', pady=2)
                nome_label = tk.Label(linha, text=cliente.nome, font=self.fonte_normal, bg=cor_fundo, fg=self.cor_texto, padx=10, pady=10, anchor='w')
                nome_label.grid(row=0, column=0, sticky='ew')
                cpf_label = tk.Label(linha, text=cliente.cpf, font=("Segoe UI", 10), bg=cor_fundo, fg=self.cor_texto_secundario, padx=10, pady=10)
                cpf_label.grid(row=0, column=1, sticky='ew')
                tel_label = tk.Label(linha, text=cliente.telefone, font=("Segoe UI", 10), bg=cor_fundo, fg=self.cor_texto_secundario, padx=10, pady=10)
                tel_label.grid(row=0, column=2, sticky='ew')
                animais_count = len(cliente.animais) if hasattr(cliente, 'animais') else 0
                animais_label = tk.Label(linha, text=f"🐾 {animais_count}", font=("Segoe UI", 10), bg=cor_fundo, fg=self.cor_sucesso, padx=10, pady=10)
                animais_label.grid(row=0, column=3, sticky='ew')
                for col in range(4):
                    linha.grid_columnconfigure(col, minsize=larguras[col])

        btn_frame = tk.Frame(main_frame, bg=self.cor_fundo)
        btn_frame.pack(fill='x', padx=40, pady=(0, 30))
        btn_exportar = self.criar_botao(btn_frame, "📤 Exportar Lista", lambda: messagebox.showinfo("Exportar", "Lista exportada com sucesso!"), "sucesso")
        btn_exportar.pack(side='right', padx=(10, 0))
        btn_imprimir = self.criar_botao(btn_frame, "🖨️ Imprimir", lambda: messagebox.showinfo("Imprimir", "Enviado para impressora!"), "primario")
        btn_imprimir.pack(side='right', padx=(10, 0))

    def listar_veterinarios_gui(self):
        self.limpar_janela()
        main_frame = tk.Frame(self.root, bg=self.cor_fundo)
        main_frame.pack(fill=tk.BOTH, expand=True)
        header = tk.Frame(main_frame, bg=self.cor_fundo)
        header.pack(fill='x', padx=40, pady=(30, 20))
        btn_voltar = self.criar_botao(header, "← Voltar", self.listar_dados_menu)
        btn_voltar.pack(side='left')
        titulo = tk.Label(header, text="🩺 Lista de Veterinários", font=self.fonte_titulo, bg=self.cor_fundo, fg='white')
        titulo.pack(side='left', padx=(20, 0))

        lista_container = tk.Frame(main_frame, bg=self.cor_fundo)
        lista_container.pack(fill='both', expand=True, padx=40, pady=(0, 30))
        cabecalho = tk.Frame(lista_container, bg=self.cor_fundo_card)
        cabecalho.pack(fill='x', pady=(0, 2))
        colunas = ["Nome", "CRM", "Especialidade", "Atendimentos"]
        larguras = [200, 100, 150, 100]
        for i, (coluna, largura) in enumerate(zip(colunas, larguras)):
            label = tk.Label(cabecalho, text=coluna, font=("Segoe UI", 10, "bold"), bg=self.cor_secundaria, fg='white', padx=10, pady=10)
            label.grid(row=0, column=i, sticky='ew', padx=(1, 0))
            cabecalho.grid_columnconfigure(i, minsize=largura)

        lista_frame = tk.Frame(lista_container, bg=self.cor_fundo)
        lista_frame.pack(fill='both', expand=True)
        canvas = tk.Canvas(lista_frame, bg=self.cor_fundo, highlightthickness=0)
        scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.cor_fundo)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        if not self.controller.veterinarios:
            vazio_frame = tk.Frame(scrollable_frame, bg=self.cor_fundo_card, height=100)
            vazio_frame.pack(fill='x', pady=2)
            label_vazio = tk.Label(vazio_frame, text="Nenhum veterinário cadastrado", font=self.fonte_normal, bg=self.cor_fundo_card, fg=self.cor_texto_secundario)
            label_vazio.pack(expand=True)
        else:
            for i, vet in enumerate(self.controller.veterinarios):
                cor_fundo = self.cor_fundo_card if i % 2 == 0 else self.clarear_cor(self.cor_fundo_card, 5)
                linha = tk.Frame(scrollable_frame, bg=cor_fundo, height=60)
                linha.pack(fill='x', pady=2)
                nome_label = tk.Label(linha, text=vet.nome, font=self.fonte_normal, bg=cor_fundo, fg=self.cor_texto, padx=10, pady=10, anchor='w')
                nome_label.grid(row=0, column=0, sticky='ew')
                crm_label = tk.Label(linha, text=getattr(vet,'crm','N/A'), font=("Segoe UI", 10), bg=cor_fundo, fg=self.cor_secundaria, padx=10, pady=10)
                crm_label.grid(row=0, column=1, sticky='ew')
                esp_label = tk.Label(linha, text=getattr(vet,'especialidade',''), font=("Segoe UI", 10), bg=cor_fundo, fg=self.cor_texto_secundario, padx=10, pady=10)
                esp_label.grid(row=0, column=2, sticky='ew')
                atend_count = len(getattr(vet,'atendimentos',[]))
                atend_label = tk.Label(linha, text=f"📅 {atend_count}", font=("Segoe UI", 10), bg=cor_fundo, fg=self.cor_sucesso if atend_count > 0 else self.cor_texto_secundario, padx=10, pady=10)
                atend_label.grid(row=0, column=3, sticky='ew')
                for col in range(4):
                    linha.grid_columnconfigure(col, minsize=larguras[col])

        btn_frame = tk.Frame(main_frame, bg=self.cor_fundo)
        btn_frame.pack(fill='x', padx=40, pady=(0, 30))
        btn_voltar_menu = self.criar_botao(btn_frame, "← Menu Principal", self.criar_menu_principal, "primario")
        btn_voltar_menu.pack(side='right')

    def listar_animais_gui(self):
        self.limpar_janela()
        main_frame = tk.Frame(self.root, bg=self.cor_fundo)
        main_frame.pack(fill=tk.BOTH, expand=True)
        header = tk.Frame(main_frame, bg=self.cor_fundo)
        header.pack(fill='x', padx=40, pady=(30, 20))
        btn_voltar = self.criar_botao(header, "← Voltar", self.listar_dados_menu)
        btn_voltar.pack(side='left')
        titulo = tk.Label(header, text="🐾 Lista de Animais", font=self.fonte_titulo, bg=self.cor_fundo, fg='white')
        titulo.pack(side='left', padx=(20, 0))

        filtros_frame = tk.Frame(main_frame, bg=self.cor_fundo)
        filtros_frame.pack(fill='x', padx=40, pady=(0, 20))
        filtros = ["Todos", "Cachorros", "Gatos"]
        filtro_var = tk.StringVar(value="Todos")
        for filtro in filtros:
            rb = tk.Radiobutton(filtros_frame, text=filtro, variable=filtro_var, value=filtro, font=self.fonte_normal, bg=self.cor_fundo, fg=self.cor_texto, selectcolor=self.cor_fundo_card, activebackground=self.cor_fundo, activeforeground=self.cor_primaria)
            rb.pack(side='left', padx=(0, 20))

        lista_container = tk.Frame(main_frame, bg=self.cor_fundo)
        lista_container.pack(fill='both', expand=True, padx=40, pady=(0, 30))
        cabecalho = tk.Frame(lista_container, bg=self.cor_fundo_card)
        cabecalho.pack(fill='x', pady=(0, 2))
        colunas = ["Nome", "Espécie", "Raça", "Idade", "Dono"]
        larguras = [150, 100, 120, 80, 150]
        for i, (coluna, largura) in enumerate(zip(colunas, larguras)):
            label = tk.Label(cabecalho, text=coluna, font=("Segoe UI", 10, "bold"), bg=self.cor_sucesso, fg='white', padx=10, pady=10)
            label.grid(row=0, column=i, sticky='ew', padx=(1, 0))
            cabecalho.grid_columnconfigure(i, minsize=largura)

        lista_frame = tk.Frame(lista_container, bg=self.cor_fundo)
        lista_frame.pack(fill='both', expand=True)
        canvas = tk.Canvas(lista_frame, bg=self.cor_fundo, highlightthickness=0)
        scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.cor_fundo)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        if not self.controller.animais:
            vazio_frame = tk.Frame(scrollable_frame, bg=self.cor_fundo_card, height=100)
            vazio_frame.pack(fill='x', pady=2)
            label_vazio = tk.Label(vazio_frame, text="Nenhum animal cadastrado", font=self.fonte_normal, bg=self.cor_fundo_card, fg=self.cor_texto_secundario)
            label_vazio.pack(expand=True)
        else:
            for i, animal in enumerate(self.controller.animais):
                cor_fundo = self.cor_fundo_card if i % 2 == 0 else self.clarear_cor(self.cor_fundo_card, 5)
                linha = tk.Frame(scrollable_frame, bg=cor_fundo, height=60)
                linha.pack(fill='x', pady=2)
                nome_label = tk.Label(linha, text=animal.nome, font=self.fonte_normal, bg=cor_fundo, fg=self.cor_texto, padx=10, pady=10, anchor='w')
                nome_label.grid(row=0, column=0, sticky='ew')
                especie = "🐕" if animal.__class__.__name__ == "Cachorro" else "🐈"
                especie_label = tk.Label(linha, text=especie, font=("Segoe UI Emoji", 12), bg=cor_fundo, fg=self.cor_texto, padx=10, pady=10)
                especie_label.grid(row=0, column=1, sticky='ew')
                raca_label = tk.Label(linha, text=animal.raca, font=("Segoe UI", 10), bg=cor_fundo, fg=self.cor_texto_secundario, padx=10, pady=10)
                raca_label.grid(row=0, column=2, sticky='ew')
                idade_label = tk.Label(linha, text=f"{animal.idade} anos", font=("Segoe UI", 10), bg=cor_fundo, fg=self.cor_texto_secundario, padx=10, pady=10)
                idade_label.grid(row=0, column=3, sticky='ew')
                dono = self.controller.encontrar_objeto(self.controller.clientes, 'cpf', animal.dono_cpf)
                nome_dono = dono.nome if dono else "Desconhecido"
                dono_label = tk.Label(linha, text=nome_dono, font=("Segoe UI", 10), bg=cor_fundo, fg=self.cor_primaria, padx=10, pady=10)
                dono_label.grid(row=0, column=4, sticky='ew')
                for col in range(5):
                    linha.grid_columnconfigure(col, minsize=larguras[col])

        btn_frame = tk.Frame(main_frame, bg=self.cor_fundo)
        btn_frame.pack(fill='x', padx=40, pady=(0, 30))
        btn_novo = self.criar_botao(btn_frame, "➕ Novo Animal", self.cadastrar_animal, "sucesso")
        btn_novo.pack(side='right', padx=(10, 0))
        btn_atualizar = self.criar_botao(btn_frame, "🔄 Atualizar", lambda: self.listar_animais_gui(), "primario")
        btn_atualizar.pack(side='right', padx=(10, 0))

    def listar_atendimentos_gui(self):
        self.limpar_janela()
        main_frame = tk.Frame(self.root, bg=self.cor_fundo)
        main_frame.pack(fill=tk.BOTH, expand=True)
        header = tk.Frame(main_frame, bg=self.cor_fundo)
        header.pack(fill='x', padx=40, pady=(30, 20))
        btn_voltar = self.criar_botao(header, "← Voltar", self.listar_dados_menu)
        btn_voltar.pack(side='left')
        titulo = tk.Label(header, text="📅 Histórico de Atendimentos", font=self.fonte_titulo, bg=self.cor_fundo, fg='white')
        titulo.pack(side='left', padx=(20, 0))

        stats_frame = tk.Frame(main_frame, bg=self.cor_fundo)
        stats_frame.pack(fill='x', padx=40, pady=(0, 20))
        stats_data = [
            ("Total", f"{len(self.controller.atendimentos)}", self.cor_primaria),
            ("Hoje", "1", self.cor_sucesso),
            ("Esta Semana", "5", self.cor_secundaria),
            ("Em Aberto", "0", self.cor_alerta),
        ]
        for stat_text, stat_value, stat_color in stats_data:
            stat_card = tk.Frame(stats_frame, bg=self.cor_fundo_card, width=150, height=80)
            stat_card.pack(side='left', padx=(0, 10))
            valor = tk.Label(stat_card, text=stat_value, font=("Segoe UI", 24, "bold"), bg=self.cor_fundo_card, fg=stat_color)
            valor.pack(expand=True)
            texto = tk.Label(stat_card, text=stat_text, font=("Segoe UI", 9), bg=self.cor_fundo_card, fg=self.cor_texto_secundario)
            texto.pack(expand=True)

        lista_container = tk.Frame(main_frame, bg=self.cor_fundo)
        lista_container.pack(fill='both', expand=True, padx=40, pady=(0, 30))

        if not self.controller.atendimentos:
            card_vazio = tk.Frame(lista_container, bg=self.cor_fundo_card)
            card_vazio.pack(fill='both', expand=True)
            emoji_vazio = tk.Label(card_vazio, text="📭", font=("Segoe UI Emoji", 48), bg=self.cor_fundo_card, fg=self.cor_texto_secundario)
            emoji_vazio.pack(pady=(50, 20))
            texto_vazio = tk.Label(card_vazio, text="Nenhum atendimento registrado", font=self.fonte_subtitulo, bg=self.cor_fundo_card, fg=self.cor_texto_secundario)
            texto_vazio.pack()
            subtexto_vazio = tk.Label(card_vazio, text="Comece agendando um novo atendimento", font=("Segoe UI", 10), bg=self.cor_fundo_card, fg=self.cor_texto_secundario)
            subtexto_vazio.pack(pady=(10, 0))
            btn_novo_atendimento = self.criar_botao(card_vazio, "➕ Novo Atendimento", self.menu_agendamento, "sucesso")
            btn_novo_atendimento.pack(pady=30)
        else:
            text_frame = tk.Frame(lista_container, bg=self.cor_fundo)
            text_frame.pack(fill='both', expand=True)
            text_widget = scrolledtext.ScrolledText(text_frame, font=('Segoe UI', 10), bg=self.cor_fundo_card, fg=self.cor_texto, wrap=tk.WORD, relief='flat', borderwidth=0, padx=20, pady=20)
            text_widget.pack(fill='both', expand=True)

            for i, atendimento in enumerate(self.controller.atendimentos):
                text_widget.tag_configure(f"titulo{i}", font=('Segoe UI', 12, 'bold'), foreground=self.cor_primaria)
                text_widget.tag_configure(f"info{i}", font=('Segoe UI', 10), foreground=self.cor_texto)
                text_widget.tag_configure(f"separador{i}", font=('Segoe UI', 10), foreground=self.cor_texto_secundario)

                text_widget.insert(tk.END, f"Atendimento #{i+1}\n", f"titulo{i}")
                text_widget.insert(tk.END, f"{'─'*50}\n", f"separador{i}")
                text_widget.insert(tk.END, f"👤 Cliente: {atendimento.cliente.nome}\n", f"info{i}")
                vet_nome = atendimento.veterinario.nome if atendimento.veterinario else "Não atribuído"
                text_widget.insert(tk.END, f"🩺 Veterinário: {vet_nome}\n", f"info{i}")
                text_widget.insert(tk.END, f"🐾 Animal: {atendimento.animal.nome}\n", f"info{i}")
                text_widget.insert(tk.END, f"📅 Data: {atendimento.data_agendada}\n", f"info{i}")
                servs = getattr(atendimento, 'servicos_solicitados', getattr(atendimento, 'servicos', []))
                text_widget.insert(tk.END, f"🛠️ Serviços: {', '.join(servs)}\n\n", f"info{i}")
                custo = atendimento.calcular_total() 
                text_widget.insert(tk.END, f"💵 Custo Total: R$ {custo:.2f}\n\n", f"info{i}")

            text_widget.config(state=tk.DISABLED)

        btn_frame = tk.Frame(main_frame, bg=self.cor_fundo)
        btn_frame.pack(fill='x', padx=40, pady=(0, 30))
        btn_exportar = self.criar_botao(btn_frame, "📊 Gerar Relatório", lambda: messagebox.showinfo("Relatório", "Relatório gerado com sucesso!"), "sucesso")
        btn_exportar.pack(side='right', padx=(10, 0))
        btn_novo = self.criar_botao(btn_frame, "➕ Novo Atendimento", self.menu_agendamento, "primario")
        btn_novo.pack(side='right', padx=(10, 0))
    

    def sair_app(self):
        confirm_window = tk.Toplevel(self.root)
        confirm_window.title("Confirmação")
        confirm_window.geometry("400x250")
        confirm_window.configure(bg=self.cor_fundo)
        confirm_window.resizable(False, False)
        confirm_window.transient(self.root)
        confirm_window.grab_set()
        confirm_window.update_idletasks()
        width = confirm_window.winfo_width()
        height = confirm_window.winfo_height()
        x = (confirm_window.winfo_screenwidth() // 2) - (width // 2)
        y = (confirm_window.winfo_screenheight() // 2) - (height // 2)
        confirm_window.geometry(f'{width}x{height}+{x}+{y}')

        content_frame = tk.Frame(confirm_window, bg=self.cor_fundo)
        content_frame.pack(fill='both', expand=True, padx=30, pady=30)
        alert_emoji = tk.Label(content_frame, text="⚠️", font=("Segoe UI Emoji", 48), bg=self.cor_fundo, fg=self.cor_alerta)
        alert_emoji.pack(pady=(0, 20))
        message = tk.Label(content_frame, text="Deseja realmente sair do sistema?", font=self.fonte_subtitulo, bg=self.cor_fundo, fg=self.cor_texto)
        message.pack(pady=(0, 10))
        submessage = tk.Label(content_frame, text="Todas as alterações foram salvas automaticamente.", font=("Segoe UI", 10), bg=self.cor_fundo, fg=self.cor_texto_secundario)
        submessage.pack(pady=(0, 30))

        btn_frame = tk.Frame(content_frame, bg=self.cor_fundo)
        btn_frame.pack()

        def confirmar_saida():
            confirm_window.destroy()
            self.root.quit()

        btn_sair = self.criar_botao(btn_frame, "✅ Sim, Sair", confirmar_saida, "erro")
        btn_sair.pack(side='left', padx=(0, 10))
        btn_cancelar = self.criar_botao(btn_frame, "❌ Cancelar", confirm_window.destroy, "primario")
        btn_cancelar.pack(side='left')

def main():
    root = tk.Tk()
    
    app = PetShopGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()