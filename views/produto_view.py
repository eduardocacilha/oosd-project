from typing import List, Optional
import FreeSimpleGUI as sg
import re
from exceptions.entidadeNaoEncontradaException import EntidadeNaoEncontradaException
from exceptions.regraDeNegocioException import RegraDeNegocioException

class ProdutoView:

    def __init__(self):
        try:
            sg.theme('Reddit')
        except Exception as e:
            print(f"Erro ao definir tema: {e}")

    def mostrar_popup(self, titulo: str, msg: str):
        try:
            sg.Popup(str(titulo), str(msg), keep_on_top=True, modal=True)
        except Exception as e:
            print(f"Erro ao exibir popup: {e}")
            print(f"Título: {titulo}, Mensagem: {msg}")

    def tela_opcoes(self) -> int:
        try:
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
                    return 0
                janela.close()
                return evento

        except Exception as e:
            self.mostrar_popup("Erro", f"Erro ao criar menu de produtos: {e}")
            return 0

    def escolher_tipo_produto(self) -> int:
        try:
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
                return evento

        except Exception as e:
            self.mostrar_popup("Erro", f"Erro ao escolher tipo de produto: {e}")
            return 0

    def pega_dados_camisa(self) -> dict:

        try:
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
                    try:

                        nome = valores['1'].strip()
                        if not nome:
                            raise RegraDeNegocioException("Nome não pode estar vazio!")


                        try:
                            preco = float(valores['2'])
                            if preco <= 0:
                                raise RegraDeNegocioException("Preço deve ser maior que zero!")
                        except ValueError:
                            raise RegraDeNegocioException("Preço inválido! Digite um número.")


                        try:
                            estoque = int(valores['3'])
                            if estoque < 0:
                                raise RegraDeNegocioException("Estoque não pode ser negativo!")
                        except ValueError:
                            raise RegraDeNegocioException("Estoque inválido! Digite um número inteiro.")


                        tamanho = valores['4']
                        if tamanho not in ["P", "M", "G", "GG"]:
                            raise RegraDeNegocioException("Tamanho inválido! Selecione uma opção.")


                        cor = valores['5'].strip()
                        if not cor:
                            raise RegraDeNegocioException("Cor não pode estar vazia!")


                        janela.close()
                        return {
                            "nome": nome, "preco": preco, "estoque": estoque,
                            "tamanho": tamanho, "cor": cor
                        }

                    except (RegraDeNegocioException, EntidadeNaoEncontradaException) as e:
                        self.mostrar_popup("Erro de Validação", str(e))
                        continue
                    except Exception as e:
                        self.mostrar_popup("Erro Inesperado", f"Erro ao validar dados da camisa: {e}")
                        continue

        except Exception as e:
            self.mostrar_popup("Erro", f"Erro ao coletar dados da camisa: {e}")
            return None

    def pega_dados_copo(self) -> dict:

        try:
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
                    try:
                        nome = valores['1'].strip()
                        if not nome:
                            raise RegraDeNegocioException("Nome não pode estar vazio!")

                        try:
                            preco = float(valores['2'])
                            if preco <= 0:
                                raise RegraDeNegocioException("Preço deve ser maior que zero!")
                        except ValueError:
                            raise RegraDeNegocioException("Preço inválido! Digite um número.")

                        try:
                            estoque = int(valores['3'])
                            if estoque < 0:
                                raise RegraDeNegocioException("Estoque não pode ser negativo!")
                        except ValueError:
                            raise RegraDeNegocioException("Estoque inválido! Digite um número inteiro.")

                        try:
                            capacidade = int(valores['4'])
                            if capacidade <= 0:
                                raise RegraDeNegocioException("Capacidade deve ser maior que zero!")
                        except ValueError:
                            raise RegraDeNegocioException("Capacidade inválida! Digite um número inteiro.")

                        material = valores['5'].strip()
                        if not material:
                            raise RegraDeNegocioException("Material não pode estar vazio!")


                        janela.close()
                        return {
                            "nome": nome, "preco": preco, "estoque": estoque,
                            "capacidade_ml": capacidade, "material": material
                        }

                    except (RegraDeNegocioException, EntidadeNaoEncontradaException) as e:
                        self.mostrar_popup("Erro de Validação", str(e))
                        continue
                    except Exception as e:
                        self.mostrar_popup("Erro Inesperado", f"Erro ao validar dados do copo: {e}")
                        continue

        except Exception as e:
            self.mostrar_popup("Erro", f"Erro ao coletar dados do copo: {e}")
            return None

    def mostra_produtos(self, lista_produtos: List[dict]):

        try:
            if not lista_produtos or not isinstance(lista_produtos, list):
                self.mostrar_popup("Produtos", "\nNenhum produto cadastrado para este evento.")
                return

            headings = ['#', 'Descrição', 'Preço (R$)', 'Estoque']
            dados_tabela = []

            for i, produto in enumerate(lista_produtos, 1):
                try:
                    if not isinstance(produto, dict):
                        raise RegraDeNegocioException("Dados de produto inválidos")

                    dados_tabela.append([
                        i,
                        str(produto.get('descricao', 'N/A')),
                        f"{float(produto.get('preco', 0)):.2f}",
                        int(produto.get('estoque', 0))
                    ])
                except (ValueError, TypeError, KeyError) as e:
                    dados_tabela.append([i, f"Erro: {e}", "0.00", "0"])

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

        except Exception as e:
            self.mostrar_popup("Erro", f"Erro ao exibir produtos: {e}")

    def seleciona_produto(self, lista_produtos: List[dict]) -> Optional[int]:

        try:
            if not lista_produtos or not isinstance(lista_produtos, list):
                self.mostrar_popup("Selecionar Produto", "\nNenhum produto disponível.")
                return None

            headings = ['#', 'Descrição', 'Preço (R$)', 'Estoque']
            dados_tabela = []

            for i, produto in enumerate(lista_produtos, 1):
                try:
                    if not isinstance(produto, dict):
                        raise RegraDeNegocioException("Dados de produto inválidos")

                    dados_tabela.append([
                        i,
                        str(produto.get('descricao', 'N/A')),
                        f"{float(produto.get('preco', 0)):.2f}",
                        int(produto.get('estoque', 0))
                    ])
                except (ValueError, TypeError, KeyError) as e:
                    dados_tabela.append([i, f"Erro: {e}", "0.00", "0"])

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
                    try:
                        indices_selecionados = valores['-TABLE-']
                        if not indices_selecionados:
                            raise RegraDeNegocioException("Nenhum produto selecionado. Por favor, clique em uma linha da tabela.")
                        else:
                            indice_selecionado = indices_selecionados[0]
                            if indice_selecionado < 0 or indice_selecionado >= len(lista_produtos):
                                raise RegraDeNegocioException("Índice de produto inválido.")
                            janela.close()

                            return indice_selecionado

                    except (RegraDeNegocioException, EntidadeNaoEncontradaException) as e:
                        self.mostrar_popup("Erro", str(e))
                        continue
                    except Exception as e:
                        self.mostrar_popup("Erro Inesperado", f"Erro ao selecionar produto: {e}")
                        continue

        except Exception as e:
            self.mostrar_popup("Erro", f"Erro ao selecionar produto: {e}")
            return None

    def pega_quantidade_venda(self) -> Optional[int]:
        try:
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
                    try:
                        qtd_str = valores['-QTD-'].strip()
                        if not qtd_str:
                            raise RegraDeNegocioException("Quantidade não pode estar vazia.")

                        try:
                            qtd_int = int(qtd_str)
                            if qtd_int <= 0:
                                raise RegraDeNegocioException("Quantidade deve ser maior que zero.")
                            janela.close()
                            return qtd_int
                        except ValueError:
                            raise RegraDeNegocioException("Quantidade inválida. Digite um número inteiro.")

                    except (RegraDeNegocioException, EntidadeNaoEncontradaException) as e:
                        self.mostrar_popup("Erro de Validação", str(e))
                        continue
                    except Exception as e:
                        self.mostrar_popup("Erro Inesperado", f"Erro ao validar quantidade: {e}")
                        continue

        except Exception as e:
            self.mostrar_popup("Erro", f"Erro ao coletar quantidade: {e}")
            return None

    def pega_metodo_pagamento(self) -> str:
        try:
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
                    return "Dinheiro"
                if evento in metodos:
                    janela.close()
                    return metodos[evento]

        except Exception as e:
            self.mostrar_popup("Erro", f"Erro ao selecionar método de pagamento: {e}")
            return "Dinheiro"

    def mostra_venda_realizada(self, dados_venda: dict):
        try:
            if not dados_venda or not isinstance(dados_venda, dict):
                raise RegraDeNegocioException("Dados da venda não disponíveis.")

            layout = [
                [sg.Text("--- VENDA REALIZADA COM SUCESSO ---", font=("Helvetica", 14, "bold"))],
                [sg.Text("ID da Venda:", size=(10, 1), font=("Helvetica", 10, "bold")),
                 sg.Text(str(dados_venda.get('id_venda', 'N/A')))],
                [sg.Text("Cliente:", size=(10, 1), font=("Helvetica", 10, "bold")),
                 sg.Text(str(dados_venda.get('cliente', 'N/A')))],
                [sg.Text("Evento:", size=(10, 1), font=("Helvetica", 10, "bold")),
                 sg.Text(str(dados_venda.get('evento', 'N/A')))],
                [sg.Text("Método:", size=(10, 1), font=("Helvetica", 10, "bold")),
                 sg.Text(str(dados_venda.get('metodo', 'N/A')))],
                [sg.Text("TOTAL:", size=(10, 1), font=("Helvetica", 12, "bold")),
                 sg.Text(f"R$ {float(dados_venda.get('total', 0)):.2f}", font=("Helvetica", 12, "bold"))],
                [sg.Button('OK', key='-OK-')]
            ]
            janela = sg.Window('Venda Concluída', layout, modal=True, finalize=True)
            while True:
                evento, valores = janela.read()
                if evento == sg.WINDOW_CLOSED or evento == '-OK-':
                    break
            janela.close()

        except (ValueError, TypeError) as e:
            self.mostrar_popup("Erro", f"Erro nos dados da venda: {e}")
        except Exception as e:
            self.mostrar_popup("Erro", f"Erro ao exibir venda realizada: {e}")

    def mostra_relatorio_vendas(self, lista_vendas: List[dict]):

        try:
            if not lista_vendas or not isinstance(lista_vendas, list):
                self.mostrar_popup("Relatório", "\nNenhuma venda registrada.")
                return

            total_geral = 0.0
            dados_tabela = []
            headings = ['ID Venda', 'Cliente', 'Evento', 'Data', 'Método', 'Total (R$)']

            for venda in lista_vendas:
                try:
                    if not isinstance(venda, dict):
                        raise RegraDeNegocioException("Dados de venda inválidos")

                    total_venda = float(venda.get('total', 0))
                    total_geral += total_venda

                    dados_tabela.append([
                        str(venda.get('id_venda', 'N/A')),
                        str(venda.get('cliente', 'N/A')),
                        str(venda.get('evento', 'N/A')),
                        str(venda.get('data', 'N/A')),
                        str(venda.get('metodo', 'N/A')),
                        f"{total_venda:.2f}"
                    ])
                except (ValueError, TypeError, KeyError) as e:
                    dados_tabela.append(['Erro', f'Erro: {e}', 'N/A', 'N/A', 'N/A', '0.00'])

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

        except Exception as e:
            self.mostrar_popup("Erro", f"Erro ao exibir relatório de vendas: {e}")

    def confirma_continuar_comprando(self) -> bool:
        try:
            resposta = sg.popup_yes_no(
                "Deseja adicionar mais produtos à venda?",
                title="Continuar Comprando",
                keep_on_top=True
            )
            return resposta == 'Yes'
        except Exception as e:
            self.mostrar_popup("Erro", f"Erro ao confirmar continuação: {e}")
            return False
