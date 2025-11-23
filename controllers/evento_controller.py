import FreeSimpleGUI as sg
from datetime import datetime, date
from typing import List, TYPE_CHECKING, Optional
from models.evento import Evento
from views.evento_view import EventoView
from exceptions.entidadeNaoEncontradaException import EntidadeNaoEncontradaException
from exceptions.regraDeNegocioException import RegraDeNegocioException
from DAOs.evento_dao import EventoDAO


if TYPE_CHECKING:
    from controllers.usuario_controller import UsuarioController


class EventoController:

    def __init__(self, evento_view: EventoView):
        self.__view = evento_view
        self.__usuario_controller: Optional["UsuarioController"] = None
        self.__evento_dao = EventoDAO()

    def set_usuario_controller(self, usuario_controller: "UsuarioController"):
        self.__usuario_controller = usuario_controller

    def get_view(self) -> EventoView:
        return self.__view

    def get_eventos_lista(self) -> List[Evento]:
        return list(self.__evento_dao.get_all())

    def selecionar_evento_gui(self) -> Evento | None:
        eventos = self.get_eventos_lista()
        try:
            if not eventos:
                raise EntidadeNaoEncontradaException("Nenhum evento cadastrado.")
            dados_para_selecao = [
                self._transformar_evento_para_view(e) for e in eventos
            ]
            indice_escolhido = self.__view.seleciona_evento(dados_para_selecao)
            if indice_escolhido is not None:
                return eventos[indice_escolhido]
            return None
        except EntidadeNaoEncontradaException as e:
            self.__view.mostrar_popup("Erro", str(e))
            return None
        except Exception as e:
            self.__view.mostrar_popup(
                "Erro Inesperado", f"Erro ao selecionar evento: {e}"
            )
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
            "data": evento.data.strftime("%d/%m/%Y"),
            "local": evento.local,
            "preco_entrada": evento.preco_entrada,
        }

    def buscar_evento_por_nome(self, nome: str) -> Evento | None:
        if not nome or not nome.strip():
            raise RegraDeNegocioException("Nome do evento não pode estar vazio.")
        for e in self.get_eventos_lista():
            if e.nome.lower() == nome.lower():
                return e
        return None

    def incluir_evento(self):
        try:
            dados_evento = self.__view.pega_dados_evento()
            if dados_evento is None:
                return
            if self.buscar_evento_por_nome(dados_evento["nome"]):
                raise RegraDeNegocioException(
                    f"O evento '{dados_evento['nome']}' já existe."
                )
            try:
                data_obj = datetime.strptime(dados_evento["data"], "%d/%m/%Y").date()
                if data_obj < date.today():
                    raise RegraDeNegocioException(
                        "A data do evento não pode ser no passado."
                    )
            except ValueError:
                raise RegraDeNegocioException(
                    "Formato de data inválido. Use DD/MM/AAAA."
                )
            if dados_evento["preco_entrada"] < 0:
                raise RegraDeNegocioException("Preço do evento não pode ser negativo.")
            novo_evento = Evento(
                nome=dados_evento["nome"],
                data=data_obj,
                local=dados_evento["local"],
                preco_entrada=dados_evento["preco_entrada"],
            )
            self.__evento_dao.add(novo_evento)
            self.__view.mostrar_popup("Sucesso", "Evento incluído com sucesso!")
        except RegraDeNegocioException as e:
            self.__view.mostrar_popup("Erro", str(e))
        except Exception as e:
            self.__view.mostrar_popup("Erro Inesperado", f"Erro ao incluir evento: {e}")

    def listar_eventos(self):
        try:
            eventos = self.get_eventos_lista()
            if not eventos:
                raise EntidadeNaoEncontradaException("Nenhum evento cadastrado.")
            dados_para_view = [self._transformar_evento_para_view(e) for e in eventos]
            self.__view.mostra_eventos(dados_para_view)
        except EntidadeNaoEncontradaException as e:
            self.__view.mostrar_popup("Lista de Eventos", str(e))
        except Exception as e:
            self.__view.mostrar_popup("Erro Inesperado", f"Erro ao listar eventos: {e}")

    def ver_detalhes_evento(self):
        try:
            eventos = self.get_eventos_lista()
            if not eventos:
                raise EntidadeNaoEncontradaException("Nenhum evento cadastrado.")
            dados_para_selecao = [
                self._transformar_evento_para_view(e) for e in eventos
            ]
            indice_escolhido = self.__view.seleciona_evento(dados_para_selecao)
            if indice_escolhido is not None:
                evento_selecionado = eventos[indice_escolhido]
                feedbacks = getattr(evento_selecionado, "feedbacks", [])
                nota_media = None
                total_avaliacoes = len(feedbacks)
                if total_avaliacoes > 0:
                    nota_media = sum([fb.nota for fb in feedbacks]) / total_avaliacoes
                dados_detalhados = self._transformar_evento_para_view(
                    evento_selecionado
                )
                dados_detalhados["nota_media"] = nota_media
                dados_detalhados["total_avaliacoes"] = total_avaliacoes
                self.__view.mostra_detalhes_evento(dados_detalhados)
        except Exception as e:
            self.__view.mostrar_popup(
                "Erro Inesperado", f"Erro ao ver detalhes do evento: {e}"
            )

    def ver_feedbacks_evento(self):
        try:
            eventos = self.get_eventos_lista()
            if not eventos:
                raise EntidadeNaoEncontradaException("Nenhum evento cadastrado.")
            dados_para_selecao = [
                self._transformar_evento_para_view(e) for e in eventos
            ]
            indice_escolhido = self.__view.seleciona_evento(dados_para_selecao)
            if indice_escolhido is not None:
                evento_selecionado = eventos[indice_escolhido]
                feedbacks_objetos = getattr(evento_selecionado, "feedbacks", [])
                if not feedbacks_objetos:
                    raise EntidadeNaoEncontradaException(
                        "Nenhum feedback encontrado para este evento."
                    )
                dados_feedbacks = []
                for fb in feedbacks_objetos:
                    dados_feedbacks.append(
                        {
                            "nome_usuario": fb.usuario.nome,
                            "nota": fb.nota,
                            "comentario": fb.comentario,
                            "data": fb.data.strftime("%d/%m/%Y"),
                        }
                    )
                self.__view.mostra_feedbacks(dados_feedbacks)
        except EntidadeNaoEncontradaException as e:
            self.__view.mostrar_popup("Feedbacks do Evento", str(e))
        except Exception as e:
            self.__view.mostrar_popup("Erro Inesperado", f"Erro ao ver feedbacks: {e}")

    def excluir_evento(self):
        try:
            eventos = self.get_eventos_lista()
            if not eventos:
                raise EntidadeNaoEncontradaException("Nenhum evento cadastrado.")
            dados_para_selecao = [
                self._transformar_evento_para_view(e) for e in eventos
            ]
            indice_escolhido = self.__view.seleciona_evento(dados_para_selecao)
            if indice_escolhido is not None:
                evento_a_excluir = eventos[indice_escolhido]
                if (
                    hasattr(evento_a_excluir, "ingressos_vendidos")
                    and len(evento_a_excluir.ingressos_vendidos) > 0
                ):
                    raise RegraDeNegocioException(
                        "Não é possível excluir evento com ingressos vendidos."
                    )
                if evento_a_excluir.data < date.today():
                    raise RegraDeNegocioException(
                        "Não é possível excluir evento que já ocorreu."
                    )
                self.__evento_dao.remove(evento_a_excluir.nome)
                self.__view.mostrar_popup("Sucesso", "Evento excluído com sucesso!")
        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostrar_popup("Erro", str(e))
        except Exception as e:
            self.__view.mostrar_popup("Erro Inesperado", f"Erro ao excluir evento: {e}")

    def alterar_evento(self):
        try:
            eventos = self.get_eventos_lista()
            if not eventos:
                raise EntidadeNaoEncontradaException("Nenhum evento cadastrado.")
            dados_para_view = [self._transformar_evento_para_view(e) for e in eventos]
            indice_escolhido = self.__view.seleciona_evento(dados_para_view)
            if indice_escolhido is None:
                return
            evento = eventos[indice_escolhido]
            if evento.data < date.today():
                raise RegraDeNegocioException(
                    "Não é possível alterar evento que já ocorreu."
                )
            if (
                hasattr(evento, "ingressos_vendidos")
                and len(evento.ingressos_vendidos) > 0
            ):
                raise RegraDeNegocioException(
                    "Não é possível alterar evento com ingressos vendidos."
                )
            self.__view.mostrar_popup(
                "Alterando Evento", f"Alterando evento: {evento.nome}"
            )
            novos_dados = self.__view.pega_dados_evento()
            if novos_dados is None:
                return
            try:
                nova_data = datetime.strptime(novos_dados["data"], "%d/%m/%Y").date()
                if nova_data < date.today():
                    raise RegraDeNegocioException(
                        "A nova data não pode ser no passado."
                    )
            except ValueError:
                raise RegraDeNegocioException(
                    "Formato de data inválido. Use DD/MM/AAAA."
                )
            if novos_dados["preco_entrada"] < 0:
                raise RegraDeNegocioException("Preço não pode ser negativo.")
            if not novos_dados["local"].strip():
                raise RegraDeNegocioException("Local não pode estar vazio.")
            evento.data = nova_data
            evento.local = novos_dados["local"]
            evento.preco_entrada = novos_dados["preco_entrada"]
            self.__evento_dao.update(evento)
            self.__view.mostrar_popup("Sucesso", "Evento alterado com sucesso!")
        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostrar_popup("Erro", str(e))
        except Exception as e:
            self.__view.mostrar_popup("Erro Inesperado", f"Erro ao alterar evento: {e}")

    def selecionar_evento_para_avaliacao(self) -> Evento | None:
        eventos = self.get_eventos_lista()
        if not eventos:
            raise EntidadeNaoEncontradaException("Nenhum evento cadastrado.")
        dados_para_view = [self._transformar_evento_para_view(e) for e in eventos]
        indice_escolhido = self.__view.seleciona_evento(dados_para_view)
        if indice_escolhido is None:
            return None
        return eventos[indice_escolhido]

    def persistir_evento(self, evento: Evento):
        try:
            if evento and isinstance(evento, Evento):
                self.__evento_dao.update(evento)
        except Exception:
            pass

    def recarregar_eventos(self):
        try:
            from DAOs.evento_dao import EventoDAO

            self.__evento_dao = EventoDAO()
        except Exception as e:
            self.__view.mostrar_popup("Aviso", f"Falha ao recarregar eventos: {e}")

    def criar_evento_teste(self, dados: dict) -> Evento:
        nome = dados.get("nome")
        data = dados.get("data")
        local = dados.get("local")
        preco = dados.get("preco_entrada")
        if self.buscar_evento_por_nome(nome):
            suffix = 1
            base = nome
            while self.buscar_evento_por_nome(nome):
                nome = f"{base}_{suffix}"
                suffix += 1
        evento = Evento(nome, data, local, preco)
        self.__evento_dao.add(evento)
        return evento
