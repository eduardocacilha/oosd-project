from typing import List
import FreeSimpleGUI as sg
import re

class UsuarioView:
    
    def __init__(self):
        # O __init__ agora só define o tema.
        sg.theme('Reddit')

    # --- MÉTODO "Popup" (Substituto do mostra_mensagem) ---
    def mostrar_popup(self, titulo: str, msg: str):
        """Exibe um popup simples."""
        sg.Popup(titulo, msg, keep_on_top=True)

    # --- MÉTODO 1: O ANTIGO "tela_opcoes" ---
    def criar_janela_menu_usuario(self) -> str:
        """
        Cria, exibe e gerencia a janela do MENU de usuários.
        Retorna a 'key' do botão clicado (ex: '-INCLUIR-') ou '-VOLTAR-'.
        """
        layout = [
            [sg.Text("============================================")],
            [sg.Text("          GERENCIAR USUÁRIOS")],
            [sg.Text("============================================")],
            [sg.Button('Incluir Usuário', key='-INCLUIR-', size=(30,1))],
            [sg.Button('Alterar Usuário', key='-ALTERAR-', size=(30,1))],
            [sg.Button('Listar Usuários', key='-LISTAR-', size=(30,1))],
            [sg.Button('Excluir Usuário', key='-EXCLUIR-', size=(30,1))],
            [sg.Button('Listar Meus Ingressos', key='-MEUS_INGRESSOS-', size=(30,1))],
            [sg.Button('Ver Meu Histórico de Compras', key='-HISTORICO-', size=(30,1))],
            [sg.Button('Avaliar um Evento', key='-AVALIAR-', size=(30,1))],
            [sg.Button('Voltar ao Menu Principal', key='-VOLTAR-', size=(30,1), button_color=('white', 'red'))]
        ]
        
        janela = sg.Window('Menu de Usuários', layout, finalize=True)
        
        # Este é o loop de eventos da janela de menu
        while True:
            evento, valores = janela.read()
            
            if evento == sg.WINDOW_CLOSED or evento == '-VOLTAR-':
                janela.close()
                return '-VOLTAR-' # Retorna o evento de "saída"
            
            # Se o usuário clicar em qualquer outra opção do menu
            else:
                janela.close()
                return evento # Retorna o evento que o Controller vai processar

    # --- MÉTODO 2: O ANTIGO "pega_dados_usuario" ---
    def pega_dados_usuario(self, pedindo_matricula=True) -> dict:
        
        layout_matricula = [
            [sg.Text('Matrícula:'), sg.Input(key='-MATRICULA-')]
        ] if pedindo_matricula else []
        
        layout = layout_matricula + [
            [sg.Text('Nome:'), sg.Input(key='-NOME-')],
            [sg.Text('Email:'), sg.Input(key='-EMAIL-')],
            [sg.Button('Salvar', key='-SALVAR-'), sg.Button('Cancelar', key='-CANCELAR-')]
        ]
        
        janela = sg.Window('Dados do Usuário', layout, modal=True, finalize=True)
        
        while True:
            evento, valores = janela.read()
            
            if evento == sg.WINDOW_CLOSED or evento == '-CANCELAR-':
                janela.close()
                return None # Retorna None se o usuário cancelar

            if evento == '-SALVAR-':
                matricula = valores['-MATRICULA-'] if pedindo_matricula else None
                nome = valores['-NOME-'].strip()
                email = valores['-EMAIL-'].strip()
                
                if pedindo_matricula:
                    if not (matricula and matricula.isdigit()):
                        self.mostrar_popup("Erro de Validação", "Matrícula deve conter apenas números!")
                        continue 
                
                if not (nome and len(nome) >= 2):
                    self.mostrar_popup("Erro de Validação", "Nome deve ter pelo menos 2 caracteres!")
                    continue 

                if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                    self.mostrar_popup("Erro de Validação", "Email inválido! Use o formato: usuario@dominio.com")
                    continue 
                    
                janela.close()
                return {"matricula": matricula, "nome": nome, "email": email}

    # --- MÉTODO 3: O ANTIGO "pega_matricula_usuario" ---
    def pega_matricula_usuario(self) -> str:
        layout = [
            [sg.Text("Digite a matrícula do usuário:")],
            [sg.Input(key='-MATRICULA-')],
            [sg.Button('OK', key='-OK-'), sg.Button('Cancelar', key='-CANCELAR-')]
        ]
        janela = sg.Window('Selecionar Usuário', layout, modal=True, finalize=True)
        
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED or evento == '-CANCELAR-':
                janela.close()
                return None
            
            if evento == '-OK-':
                matricula = valores['-MATRICULA-']
                if matricula and matricula.isdigit():
                    janela.close()
                    return matricula
                else:
                    self.mostrar_popup("Erro", "Matrícula deve conter apenas números!")

    # --- MÉTODO 4: O ANTIGO "mostra_usuarios" ---
    def mostra_usuarios(self, lista_dados_usuarios: List[dict]):
        if not lista_dados_usuarios:
            self.mostrar_popup("Lista de Usuários", "Nenhum usuário cadastrado.")
            return

        headings = ['Matrícula', 'Nome', 'Email']
        dados_tabela = [
            [dados['matricula'], dados['nome'], dados['email']] 
            for dados in lista_dados_usuarios
        ]

        layout = [
            [sg.Text("-------- LISTA DE USUÁRIOS ----------")],
            [sg.Table(values=dados_tabela, headings=headings,
                      auto_size_columns=True, justification='left',
                      key='-TABLE-', expand_x=True, expand_y=True)],
            [sg.Button('Fechar')]
        ]
        
        janela = sg.Window('Lista de Usuários', layout, resizable=True, modal=True, finalize=True)
        janela.read() 
        janela.close()
        
    # --- MÉTODO 5: O ANTIGO "pega_dados_avaliacao" ---
    def pega_dados_avaliacao(self) -> dict:
        layout = [
            [sg.Text("\n-------- AVALIAR EVENTO ----------", font=("Helvetica", 14, "bold"))],
            [sg.Text("Nota (1-5):", size=(10,1)), sg.Input(size=(5, 1), key='-NOTA-')],
            [sg.Text("Comentário:")],
            [sg.Multiline(size=(45, 5), key='-COMENTARIO-')],
            [sg.Button('Salvar', key='-SALVAR-'), sg.Button('Cancelar', key='-CANCELAR-')]
        ]
        janela = sg.Window('Avaliar Evento', layout, modal=True, finalize=True)
        
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED or evento == '-CANCELAR-':
                janela.close()
                return None 
            if evento == '-SALVAR-':
                nota_str = valores['-NOTA-']
                comentario = valores['-COMENTARIO-']
                if not nota_str.isdigit():
                    self.mostrar_popup("Erro de Validação", "Entrada inválida. Digite um número para a nota.")
                    continue
                nota_int = int(nota_str)
                if not (1 <= nota_int <= 5):
                    self.mostrar_popup("Erro de Validação", "Nota inválida. Por favor, insira um valor entre 1 e 5.")
                    continue
                janela.close()
                return {"nota": nota_int, "comentario": comentario}

    # --- MÉTODO 6: O ANTIGO "mostra_usuario" ---
    def mostra_usuario(self, dados_usuario: dict):
        layout = [
            [sg.Text("--- DETALHES DO USUÁRIO ---", font=("Helvetica", 14, "bold"))],
            [sg.Text("Matrícula:", size=(10, 1), font=("Helvetica", 10, "bold")), 
             sg.Text(dados_usuario['matricula'])],
            [sg.Text("Nome:", size=(10, 1), font=("Helvetica", 10, "bold")), 
             sg.Text(dados_usuario['nome'])],
            [sg.Text("Email:", size=(10, 1), font=("Helvetica", 10, "bold")), 
             sg.Text(dados_usuario['email'])],
            [sg.Text("-----------------------------")],
            [sg.Button('OK', key='-OK-')]
        ]
        janela = sg.Window('Detalhes do Usuário', layout, modal=True, finalize=True)
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED or evento == '-OK-':
                break
        janela.close()

    # --- MÉTODO 7: O ANTIGO "mostra_historico_compras" ---
    def mostra_historico_compras(self, historico_dados: list):
        if not historico_dados:
            self.mostrar_popup("Histórico de Compras", "\nNenhuma compra realizada.")
            return 

        total_gasto = sum(item['valor'] for item in historico_dados)
        headings = ['#', 'Tipo', 'Descrição', 'Valor (R$)', 'Data', 'Método']
        
        dados_tabela = []
        for i, item in enumerate(historico_dados, 1):
            dados_tabela.append([
                i, item['tipo'], item['descricao'],
                f"{item['valor']:.2f}", item['data'], item['metodo']
            ])
            
        layout = [
            [sg.Text("\n-------- HISTÓRICO DE COMPRAS ----------", font=("Helvetica", 14, "bold"))],
            [sg.Table(values=dados_tabela, headings=headings,
                      auto_size_columns=True, justification='left',
                      num_rows=min(len(dados_tabela), 15), 
                      key='-TABLE-', expand_x=True, expand_y=True)],
            [sg.Text(f"💰 TOTAL GASTO: R$ {total_gasto:.2f}", font=("Helvetica", 12, "bold"))],
            [sg.Button('Fechar')]
        ]
        
        janela = sg.Window('Histórico de Compras', layout, resizable=True, modal=True, finalize=True)
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED or evento == 'Fechar':
                break
        janela.close()

    # --- MÉTODO 8: O ANTIGO "mostra_ingressos_usuario" ---
    def mostra_ingressos_usuario(self, dados_ingressos: list):
        if not dados_ingressos:
            self.mostrar_popup("Meus Ingressos", "\nVocê não possui ingressos.")
            return

        headings = ['#', 'Evento', 'Data Evento', 'Local', 'Preço (R$)', 'Data Compra']
        dados_tabela = []
        for i, ingresso in enumerate(dados_ingressos, 1):
            dados_tabela.append([
                i, ingresso['evento_nome'], ingresso['evento_data'],
                ingresso['evento_local'], f"{ingresso['preco']:.2f}",
                ingresso['data_compra']
            ])
            
        layout = [
            [sg.Text("\n-------- MEUS INGRESSOS ----------", font=("Helvetica", 14, "bold"))],
            [sg.Table(values=dados_tabela, headings=headings,
                      auto_size_columns=True, justification='left',
                      num_rows=min(len(dados_ingressos), 10),
                      key='-TABLE-', expand_x=True, expand_y=True)],
            [sg.Button('Fechar')]
        ]
        
        janela = sg.Window('Meus Ingressos', layout, resizable=True, modal=True, finalize=True)
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED or evento == 'Fechar':
                break
        janela.close()