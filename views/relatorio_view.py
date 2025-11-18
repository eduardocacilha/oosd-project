from typing import List
import FreeSimpleGUI as sg
from exceptions.entidadeNaoEncontradaException import EntidadeNaoEncontradaException
from exceptions.regraDeNegocioException import RegraDeNegocioException

class RelatorioView:

    def __init__(self):
        try:
            sg.theme('Reddit')
        except Exception as e:
            print(f"Erro ao definir tema: {e}")


    def tela_opcoes(self) -> int:

        try:
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
                    return 0
                janela.close()
                return evento

        except Exception as e:
            self.mostra_mensagem(f"Erro ao criar menu principal: {e}")
            return 0

    def tela_opcoes_eventos(self) -> int:

        try:
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

        except Exception as e:
            self.mostra_mensagem(f"Erro ao criar menu de eventos: {e}")
            return 0

    def tela_opcoes_produtos(self) -> int:

        try:
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

        except Exception as e:
            self.mostra_mensagem(f"Erro ao criar menu de produtos: {e}")
            return 0

    def tela_opcoes_vendas(self) -> int:

        try:
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

        except Exception as e:
            self.mostra_mensagem(f"Erro ao criar menu de vendas: {e}")
            return 0

    def tela_opcoes_usuarios(self) -> int:

        try:
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

        except Exception as e:
            self.mostra_mensagem(f"Erro ao criar menu de usuários: {e}")
            return 0

    def mostra_eventos_preco(self, mais_caros: List[dict], mais_baratos: List[dict]):

        try:

            if not isinstance(mais_caros, list):
                mais_caros = []
            if not isinstance(mais_baratos, list):
                mais_baratos = []


            texto_caros = "EVENTOS MAIS CAROS:\n" + ("-"*20) + "\n"
            if mais_caros:
                for i, evento in enumerate(mais_caros, 1):
                    try:
                        texto_caros += f"{i}. {evento.get('nome', 'N/A')} - R$ {float(evento.get('preco', 0)):.2f}\n"
                        texto_caros += f"   Data: {evento.get('data', 'N/A')} Local: {evento.get('local', 'N/A')}\n"
                    except (KeyError, ValueError, TypeError) as e:
                        texto_caros += f"{i}. Erro ao exibir evento: {e}\n"
            else:
                texto_caros += "Nenhum evento cadastrado."


            texto_baratos = "EVENTOS MAIS BARATOS:\n" + ("-"*20) + "\n"
            if mais_baratos:
                for i, evento in enumerate(mais_baratos, 1):
                    try:
                        texto_baratos += f"{i}. {evento.get('nome', 'N/A')} - R$ {float(evento.get('preco', 0)):.2f}\n"
                        texto_baratos += f"   Data: {evento.get('data', 'N/A')} Local: {evento.get('local', 'N/A')}\n"
                    except (KeyError, ValueError, TypeError) as e:
                        texto_baratos += f"{i}. Erro ao exibir evento: {e}\n"
            else:
                texto_baratos += "Nenhum evento cadastrado."


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

        except Exception as e:
            self.mostra_mensagem(f"Erro ao exibir relatório de eventos por preço: {e}")

    def mostra_eventos_avaliacao(self, eventos: List[dict]):

        try:
            if not eventos or not isinstance(eventos, list):
                self.mostra_mensagem("Nenhum evento com avaliacoes encontrado.")
                return

            headings = ['#', 'Nome', 'Nota Média', 'Avaliações', 'Data', 'Local', 'Preço (R$)']
            dados_tabela = []

            for i, evento in enumerate(eventos, 1):
                try:
                    dados_tabela.append([
                        i,
                        str(evento.get('nome', 'N/A')),
                        f"{float(evento.get('nota_media', 0)):.1f}/5.0",
                        int(evento.get('total_avaliacoes', 0)),
                        str(evento.get('data', 'N/A')),
                        str(evento.get('local', 'N/A')),
                        f"{float(evento.get('preco', 0)):.2f}"
                    ])
                except (ValueError, TypeError, KeyError) as e:
                    dados_tabela.append([i, "Erro nos dados", str(e), "", "", "", ""])

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

        except Exception as e:
            self.mostra_mensagem(f"Erro ao exibir relatório de avaliações: {e}")

    def mostra_eventos_vendas(self, eventos: List[dict]):

        try:
            if not eventos or not isinstance(eventos, list):
                self.mostra_mensagem("Nenhuma venda de ingresso encontrada.")
                return

            headings = ['#', 'Nome', 'Ingressos Vendidos', 'Faturamento (R$)', 'Data', 'Local']
            dados_tabela = []

            for i, evento in enumerate(eventos, 1):
                try:
                    dados_tabela.append([
                        i,
                        str(evento.get('nome', 'N/A')),
                        int(evento.get('ingressos_vendidos', 0)),
                        f"{float(evento.get('faturamento', 0)):.2f}",
                        str(evento.get('data', 'N/A')),
                        str(evento.get('local', 'N/A'))
                    ])
                except (ValueError, TypeError, KeyError) as e:
                    dados_tabela.append([i, "Erro nos dados", str(e), "", "", ""])

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

        except Exception as e:
            self.mostra_mensagem(f"Erro ao exibir relatório de vendas: {e}")

    def mostra_ranking_eventos(self, eventos: List[dict]):

        try:
            if not eventos or not isinstance(eventos, list):
                self.mostra_mensagem("Nenhum evento cadastrado.")
                return

            headings = ['#', 'Nome', 'Nota', 'Ingressos', 'Faturamento (R$)', 'Data', 'Local', 'Preço (R$)']
            dados_tabela = []

            for i, evento in enumerate(eventos, 1):
                try:
                    nota_media = float(evento.get('nota_media', 0))
                    nota_str = f"{nota_media:.1f}" if nota_media > 0 else "N/A"

                    dados_tabela.append([
                        i,
                        str(evento.get('nome', 'N/A')),
                        nota_str,
                        int(evento.get('ingressos_vendidos', 0)),
                        f"{float(evento.get('faturamento', 0)):.2f}",
                        str(evento.get('data', 'N/A')),
                        str(evento.get('local', 'N/A')),
                        f"{float(evento.get('preco', 0)):.2f}"
                    ])
                except (ValueError, TypeError, KeyError) as e:
                    dados_tabela.append([i, "Erro nos dados", str(e), "", "", "", "", ""])

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

        except Exception as e:
            self.mostra_mensagem(f"Erro ao exibir ranking de eventos: {e}")

    def mostra_produtos_preco(self, mais_caros: List[dict], mais_baratos: List[dict]):

        try:
            if not isinstance(mais_caros, list):
                mais_caros = []
            if not isinstance(mais_baratos, list):
                mais_baratos = []

            texto_caros = "PRODUTOS MAIS CAROS:\n" + ("-"*20) + "\n"
            if mais_caros:
                for i, p in enumerate(mais_caros, 1):
                    try:
                        texto_caros += f"{i}. {p.get('nome', 'N/A')} - R$ {float(p.get('preco', 0)):.2f}\n"
                        texto_caros += f"   Estoque: {int(p.get('estoque', 0))} | Evento: {p.get('evento', 'N/A')}\n"
                    except (ValueError, TypeError, KeyError) as e:
                        texto_caros += f"{i}. Erro ao exibir produto: {e}\n"
            else:
                texto_caros += "Nenhum produto cadastrado."

            texto_baratos = "PRODUTOS MAIS BARATOS:\n" + ("-"*20) + "\n"
            if mais_baratos:
                for i, p in enumerate(mais_baratos, 1):
                    try:
                        texto_baratos += f"{i}. {p.get('nome', 'N/A')} - R$ {float(p.get('preco', 0)):.2f}\n"
                        texto_baratos += f"   Estoque: {int(p.get('estoque', 0))} | Evento: {p.get('evento', 'N/A')}\n"
                    except (ValueError, TypeError, KeyError) as e:
                        texto_baratos += f"{i}. Erro ao exibir produto: {e}\n"
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

        except Exception as e:
            self.mostra_mensagem(f"Erro ao exibir relatório de produtos por preço: {e}")

    def mostra_produtos_vendidos(self, produtos: List[dict]):

        try:
            if not produtos or not isinstance(produtos, list):
                self.mostra_mensagem("Nenhuma venda de produto encontrada.")
                return

            headings = ['#', 'Nome', 'Qtd. Vendida', 'Faturamento (R$)', 'Estoque Atual']
            dados_tabela = []

            for i, produto in enumerate(produtos, 1):
                try:
                    dados_tabela.append([
                        i,
                        str(produto.get('nome', 'N/A')),
                        int(produto.get('quantidade_vendida', 0)),
                        f"{float(produto.get('faturamento', 0)):.2f}",
                        int(produto.get('estoque', 0))
                    ])
                except (ValueError, TypeError, KeyError) as e:
                    dados_tabela.append([i, "Erro nos dados", str(e), "", ""])

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

        except Exception as e:
            self.mostra_mensagem(f"Erro ao exibir produtos mais vendidos: {e}")

    def mostra_produtos_faturamento(self, produtos: List[dict]):

        try:
            if not produtos or not isinstance(produtos, list):
                self.mostra_mensagem("Nenhuma venda de produto encontrada.")
                return

            headings = ['#', 'Nome', 'Faturamento (R$)', 'Qtd. Vendida', 'Preço Unit. (R$)']
            dados_tabela = []

            for i, produto in enumerate(produtos, 1):
                try:
                    dados_tabela.append([
                        i,
                        str(produto.get('nome', 'N/A')),
                        f"{float(produto.get('faturamento', 0)):.2f}",
                        int(produto.get('quantidade_vendida', 0)),
                        f"{float(produto.get('preco', 0)):.2f}"
                    ])
                except (ValueError, TypeError, KeyError) as e:
                    dados_tabela.append([i, "Erro nos dados", str(e), "", ""])

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

        except Exception as e:
            self.mostra_mensagem(f"Erro ao exibir faturamento de produtos: {e}")

    def mostra_relatorio_estoque(self, produtos: List[dict]):

        try:
            if not produtos or not isinstance(produtos, list):
                self.mostra_mensagem("Nenhum produto cadastrado.")
                return

            estoque_baixo = []
            bom_estoque = []

            for p in produtos:
                try:
                    estoque_atual = int(p.get('estoque', 0))
                    if estoque_atual <= 5:
                        estoque_baixo.append(p)
                    else:
                        bom_estoque.append(p)
                except (ValueError, TypeError, KeyError):

                    estoque_baixo.append(p)

            texto_baixo = "PRODUTOS COM ESTOQUE BAIXO (<=5):\n" + ("-"*30) + "\n"
            if estoque_baixo:
                for p in estoque_baixo:
                    try:
                        nome = p.get('nome', 'N/A')
                        estoque = int(p.get('estoque', 0))
                        texto_baixo += f" {nome} - {estoque} unidades\n"
                    except (ValueError, TypeError, KeyError) as e:
                        texto_baixo += f" Erro ao exibir produto: {e}\n"
            else:
                texto_baixo += "Nenhum produto com estoque baixo."

            texto_bom = "PRODUTOS COM BOM ESTOQUE (>5):\n" + ("-"*30) + "\n"
            if bom_estoque:
                for p in bom_estoque:
                    try:
                        nome = p.get('nome', 'N/A')
                        estoque = int(p.get('estoque', 0))
                        texto_bom += f" {nome} - {estoque} unidades\n"
                    except (ValueError, TypeError, KeyError) as e:
                        texto_bom += f" Erro ao exibir produto: {e}\n"
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

        except Exception as e:
            self.mostra_mensagem(f"Erro ao exibir relatório de estoque: {e}")

    def mostra_vendas_pagamento(self, dados: dict):

        try:
            if not dados or not isinstance(dados, dict):
                self.mostra_mensagem("Nenhuma venda encontrada.")
                return

            total_geral = 0
            try:
                total_geral = sum(float(valor) for valor in dados.values() if isinstance(valor, (int, float)))
            except (ValueError, TypeError) as e:
                self.mostra_mensagem(f"Erro ao calcular total geral: {e}")
                return

            texto_relatorio = ""
            for metodo, valor in dados.items():
                try:
                    valor_float = float(valor)
                    percentual = (valor_float / total_geral * 100) if total_geral > 0 else 0
                    texto_relatorio += f"{metodo}: R$ {valor_float:.2f} ({percentual:.1f}%)\n"
                except (ValueError, TypeError) as e:
                    texto_relatorio += f"{metodo}: Erro nos dados - {e}\n"

            texto_relatorio += f"\nTOTAL GERAL: R$ {total_geral:.2f}"

            layout = [
                [sg.Text("======== VENDAS POR METODO DE PAGAMENTO ========", font=("Helvetica", 14, "bold"))],
                [sg.Multiline(texto_relatorio, size=(40, 10), disabled=True, no_scrollbar=True)],
                [sg.Button('Fechar')]
            ]

            janela = sg.Window('Relatório: Vendas por Pagamento', layout, modal=True, finalize=True)
            janela.read()
            janela.close()

        except Exception as e:
            self.mostra_mensagem(f"Erro ao exibir vendas por pagamento: {e}")

    def mostra_faturamento_evento(self, eventos: List[dict]):

        try:
            if not eventos or not isinstance(eventos, list):
                self.mostra_mensagem("Nenhuma venda encontrada.")
                return

            texto_relatorio = ""
            total_sistema = 0

            for i, evento in enumerate(eventos, 1):
                try:
                    faturamento_ingressos = float(evento.get('faturamento_ingressos', 0))
                    faturamento_produtos = float(evento.get('faturamento_produtos', 0))
                    faturamento_total = faturamento_ingressos + faturamento_produtos
                    total_sistema += faturamento_total

                    nome_evento = str(evento.get('nome', 'N/A'))

                    texto_relatorio += f"{i}. {nome_evento}\n"
                    texto_relatorio += f"   Ingressos: R$ {faturamento_ingressos:.2f}\n"
                    texto_relatorio += f"   Produtos: R$ {faturamento_produtos:.2f}\n"
                    texto_relatorio += f"   TOTAL: R$ {faturamento_total:.2f}\n\n"

                except (ValueError, TypeError, KeyError) as e:
                    texto_relatorio += f"{i}. Erro ao processar evento: {e}\n\n"

            texto_relatorio += f"FATURAMENTO TOTAL DO SISTEMA: R$ {total_sistema:.2f}"

            layout = [
                [sg.Text("======== FATURAMENTO POR EVENTO ========", font=("Helvetica", 14, "bold"))],
                [sg.Multiline(texto_relatorio, size=(50, 15), disabled=True)],
                [sg.Button('Fechar')]
            ]

            janela = sg.Window('Relatório: Faturamento por Evento', layout, resizable=True, modal=True, finalize=True)
            janela.read()
            janela.close()

        except Exception as e:
            self.mostra_mensagem(f"Erro ao exibir faturamento por evento: {e}")

    def mostra_top_clientes(self, clientes: List[dict]):

        try:
            if not clientes or not isinstance(clientes, list):
                self.mostra_mensagem("Nenhuma compra encontrada.")
                return

            headings = ['#', 'Nome', 'Matrícula', 'Total Gasto (R$)', 'Ingressos', 'Itens (Produtos)']
            dados_tabela = []

            for i, cliente in enumerate(clientes, 1):
                try:
                    dados_tabela.append([
                        i,
                        str(cliente.get('nome', 'N/A')),
                        str(cliente.get('matricula', 'N/A')),
                        f"{float(cliente.get('total_gasto', 0)):.2f}",
                        int(cliente.get('ingressos_comprados', 0)),
                        int(cliente.get('produtos_comprados', 0))
                    ])
                except (ValueError, TypeError, KeyError) as e:
                    dados_tabela.append([i, "Erro nos dados", str(e), "", "", ""])

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

        except Exception as e:
            self.mostra_mensagem(f"Erro ao exibir top clientes: {e}")

    def mostra_relatorio_geral(self, dados: dict):

        try:
            if not dados or not isinstance(dados, dict):
                self.mostra_mensagem("Dados do relatório não disponíveis.")
                return

            texto_estatisticas = "ESTATISTICAS GERAIS:\n" + ("-"*30) + "\n"
            try:
                texto_estatisticas += f"   Usuarios cadastrados: {int(dados.get('total_usuarios', 0))}\n"
                texto_estatisticas += f"   Eventos cadastrados: {int(dados.get('total_eventos', 0))}\n"
                texto_estatisticas += f"   Produtos cadastrados: {int(dados.get('total_produtos', 0))}\n"
                texto_estatisticas += f"   Ingressos vendidos: {int(dados.get('total_ingressos_vendidos', 0))}\n"
                texto_estatisticas += f"   Itens de produtos vendidos: {int(dados.get('total_produtos_vendidos', 0))}\n"
            except (ValueError, TypeError) as e:
                texto_estatisticas += f"   Erro ao processar estatísticas: {e}\n"

            texto_faturamento = "FATURAMENTO:\n" + ("-"*30) + "\n"
            try:
                faturamento_ingressos = float(dados.get('faturamento_ingressos', 0))
                faturamento_produtos = float(dados.get('faturamento_produtos', 0))
                faturamento_total = float(dados.get('faturamento_total', 0))

                texto_faturamento += f"   Ingressos: R$ {faturamento_ingressos:.2f}\n"
                texto_faturamento += f"   Produtos: R$ {faturamento_produtos:.2f}\n"
                texto_faturamento += f"   TOTAL: R$ {faturamento_total:.2f}\n"
            except (ValueError, TypeError) as e:
                texto_faturamento += f"   Erro ao processar faturamento: {e}\n"

            texto_destaques = "DESTAQUES:\n" + ("-"*30) + "\n"
            try:
                evento_popular = dados.get('evento_mais_popular', '')
                produto_vendido = dados.get('produto_mais_vendido', '')
                melhor_cliente = dados.get('melhor_cliente', '')

                if evento_popular:
                    texto_destaques += f"   Evento mais popular: {evento_popular}\n"
                    texto_destaques += f"   Produto mais vendido: {produto_vendido}\n"
                    texto_destaques += f"   Melhor cliente: {melhor_cliente}\n"
                else:
                    texto_destaques += "   Nenhuma venda registrada."
            except Exception as e:
                texto_destaques += f"   Erro ao processar destaques: {e}"

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

        except Exception as e:
            self.mostra_mensagem(f"Erro ao exibir relatório geral: {e}")

    def mostra_mensagem(self, msg: str):
        try:
            sg.Popup(str(msg), title="Aviso", keep_on_top=True, modal=True)
        except Exception as e:
            print(f"Erro crítico ao exibir mensagem: {e}")
            print(f"Mensagem original: {msg}")
