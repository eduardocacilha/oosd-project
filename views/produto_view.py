from typing import List, Optional
import FreeSimpleGUI as sg
import re # Para a validação de email, embora não seja usado aqui

class ProdutoView:
    
    def __init__(self):
        sg.theme('Reddit')

    def mostrar_popup(self, titulo: str, msg: str):
        """Substituto do 'mostra_mensagem'. Exibe um popup."""
        sg.Popup(titulo, msg, keep_on_top=True, modal=True)

    def tela_opcoes(self) -> int:
        """Cria e gerencia a janela do MENU de Produtos."""
        layout = [
            [sg.Text("\n-------- MENU PRODUTOS ----------", font=("Helvetica", 14, "bold"))],
            [sg.Button('Adicionar Produto a um Evento', key=1, size=(30,1))],
            [sg.Button('Alterar Produto', key=2, size=(30,1))],
            [sg.Button('Listar Produtos de um Evento', key=3, size=(30,1))],
            [sg.Button('Excluir Produto', key=4, size=(30,1))],
            [sg.Button('Registrar Venda', key=5, size=(30,1))],
            [sg.Button('Relatório de Vendas', key=6, size=(30,1))],
            [sg.Button('Retornar ao Menu Principal', key=0, size=(30,1), button_color=('white', 'red'))]
        ]
        
        janela = sg.Window('Menu Produtos', layout, finalize=True, modal=True)
        
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED:
                janela.close()
                return 0 # Trata o 'X' como 'Retornar'
            janela.close()
            return evento # Retorna o NÚMERO (int) da key

    def escolher_tipo_produto(self) -> int:
        """Abre um menu para escolher o tipo de produto (Camisa ou Copo)."""
        layout = [
            [sg.Text("\n-------- TIPO DE PRODUTO ----------", font=("Helvetica", 14, "bold"))],
            [sg.Button('Camisa', key=1, size=(20,1))],
            [sg.Button('Copo', key=2, size=(20,1))],
            [sg.Button('Cancelar', key=0, size=(20,1), button_color=('white', 'red'))]
        ]
        janela = sg.Window('Escolher Tipo de Produto', layout, modal=True, finalize=True)
        
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED:
                janela.close()
                return 0
            janela.close()
            return evento # Retorna 1, 2 ou 0

    def pega_dados_camisa(self) -> dict:
        """Abre um formulário para dados de Camisa e valida."""
        
        layout = [
            [sg.Text("\n-------- DADOS DA CAMISA ----------", font=("Helvetica", 14, "bold"))],
            [sg.Text("Nome:", size=(10,1)), sg.Input(key='1')],
            [sg.Text("Preço (R$):", size=(10,1)), sg.Input(key='2', size=(10,1))],
            [sg.Text("Estoque:", size=(10,1)), sg.Input(key='3', size=(10,1))],
            [sg.Text("Tamanho:", size=(10,1)), 
             sg.Combo(['P', 'M', 'G', 'GG'], key='4', size=(10,1), readonly=True)],
            [sg.Text("Cor:", size=(10,1)), sg.Input(key='5')],
            [sg.Button('Salvar', key='6'), sg.Button('Cancelar', key='7')]
        ]
        janela = sg.Window('Dados da Camisa', layout, modal=True, finalize=True)
        
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED or evento == '7':
                janela.close()
                return None

            if evento == '6':
                # Validação de Nome
                nome = valores['1'].strip()
                if not nome:
                    self.mostrar_popup("Erro", "Nome não pode estar vazio!")
                    continue
                
                # Validação de Preço
                try:
                    preco = float(valores['2'])
                    if preco <= 0:
                        self.mostrar_popup("Erro", "Preço deve ser maior que zero!")
                        continue
                except ValueError:
                    self.mostrar_popup("Erro", "Preço inválido! Digite um número.")
                    continue
                
                # Validação de Estoque
                try:
                    estoque = int(valores['3'])
                    if estoque < 0:
                        self.mostrar_popup("Erro", "Estoque não pode ser negativo!")
                        continue
                except ValueError:
                    self.mostrar_popup("Erro", "Estoque inválido! Digite um número inteiro.")
                    continue

                # Validação de Tamanho
                tamanho = valores['4']
                if tamanho not in ["P", "M", "G", "GG"]:
                    self.mostrar_popup("Erro", "Tamanho inválido! Selecione uma opção.")
                    continue
                    
                # Validação de Cor
                cor = valores['5'].strip()
                if not cor:
                    self.mostrar_popup("Erro", "Cor não pode estar vazia!")
                    continue
                    
                # Se tudo passou
                janela.close()
                return {
                    "nome": nome, "preco": preco, "estoque": estoque,
                    "tamanho": tamanho, "cor": cor
                }

    def pega_dados_copo(self) -> dict:
        """Abre um formulário para dados de Copo e valida."""
        
        layout = [
            [sg.Text("\n-------- DADOS DO COPO ----------", font=("Helvetica", 14, "bold"))],
            [sg.Text("Nome:", size=(12,1)), sg.Input(key='1')],
            [sg.Text("Preço (R$):", size=(12,1)), sg.Input(key='2', size=(10,1))],
            [sg.Text("Estoque:", size=(12,1)), sg.Input(key='3', size=(10,1))],
            [sg.Text("Capacidade (ml):", size=(12,1)), sg.Input(key='4', size=(10,1))],
            [sg.Text("Material:", size=(12,1)), sg.Input(key='5')],
            [sg.Button('Salvar', key='6'), sg.Button('Cancelar', key='7')]
        ]
        janela = sg.Window('Dados do Copo', layout, modal=True, finalize=True)
        
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED or evento == '7':
                janela.close()
                return None

            if evento == '6':
                nome = valores['1'].strip()
                if not nome:
                    self.mostrar_popup("Erro", "Nome não pode estar vazio!")
                    continue
                
                try:
                    preco = float(valores['2'])
                    if preco <= 0:
                        self.mostrar_popup("Erro", "Preço deve ser maior que zero!")
                        continue
                except ValueError:
                    self.mostrar_popup("Erro", "Preço inválido! Digite um número.")
                    continue
                
                try:
                    estoque = int(valores['3'])
                    if estoque < 0:
                        self.mostrar_popup("Erro", "Estoque não pode ser negativo!")
                        continue
                except ValueError:
                    self.mostrar_popup("Erro", "Estoque inválido! Digite um número inteiro.")
                    continue
                
                try:
                    capacidade = int(valores['4'])
                    if capacidade <= 0:
                        self.mostrar_popup("Erro", "Capacidade deve ser maior que zero!")
                        continue
                except ValueError:
                    self.mostrar_popup("Erro", "Capacidade inválida! Digite um número inteiro.")
                    continue
                    
                material = valores['5'].strip()
                if not material:
                    self.mostrar_popup("Erro", "Material não pode estar vazio!")
                    continue
                    
                # Se tudo passou
                janela.close()
                return {
                    "nome": nome, "preco": preco, "estoque": estoque,
                    "capacidade_ml": capacidade, "material": material
                }

    def mostra_produtos(self, lista_produtos: List[dict]):
        """Mostra uma tabela de produtos (para um evento)."""
        
        if not lista_produtos:
            self.mostrar_popup("Produtos", "\nNenhum produto cadastrado para este evento.")
            return
        
        headings = ['#', 'Descrição', 'Preço (R$)', 'Estoque']
        dados_tabela = []
        for i, produto in enumerate(lista_produtos, 1):
            dados_tabela.append([
                i,
                produto['descricao'],
                f"{produto['preco']:.2f}",
                produto['estoque']
            ])

        layout = [
            [sg.Text("\n-------- PRODUTOS DO EVENTO ----------", font=("Helvetica", 14, "bold"))],
            [sg.Table(values=dados_tabela, headings=headings,
                      auto_size_columns=True, justification='left',
                      num_rows=min(len(dados_tabela), 15),
                      key='-TABLE-', expand_x=True, expand_y=True)],
            [sg.Button('Fechar')]
        ]
        
        janela = sg.Window('Produtos do Evento', layout, resizable=True, modal=True, finalize=True)
        janela.read()
        janela.close()

    def seleciona_produto(self, lista_produtos: List[dict]) -> Optional[int]:
        """Mostra uma tabela de produtos e permite a seleção, retornando o ÍNDICE."""
        
        if not lista_produtos:
            self.mostrar_popup("Selecionar Produto", "\nNenhum produto disponível.")
            return None
        
        headings = ['#', 'Descrição', 'Preço (R$)', 'Estoque']
        dados_tabela = []
        for i, produto in enumerate(lista_produtos, 1):
            dados_tabela.append([
                i,
                produto['descricao'],
                f"{produto['preco']:.2f}",
                produto['estoque']
            ])
            
        layout = [
            [sg.Text("\n-------- SELECIONE UM PRODUTO ----------", font=("Helvetica", 14, "bold"))],
            [sg.Table(values=dados_tabela, headings=headings,
                      auto_size_columns=True, justification='left',
                      num_rows=min(len(dados_tabela), 10),
                      key='-TABLE-', 
                      enable_events=True,
                      select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                      expand_x=True, expand_y=True)],
            [sg.Text("0 - Cancelar")],
            [sg.Button('Selecionar', key='1'), sg.Button('Cancelar', key='2')]
        ]
        
        janela = sg.Window('Selecionar Produto', layout, resizable=True, modal=True, finalize=True)
        
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED or evento == '2':
                janela.close()
                return None
            
            if evento == '1':
                indices_selecionados = valores['-TABLE-']
                if not indices_selecionados:
                    self.mostrar_popup("Erro", "Nenhum produto selecionado. Por favor, clique em uma linha da tabela.")
                    continue
                else:
                    indice_selecionado = indices_selecionados[0]
                    janela.close()
                    # Retorna o índice (base 0)
                    return indice_selecionado

    def pega_quantidade_venda(self) -> Optional[int]:
        """Pede a quantidade do produto."""
        layout = [
            [sg.Text("Digite a quantidade:")],
            [sg.Input(key='-QTD-', size=(10,1))],
            [sg.Button('OK', key='1'), sg.Button('Cancelar', key='2')]
        ]
        janela = sg.Window('Quantidade', layout, modal=True, finalize=True)
        
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED or evento == '2':
                janela.close()
                return None
            
            if evento == '1':
                qtd_str = valores['-QTD-']
                try:
                    qtd_int = int(qtd_str)
                    if qtd_int > 0:
                        janela.close()
                        return qtd_int
                    else:
                        self.mostrar_popup("Erro", "Quantidade deve ser maior que zero.")
                except ValueError:
                    self.mostrar_popup("Erro", "Quantidade inválida. Digite um número.")

    def pega_metodo_pagamento(self) -> str:
        """Cria um menu para selecionar o método de pagamento."""
        layout = [
            [sg.Text("\n-------- MÉTODO DE PAGAMENTO ----------", font=("Helvetica", 14, "bold"))],
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
                return "Dinheiro" # Default do seu código antigo
            if evento in metodos:
                janela.close()
                return metodos[evento]

    def mostra_venda_realizada(self, dados_venda: dict):
        """Mostra um resumo da venda ao finalizá-la."""
        layout = [
            [sg.Text("--- VENDA REALIZADA COM SUCESSO ---", font=("Helvetica", 14, "bold"))],
            [sg.Text("ID da Venda:", size=(10, 1), font=("Helvetica", 10, "bold")), 
             sg.Text(dados_venda['id_venda'])],
            [sg.Text("Cliente:", size=(10, 1), font=("Helvetica", 10, "bold")), 
             sg.Text(dados_venda['cliente'])],
            [sg.Text("Evento:", size=(10, 1), font=("Helvetica", 10, "bold")), 
             sg.Text(dados_venda['evento'])],
            [sg.Text("Método:", size=(10, 1), font=("Helvetica", 10, "bold")), 
             sg.Text(dados_venda['metodo'])],
            [sg.Text("TOTAL:", size=(10, 1), font=("Helvetica", 12, "bold")), 
             sg.Text(f"R$ {dados_venda['total']:.2f}", font=("Helvetica", 12, "bold"))],
            [sg.Button('OK', key='-OK-')]
        ]
        janela = sg.Window('Venda Concluída', layout, modal=True, finalize=True)
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED or evento == '-OK-':
                break
        janela.close()

    def mostra_relatorio_vendas(self, lista_vendas: List[dict]):
        """Mostra uma tabela com o relatório de vendas e o total."""
        
        if not lista_vendas:
            self.mostrar_popup("Relatório", "\nNenhuma venda registrada.")
            return
        
        total_geral = sum(venda['total'] for venda in lista_vendas)

        headings = ['ID Venda', 'Cliente', 'Evento', 'Data', 'Método', 'Total (R$)']
        dados_tabela = []
        for venda in lista_vendas:
            dados_tabela.append([
                venda['id_venda'],
                venda['cliente'],
                venda['evento'],
                venda['data'],
                venda['metodo'],
                f"{venda['total']:.2f}"
            ])
            
        layout = [
            [sg.Text("\n-------- RELATÓRIO DE VENDAS ----------", font=("Helvetica", 14, "bold"))],
            [sg.Table(values=dados_tabela, headings=headings,
                      auto_size_columns=True, justification='left',
                      num_rows=min(len(dados_tabela), 15),
                      key='-TABLE-', expand_x=True, expand_y=True)],
            [sg.Text(f"\nTOTAL GERAL: R$ {total_geral:.2f}", font=("Helvetica", 12, "bold"))],
            [sg.Button('Fechar')]
        ]
        
        janela = sg.Window('Relatório de Vendas', layout, resizable=True, modal=True, finalize=True)
        janela.read()
        janela.close()

