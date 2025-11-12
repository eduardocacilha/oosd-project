from typing import List, Optional
import FreeSimpleGUI as sg
from datetime import datetime

class EventoView:
    
    
    def __init__(self):
        sg.theme('Reddit')

    def mostrar_popup(self, titulo: str, msg: str):
        """Exibe um popup simples."""
        sg.Popup(titulo, msg, keep_on_top=True)
    
    def tela_opcoes(self) -> int:
        
        layout = [
            [sg.Text("\n-------- MENU EVENTOS ----------", font=("Helvetica", 14, "bold"))],
            [sg.Button('Incluir Evento', key=1, size=(30,1))],
            [sg.Button('Alterar Evento', key=2, size=(30,1))],
            [sg.Button('Listar Eventos', key=3, size=(30,1))],
            [sg.Button('Excluir Evento', key=4, size=(30,1))],
            [sg.Button('Ver Detalhes de um Evento', key=5, size=(30,1))],
            [sg.Button('Ver Feedbacks de um Evento', key=6, size=(30,1))],
            [sg.Button('Retornar ao Menu Principal', key=0, size=(30,1), button_color=('white', 'red'))]
        ]
        

        janela = sg.Window('Menu Eventos', layout, finalize=True, modal=True)
        while True:
            evento, valores = janela.read()
            
            if evento == sg.WINDOW_CLOSED:
                janela.close()
                return 0 

            janela.close()
            return evento
        
    def pega_dados_evento(self) -> dict:
        """Cria um formulário, valida os dados e retorna um dicionário."""
        
        # O CalendarButton facilita a vida do usuário e a validação
        layout = [
            [sg.Text("\n-------- DADOS DO EVENTO ----------", font=("Helvetica", 14, "bold"))],
            [sg.Text("Nome:", size=(10,1)), sg.Input(key='1')],
            [sg.Text("Data:", size=(10,1)), sg.Input(key='2', size=(10,1)), 
             sg.CalendarButton('Escolher', target='-DATA-', format='%d/%m/%Y')],
            [sg.Text("Local:", size=(10,1)), sg.Input(key='3')],
            [sg.Text("Preço (R$):", size=(10,1)), sg.Input(key='4', size=(10,1))],
            [sg.Button('Salvar', key='5'), sg.Button('Cancelar', key='6')]
        ]
        
        janela = sg.Window('Dados do Evento', layout, modal=True, finalize=True)
        
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED or evento == '6':
                janela.close()
                return None # Retorna None se o usuário cancelar

            if evento == '5':
                nome = valores['1'].strip()
                data_str = valores['2'].strip()
                local = valores['3'].strip()
                preco_str = valores['4'].strip()
                
                # Validação 1: Nome
                if not nome:
                    self.mostrar_popup("Erro", "Nome do evento não pode estar vazio!")
                    continue
                
                # Validação 2: Data (formato e se é no passado)
                try:
                    data_obj = datetime.strptime(data_str, '%d/%m/%Y')
                    if data_obj.date() < datetime.now().date():
                        self.mostrar_popup("Erro", "A data do evento não pode ser no passado!")
                        continue
                except ValueError:
                    self.mostrar_popup("Erro", "ERRO: Formato de data inválido. Use o calendário ou DD/MM/AAAA.")
                    continue
                
                # Validação 3: Local
                if not local:
                    self.mostrar_popup("Erro", "Local não pode estar vazio!")
                    continue
                
                # Validação 4: Preço (se é número e se é positivo)
                try:
                    preco_float = float(preco_str)
                    if preco_float < 0:
                        self.mostrar_popup("Erro", "Preço não pode ser negativo!")
                        continue
                except ValueError:
                    self.mostrar_popup("Erro", "Preço inválido. Use apenas números (ex: 100.50).")
                    continue
                    
                # Se todas as validações passaram:
                janela.close()
                return {
                    "nome": nome,
                    "data": data_str, # Retorna a string, o Model/Controller que lide com o objeto
                    "local": local,
                    "preco_entrada": preco_float
                }

    def mostra_evento(self, dados_evento: dict):
        """Cria uma janela modal para mostrar os dados de UM evento."""
        
        layout = [
            [sg.Text("--- DETALHES DO EVENTO ---", font=("Helvetica", 14, "bold"))],
            [sg.Text("Nome:", size=(10, 1), font=("Helvetica", 10, "bold")), 
             sg.Text(dados_evento['nome'])],
            [sg.Text("Data:", size=(10, 1), font=("Helvetica", 10, "bold")), 
             sg.Text(dados_evento['data'])],
            [sg.Text("Local:", size=(10, 1), font=("Helvetica", 10, "bold")), 
             sg.Text(dados_evento['local'])],
            [sg.Text("Preço:", size=(10, 1), font=("Helvetica", 10, "bold")), 
             sg.Text(f"R$ {dados_evento['preco_entrada']:.2f}")],
            [sg.Text("-----------------------------")],
            [sg.Button('OK', Okey='1')]
        ]
        
        janela = sg.Window('Detalhes do Evento', layout, modal=True, finalize=True)
        
        # Loop simples, só espera o usuário fechar
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED or evento == '-OK-':
                break
        
        janela.close()

    def mostra_eventos(self, lista_dados_eventos: List[dict]):
        """Cria uma janela com uma tabela para mostrar VÁRIOS eventos."""
        
        if not lista_dados_eventos:
            self.mostrar_popup("Lista de Eventos", "\nNenhum evento cadastrado.")
            return

        headings = ['#', 'Nome', 'Data', 'Local', 'Preço (R$)']
        dados_tabela = []
        
        for i, dados in enumerate(lista_dados_eventos, 1):
            dados_tabela.append([
                i,
                dados['nome'],
                dados['data'],
                dados['local'],
                f"{dados['preco_entrada']:.2f}"
            ])

        layout = [
            [sg.Text("\n-------- LISTA DE EVENTOS ----------", font=("Helvetica", 14, "bold"))],
            [sg.Table(values=dados_tabela, headings=headings,
                      auto_size_columns=True, justification='left',
                      num_rows=min(len(dados_tabela), 15),
                      key='1', expand_x=True, expand_y=True)],
            [sg.Button('Fechar')]
        ]
        
        janela = sg.Window('Lista de Eventos', layout, resizable=True, modal=True, finalize=True)
        janela.read() # Espera o usuário clicar em "Fechar" ou no 'X'
        janela.close()

    def mostra_detalhes_evento(self, dados_detalhados_evento: dict):
        """Mostra os dados de um evento, incluindo a nota média."""
        
        # Prepara a string da nota média
        if dados_detalhados_evento.get('nota_media') is not None:
            nota = dados_detalhados_evento['nota_media']
            avaliacoes = dados_detalhados_evento['total_avaliacoes']
            nota_str = f"{nota:.1f}/5.0 ({avaliacoes} avaliações)"
        else:
            nota_str = "Ainda não há avaliações para este evento."
            
        layout = [
            [sg.Text("--- DETALHES DO EVENTO ---", font=("Helvetica", 14, "bold"))],
            [sg.Text("Nome:", size=(15, 1), font=("Helvetica", 10, "bold")), 
             sg.Text(dados_detalhados_evento['nome'])],
            [sg.Text("Data:", size=(15, 1), font=("Helvetica", 10, "bold")), 
             sg.Text(dados_detalhados_evento['data'])],
            [sg.Text("Local:", size=(15, 1), font=("Helvetica", 10, "bold")), 
             sg.Text(dados_detalhados_evento['local'])],
            [sg.Text("Preço:", size=(15, 1), font=("Helvetica", 10, "bold")), 
             sg.Text(f"R$ {dados_detalhados_evento['preco_entrada']:.2f}")],
            [sg.Text("------------------------------------")],
            [sg.Text("Avaliação Média:", size=(15, 1), font=("Helvetica", 10, "bold")), 
             sg.Text(nota_str)],
            [sg.Text("------------------------------------")],
            [sg.Button('OK', key='1')]
        ]
        
        janela = sg.Window('Detalhes do Evento', layout, modal=True, finalize=True)
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED or evento == '1':
                break
        janela.close()

    def mostra_feedbacks(self, lista_dados_feedbacks: List[dict]):
        """Cria uma janela com uma tabela para mostrar os feedbacks."""
        
        if not lista_dados_feedbacks:
            self.mostrar_popup("Feedbacks do Evento", "\nNenhum feedback encontrado para este evento.")
            return

        headings = ['#', 'Usuário', 'Nota', 'Comentário', 'Data']
        dados_tabela = []
        
        for i, dados in enumerate(lista_dados_feedbacks, 1):
            dados_tabela.append([
                i,
                dados['nome_usuario'],
                f"{dados['nota']}/5",
                dados['comentario'],
                dados['data']
            ])

        layout = [
            [sg.Text("\n-------- FEEDBACKS DO EVENTO ----------", font=("Helvetica", 14, "bold"))],
            [sg.Table(values=dados_tabela, headings=headings,
                      auto_size_columns=True, justification='left',
                      col_widths=[5, 15, 5, 30, 10], # Ajusta o tamanho da coluna de comentário
                      num_rows=min(len(dados_tabela), 10),
                      key='1', expand_x=True, expand_y=True)],
            [sg.Button('Fechar')]
        ]
        
        janela = sg.Window('Feedbacks do Evento', layout, resizable=True, modal=True, finalize=True)
        janela.read()
        janela.close()

    def seleciona_evento(self, lista_dados_eventos: List[dict]) -> Optional[int]:
        """
        Mostra uma tabela de eventos e permite ao usuário selecionar um.
        Retorna o ÍNDICE (int) do evento selecionado na lista.
        """
        
        if not lista_dados_eventos:
            self.mostrar_popup("Selecionar Evento", "Nenhum evento disponível para selecionar.")
            return None
        
        headings = ['#', 'Nome', 'Data', 'Local', 'Preço (R$)']
        dados_tabela = []
        
        for i, dados in enumerate(lista_dados_eventos, 1):
            dados_tabela.append([
                i,
                dados['nome'],
                dados['data'],
                dados['local'],
                f"{dados['preco_entrada']:.2f}"
            ])
            
        layout = [
            [sg.Text("\n-------- SELECIONE UM EVENTO ----------", font=("Helvetica", 14, "bold"))],
            [sg.Table(values=dados_tabela, headings=headings,
                      auto_size_columns=True, justification='left',
                      num_rows=min(len(dados_tabela), 15),
                      key='1', 
                      enable_events=True, # Habilita eventos de clique na tabela
                      select_mode=sg.TABLE_SELECT_MODE_BROWSE, # Permite selecionar 1 linha
                      expand_x=True, expand_y=True)],
            [sg.Button('Selecionar', key='2'), sg.Button('Cancelar', key='3')]
        ]
        
        janela = sg.Window('Selecionar Evento', layout, resizable=True, modal=True, finalize=True)
        
        while True:
            evento, valores = janela.read()
            
            if evento == sg.WINDOW_CLOSED or evento == '3':
                janela.close()
                return None
            
            if evento == '2':
                # 'valores' é um dicionário. A chave '1' contém
                # uma LISTA de índices de linhas selecionadas.
                indices_selecionados = valores['1']
                
                if not indices_selecionados:
                    # Se o usuário não selecionou nenhuma linha
                    self.mostrar_popup("Erro", "Nenhum evento selecionado. Por favor, clique em uma linha da tabela.")
                    continue
                else:
                    # Pega o primeiro (e único) índice da lista
                    indice_selecionado = indices_selecionados[0]
                    janela.close()
                    # Retorna o índice, exatamente como seu código antigo
                    return indice_selecionado