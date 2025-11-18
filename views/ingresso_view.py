from typing import List, Optional
import FreeSimpleGUI as sg
from exceptions.entidadeNaoEncontradaException import EntidadeNaoEncontradaException
from exceptions.regraDeNegocioException import RegraDeNegocioException

class IngressoView:

    def __init__(self):
        try:
            sg.theme('Reddit')
        except Exception as e:
            print(f"Erro ao definir tema: {e}")

    def mostra_mensagem(self, msg: str):
        try:
            sg.Popup(str(msg), title="Aviso", keep_on_top=True, modal=True)
        except Exception as e:
            print(f"Erro ao exibir mensagem: {e}")
            print(f"Mensagem: {msg}")

    def tela_opcoes(self) -> int:
        try:
            layout = [
                [sg.Text("\n-------- MENU INGRESSOS ----------", font=("Helvetica", 14, "bold"))],
                [sg.Button('Comprar Ingresso de Evento', key=1, size=(30,1))],
                [sg.Button('Listar Meus Ingressos', key=2, size=(30,1))],
                [sg.Button('Gerenciar Revenda', key=3, size=(30,1))],
                [sg.Button('Retornar ao Menu Principal', key=0, size=(30,1), button_color=('white', 'red'))]
            ]

            janela = sg.Window('Menu Ingressos', layout, finalize=True, modal=True)

            while True:
                evento, valores = janela.read()
                if evento == sg.WINDOW_CLOSED:
                    janela.close()
                    return 0
                janela.close()
                return evento

        except Exception as e:
            self.mostra_mensagem(f"Erro ao criar menu de ingressos: {e}")
            return 0

    def tela_opcoes_revenda(self) -> int:
        try:
            layout = [
                [sg.Text("\n-------- MENU REVENDA ----------", font=("Helvetica", 14, "bold"))],
                [sg.Button('Colocar Ingresso à Venda', key=1, size=(30,1))],
                [sg.Button('Remover Ingresso da Venda', key=2, size=(30,1))],
                [sg.Button('Comprar Ingresso de Revenda', key=3, size=(30,1))],
                [sg.Button('Listar Meus Ingressos à Venda', key=4, size=(30,1))],
                [sg.Button('Voltar', key=0, size=(30,1), button_color=('white', 'red'))]
            ]

            janela = sg.Window('Menu Revenda', layout, finalize=True, modal=True)

            while True:
                evento, valores = janela.read()
                if evento == sg.WINDOW_CLOSED:
                    janela.close()
                    return 0
                janela.close()
                return evento

        except Exception as e:
            self.mostra_mensagem(f"Erro ao criar menu de revenda: {e}")
            return 0

    def pega_matricula_comprador(self) -> str:
        try:
            layout = [
                [sg.Text("Digite sua matrícula:")],
                [sg.Input(key='-MATRICULA-')],
                [sg.Button('OK', key='-OK-'), sg.Button('Cancelar', key='-CANCELAR-')]
            ]

            janela = sg.Window('Matrícula do Comprador', layout, modal=True, finalize=True)

            while True:
                evento, valores = janela.read()
                if evento == sg.WINDOW_CLOSED or evento == '-CANCELAR-':
                    janela.close()
                    return None

                if evento == '-OK-':
                    try:
                        matricula = valores['-MATRICULA-'].strip()

                        if not matricula:
                            raise RegraDeNegocioException("Matrícula não pode estar vazia!")

                        if not matricula.isdigit():
                            raise RegraDeNegocioException("Matrícula deve conter apenas números!")

                        janela.close()
                        return matricula

                    except (RegraDeNegocioException, EntidadeNaoEncontradaException) as e:
                        self.mostra_mensagem(str(e))
                        continue
                    except Exception as e:
                        self.mostra_mensagem(f"Erro ao validar matrícula: {e}")
                        continue

        except Exception as e:
            self.mostra_mensagem(f"Erro ao coletar matrícula: {e}")
            return None

    def pega_metodo_pagamento(self) -> str:
        try:
            layout = [
                [sg.Text("\n-------- MÉTODO DE PAGAMENTO ----------", font=("Helvetica", 14, "bold"))],
                [sg.Button('Dinheiro', key=1, size=(20,1))],
                [sg.Button('PIX', key=2, size=(20,1))],
                [sg.Button('Débito', key=3, size=(20,1))],
                [sg.Button('Crédito', key=4, size=(20,1))],
                [sg.Button('Cancelar', key=0, size=(20,1), button_color=('white', 'red'))]
            ]

            janela = sg.Window('Método de Pagamento', layout, modal=True, finalize=True)
            metodos = {1: "Dinheiro", 2: "PIX", 3: "Debito", 4: "Credito"}

            while True:
                evento, valores = janela.read()
                if evento == sg.WINDOW_CLOSED or evento == 0:
                    janela.close()
                    return None
                if evento in metodos:
                    janela.close()
                    return metodos[evento]

        except Exception as e:
            self.mostra_mensagem(f"Erro ao selecionar método de pagamento: {e}")
            return None

    def confirma_compra_ingresso(self, dados_compra: dict) -> bool:
        try:
            if not dados_compra or not isinstance(dados_compra, dict):
                raise RegraDeNegocioException("Dados da compra não disponíveis.")

            evento_nome = str(dados_compra.get('evento', 'N/A'))
            preco = float(dados_compra.get('preco', 0))
            metodo = str(dados_compra.get('metodo_pagamento', 'N/A'))

            # Criar a mensagem de confirmação
            mensagem = f"""
CONFIRMAR COMPRA DE INGRESSO:

Evento: {evento_nome}
Preço: R$ {preco:.2f}
Método de Pagamento: {metodo}

Deseja confirmar esta compra?
            """

            resposta = sg.popup_yes_no(
                mensagem,
                title="Confirmar Compra",
                keep_on_top=True
            )

            return resposta == 'Yes'

        except (ValueError, TypeError) as e:
            self.mostra_mensagem(f"Erro nos dados da compra: {e}")
            return False
        except Exception as e:
            self.mostra_mensagem(f"Erro ao confirmar compra: {e}")
            return False

    def mostra_ingressos(self, lista_ingressos: List[dict]):
        try:
            if not lista_ingressos or not isinstance(lista_ingressos, list):
                self.mostra_mensagem("Nenhum ingresso encontrado.")
                return

            headings = ['#', 'Evento', 'Comprador', 'Data Compra', 'Preço (R$)', 'Revendedor']
            dados_tabela = []

            for i, ingresso in enumerate(lista_ingressos, 1):
                try:
                    if not isinstance(ingresso, dict):
                        raise RegraDeNegocioException("Dados de ingresso inválidos")

                    revendedor = ingresso.get('nome_revendedor', None)
                    revendedor_str = revendedor if revendedor else "Não"

                    dados_tabela.append([
                        i,
                        str(ingresso.get('nome_evento', 'N/A')),
                        str(ingresso.get('nome_comprador', 'N/A')),
                        str(ingresso.get('data_compra', 'N/A')),
                        f"{float(ingresso.get('preco', 0)):.2f}",
                        revendedor_str
                    ])
                except (ValueError, TypeError, KeyError) as e:
                    dados_tabela.append([i, f"Erro: {e}", "N/A", "N/A", "0.00", "N/A"])

            layout = [
                [sg.Text("\n-------- MEUS INGRESSOS ----------", font=("Helvetica", 14, "bold"))],
                [sg.Table(values=dados_tabela, headings=headings,
                          auto_size_columns=True, justification='left',
                          num_rows=min(len(dados_tabela), 15),
                          key='-TABLE-', expand_x=True, expand_y=True)],
                [sg.Button('Fechar')]
            ]

            janela = sg.Window('Meus Ingressos', layout, resizable=True, modal=True, finalize=True)
            janela.read()
            janela.close()

        except Exception as e:
            self.mostra_mensagem(f"Erro ao exibir ingressos: {e}")

    def seleciona_ingresso(self, lista_ingressos: List[dict]) -> Optional[int]:
        try:
            if not lista_ingressos or not isinstance(lista_ingressos, list):
                self.mostra_mensagem("Nenhum ingresso disponível para seleção.")
                return None

            headings = ['#', 'Evento', 'Preço (R$)', 'Data Compra']
            dados_tabela = []

            for i, ingresso in enumerate(lista_ingressos, 1):
                try:
                    if not isinstance(ingresso, dict):
                        raise RegraDeNegocioException("Dados de ingresso inválidos")

                    dados_tabela.append([
                        i,
                        str(ingresso.get('nome_evento', 'N/A')),
                        f"{float(ingresso.get('preco', 0)):.2f}",
                        str(ingresso.get('data_compra', 'N/A'))
                    ])
                except (ValueError, TypeError, KeyError) as e:
                    dados_tabela.append([i, f"Erro: {e}", "0.00", "N/A"])

            layout = [
                [sg.Text("\n-------- SELECIONE UM INGRESSO ----------", font=("Helvetica", 14, "bold"))],
                [sg.Table(values=dados_tabela, headings=headings,
                          auto_size_columns=True, justification='left',
                          num_rows=min(len(dados_tabela), 10),
                          key='-TABLE-',
                          enable_events=True,
                          select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                          expand_x=True, expand_y=True)],
                [sg.Button('Selecionar', key='1'), sg.Button('Cancelar', key='2')]
            ]

            janela = sg.Window('Selecionar Ingresso', layout, resizable=True, modal=True, finalize=True)

            while True:
                evento, valores = janela.read()
                if evento == sg.WINDOW_CLOSED or evento == '2':
                    janela.close()
                    return None

                if evento == '1':
                    try:
                        indices_selecionados = valores['-TABLE-']
                        if not indices_selecionados:
                            raise RegraDeNegocioException("Nenhum ingresso selecionado. Por favor, clique em uma linha da tabela.")
                        else:
                            indice_selecionado = indices_selecionados[0]
                            if indice_selecionado < 0 or indice_selecionado >= len(lista_ingressos):
                                raise RegraDeNegocioException("Índice de ingresso inválido.")
                            janela.close()
                            return indice_selecionado

                    except (RegraDeNegocioException, EntidadeNaoEncontradaException) as e:
                        self.mostra_mensagem(str(e))
                        continue
                    except Exception as e:
                        self.mostra_mensagem(f"Erro ao selecionar ingresso: {e}")
                        continue

        except Exception as e:
            self.mostra_mensagem(f"Erro ao selecionar ingresso: {e}")
            return None

    def seleciona_ingresso_revenda(self, lista_ingressos: List[dict]) -> Optional[int]:
        try:
            if not lista_ingressos or not isinstance(lista_ingressos, list):
                self.mostra_mensagem("Nenhum ingresso de revenda disponível.")
                return None

            headings = ['#', 'Evento', 'Revendedor', 'Preço (R$)', 'Data Original']
            dados_tabela = []

            for i, ingresso in enumerate(lista_ingressos, 1):
                try:
                    if not isinstance(ingresso, dict):
                        raise RegraDeNegocioException("Dados de ingresso inválidos")

                    dados_tabela.append([
                        i,
                        str(ingresso.get('nome_evento', 'N/A')),
                        str(ingresso.get('nome_revendedor', 'N/A')),
                        f"{float(ingresso.get('preco', 0)):.2f}",
                        str(ingresso.get('data_compra', 'N/A'))
                    ])
                except (ValueError, TypeError, KeyError) as e:
                    dados_tabela.append([i, f"Erro: {e}", "N/A", "0.00", "N/A"])

            layout = [
                [sg.Text("\n-------- INGRESSOS DE REVENDA ----------", font=("Helvetica", 14, "bold"))],
                [sg.Table(values=dados_tabela, headings=headings,
                          auto_size_columns=True, justification='left',
                          num_rows=min(len(dados_tabela), 10),
                          key='-TABLE-',
                          enable_events=True,
                          select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                          expand_x=True, expand_y=True)],
                [sg.Button('Comprar', key='1'), sg.Button('Cancelar', key='2')]
            ]

            janela = sg.Window('Ingressos de Revenda', layout, resizable=True, modal=True, finalize=True)

            while True:
                evento, valores = janela.read()
                if evento == sg.WINDOW_CLOSED or evento == '2':
                    janela.close()
                    return None

                if evento == '1':
                    try:
                        indices_selecionados = valores['-TABLE-']
                        if not indices_selecionados:
                            raise RegraDeNegocioException("Nenhum ingresso selecionado. Por favor, clique em uma linha da tabela.")
                        else:
                            indice_selecionado = indices_selecionados[0]
                            if indice_selecionado < 0 or indice_selecionado >= len(lista_ingressos):
                                raise RegraDeNegocioException("Índice de ingresso inválido.")
                            janela.close()
                            return indice_selecionado

                    except (RegraDeNegocioException, EntidadeNaoEncontradaException) as e:
                        self.mostra_mensagem(str(e))
                        continue
                    except Exception as e:
                        self.mostra_mensagem(f"Erro ao selecionar ingresso: {e}")
                        continue

        except Exception as e:
            self.mostra_mensagem(f"Erro ao selecionar ingresso de revenda: {e}")
            return None

    def pega_novo_preco_revenda(self) -> Optional[float]:
        try:
            layout = [
                [sg.Text("Digite o novo preço para revenda:")],
                [sg.Text("R$"), sg.Input(key='-PRECO-', size=(10,1))],
                [sg.Button('OK', key='-OK-'), sg.Button('Cancelar', key='-CANCELAR-')]
            ]

            janela = sg.Window('Novo Preço de Revenda', layout, modal=True, finalize=True)

            while True:
                evento, valores = janela.read()
                if evento == sg.WINDOW_CLOSED or evento == '-CANCELAR-':
                    janela.close()
                    return None

                if evento == '-OK-':
                    try:
                        preco_str = valores['-PRECO-'].strip()

                        if not preco_str:
                            raise RegraDeNegocioException("Preço não pode estar vazio!")

                        try:
                            preco_float = float(preco_str)
                            if preco_float <= 0:
                                raise RegraDeNegocioException("Preço deve ser maior que zero!")
                            janela.close()
                            return preco_float
                        except ValueError:
                            raise RegraDeNegocioException("Preço inválido! Digite um número (ex: 50.00).")

                    except (RegraDeNegocioException, EntidadeNaoEncontradaException) as e:
                        self.mostra_mensagem(str(e))
                        continue
                    except Exception as e:
                        self.mostra_mensagem(f"Erro ao validar preço: {e}")
                        continue

        except Exception as e:
            self.mostra_mensagem(f"Erro ao coletar preço: {e}")
            return None