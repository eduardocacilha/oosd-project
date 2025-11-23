from typing import List, Optional
import FreeSimpleGUI as sg
import re
from exceptions.entidadeNaoEncontradaException import EntidadeNaoEncontradaException
from exceptions.regraDeNegocioException import RegraDeNegocioException


class ProdutoView:

    def __init__(self):
        try:
            sg.theme("Reddit")
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
                [
                    sg.Text(
                        "\n-------- MENU PRODUTOS ----------",
                        font=("Helvetica", 14, "bold"),
                    )
                ],
                [sg.Button("Adicionar Produto a um Evento", key=1, size=(30, 1))],
                [sg.Button("Alterar Produto", key=2, size=(30, 1))],
                [sg.Button("Listar Produtos de um Evento", key=3, size=(30, 1))],
                [sg.Button("Excluir Produto", key=4, size=(30, 1))],
                [
                    sg.Button(
                        "Retornar ao Menu Principal",
                        key=0,
                        size=(30, 1),
                        button_color=("white", "red"),
                    )
                ],
            ]
            janela = sg.Window("Menu Produtos", layout, finalize=True, modal=True)
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
                [
                    sg.Text(
                        "\n-------- TIPO DE PRODUTO ----------",
                        font=("Helvetica", 14, "bold"),
                    )
                ],
                [sg.Button("Camisa", key=1, size=(20, 1))],
                [sg.Button("Copo", key=2, size=(20, 1))],
                [
                    sg.Button(
                        "Cancelar", key=0, size=(20, 1), button_color=("white", "red")
                    )
                ],
            ]
            janela = sg.Window(
                "Escolher Tipo de Produto", layout, modal=True, finalize=True
            )
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
                [
                    sg.Text(
                        "\n-------- DADOS DA CAMISA ----------",
                        font=("Helvetica", 14, "bold"),
                    )
                ],
                [sg.Text("Nome:", size=(10, 1)), sg.Input(key="1")],
                [sg.Text("Preço (R$):", size=(10, 1)), sg.Input(key="2", size=(10, 1))],
                [sg.Text("Estoque:", size=(10, 1)), sg.Input(key="3", size=(10, 1))],
                [
                    sg.Text("Tamanho:", size=(10, 1)),
                    sg.Combo(
                        ["P", "M", "G", "GG"], key="4", size=(10, 1), readonly=True
                    ),
                ],
                [sg.Text("Cor:", size=(10, 1)), sg.Input(key="5")],
                [sg.Button("Salvar", key="6"), sg.Button("Cancelar", key="7")],
            ]
            janela = sg.Window("Dados da Camisa", layout, modal=True, finalize=True)
            while True:
                evento, valores = janela.read()
                if evento == sg.WINDOW_CLOSED or evento == "7":
                    janela.close()
                    return None
                if evento == "6":
                    try:
                        nome = valores["1"].strip()
                        if not nome:
                            raise RegraDeNegocioException("Nome não pode estar vazio!")
                        try:
                            preco = float(valores["2"])
                            if preco <= 0:
                                raise RegraDeNegocioException(
                                    "Preço deve ser maior que zero!"
                                )
                        except ValueError:
                            raise RegraDeNegocioException(
                                "Preço inválido! Digite um número."
                            )
                        try:
                            estoque = int(valores["3"])
                            if estoque < 0:
                                raise RegraDeNegocioException(
                                    "Estoque não pode ser negativo!"
                                )
                        except ValueError:
                            raise RegraDeNegocioException(
                                "Estoque inválido! Digite um número inteiro."
                            )
                        tamanho = valores["4"]
                        if tamanho not in ["P", "M", "G", "GG"]:
                            raise RegraDeNegocioException(
                                "Tamanho inválido! Selecione uma opção."
                            )
                        cor = valores["5"].strip()
                        if not cor:
                            raise RegraDeNegocioException("Cor não pode estar vazia!")
                        janela.close()
                        return {
                            "nome": nome,
                            "preco": preco,
                            "estoque": estoque,
                            "tamanho": tamanho,
                            "cor": cor,
                        }
                    except (
                        RegraDeNegocioException,
                        EntidadeNaoEncontradaException,
                    ) as e:
                        self.mostrar_popup("Erro de Validação", str(e))
                        continue
                    except Exception as e:
                        self.mostrar_popup(
                            "Erro Inesperado", f"Erro ao validar dados da camisa: {e}"
                        )
                        continue
        except Exception as e:
            self.mostrar_popup("Erro", f"Erro ao coletar dados da camisa: {e}")
            return None

    def pega_dados_copo(self) -> dict:
        try:
            layout = [
                [
                    sg.Text(
                        "\n-------- DADOS DO COPO ----------",
                        font=("Helvetica", 14, "bold"),
                    )
                ],
                [sg.Text("Nome:", size=(12, 1)), sg.Input(key="1")],
                [sg.Text("Preço (R$):", size=(12, 1)), sg.Input(key="2", size=(10, 1))],
                [sg.Text("Estoque:", size=(12, 1)), sg.Input(key="3", size=(10, 1))],
                [
                    sg.Text("Capacidade (ml):", size=(12, 1)),
                    sg.Input(key="4", size=(10, 1)),
                ],
                [sg.Text("Material:", size=(12, 1)), sg.Input(key="5")],
                [sg.Button("Salvar", key="6"), sg.Button("Cancelar", key="7")],
            ]
            janela = sg.Window("Dados do Copo", layout, modal=True, finalize=True)
            while True:
                evento, valores = janela.read()
                if evento == sg.WINDOW_CLOSED or evento == "7":
                    janela.close()
                    return None
                if evento == "6":
                    try:
                        nome = valores["1"].strip()
                        if not nome:
                            raise RegraDeNegocioException("Nome não pode estar vazio!")
                        try:
                            preco = float(valores["2"])
                            if preco <= 0:
                                raise RegraDeNegocioException(
                                    "Preço deve ser maior que zero!"
                                )
                        except ValueError:
                            raise RegraDeNegocioException(
                                "Preço inválido! Digite um número."
                            )
                        try:
                            estoque = int(valores["3"])
                            if estoque < 0:
                                raise RegraDeNegocioException(
                                    "Estoque não pode ser negativo!"
                                )
                        except ValueError:
                            raise RegraDeNegocioException(
                                "Estoque inválido! Digite um número inteiro."
                            )
                        try:
                            capacidade = int(valores["4"])
                            if capacidade <= 0:
                                raise RegraDeNegocioException(
                                    "Capacidade deve ser maior que zero!"
                                )
                        except ValueError:
                            raise RegraDeNegocioException(
                                "Capacidade inválida! Digite um número inteiro."
                            )
                        material = valores["5"].strip()
                        if not material:
                            raise RegraDeNegocioException(
                                "Material não pode estar vazio!"
                            )
                        janela.close()
                        return {
                            "nome": nome,
                            "preco": preco,
                            "estoque": estoque,
                            "capacidade_ml": capacidade,
                            "material": material,
                        }
                    except (
                        RegraDeNegocioException,
                        EntidadeNaoEncontradaException,
                    ) as e:
                        self.mostrar_popup("Erro de Validação", str(e))
                        continue
                    except Exception as e:
                        self.mostrar_popup(
                            "Erro Inesperado", f"Erro ao validar dados do copo: {e}"
                        )
                        continue
        except Exception as e:
            self.mostrar_popup("Erro", f"Erro ao coletar dados do copo: {e}")
            return None

    def mostra_produtos(self, lista_produtos: List[dict]):
        try:
            if not lista_produtos or not isinstance(lista_produtos, list):
                self.mostrar_popup(
                    "Produtos", "\nNenhum produto cadastrado para este evento."
                )
                return
            headings = ["#", "Descrição", "Preço (R$)", "Estoque"]
            dados_tabela = []
            for i, produto in enumerate(lista_produtos, 1):
                try:
                    if not isinstance(produto, dict):
                        raise RegraDeNegocioException("Dados de produto inválidos")
                    dados_tabela.append(
                        [
                            i,
                            str(produto.get("descricao", "N/A")),
                            f"{float(produto.get('preco', 0)):.2f}",
                            int(produto.get("estoque", 0)),
                        ]
                    )
                except (ValueError, TypeError, KeyError) as e:
                    dados_tabela.append([i, f"Erro: {e}", "0.00", "0"])
            layout = [
                [
                    sg.Text(
                        "\n-------- PRODUTOS DO EVENTO ----------",
                        font=("Helvetica", 14, "bold"),
                    )
                ],
                [
                    sg.Table(
                        values=dados_tabela,
                        headings=headings,
                        auto_size_columns=True,
                        justification="left",
                        num_rows=min(len(dados_tabela), 15),
                        key="-TABLE-",
                        expand_x=True,
                        expand_y=True,
                    )
                ],
                [sg.Button("Fechar")],
            ]
            janela = sg.Window(
                "Produtos do Evento", layout, resizable=True, modal=True, finalize=True
            )
            janela.read()
            janela.close()
        except Exception as e:
            self.mostrar_popup("Erro", f"Erro ao exibir produtos: {e}")

    def seleciona_produto(self, lista_produtos: List[dict]) -> Optional[int]:
        try:
            if not lista_produtos or not isinstance(lista_produtos, list):
                self.mostrar_popup("Selecionar Produto", "\nNenhum produto disponível.")
                return None
            headings = ["#", "Descrição", "Preço (R$)", "Estoque"]
            dados_tabela = []
            for i, produto in enumerate(lista_produtos, 1):
                try:
                    if not isinstance(produto, dict):
                        raise RegraDeNegocioException("Dados de produto inválidos")
                    dados_tabela.append(
                        [
                            i,
                            str(produto.get("descricao", "N/A")),
                            f"{float(produto.get('preco', 0)):.2f}",
                            int(produto.get("estoque", 0)),
                        ]
                    )
                except (ValueError, TypeError, KeyError) as e:
                    dados_tabela.append([i, f"Erro: {e}", "0.00", "0"])
            layout = [
                [
                    sg.Text(
                        "\n-------- SELECIONE UM PRODUTO ----------",
                        font=("Helvetica", 14, "bold"),
                    )
                ],
                [
                    sg.Table(
                        values=dados_tabela,
                        headings=headings,
                        auto_size_columns=True,
                        justification="left",
                        num_rows=min(len(dados_tabela), 10),
                        key="-TABLE-",
                        enable_events=True,
                        select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                        expand_x=True,
                        expand_y=True,
                    )
                ],
                [sg.Text("0 - Cancelar")],
                [sg.Button("Selecionar", key="1"), sg.Button("Cancelar", key="2")],
            ]
            janela = sg.Window(
                "Selecionar Produto", layout, resizable=True, modal=True, finalize=True
            )
            while True:
                evento, valores = janela.read()
                if evento == sg.WINDOW_CLOSED or evento == "2":
                    janela.close()
                    return None
                if evento == "1":
                    try:
                        indices_selecionados = valores["-TABLE-"]
                        if not indices_selecionados:
                            raise RegraDeNegocioException(
                                "Nenhum produto selecionado. Por favor, clique em uma linha da tabela."
                            )
                        else:
                            indice_selecionado = indices_selecionados[0]
                            if indice_selecionado < 0 or indice_selecionado >= len(
                                lista_produtos
                            ):
                                raise RegraDeNegocioException(
                                    "Índice de produto inválido."
                                )
                            janela.close()
                            return indice_selecionado
                    except (
                        RegraDeNegocioException,
                        EntidadeNaoEncontradaException,
                    ) as e:
                        self.mostrar_popup("Erro", str(e))
                        continue
                    except Exception as e:
                        self.mostrar_popup(
                            "Erro Inesperado", f"Erro ao selecionar produto: {e}"
                        )
                        continue
        except Exception as e:
            self.mostrar_popup("Erro", f"Erro ao selecionar produto: {e}")
            return None

    def pega_quantidade_venda(self) -> Optional[int]:
        return None

    def pega_metodo_pagamento(self) -> str:
        return "Dinheiro"

    def mostra_venda_realizada(self, dados_venda: dict):
        pass

    def mostra_relatorio_vendas(self, lista_vendas: List[dict]):
        pass

    def confirma_continuar_comprando(self) -> bool:
        return False
