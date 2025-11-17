from typing import List
import FreeSimpleGUI as sg
import re
from exceptions.entidadeNaoEncontradaException import EntidadeNaoEncontradaException
from exceptions.regraDeNegocioException import RegraDeNegocioException

class UsuarioView:
    
    def __init__(self):
        sg.theme('Reddit')

    def mostrar_popup(self, titulo: str, msg: str):
        """Exibe um popup simples, agora com modal=True."""
        try:
            sg.Popup(titulo, msg, keep_on_top=True, modal=True)
        except Exception as e:
            print(f"✗ Erro ao exibir popup: {str(e)}")

    def criar_janela_menu_usuario(self) -> str:
        """
        Cria, exibe e gerencia a janela do MENU de usuários.
        Retorna a 'key' do botão clicado (ex: '1') ou '0'.
        """
        try:
            layout = [
                [sg.Text("============================================")],
                [sg.Text("          GERENCIAR USUÁRIOS")],
                [sg.Text("============================================")],
                [sg.Button('Incluir Usuário', key='1', size=(30,1))],
                [sg.Button('Alterar Usuário', key='3', size=(30,1))],
                [sg.Button('Listar Usuários', key='2', size=(30,1))],
                [sg.Button('Excluir Usuário', key='4', size=(30,1))],
                [sg.Button('Listar Meus Ingressos', key='6', size=(30,1))],
                [sg.Button('Ver Meu Histórico de Compras', key='5', size=(30,1))],
                [sg.Button('Avaliar um Evento', key='7', size=(30,1))],
                [sg.Button('Voltar ao Menu Principal', key='0', size=(30,1), button_color=('white', 'red'))]
            ]
            
            janela = sg.Window('Menu de Usuários', layout, finalize=True)
            
            while True:
                evento, valores = janela.read()
                
                if evento == sg.WINDOW_CLOSED or evento == '0':
                    janela.close()
                    return '0'
                else:
                    janela.close()
                    return evento
                    
        except Exception as e:
            self.mostrar_popup("✗ Erro", f"Erro ao criar menu: {str(e)}")
            return '0'

    def pega_dados_usuario(self, pedindo_matricula=True) -> dict:
        """Coleta dados do usuário com validação e tratamento de exceções"""
        try:
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
                    return None

                if evento == '-SALVAR-':
                    try:
                        matricula = valores['-MATRICULA-'].strip() if pedindo_matricula else None
                        nome = valores['-NOME-'].strip()
                        email = valores['-EMAIL-'].strip()
                        
                        # Validações
                        if pedindo_matricula:
                            if not matricula:
                                raise ValueError("Matrícula não pode estar vazia!")
                            if not matricula.isdigit():
                                raise ValueError("Matrícula deve conter apenas números!")
                        
                        if not nome or len(nome) < 2:
                            raise ValueError("Nome deve ter pelo menos 2 caracteres!")
                        
                        if not email:
                            raise ValueError("Email não pode estar vazio!")
                        
                        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                            raise ValueError("Email inválido! Use o formato: usuario@dominio.com")
                        
                        janela.close()
                        return {"matricula": matricula, "nome": nome, "email": email}
                        
                    except ValueError as ve:
                        self.mostrar_popup("✗ Erro de Validação", str(ve))
                        continue
                        
        except Exception as e:
            self.mostrar_popup("✗ Erro", f"Erro ao coletar dados: {str(e)}")
            return None

    def pega_matricula_usuario(self) -> str:
        """Coleta matrícula do usuário com validação"""
        try:
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
                    try:
                        matricula = valores['-MATRICULA-'].strip()
                        
                        if not matricula:
                            raise ValueError("Matrícula não pode estar vazia!")
                        
                        if not matricula.isdigit():
                            raise ValueError("Matrícula deve conter apenas números!")
                        
                        janela.close()
                        return matricula
                        
                    except ValueError as ve:
                        self.mostrar_popup("✗ Erro de Validação", str(ve))
                        continue
                        
        except Exception as e:
            self.mostrar_popup("✗ Erro", f"Erro ao coletar matrícula: {str(e)}")
            return None

    def mostra_usuarios(self, lista_dados_usuarios: List[dict]):
        """Exibe lista de usuários com tratamento de exceções"""
        try:
            if not lista_dados_usuarios:
                self.mostrar_popup("ℹ Informação", "Nenhum usuário cadastrado.")
                return

            headings = ['Matrícula', 'Nome', 'Email']
            dados_tabela = [
                [str(dados.get('matricula', '')), str(dados.get('nome', '')), str(dados.get('email', ''))] 
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
            
        except Exception as e:
            self.mostrar_popup("✗ Erro", f"Erro ao exibir lista de usuários: {str(e)}")
        
    def pega_dados_avaliacao(self) -> dict:
        """Coleta dados de avaliação com validação"""
        try:
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
                    try:
                        nota_str = valores['-NOTA-'].strip()
                        comentario = valores['-COMENTARIO-'].strip()
                        
                        if not nota_str:
                            raise ValueError("Nota não pode estar vazia!")
                        
                        if not nota_str.isdigit():
                            raise ValueError("Nota deve ser um número!")
                        
                        nota_int = int(nota_str)
                        if not (1 <= nota_int <= 5):
                            raise ValueError("Nota deve estar entre 1 e 5!")
                        
                        if not comentario:
                            raise ValueError("Comentário não pode estar vazio!")
                        
                        janela.close()
                        return {"nota": nota_int, "comentario": comentario}
                        
                    except ValueError as ve:
                        self.mostrar_popup("✗ Erro de Validação", str(ve))
                        continue
                        
        except Exception as e:
            self.mostrar_popup("✗ Erro", f"Erro ao coletar avaliação: {str(e)}")
            return None

    def mostra_usuario(self, dados_usuario: dict):
        """Exibe detalhes do usuário"""
        try:
            layout = [
                [sg.Text("--- DETALHES DO USUÁRIO ---", font=("Helvetica", 14, "bold"))],
                [sg.Text("Matrícula:", size=(10, 1), font=("Helvetica", 10, "bold")), 
                 sg.Text(str(dados_usuario.get('matricula', 'N/A')))],
                [sg.Text("Nome:", size=(10, 1), font=("Helvetica", 10, "bold")), 
                 sg.Text(str(dados_usuario.get('nome', 'N/A')))],
                [sg.Text("Email:", size=(10, 1), font=("Helvetica", 10, "bold")), 
                 sg.Text(str(dados_usuario.get('email', 'N/A')))],
                [sg.Text("-----------------------------")],
                [sg.Button('OK', key='-OK-')]
            ]
            janela = sg.Window('Detalhes do Usuário', layout, modal=True, finalize=True)
            while True:
                evento, valores = janela.read()
                if evento == sg.WINDOW_CLOSED or evento == '-OK-':
                    break
            janela.close()
        except Exception as e:
            self.mostrar_popup("✗ Erro", f"Erro ao exibir detalhes: {str(e)}")

    def mostra_historico_compras(self, historico_dados: list):
        """Exibe histórico de compras com tratamento de exceções"""
        try:
            if not historico_dados:
                self.mostrar_popup("ℹ Informação", "Nenhuma compra realizada.")
                return 

            total_gasto = sum(float(item.get('valor', 0)) for item in historico_dados)
            headings = ['#', 'Tipo', 'Descrição', 'Valor (R$)', 'Data', 'Método']
            
            dados_tabela = []
            for i, item in enumerate(historico_dados, 1):
                dados_tabela.append([
                    i, 
                    str(item.get('tipo', 'N/A')), 
                    str(item.get('descricao', 'N/A')),
                    f"{float(item.get('valor', 0)):.2f}", 
                    str(item.get('data', 'N/A')), 
                    str(item.get('metodo', 'N/A'))
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
        except Exception as e:
            self.mostrar_popup("✗ Erro", f"Erro ao exibir histórico: {str(e)}")

    def mostra_ingressos_usuario(self, dados_ingressos: list):
        """Exibe ingressos do usuário com tratamento de exceções"""
        try:
            if not dados_ingressos:
                self.mostrar_popup("ℹ Informação", "Nenhum ingresso cadastrado.")
                return

            headings = ['#', 'Evento', 'Data Evento', 'Local', 'Preço (R$)', 'Data Compra']
            dados_tabela = []
            for i, ingresso in enumerate(dados_ingressos, 1):
                dados_tabela.append([
                    i, 
                    str(ingresso.get('evento_nome', 'N/A')), 
                    str(ingresso.get('evento_data', 'N/A')),
                    str(ingresso.get('evento_local', 'N/A')), 
                    f"{float(ingresso.get('preco', 0)):.2f}",
                    str(ingresso.get('data_compra', 'N/A'))
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
        except Exception as e:
            self.mostrar_popup("✗ Erro", f"Erro ao exibir ingressos: {str(e)}")