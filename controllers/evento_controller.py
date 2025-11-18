import FreeSimpleGUI as sg
from datetime import datetime, date
from typing import List, Optional, TYPE_CHECKING
from models.evento import Evento
from models.feedback import Feedback
from views.evento_view import EventoView
from exceptions.entidadeNaoEncontradaException import EntidadeNaoEncontradaException
from exceptions.regraDeNegocioException import RegraDeNegocioException

if TYPE_CHECKING:
    from controllers.usuario_controller import UsuarioController

class EventoController:

    def __init__(self, evento_view: EventoView):
        self.__view = evento_view
        self.__usuario_controller: UsuarioController = None
        self.__eventos: List[Evento] = []

    def set_usuario_controller(self, usuario_controller: 'UsuarioController'):
        self.__usuario_controller = usuario_controller

    def get_view(self) -> EventoView:
        return self.__view

    def get_eventos_lista(self) -> List[Evento]:
        return self.__eventos

    def selecionar_evento_gui(self) -> Evento | None:
        try:
            if not self.__eventos:
                raise EntidadeNaoEncontradaException("Nenhum evento cadastrado.")

            dados_para_selecao = [self._transformar_evento_para_view(e) for e in self.__eventos]
            indice_escolhido = self.__view.seleciona_evento(dados_para_selecao)

            if indice_escolhido is not None:
                return self.__eventos[indice_escolhido]

            return None
        except EntidadeNaoEncontradaException as e:
            self.__view.mostrar_popup("Erro", str(e))
            return None
        except Exception as e:
            self.__view.mostrar_popup("Erro Inesperado", f"Erro ao selecionar evento: {e}")
            return None

    def rodar_menu_evento(self):
        while True:
            try:
                opcao = self.__view.tela_opcoes()

                if opcao == 1:
                    self.incluir_evento()
                elif opcao == 2:
                    self.alterar_evento()
                elif opcao == 3:
                    self.listar_eventos()
                elif opcao == 4:
                    self.excluir_evento()
                elif opcao == 5:
                    self.ver_detalhes_evento()
                elif opcao == 6:
                    self.ver_feedbacks_evento()
                elif opcao == 0:
                    break
            except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
                self.__view.mostrar_popup("Erro", str(e))
            except Exception as e:
                self.__view.mostrar_popup("Erro Inesperado", f"Ocorreu um erro: {e}")

    def _transformar_evento_para_view(self, evento: Evento) -> dict:
        return {
            "nome": evento.nome,
            "data": evento.data.strftime('%d/%m/%Y'),
            "local": evento.local,
            "preco_entrada": evento.preco_entrada
        }

    def buscar_evento_por_nome(self, nome: str) -> Evento | None:
        try:
            if not nome or not nome.strip():
                raise RegraDeNegocioException("Nome do evento não pode estar vazio.")

            for evento in self.__eventos:
                if evento.nome.lower() == nome.lower():
                    return evento
            return None
        except RegraDeNegocioException:
            raise
        except Exception as e:
            raise RegraDeNegocioException(f"Erro ao buscar evento por nome: {e}")

    def incluir_evento(self):
        try:
            dados_evento = self.__view.pega_dados_evento()

            if dados_evento is None:
                return


            if self.buscar_evento_por_nome(dados_evento["nome"]):
                raise RegraDeNegocioException(f"O evento '{dados_evento['nome']}' já existe.")


            try:
                data_obj = datetime.strptime(dados_evento["data"], '%d/%m/%Y').date()
                if data_obj < date.today():
                    raise RegraDeNegocioException("A data do evento não pode ser no passado.")
            except ValueError:
                raise RegraDeNegocioException("Formato de data inválido. Use DD/MM/AAAA.")


            if dados_evento["preco_entrada"] < 0:
                raise RegraDeNegocioException("Preço do evento não pode ser negativo.")

            novo_evento = Evento(
                nome=dados_evento["nome"],
                data=data_obj,
                local=dados_evento["local"],
                preco_entrada=dados_evento["preco_entrada"]
            )

            self.__eventos.append(novo_evento)
            self.__view.mostrar_popup("Sucesso", "Evento incluído com sucesso!")

        except RegraDeNegocioException as e:
            self.__view.mostrar_popup("Erro", str(e))
        except Exception as e:
            self.__view.mostrar_popup("Erro Inesperado", f"Erro ao incluir evento: {e}")

    def listar_eventos(self):
        try:
            if not self.__eventos:
                raise EntidadeNaoEncontradaException("Nenhum evento cadastrado.")

            dados_para_view = [self._transformar_evento_para_view(e) for e in self.__eventos]
            self.__view.mostra_eventos(dados_para_view)

        except EntidadeNaoEncontradaException as e:
            self.__view.mostrar_popup("Lista de Eventos", str(e))
        except Exception as e:
            self.__view.mostrar_popup("Erro Inesperado", f"Erro ao listar eventos: {e}")

    def ver_detalhes_evento(self):
        try:
            if not self.__eventos:
                raise EntidadeNaoEncontradaException("Nenhum evento cadastrado.")

            dados_para_selecao = [self._transformar_evento_para_view(e) for e in self.__eventos]
            indice_escolhido = self.__view.seleciona_evento(dados_para_selecao)

            if indice_escolhido is not None:
                evento_selecionado = self.__eventos[indice_escolhido]

                feedbacks = evento_selecionado.feedbacks
                nota_media = None
                total_avaliacoes = len(feedbacks)
                if total_avaliacoes > 0:
                    nota_media = sum([fb.nota for fb in feedbacks]) / total_avaliacoes

                dados_detalhados = self._transformar_evento_para_view(evento_selecionado)
                dados_detalhados['nota_media'] = nota_media
                dados_detalhados['total_avaliacoes'] = total_avaliacoes

                self.__view.mostra_detalhes_evento(dados_detalhados)

        except EntidadeNaoEncontradaException as e:
            self.__view.mostrar_popup("Erro", str(e))
        except Exception as e:
            self.__view.mostrar_popup("Erro Inesperado", f"Erro ao ver detalhes do evento: {e}")

    def ver_feedbacks_evento(self):
        try:
            if not self.__eventos:
                raise EntidadeNaoEncontradaException("Nenhum evento cadastrado.")

            dados_para_selecao = [self._transformar_evento_para_view(e) for e in self.__eventos]
            indice_escolhido = self.__view.seleciona_evento(dados_para_selecao)

            if indice_escolhido is not None:
                evento_selecionado = self.__eventos[indice_escolhido]
                feedbacks_objetos = evento_selecionado.feedbacks

                if not feedbacks_objetos:
                    raise EntidadeNaoEncontradaException("Nenhum feedback encontrado para este evento.")

                dados_feedbacks = []
                for fb in feedbacks_objetos:
                    dados_feedbacks.append({
                        "nome_usuario": fb.usuario.nome,
                        "nota": fb.nota,
                        "comentario": fb.comentario,
                        "data": fb.data.strftime('%d/%m/%Y')
                    })

                self.__view.mostra_feedbacks(dados_feedbacks)

        except EntidadeNaoEncontradaException as e:
            self.__view.mostrar_popup("Feedbacks do Evento", str(e))
        except Exception as e:
            self.__view.mostrar_popup("Erro Inesperado", f"Erro ao ver feedbacks: {e}")

    def excluir_evento(self):
        try:
            if not self.__eventos:
                raise EntidadeNaoEncontradaException("Nenhum evento cadastrado.")

            dados_para_selecao = [self._transformar_evento_para_view(e) for e in self.__eventos]
            indice_escolhido = self.__view.seleciona_evento(dados_para_selecao)

            if indice_escolhido is not None:
                evento_a_excluir = self.__eventos[indice_escolhido]


                if hasattr(evento_a_excluir, 'ingressos_vendidos') and len(evento_a_excluir.ingressos_vendidos) > 0:
                    raise RegraDeNegocioException("Não é possível excluir um evento que já possui ingressos vendidos.")


                if evento_a_excluir.data < date.today():
                    raise RegraDeNegocioException("Não é possível excluir um evento que já ocorreu.")

                self.__eventos.remove(evento_a_excluir)
                self.__view.mostrar_popup("Sucesso", "Evento excluído com sucesso!")

        except EntidadeNaoEncontradaException as e:
            self.__view.mostrar_popup("Erro", str(e))
        except RegraDeNegocioException as e:
            self.__view.mostrar_popup("Erro", str(e))
        except Exception as e:
            self.__view.mostrar_popup("Erro Inesperado", f"Erro ao excluir evento: {e}")

    def alterar_evento(self):
        try:
            if not self.__eventos:
                raise EntidadeNaoEncontradaException("Nenhum evento cadastrado.")

            dados_para_view = [self._transformar_evento_para_view(e) for e in self.__eventos]
            indice_escolhido = self.__view.seleciona_evento(dados_para_view)

            if indice_escolhido is None:
                return

            evento = self.__eventos[indice_escolhido]


            if evento.data < date.today():
                raise RegraDeNegocioException("Não é possível alterar um evento que já ocorreu.")


            if hasattr(evento, 'ingressos_vendidos') and len(evento.ingressos_vendidos) > 0:
                raise RegraDeNegocioException("Não é possível alterar um evento que já possui ingressos vendidos.")

            self.__view.mostrar_popup("Alterando Evento", f"Alterando evento: {evento.nome}")

            novos_dados = self.__view.pega_dados_evento()
            if novos_dados is None:
                return


            try:
                nova_data = datetime.strptime(novos_dados["data"], "%d/%m/%Y").date()
                if nova_data < date.today():
                    raise RegraDeNegocioException("A nova data do evento não pode ser no passado.")
            except ValueError:
                raise RegraDeNegocioException("Formato de data inválido. Use DD/MM/AAAA.")


            if novos_dados["preco_entrada"] < 0:
                raise RegraDeNegocioException("Preço do evento não pode ser negativo.")


            if not novos_dados["local"].strip():
                raise RegraDeNegocioException("Local do evento não pode estar vazio.")

            evento.data = nova_data
            evento.local = novos_dados["local"]
            evento.preco_entrada = novos_dados["preco_entrada"]

            self.__view.mostrar_popup("Sucesso", "Evento alterado com sucesso!")

        except EntidadeNaoEncontradaException as e:
            self.__view.mostrar_popup("Erro", str(e))
        except RegraDeNegocioException as e:
            self.__view.mostrar_popup("Erro", str(e))
        except Exception as e:
            self.__view.mostrar_popup("Erro Inesperado", f"Erro ao alterar evento: {e}")

    def avaliar_evento(self):
        try:
            if not self.__usuario_controller:
                raise RegraDeNegocioException("Controlador de Usuário não inicializado.")


            matricula = self.__usuario_controller.pega_matricula_usuario_gui()
            if not matricula:
                return

            usuario = self.__usuario_controller.buscar_usuario_por_matricula(matricula)
            if not usuario:
                raise EntidadeNaoEncontradaException("Usuário não encontrado.")


            if not self.__eventos:
                raise EntidadeNaoEncontradaException("Nenhum evento cadastrado para avaliar.")

            dados_para_view = [self._transformar_evento_para_view(e) for e in self.__eventos]
            indice_escolhido = self.__view.seleciona_evento(dados_para_view)
            if indice_escolhido is None:
                return

            evento_escolhido = self.__eventos[indice_escolhido]


            if evento_escolhido.data > date.today():
                raise RegraDeNegocioException("Só é possível avaliar eventos que já ocorreram.")


            for feedback in evento_escolhido.feedbacks:
                if feedback.usuario == usuario:
                    raise RegraDeNegocioException("Usuário já avaliou este evento.")


            dados_avaliacao = self.__usuario_controller.pega_dados_avaliacao_gui()
            if dados_avaliacao is None:
                return


            if dados_avaliacao["nota"] < 1 or dados_avaliacao["nota"] > 5:
                raise RegraDeNegocioException("Nota deve estar entre 1 e 5.")

            if not dados_avaliacao["comentario"].strip():
                raise RegraDeNegocioException("Comentário não pode estar vazio.")


            feedback = Feedback(
                usuario=usuario,
                evento=evento_escolhido,
                nota=dados_avaliacao["nota"],
                comentario=dados_avaliacao["comentario"],
                data=date.today()
            )

            evento_escolhido.adicionar_feedback(feedback)
            self.__view.mostrar_popup("Sucesso", f"Avaliação registrada com sucesso para o evento '{evento_escolhido.nome}'!")

        except EntidadeNaoEncontradaException as e:
            self.__view.mostrar_popup("Erro", str(e))
        except RegraDeNegocioException as e:
            self.__view.mostrar_popup("Erro", str(e))
        except Exception as e:
            self.__view.mostrar_popup("Erro Inesperado", f"Erro ao avaliar evento: {e}")
