from typing import List, Optional
import FreeSimpleGUI as sg
from datetime import datetime
from exceptions.entidadeNaoEncontradaException import EntidadeNaoEncontradaException
from exceptions.regraDeNegocioException import RegraDeNegocioException

class EventoView:

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

    def tela_opcoes(self) -> int:
        try:
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
        except Exception as e:
            self.mostrar_popup("Erro", f"Erro ao criar menu de eventos: {e}")
            return 0

    def pega_dados_evento(self) -> dict:
        try:
            layout = [
                [sg.Text("\n-------- DADOS DO EVENTO ----------", font=("Helvetica", 14, "bold"))],
                [sg.Text("Nome:", size=(10,1)), sg.Input(key='1')],
                [sg.Text("Data:", size=(10,1)), sg.Input(key='2', size=(10,1)),
                 sg.CalendarButton('Escolher', target='2', format='%d/%m/%Y')],
                [sg.Text("Local:", size=(10,1)), sg.Input(key='3')],
                [sg.Text("Preço (R$):", size=(10,1)), sg.Input(key='4', size=(10,1))],
                [sg.Button('Salvar', key='5'), sg.Button('Cancelar', key='6')]
            ]

            janela = sg.Window('Dados do Evento', layout, modal=True, finalize=True)

            while True:
                try:
                    evento, valores = janela.read()
                    if evento == sg.WINDOW_CLOSED or evento == '6':
                        janela.close()
                        return None

                    if evento == '5':
                        nome = valores['1'].strip()
                        data_str = valores['2'].strip()
                        local = valores['3'].strip()
                        preco_str = valores['4'].strip()


                        if not nome:
                            raise RegraDeNegocioException("Nome do evento não pode estar vazio!")

                        if not data_str:
                            raise RegraDeNegocioException("Data do evento deve ser informada!")

                        try:
                            data_obj = datetime.strptime(data_str, '%d/%m/%Y')
                            if data_obj.date() < datetime.now().date():
                                raise RegraDeNegocioException("A data do evento não pode ser no passado!")
                        except ValueError:
                            raise RegraDeNegocioException("Formato de data inválido. Use o calendário ou DD/MM/AAAA.")

                        if not local:
                            raise RegraDeNegocioException("Local não pode estar vazio!")

                        try:
                            preco_float = float(preco_str)
                            if preco_float < 0:
                                raise RegraDeNegocioException("Preço não pode ser negativo!")
                        except ValueError:
                            raise RegraDeNegocioException("Preço inválido. Use apenas números (ex: 100.50).")


                        janela.close()
                        return {
                            "nome": nome,
                            "data": data_str,
                            "local": local,
                            "preco_entrada": preco_float
                        }

                except (RegraDeNegocioException, EntidadeNaoEncontradaException) as e:
                    self.mostrar_popup("Erro", str(e))
                    continue
                except Exception as e:
                    self.mostrar_popup("Erro Inesperado", f"Erro ao processar dados: {e}")
                    continue
        except Exception as e:
            self.mostrar_popup("Erro", f"Erro ao coletar dados do evento: {e}")
            return None

    def mostra_evento(self, dados_evento: dict):
        try:
            if not dados_evento:
                raise EntidadeNaoEncontradaException("Dados do evento não encontrados.")

            layout = [
                [sg.Text("--- DETALHES DO EVENTO ---", font=("Helvetica", 14, "bold"))],
                [sg.Text("Nome:", size=(10, 1), font=("Helvetica", 10, "bold")),
                 sg.Text(str(dados_evento.get('nome', 'N/A')))],
                [sg.Text("Data:", size=(10, 1), font=("Helvetica", 10, "bold")),
                 sg.Text(str(dados_evento.get('data', 'N/A')))],
                [sg.Text("Local:", size=(10, 1), font=("Helvetica", 10, "bold")),
                 sg.Text(str(dados_evento.get('local', 'N/A')))],
                [sg.Text("Preço:", size=(10, 1), font=("Helvetica", 10, "bold")),
                 sg.Text(f"R$ {float(dados_evento.get('preco_entrada', 0)):.2f}")],
                [sg.Text("-----------------------------")],
                [sg.Button('OK', key='1')]
            ]

            janela = sg.Window('Detalhes do Evento', layout, modal=True, finalize=True)

            while True:
                evento, valores = janela.read()
                if evento == sg.WINDOW_CLOSED or evento == '1':
                    break

            janela.close()

        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.mostrar_popup("Erro", str(e))
        except Exception as e:
            self.mostrar_popup("Erro Inesperado", f"Erro ao mostrar evento: {e}")

    def mostra_eventos(self, lista_dados_eventos: List[dict]):
        try:
            if not lista_dados_eventos or not isinstance(lista_dados_eventos, list):
                raise EntidadeNaoEncontradaException("Nenhum evento cadastrado.")

            headings = ['#', 'Nome', 'Data', 'Local', 'Preço (R$)']
            dados_tabela = []

            for i, dados in enumerate(lista_dados_eventos, 1):
                try:
                    if not isinstance(dados, dict):
                        raise RegraDeNegocioException("Dados de evento inválidos")

                    dados_tabela.append([
                        i,
                        str(dados.get('nome', 'N/A')),
                        str(dados.get('data', 'N/A')),
                        str(dados.get('local', 'N/A')),
                        f"{float(dados.get('preco_entrada', 0)):.2f}"
                    ])
                except (ValueError, TypeError, KeyError) as e:
                    dados_tabela.append([i, f"Erro: {e}", "N/A", "N/A", "0.00"])

            layout = [
                [sg.Text("\n-------- LISTA DE EVENTOS ----------", font=("Helvetica", 14, "bold"))],
                [sg.Table(values=dados_tabela, headings=headings,
                          auto_size_columns=True, justification='left',
                          num_rows=min(len(dados_tabela), 15),
                          key='1', expand_x=True, expand_y=True)],
                [sg.Button('Fechar')]
            ]

            janela = sg.Window('Lista de Eventos', layout, resizable=True, modal=True, finalize=True)
            janela.read()
            janela.close()

        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.mostrar_popup("Lista de Eventos", str(e))
        except Exception as e:
            self.mostrar_popup("Erro Inesperado", f"Erro ao mostrar lista de eventos: {e}")

    def mostra_detalhes_evento(self, dados_detalhados_evento: dict):
        try:
            if not dados_detalhados_evento or not isinstance(dados_detalhados_evento, dict):
                raise EntidadeNaoEncontradaException("Dados detalhados do evento não encontrados.")


            try:
                if dados_detalhados_evento.get('nota_media') is not None:
                    nota = float(dados_detalhados_evento['nota_media'])
                    avaliacoes = int(dados_detalhados_evento.get('total_avaliacoes', 0))
                    nota_str = f"{nota:.1f}/5.0 ({avaliacoes} avaliações)"
                else:
                    nota_str = "Ainda não há avaliações para este evento."
            except (ValueError, TypeError) as e:
                nota_str = "Erro ao processar avaliações."

            layout = [
                [sg.Text("--- DETALHES DO EVENTO ---", font=("Helvetica", 14, "bold"))],
                [sg.Text("Nome:", size=(15, 1), font=("Helvetica", 10, "bold")),
                 sg.Text(str(dados_detalhados_evento.get('nome', 'N/A')))],
                [sg.Text("Data:", size=(15, 1), font=("Helvetica", 10, "bold")),
                 sg.Text(str(dados_detalhados_evento.get('data', 'N/A')))],
                [sg.Text("Local:", size=(15, 1), font=("Helvetica", 10, "bold")),
                 sg.Text(str(dados_detalhados_evento.get('local', 'N/A')))],
                [sg.Text("Preço:", size=(15, 1), font=("Helvetica", 10, "bold")),
                 sg.Text(f"R$ {float(dados_detalhados_evento.get('preco_entrada', 0)):.2f}")],
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

        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.mostrar_popup("Erro", str(e))
        except Exception as e:
            self.mostrar_popup("Erro Inesperado", f"Erro ao mostrar detalhes: {e}")

    def mostra_feedbacks(self, lista_dados_feedbacks: List[dict]):
        try:
            if not lista_dados_feedbacks or not isinstance(lista_dados_feedbacks, list):
                raise EntidadeNaoEncontradaException("Nenhum feedback encontrado para este evento.")

            headings = ['#', 'Usuário', 'Nota', 'Comentário', 'Data']
            dados_tabela = []

            for i, dados in enumerate(lista_dados_feedbacks, 1):
                try:
                    if not isinstance(dados, dict):
                        raise RegraDeNegocioException("Dados de feedback inválidos")

                    dados_tabela.append([
                        i,
                        str(dados.get('nome_usuario', 'N/A')),
                        f"{int(dados.get('nota', 0))}/5",
                        str(dados.get('comentario', 'N/A')),
                        str(dados.get('data', 'N/A'))
                    ])
                except (ValueError, TypeError, KeyError) as e:
                    dados_tabela.append([i, "Erro", f"Erro: {e}", "N/A", "N/A"])

            layout = [
                [sg.Text("\n-------- FEEDBACKS DO EVENTO ----------", font=("Helvetica", 14, "bold"))],
                [sg.Table(values=dados_tabela, headings=headings,
                          auto_size_columns=True, justification='left',
                          col_widths=[5, 15, 5, 30, 10],
                          num_rows=min(len(dados_tabela), 10),
                          key='1', expand_x=True, expand_y=True)],
                [sg.Button('Fechar')]
            ]

            janela = sg.Window('Feedbacks do Evento', layout, resizable=True, modal=True, finalize=True)
            janela.read()
            janela.close()

        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.mostrar_popup("Feedbacks do Evento", str(e))
        except Exception as e:
            self.mostrar_popup("Erro Inesperado", f"Erro ao mostrar feedbacks: {e}")

    def seleciona_evento(self, lista_dados_eventos: List[dict]) -> Optional[int]:
        try:
            if not lista_dados_eventos or not isinstance(lista_dados_eventos, list):
                raise EntidadeNaoEncontradaException("Nenhum evento disponível para selecionar.")

            headings = ['#', 'Nome', 'Data', 'Local', 'Preço (R$)']
            dados_tabela = []

            for i, dados in enumerate(lista_dados_eventos, 1):
                try:
                    if not isinstance(dados, dict):
                        raise RegraDeNegocioException("Dados de evento inválidos")

                    dados_tabela.append([
                        i,
                        str(dados.get('nome', 'N/A')),
                        str(dados.get('data', 'N/A')),
                        str(dados.get('local', 'N/A')),
                        f"{float(dados.get('preco_entrada', 0)):.2f}"
                    ])
                except (ValueError, TypeError, KeyError) as e:
                    dados_tabela.append([i, f"Erro: {e}", "N/A", "N/A", "0.00"])

            layout = [
                [sg.Text("\n-------- SELECIONE UM EVENTO ----------", font=("Helvetica", 14, "bold"))],
                [sg.Table(values=dados_tabela, headings=headings,
                          auto_size_columns=True, justification='left',
                          num_rows=min(len(dados_tabela), 15),
                          key='1',
                          enable_events=True,
                          select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                          expand_x=True, expand_y=True)],
                [sg.Button('Selecionar', key='2'), sg.Button('Cancelar', key='3')]
            ]

            janela = sg.Window('Selecionar Evento', layout, resizable=True, modal=True, finalize=True)

            while True:
                try:
                    evento, valores = janela.read()

                    if evento == sg.WINDOW_CLOSED or evento == '3':
                        janela.close()
                        return None

                    if evento == '2':
                        indices_selecionados = valores['1']

                        if not indices_selecionados:
                            raise RegraDeNegocioException("Nenhum evento selecionado. Por favor, clique em uma linha da tabela.")
                        else:
                            indice_selecionado = indices_selecionados[0]
                            if indice_selecionado < 0 or indice_selecionado >= len(lista_dados_eventos):
                                raise RegraDeNegocioException("Índice de evento inválido.")
                            janela.close()
                            return indice_selecionado

                except (RegraDeNegocioException, EntidadeNaoEncontradaException) as e:
                    self.mostrar_popup("Erro", str(e))
                    continue
                except Exception as e:
                    self.mostrar_popup("Erro Inesperado", f"Erro ao selecionar evento: {e}")
                    janela.close()
                    return None

        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.mostrar_popup("Selecionar Evento", str(e))
            return None
        except Exception as e:
            self.mostrar_popup("Erro Inesperado", f"Erro geral ao selecionar evento: {e}")
            return None
