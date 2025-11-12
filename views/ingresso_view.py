from typing import List, Optional
import FreeSimpleGUI as sg 

class IngressoView:
    
    def __init__(self):
        sg.theme('Reddit')

    def tela_opcoes(self) -> int:
        
        layout = [
            [sg.Text("\n-------- MENU INGRESSOS ----------", font=("Helvetica", 14, "bold"))],
            [sg.Button('Comprar Ingresso de Evento', key=1, size=(30,1))],
            [sg.Button('Listar Meus Ingressos', key=2, size=(30,1))],
            [sg.Button('Gerenciar Revenda de Ingressos', key=3, size=(30,1))],
            [sg.Button('Retornar', key=0, size=(30,1), button_color=('white', 'red'))]
        ]
        
        janela = sg.Window('Menu Ingressos', layout, finalize=True, modal=True)
        
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED:
                janela.close()
                return 0 
            
            janela.close()
            return evento 
    
    def tela_opcoes_revenda(self) -> int:
        
        layout = [
            [sg.Text("\n-------- MENU REVENDA ----------", font=("Helvetica", 14, "bold"))],
            [sg.Button('Colocar Ingresso à Venda', key=1, size=(30,1))],
            [sg.Button('Remover Ingresso da Venda', key=2, size=(30,1))],
            [sg.Button('Comprar Ingresso de Revenda', key=3, size=(30,1))],
            [sg.Button('Listar Meus Ingressos à Venda', key=4, size=(30,1))],
            [sg.Button('Retornar', key=0, size=(30,1), button_color=('white', 'red'))]
        ]
        
        janela = sg.Window('Menu Revenda', layout, finalize=True, modal=True)
        
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED:
                janela.close()
                return 0 
            
            janela.close()
            return evento 

    def pega_novo_preco_revenda(self) -> Optional[float]:
        
        layout = [
            [sg.Text("Digite o novo preço para revenda: R$")],
            [sg.Input(key='2', size=(15,1))],
            [sg.Button('OK', key=1), sg.Button('Cancelar', key=0)]
        ]
        
        janela = sg.Window('Preço de Revenda', layout, modal=True, finalize=True)
        
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED or evento == 0:
                janela.close()
                return None 

            if evento == 1:
                preco_str = valores['2']
                try:
                    preco_float = float(preco_str)
                    if preco_float <= 0:
                         self.mostra_mensagem("Preço deve ser maior que zero.")
                         continue
                    janela.close()
                    return preco_float
                except ValueError:
                    self.mostra_mensagem("Preço inválido. Por favor, digite um número (ex: 50.00).")

    def mostra_ingresso(self, dados_ingresso: dict):
        
        if dados_ingresso.get('nome_revendedor'):
            status = f"À venda por {dados_ingresso['nome_revendedor']}"
        else:
            status = "Uso pessoal"
            
        layout = [
            [sg.Text("--- DETALHES DO INGRESSO ---", font=("Helvetica", 14, "bold"))],
            [sg.Text("Evento:", size=(12, 1), font=("Helvetica", 10, "bold")), 
             sg.Text(dados_ingresso['nome_evento'])],
            [sg.Text("Comprador:", size=(12, 1), font=("Helvetica", 10, "bold")), 
             sg.Text(dados_ingresso['nome_comprador'])],
            [sg.Text("Data da Compra:", size=(12, 1), font=("Helvetica", 10, "bold")), 
             sg.Text(dados_ingresso['data_compra'])],
            [sg.Text("Preço:", size=(12, 1), font=("Helvetica", 10, "bold")), 
             sg.Text(f"R$ {dados_ingresso['preco']:.2f}")],
            [sg.Text("Status:", size=(12, 1), font=("Helvetica", 10, "bold")), 
             sg.Text(status)],
            [sg.Text("-----------------------------")],
            [sg.Button('OK', key=1)]
        ]
        
        janela = sg.Window('Detalhes do Ingresso', layout, modal=True, finalize=True)
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED or evento == 1:
                break
        janela.close()

    def mostra_ingressos(self, lista_dados_ingressos: List[dict]):
        
        if not lista_dados_ingressos:
            self.mostra_mensagem("\nNenhum ingresso encontrado.")
            return

        headings = ['#', 'Evento', 'Comprador', 'Preço (R$)', 'Data Compra', 'Status']
        dados_tabela = []
        for i, dados in enumerate(lista_dados_ingressos, 1):
            if dados.get('nome_revendedor'):
                status = f"À venda por {dados['nome_revendedor']}"
            else:
                status = "Uso pessoal"
                
            dados_tabela.append([
                i,
                dados['nome_evento'],
                dados['nome_comprador'],
                f"{dados['preco']:.2f}",
                dados['data_compra'],
                status
            ])

        layout = [
            [sg.Text("\n-------- LISTA DE INGRESSOS ----------", font=("Helvetica", 14, "bold"))],
            [sg.Table(values=dados_tabela, headings=headings,
                      auto_size_columns=True, justification='left',
                      num_rows=min(len(dados_tabela), 15),
                      key='-TABLE-', expand_x=True, expand_y=True)],
            [sg.Button('Fechar', key=0)]
        ]
        
        janela = sg.Window('Lista de Ingressos', layout, resizable=True, modal=True, finalize=True)
        
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED or evento == 0:
                break
        janela.close()

    def mostra_ingressos_revenda(self, lista_dados_ingressos: List[dict]):
        
        if not lista_dados_ingressos:
            self.mostra_mensagem("\nNenhum ingresso disponível para revenda no momento.")
            return

        headings = ['#', 'Evento', 'Vendido por', 'Preço (R$)']
        dados_tabela = []
        for i, dados in enumerate(lista_dados_ingressos, 1):
            dados_tabela.append([
                i,
                dados['nome_evento'],
                dados['nome_revendedor'],
                f"{dados['preco']:.2f}"
            ])

        layout = [
            [sg.Text("\n-------- INGRESSOS DISPONÍVEIS PARA REVENDA ----------", font=("Helvetica", 14, "bold"))],
            [sg.Table(values=dados_tabela, headings=headings,
                      auto_size_columns=True, justification='left',
                      num_rows=min(len(dados_tabela), 15),
                      key='-TABLE-', expand_x=True, expand_y=True)],
            [sg.Button('Fechar', key=0)]
        ]
        
        janela = sg.Window('Ingressos para Revenda', layout, resizable=True, modal=True, finalize=True)
        
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED or evento == 0:
                break
        janela.close()

    def seleciona_ingresso(self, lista_dados_ingressos: List[dict]) -> Optional[int]:
        
        if not lista_dados_ingressos:
            self.mostra_mensagem("\n--- Selecione um de seus ingressos ---\nVocê não possui ingressos.")
            return None
        
        headings = ['#', 'Evento', 'Preço (R$)', 'Data Compra', 'Status']
        dados_tabela = []
        for i, dados in enumerate(lista_dados_ingressos, 1):
            status = "À venda" if dados.get('nome_revendedor') else "Uso pessoal"
            dados_tabela.append([
                i,
                dados['nome_evento'],
                f"{dados['preco']:.2f}",
                dados['data_compra'],
                status
            ])

        layout = [
            [sg.Text("\n--- Selecione um de seus ingressos ---", font=("Helvetica", 14, "bold"))],
            [sg.Table(values=dados_tabela, headings=headings,
                      auto_size_columns=True, justification='left',
                      num_rows=min(len(dados_tabela), 10),
                      key='-TABLE-', 
                      enable_events=True,
                      select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                      expand_x=True, expand_y=True)],
            [sg.Button('Selecionar', key=1), sg.Button('Cancelar', key=0)]
        ]
        
        janela = sg.Window('Selecionar Ingresso', layout, resizable=True, modal=True, finalize=True)
        
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED or evento == 0:
                janela.close()
                return None
            
            if evento == 1:
                indices_selecionados = valores['-TABLE-']
                if not indices_selecionados:
                    self.mostra_mensagem("Nenhum ingresso selecionado. Por favor, clique em uma linha da tabela.")
                    continue
                else:
                    indice_selecionado = indices_selecionados[0]
                    janela.close()
                    return indice_selecionado

    def seleciona_ingresso_revenda(self, lista_dados_ingressos: List[dict]) -> Optional[int]:
        
        if not lista_dados_ingressos:
            self.mostra_mensagem("\nNenhum ingresso disponível para revenda no momento.")
            return None

        headings = ['#', 'Evento', 'Vendido por', 'Preço (R$)']
        dados_tabela = []
        for i, dados in enumerate(lista_dados_ingressos, 1):
            dados_tabela.append([
                i,
                dados['nome_evento'],
                dados['nome_revendedor'],
                f"{dados['preco']:.2f}"
            ])

        layout = [
            [sg.Text("\n-------- INGRESSOS DISPONÍVEIS PARA REVENDA ----------", font=("Helvetica", 14, "bold"))],
            [sg.Table(values=dados_tabela, headings=headings,
                      auto_size_columns=True, justification='left',
                      num_rows=min(len(dados_tabela), 15),
                      key='-TABLE-',
                      enable_events=True,
                      select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                      expand_x=True, expand_y=True)],
            [sg.Button('Comprar Selecionado', key=1), sg.Button('Cancelar', key=0)]
        ]
        
        janela = sg.Window('Comprar Ingresso de Revenda', layout, resizable=True, modal=True, finalize=True)
        
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED or evento == 0:
                janela.close()
                return None
            
            if evento == 1:
                indices_selecionados = valores['-TABLE-']
                if not indices_selecionados:
                    self.mostra_mensagem("Nenhum ingresso selecionado. Por favor, clique em uma linha da tabela.")
                    continue
                else:
                    indice_selecionado = indices_selecionados[0]
                    janela.close()
                    return indice_selecionado

    def pega_matricula_comprador(self) -> str:
        
        layout = [
            [sg.Text("Digite a matrícula do comprador:")],
            [sg.Input(key='-MATRICULA-')],
            [sg.Button('OK', key=1), sg.Button('Cancelar', key=0)]
        ]
        janela = sg.Window('Identificar Comprador', layout, modal=True, finalize=True)
        
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED or evento == 0:
                janela.close()
                return None
            
            if evento == 1:
                matricula = valores['-MATRICULA-']
                if matricula and matricula.isdigit():
                    janela.close()
                    return matricula
                else:
                    self.mostra_mensagem("Matrícula deve conter apenas números!")

    def pega_metodo_pagamento(self) -> str:
        
        layout = [
            [sg.Text("\n-------- METODO DE PAGAMENTO ----------", font=("Helvetica", 14, "bold"))],
            [sg.Button('Dinheiro', key=1, size=(20,1))],
            [sg.Button('PIX', key=2, size=(20,1))],
            [sg.Button('Débito', key=3, size=(20,1))],
            [sg.Button('Crédito', key=4, size=(20,1))],
        ]
        
        janela = sg.Window('Método de Pagamento', layout, modal=True, finalize=True)
        
        metodos = {1: "Dinheiro", 2: "PIX", 3: "Debito", 4: "Credito"}
        
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED:
                janela.close()
                return None 
            
            if evento in metodos:
                janela.close()
                return metodos[evento] 

    def confirma_compra_ingresso(self, dados: dict) -> bool:
        
        evento_nome = dados['evento']
        preco = dados['preco']
        metodo = dados['metodo_pagamento']
        
        resposta = sg.popup_yes_no(
            "--- CONFIRMAR COMPRA ---",
            f"Evento: {evento_nome}",
            f"Preço: R$ {preco:.2f}",
            f"Método de Pagamento: {metodo}",
            "\nConfirmar compra?",
            title="Confirmação",
            keep_on_top=True
        )
        
        if resposta == 'Yes':
            return True
        else:
            self.mostra_mensagem("Compra cancelada.") 
            return False

    def mostra_mensagem(self, msg: str):
        sg.Popup(msg, title="Aviso", keep_on_top=True, modal=True)