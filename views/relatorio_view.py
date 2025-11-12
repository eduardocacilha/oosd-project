from typing import List
import FreeSimpleGUI as sg

class RelatorioView:
    
    def __init__(self):
        sg.theme('Reddit')
        
    def tela_opcoes(self) -> int:
        """Cria e gerencia a janela do MENU PRINCIPAL de Relatórios."""
        
        layout = [
            [sg.Text("\n======== MENU RELATORIOS ========", font=("Helvetica", 14, "bold"))],
            [sg.Button("Relatorios de Eventos", key=1, size=(30,1))],
            [sg.Button("Relatorios de Produtos", key=2, size=(30,1))],
            [sg.Button("Relatorios de Vendas", key=3, size=(30,1))],
            [sg.Button("Relatorios de Usuarios", key=4, size=(30,1))],
            [sg.Button("Retornar ao Menu Principal", key=0, size=(30,1), button_color=('white', 'red'))]
        ]
        
        janela = sg.Window('Menu Relatórios', layout, finalize=True, modal=True)
        
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED:
                janela.close()
                return 0 # Trata o 'X' como 'Retornar'
            janela.close()
            return evento # Retorna 1, 2, 3, 4, ou 0

    def tela_opcoes_eventos(self) -> int:
        """Cria e gerencia a janela do SUB-MENU de Relatórios de Eventos."""
        
        layout = [
            [sg.Text("\n-------- RELATORIOS DE EVENTOS ----------", font=("Helvetica", 14, "bold"))],
            [sg.Button("Eventos Mais Caros e Mais Baratos", key=1, size=(30,1))],
            [sg.Button("Eventos com Melhores Avaliacoes", key=2, size=(30,1))],
            [sg.Button("Eventos com Mais Ingressos Vendidos", key=3, size=(30,1))],
            [sg.Button("Ranking Completo de Eventos", key=4, size=(30,1))],
            [sg.Button("Voltar", key=0, size=(30,1), button_color=('white', 'red'))]
        ]
        
        janela = sg.Window('Relatórios de Eventos', layout, finalize=True, modal=True)
        
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED:
                janela.close()
                return 0
            janela.close()
            return evento

    def tela_opcoes_produtos(self) -> int:
        """Cria e gerencia a janela do SUB-MENU de Relatórios de Produtos."""
        
        layout = [
            [sg.Text("\n-------- RELATORIOS DE PRODUTOS ----------", font=("Helvetica", 14, "bold"))],
            [sg.Button("Produtos Mais Caros e Mais Baratos", key=1, size=(30,1))],
            [sg.Button("Produtos Mais Vendidos", key=2, size=(30,1))],
            [sg.Button("Produtos com Maior Faturamento", key=3, size=(30,1))],
            [sg.Button("Relatorio de Estoque", key=4, size=(30,1))],
            [sg.Button("Ranking Completo de Produtos", key=5, size=(30,1))],
            [sg.Button("Voltar", key=0, size=(30,1), button_color=('white', 'red'))]
        ]
        
        janela = sg.Window('Relatórios de Produtos', layout, finalize=True, modal=True)
        
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED:
                janela.close()
                return 0
            janela.close()
            return evento

    def tela_opcoes_vendas(self) -> int:
        """Cria e gerencia a janela do SUB-MENU de Relatórios de Vendas."""
        
        layout = [
            [sg.Text("\n-------- RELATORIOS DE VENDAS ----------", font=("Helvetica", 14, "bold"))],
            [sg.Button("Vendas por Metodo de Pagamento", key=1, size=(30,1))],
            [sg.Button("Faturamento por Evento", key=2, size=(30,1))],
            [sg.Button("Vendas por Periodo", key=3, size=(30,1))],
            [sg.Button("Top Clientes", key=4, size=(30,1))],
            [sg.Button("Voltar", key=0, size=(30,1), button_color=('white', 'red'))]
        ]
        
        janela = sg.Window('Relatórios de Vendas', layout, finalize=True, modal=True)
        
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED:
                janela.close()
                return 0
            janela.close()
            return evento

    def tela_opcoes_usuarios(self) -> int:
        """Cria e gerencia a janela do SUB-MENU de Relatórios de Usuários."""
        
        layout = [
            [sg.Text("\n-------- RELATORIOS DE USUARIOS ----------", font=("Helvetica", 14, "bold"))],
            [sg.Button("Usuarios que Mais Gastaram", key=1, size=(30,1))],
            [sg.Button("Usuarios Mais Ativos", key=2, size=(30,1))],
            [sg.Button("Usuarios por Quantidade de Ingressos", key=3, size=(30,1))],
            [sg.Button("Voltar", key=0, size=(30,1), button_color=('white', 'red'))]
        ]
        
        janela = sg.Window('Relatórios de Usuários', layout, finalize=True, modal=True)
        
        while True:
            evento, valores = janela.read()
            if evento == sg.WINDOW_CLOSED:
                janela.close()
                return 0
            janela.close()
            return evento


    def mostra_eventos_preco(self, mais_caros: List[dict], mais_baratos: List[dict]):
        """Cria uma janela para mostrar os eventos mais caros e mais baratos."""
        
        # Constrói o texto para a coluna "Mais Caros"
        texto_caros = "EVENTOS MAIS CAROS:\n" + ("-"*20) + "\n"
        if mais_caros:
            for i, evento in enumerate(mais_caros, 1):
                texto_caros += f"{i}. {evento['nome']} - R$ {evento['preco']:.2f}\n"
                texto_caros += f"   Data: {evento['data']} Local: {evento['local']}\n"
        else:
            texto_caros += "Nenhum evento cadastrado."

        # Constrói o texto para a coluna "Mais Baratos"
        texto_baratos = "EVENTOS MAIS BARATOS:\n" + ("-"*20) + "\n"
        if mais_baratos:
            for i, evento in enumerate(mais_baratos, 1):
                texto_baratos += f"{i}. {evento['nome']} - R$ {evento['preco']:.2f}\n"
                texto_baratos += f"   Data: {evento['data']} Local: {evento['local']}\n"
        else:
            texto_baratos += "Nenhum evento cadastrado."
            
        # Usa Colunas para exibir lado a lado
        layout = [
            [sg.Text("======== EVENTOS POR PRECO ========", font=("Helvetica", 14, "bold"))],
            [
                sg.Column([[sg.Multiline(texto_caros, size=(40, 10), disabled=True, no_scrollbar=True)]]),
                sg.Column([[sg.Multiline(texto_baratos, size=(40, 10), disabled=True, no_scrollbar=True)]])
            ],
            [sg.Button('Fechar')]
        ]
        
        janela = sg.Window('Relatório: Eventos por Preço', layout, modal=True, finalize=True)
        janela.read()
        janela.close()

    def mostra_eventos_avaliacao(self, eventos: List[dict]):
        """Mostra eventos por avaliação em uma tabela."""
        
        if not eventos:
            self.mostra_mensagem("Nenhum evento com avaliacoes encontrado.")
            return
        
        headings = ['#', 'Nome', 'Nota Média', 'Avaliações', 'Data', 'Local', 'Preço (R$)']
        dados_tabela = []
        for i, evento in enumerate(eventos, 1):
            dados_tabela.append([
                i, evento['nome'], f"{evento['nota_media']:.1f}/5.0",
                evento['total_avaliacoes'], evento['data'], evento['local'],
                f"{evento['preco']:.2f}"
            ])
            
        layout = [
            [sg.Text("======== EVENTOS MAIS BEM AVALIADOS ========", font=("Helvetica", 14, "bold"))],
            [sg.Table(values=dados_tabela, headings=headings,
                      auto_size_columns=True, justification='left',
                      num_rows=min(len(dados_tabela), 15),
                      key='-TABLE-', expand_x=True, expand_y=True)],
            [sg.Button('Fechar')]
        ]
        
        janela = sg.Window('Relatório: Eventos por Avaliação', layout, resizable=True, modal=True, finalize=True)
        janela.read()
        janela.close()

    def mostra_eventos_vendas(self, eventos: List[dict]):
        """Mostra eventos por ingressos vendidos em uma tabela."""
        
        if not eventos:
            self.mostra_mensagem("Nenhuma venda de ingresso encontrada.")
            return
        
        headings = ['#', 'Nome', 'Ingressos Vendidos', 'Faturamento (R$)', 'Data', 'Local']
        dados_tabela = []
        for i, evento in enumerate(eventos, 1):
            dados_tabela.append([
                i, evento['nome'], evento['ingressos_vendidos'],
                f"{evento['faturamento']:.2f}", evento['data'], evento['local']
            ])
            
        layout = [
            [sg.Text("======== EVENTOS COM MAIS INGRESSOS VENDIDOS ========", font=("Helvetica", 14, "bold"))],
            [sg.Table(values=dados_tabela, headings=headings,
                      auto_size_columns=True, justification='left',
                      num_rows=min(len(dados_tabela), 15),
                      key='-TABLE-', expand_x=True, expand_y=True)],
            [sg.Button('Fechar')]
        ]
        
        janela = sg.Window('Relatório: Eventos por Vendas', layout, resizable=True, modal=True, finalize=True)
        janela.read()
        janela.close()

    def mostra_ranking_eventos(self, eventos: List[dict]):
        """Mostra o ranking completo de eventos em uma tabela."""
        
        if not eventos:
            self.mostra_mensagem("Nenhum evento cadastrado.")
            return
        
        headings = ['#', 'Nome', 'Nota', 'Ingressos', 'Faturamento (R$)', 'Data', 'Local', 'Preço (R$)']
        dados_tabela = []
        for i, evento in enumerate(eventos, 1):
            nota_str = f"{evento['nota_media']:.1f}" if evento['nota_media'] > 0 else "N/A"
            dados_tabela.append([
                i, evento['nome'], nota_str, evento['ingressos_vendidos'],
                f"{evento['faturamento']:.2f}", evento['data'], evento['local'],
                f"{evento['preco']:.2f}"
            ])
            
        layout = [
            [sg.Text("======== RANKING COMPLETO DE EVENTOS ========", font=("Helvetica", 14, "bold"))],
            [sg.Table(values=dados_tabela, headings=headings,
                      auto_size_columns=True, justification='left',
                      num_rows=min(len(dados_tabela), 15),
                      key='-TABLE-', expand_x=True, expand_y=True)],
            [sg.Button('Fechar')]
        ]
        
        janela = sg.Window('Relatório: Ranking de Eventos', layout, resizable=True, modal=True, finalize=True)
        janela.read()
        janela.close()

    def mostra_produtos_preco(self, mais_caros: List[dict], mais_baratos: List[dict]):
        """Mostra produtos mais caros e mais baratos em colunas."""
        
        texto_caros = "PRODUTOS MAIS CAROS:\n" + ("-"*20) + "\n"
        if mais_caros:
            for i, p in enumerate(mais_caros, 1):
                texto_caros += f"{i}. {p['nome']} - R$ {p['preco']:.2f}\n"
                texto_caros += f"   Estoque: {p['estoque']} | Evento: {p['evento']}\n"
        else:
            texto_caros += "Nenhum produto cadastrado."

        texto_baratos = "PRODUTOS MAIS BARATOS:\n" + ("-"*20) + "\n"
        if mais_baratos:
            for i, p in enumerate(mais_baratos, 1):
                texto_baratos += f"{i}. {p['nome']} - R$ {p['preco']:.2f}\n"
                texto_baratos += f"   Estoque: {p['estoque']} | Evento: {p['evento']}\n"
        else:
            texto_baratos += "Nenhum produto cadastrado."

        layout = [
            [sg.Text("======== PRODUTOS POR PRECO ========", font=("Helvetica", 14, "bold"))],
            [
                sg.Column([[sg.Multiline(texto_caros, size=(40, 10), disabled=True, no_scrollbar=True)]]),
                sg.Column([[sg.Multiline(texto_baratos, size=(40, 10), disabled=True, no_scrollbar=True)]])
            ],
            [sg.Button('Fechar')]
        ]
        
        janela = sg.Window('Relatório: Produtos por Preço', layout, modal=True, finalize=True)
        janela.read()
        janela.close()

    def mostra_produtos_vendidos(self, produtos: List[dict]):
        """Mostra produtos mais vendidos em uma tabela."""
        
        if not produtos:
            self.mostra_mensagem("Nenhuma venda de produto encontrada.")
            return
        
        headings = ['#', 'Nome', 'Qtd. Vendida', 'Faturamento (R$)', 'Estoque Atual']
        dados_tabela = []
        for i, produto in enumerate(produtos, 1):
            dados_tabela.append([
                i, produto['nome'], produto['quantidade_vendida'],
                f"{produto['faturamento']:.2f}", produto['estoque']
            ])
            
        layout = [
            [sg.Text("======== PRODUTOS MAIS VENDIDOS ========", font=("Helvetica", 14, "bold"))],
            [sg.Table(values=dados_tabela, headings=headings,
                      auto_size_columns=True, justification='left',
                      num_rows=min(len(produtos), 15),
                      key='-TABLE-', expand_x=True, expand_y=True)],
            [sg.Button('Fechar')]
        ]
        
        janela = sg.Window('Relatório: Produtos Mais Vendidos', layout, resizable=True, modal=True, finalize=True)
        janela.read()
        janela.close()

    def mostra_produtos_faturamento(self, produtos: List[dict]):
        """Mostra produtos com maior faturamento em uma tabela."""
        
        if not produtos:
            self.mostra_mensagem("Nenhuma venda de produto encontrada.")
            return
        
        headings = ['#', 'Nome', 'Faturamento (R$)', 'Qtd. Vendida', 'Preço Unit. (R$)']
        dados_tabela = []
        for i, produto in enumerate(produtos, 1):
            dados_tabela.append([
                i, produto['nome'], f"{produto['faturamento']:.2f}",
                produto['quantidade_vendida'], f"{produto['preco']:.2f}"
            ])
            
        layout = [
            [sg.Text("======== PRODUTOS COM MAIOR FATURAMENTO ========", font=("Helvetica", 14, "bold"))],
            [sg.Table(values=dados_tabela, headings=headings,
                      auto_size_columns=True, justification='left',
                      num_rows=min(len(produtos), 15),
                      key='-TABLE-', expand_x=True, expand_y=True)],
            [sg.Button('Fechar')]
        ]
        
        janela = sg.Window('Relatório: Faturamento de Produtos', layout, resizable=True, modal=True, finalize=True)
        janela.read()
        janela.close()

    def mostra_relatorio_estoque(self, produtos: List[dict]):
        """Mostra produtos com estoque baixo e bom em colunas."""
        
        if not produtos:
            self.mostra_mensagem("Nenhum produto cadastrado.")
            return

        estoque_baixo = [p for p in produtos if p['estoque'] <= 5]
        bom_estoque = [p for p in produtos if p['estoque'] > 5]

        texto_baixo = "PRODUTOS COM ESTOQUE BAIXO (<=5):\n" + ("-"*30) + "\n"
        if estoque_baixo:
            for p in estoque_baixo:
                texto_baixo += f" {p['nome']} - {p['estoque']} unidades\n"
        else:
            texto_baixo += "Nenhum produto com estoque baixo."

        texto_bom = "PRODUTOS COM BOM ESTOQUE (>5):\n" + ("-"*30) + "\n"
        if bom_estoque:
            for p in bom_estoque:
                texto_bom += f" {p['nome']} - {p['estoque']} unidades\n"
        else:
            texto_bom += "Nenhum produto com bom estoque."

        layout = [
            [sg.Text("======== RELATORIO DE ESTOQUE ========", font=("Helvetica", 14, "bold"))],
            [
                sg.Column([[sg.Multiline(texto_baixo, size=(40, 10), disabled=True, no_scrollbar=True)]]),
                sg.Column([[sg.Multiline(texto_bom, size=(40, 10), disabled=True, no_scrollbar=True)]])
            ],
            [sg.Button('Fechar')]
        ]
        
        janela = sg.Window('Relatório: Estoque de Produtos', layout, modal=True, finalize=True)
        janela.read()
        janela.close()

    def mostra_vendas_pagamento(self, dados: dict):
        """Mostra um resumo das vendas por método de pagamento."""
        
        if not dados:
            self.mostra_mensagem("Nenhuma venda encontrada.")
            return

        total_geral = sum(dados.values())
        
        texto_relatorio = ""
        for metodo, valor in dados.items():
            percentual = (valor / total_geral * 100) if total_geral > 0 else 0
            texto_relatorio += f"{metodo}: R$ {valor:.2f} ({percentual:.1f}%)\n"
        
        texto_relatorio += f"\nTOTAL GERAL: R$ {total_geral:.2f}"

        layout = [
            [sg.Text("======== VENDAS POR METODO DE PAGAMENTO ========", font=("Helvetica", 14, "bold"))],
            [sg.Multiline(texto_relatorio, size=(40, 10), disabled=True, no_scrollbar=True)],
            [sg.Button('Fechar')]
        ]
        
        janela = sg.Window('Relatório: Vendas por Pagamento', layout, modal=True, finalize=True)
        janela.read()
        janela.close()

    def mostra_faturamento_evento(self, eventos: List[dict]):
        """Mostra o faturamento (ingressos + produtos) por evento."""
        
        if not eventos:
            self.mostra_mensagem("Nenhuma venda encontrada.")
            return

        texto_relatorio = ""
        total_sistema = 0
        for i, evento in enumerate(eventos, 1):
            faturamento_total = evento['faturamento_ingressos'] + evento['faturamento_produtos']
            total_sistema += faturamento_total
            
            texto_relatorio += f"{i}. {evento['nome']}\n"
            texto_relatorio += f"   Ingressos: R$ {evento['faturamento_ingressos']:.2f}\n"
            texto_relatorio += f"   Produtos: R$ {evento['faturamento_produtos']:.2f}\n"
            texto_relatorio += f"   TOTAL: R$ {faturamento_total:.2f}\n\n"
        
        texto_relatorio += f"FATURAMENTO TOTAL DO SISTEMA: R$ {total_sistema:.2f}"

        layout = [
            [sg.Text("======== FATURAMENTO POR EVENTO ========", font=("Helvetica", 14, "bold"))],
            [sg.Multiline(texto_relatorio, size=(50, 15), disabled=True)],
            [sg.Button('Fechar')]
        ]
        
        janela = sg.Window('Relatório: Faturamento por Evento', layout, resizable=True, modal=True, finalize=True)
        janela.read()
        janela.close()

    def mostra_top_clientes(self, clientes: List[dict]):
        """Mostra o ranking de top clientes (que mais gastaram)."""
        
        if not clientes:
            self.mostra_mensagem("Nenhuma compra encontrada.")
            return
        
        headings = ['#', 'Nome', 'Matrícula', 'Total Gasto (R$)', 'Ingressos', 'Itens (Produtos)']
        dados_tabela = []
        for i, cliente in enumerate(clientes, 1):
            dados_tabela.append([
                i, cliente['nome'], cliente['matricula'],
                f"{cliente['total_gasto']:.2f}",
                cliente['ingressos_comprados'],
                cliente['produtos_comprados']
            ])

        layout = [
            [sg.Text("======== TOP CLIENTES ========", font=("Helvetica", 14, "bold"))],
            [sg.Table(values=dados_tabela, headings=headings,
                      auto_size_columns=True, justification='left',
                      num_rows=min(len(dados_tabela), 10),
                      key='-TABLE-', expand_x=True, expand_y=True)],
            [sg.Button('Fechar')]
        ]
        
        janela = sg.Window('Relatório: Top Clientes', layout, resizable=True, modal=True, finalize=True)
        janela.read()
        janela.close()

    def mostra_relatorio_geral(self, dados: dict):
        """Mostra um resumo geral de todo o sistema."""
        
        texto_estatisticas = "ESTATISTICAS GERAIS:\n" + ("-"*30) + "\n"
        texto_estatisticas += f"   Usuarios cadastrados: {dados['total_usuarios']}\n"
        texto_estatisticas += f"   Eventos cadastrados: {dados['total_eventos']}\n"
        texto_estatisticas += f"   Produtos cadastrados: {dados['total_produtos']}\n"
        texto_estatisticas += f"   Ingressos vendidos: {dados['total_ingressos_vendidos']}\n"
        texto_estatisticas += f"   Itens de produtos vendidos: {dados['total_produtos_vendidos']}\n"

        texto_faturamento = "FATURAMENTO:\n" + ("-"*30) + "\n"
        texto_faturamento += f"   Ingressos: R$ {dados['faturamento_ingressos']:.2f}\n"
        texto_faturamento += f"   Produtos: R$ {dados['faturamento_produtos']:.2f}\n"
        texto_faturamento += f"   TOTAL: R$ {dados['faturamento_total']:.2f}\n"
        
        texto_destaques = "DESTAQUES:\n" + ("-"*30) + "\n"
        if dados.get('evento_mais_popular'):
            texto_destaques += f"   Evento mais popular: {dados['evento_mais_popular']}\n"
            texto_destaques += f"   Produto mais vendido: {dados['produto_mais_vendido']}\n"
            texto_destaques += f"   Melhor cliente: {dados['melhor_cliente']}\n"
        else:
            texto_destaques += "   Nenhuma venda registrada."

        layout = [
            [sg.Text("======== RELATORIO GERAL DO SISTEMA ========", font=("Helvetica", 14, "bold"))],
            [sg.Multiline(texto_estatisticas, size=(50, 7), disabled=True, no_scrollbar=True)],
            [sg.Multiline(texto_faturamento, size=(50, 5), disabled=True, no_scrollbar=True)],
            [sg.Multiline(texto_destaques, size=(50, 5), disabled=True, no_scrollbar=True)],
            [sg.Button('Fechar')]
        ]
        
        janela = sg.Window('Relatório Geral do Sistema', layout, modal=True, finalize=True)
        janela.read()
        janela.close()

    def mostra_mensagem(self, msg: str):
        """Método genérico para mostrar mensagens (agora um popup)."""
        sg.Popup(msg, title="Aviso", keep_on_top=True, modal=True)