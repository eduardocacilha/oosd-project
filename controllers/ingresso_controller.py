from views.ingresso_view import IngressoView
from controllers.usuario_controller import UsuarioController
from controllers.evento_controller import EventoController
import FreeSimpleGUI as sg
from exceptions.entidadeNaoEncontradaException import EntidadeNaoEncontradaException
from exceptions.regraDeNegocioException import RegraDeNegocioException
from models.ingresso import Ingresso
from DAOs.ingresso_dao import IngressoDAO


class IngressoController:

    def __init__(self, ingresso_view: IngressoView):
        self.__view = ingresso_view
        self.__usuario_controller: UsuarioController = None
        self.__evento_controller: EventoController = None
        self.__ingresso_dao = IngressoDAO()

    def set_usuario_controller(self, usuario_controller: UsuarioController):
        try:
            self.__usuario_controller = usuario_controller
        except Exception as e:
            print(f"Erro ao definir usuario_controller: {e}")

    def set_evento_controller(self, evento_controller: EventoController):
        try:
            self.__evento_controller = evento_controller
        except Exception as e:
            print(f"Erro ao definir evento_controller: {e}")

    def rodar_menu_ingresso(self):
        try:
            while True:
                opcao = self.__view.tela_opcoes()
                try:
                    if opcao == 1:
                        self.comprar_ingresso_de_evento()
                    elif opcao == 2:
                        matricula = self.__view.pega_matricula_comprador()
                        if matricula:
                            self.listar_meus_ingressos(matricula)
                    elif opcao == 3:
                        self.rodar_menu_revenda()
                    elif opcao == 0:
                        break
                except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
                    self.__view.mostra_mensagem(str(e))
                except Exception as e:
                    self.__view.mostra_mensagem(f"Erro Inesperado: {e}")
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro no menu de ingressos: {e}")

    def rodar_menu_revenda(self):
        try:
            matricula_usuario = self.__view.pega_matricula_comprador()
            if not matricula_usuario:
                return
            usuario = self.__usuario_controller.buscar_usuario_por_matricula(
                matricula_usuario
            )
            if not usuario:
                raise EntidadeNaoEncontradaException("Usuário não encontrado.")
            while True:
                opcao = self.__view.tela_opcoes_revenda()
                try:
                    if opcao == 1:
                        self.colocar_ingresso_a_venda(matricula_usuario)
                    elif opcao == 2:
                        self.remover_ingresso_da_venda(matricula_usuario)
                    elif opcao == 3:
                        self.comprar_ingresso_revenda(matricula_usuario)
                    elif opcao == 4:
                        self.listar_meus_ingressos_a_venda(matricula_usuario)
                    elif opcao == 0:
                        break
                except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
                    self.__view.mostra_mensagem(str(e))
                except Exception as e:
                    self.__view.mostra_mensagem(f"Erro Inesperado: {e}")
        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostra_mensagem(str(e))
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro Inesperado: {e}")

    def _transformar_ingresso_para_view(self, ingresso):
        try:
            if not ingresso:
                raise RegraDeNegocioException("Ingresso não pode ser nulo.")
            return {
                "id_ingresso": id(ingresso),
                "nome_evento": ingresso.evento.nome if ingresso.evento else "N/A",
                "nome_comprador": (
                    ingresso.comprador.nome if ingresso.comprador else "N/A"
                ),
                "data_compra": (
                    ingresso.data_compra.strftime("%d/%m/%Y")
                    if ingresso.data_compra
                    else "N/A"
                ),
                "preco": float(ingresso.preco) if ingresso.preco else 0.0,
                "nome_revendedor": (
                    ingresso.revendedor.nome if ingresso.revendedor else None
                ),
            }
        except AttributeError as e:
            raise RegraDeNegocioException(f"Erro ao processar dados do ingresso: {e}")
        except Exception as e:
            raise RegraDeNegocioException(f"Erro inesperado ao formatar ingresso: {e}")

    def comprar_ingresso_de_evento(self):
        try:
            matricula = self.__view.pega_matricula_comprador()
            if not matricula:
                return
            usuario = self.__usuario_controller.buscar_usuario_por_matricula(matricula)
            if not usuario:
                raise EntidadeNaoEncontradaException("Usuário não encontrado.")
            if not self.__evento_controller.get_eventos_lista():
                raise EntidadeNaoEncontradaException("Nenhum evento disponível.")
            evento = self.__evento_controller.selecionar_evento_gui()
            if not evento:
                return
            metodo = self.__view.pega_metodo_pagamento()
            if not metodo:
                return
            dados_compra = {
                "evento": evento.nome,
                "preco": evento.preco_entrada,
                "metodo_pagamento": metodo,
            }
            if not self.__view.confirma_compra_ingresso(dados_compra):
                return
            ingresso = usuario.comprar_ingresso(evento, evento.preco_entrada, metodo)
            if isinstance(ingresso, Ingresso):
                self.__ingresso_dao.add(ingresso)
                try:
                    from DAOs.usuario_dao import UsuarioDAO
                    from DAOs.evento_dao import EventoDAO

                    UsuarioDAO().update(usuario)
                    EventoDAO().update(evento)
                except Exception as e:
                    print(f"Aviso: falha ao atualizar usuario/evento: {e}")
            self.__view.mostra_mensagem("Ingresso comprado com sucesso!")
        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostra_mensagem(str(e))
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao comprar ingresso: {e}")

    def listar_meus_ingressos(self, matricula_usuario: str):
        try:
            if not matricula_usuario or not matricula_usuario.strip():
                raise RegraDeNegocioException(
                    "Matrícula do usuário não pode estar vazia."
                )
            usuario = self.__usuario_controller.buscar_usuario_por_matricula(
                matricula_usuario
            )
            if not usuario:
                raise EntidadeNaoEncontradaException("Usuário não encontrado.")
            ingressos_objetos = list(usuario.listar_ingressos())
            if not ingressos_objetos:
                try:
                    for ing in self.__ingresso_dao.get_all():
                        if getattr(ing, "comprador", None) == usuario:
                            ingressos_objetos.append(ing)
                except Exception as e:
                    print(f"Falha ao executar fallback de ingressos: {e}")
            if not ingressos_objetos:
                raise EntidadeNaoEncontradaException("Você não possui ingressos.")
            dados_para_view = []
            for ingresso in ingressos_objetos:
                try:
                    dados_para_view.append(
                        self._transformar_ingresso_para_view(ingresso)
                    )
                except (RegraDeNegocioException, EntidadeNaoEncontradaException) as e:
                    print(f"Erro ao processar ingresso: {e}")
                    continue
            if not dados_para_view:
                raise EntidadeNaoEncontradaException(
                    "Nenhum ingresso válido encontrado."
                )
            self.__view.mostra_ingressos(dados_para_view)
        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostra_mensagem(str(e))
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao listar ingressos: {e}")

    def colocar_ingresso_a_venda(self, matricula_usuario: str):
        try:
            if not matricula_usuario:
                return
            usuario = self.__usuario_controller.buscar_usuario_por_matricula(
                matricula_usuario
            )
            if not usuario:
                raise EntidadeNaoEncontradaException("Usuário não encontrado.")
            disponiveis = [i for i in usuario.listar_ingressos() if not i.revendedor]
            if not disponiveis:
                raise EntidadeNaoEncontradaException(
                    "Nenhum ingresso disponível para venda."
                )
            dados = [self._transformar_ingresso_para_view(i) for i in disponiveis]
            idx = self.__view.seleciona_ingresso(dados)
            if idx is None:
                return
            ingresso = disponiveis[idx]
            novo_preco = self.__view.pega_novo_preco_revenda()
            if novo_preco is None:
                return
            usuario.colocar_ingresso_a_venda(ingresso, novo_preco)
            self.__ingresso_dao.update(ingresso)
            self.__view.mostra_mensagem("Ingresso colocado à venda.")
        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostra_mensagem(str(e))
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro: {e}")

    def comprar_ingresso_revenda(self, matricula_comprador: str):
        try:
            if not matricula_comprador:
                return
            comprador = self.__usuario_controller.buscar_usuario_por_matricula(
                matricula_comprador
            )
            if not comprador:
                raise EntidadeNaoEncontradaException("Comprador não encontrado.")
            usuarios = self.__usuario_controller.listar_usuarios_objetos()
            ingressos_revenda = []
            for u in usuarios:
                for ing in getattr(u, "ingressos_comprados", []):
                    if ing.revendedor and ing.revendedor != comprador:
                        ingressos_revenda.append(ing)
            if not ingressos_revenda:
                raise EntidadeNaoEncontradaException("Sem ingressos de revenda.")
            dados = [self._transformar_ingresso_para_view(i) for i in ingressos_revenda]
            idx = self.__view.seleciona_ingresso_revenda(dados)
            if idx is None:
                return
            ingresso = ingressos_revenda[idx]
            metodo = self.__view.pega_metodo_pagamento()
            if not metodo:
                return
            dados_compra = {
                "evento": ingresso.evento.nome,
                "preco": ingresso.preco,
                "metodo_pagamento": metodo,
            }
            if not self.__view.confirma_compra_ingresso(dados_compra):
                return
            comprador.comprar_ingresso_revenda(ingresso)
            self.__ingresso_dao.update(ingresso)
            try:
                from DAOs.usuario_dao import UsuarioDAO

                UsuarioDAO().update(comprador)
            except Exception as e:
                print(f"Aviso: falha ao atualizar comprador na revenda: {e}")
            self.__view.mostra_mensagem("Revenda concluída.")
        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostra_mensagem(str(e))
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro: {e}")

    def remover_ingresso_da_venda(self, matricula_usuario: str):
        try:
            if not matricula_usuario:
                return
            usuario = self.__usuario_controller.buscar_usuario_por_matricula(
                matricula_usuario
            )
            if not usuario:
                raise EntidadeNaoEncontradaException("Usuário não encontrado.")
            a_venda = [i for i in usuario.listar_ingressos() if i.revendedor == usuario]
            if not a_venda:
                raise EntidadeNaoEncontradaException("Sem ingressos à venda.")
            dados = [self._transformar_ingresso_para_view(i) for i in a_venda]
            idx = self.__view.seleciona_ingresso(dados)
            if idx is None:
                return
            ingresso = a_venda[idx]
            usuario.remover_ingresso_da_venda(ingresso)
            self.__ingresso_dao.update(ingresso)
            self.__view.mostra_mensagem("Ingresso removido da venda.")
        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostra_mensagem(str(e))
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro: {e}")

    def listar_meus_ingressos_a_venda(self, matricula_usuario: str):
        try:
            if not matricula_usuario:
                return
            usuario = self.__usuario_controller.buscar_usuario_por_matricula(
                matricula_usuario
            )
            if not usuario:
                raise EntidadeNaoEncontradaException("Usuário não encontrado.")
            a_venda = [i for i in usuario.listar_ingressos() if i.revendedor == usuario]
            if not a_venda:
                raise EntidadeNaoEncontradaException("Sem ingressos à venda.")
            dados = [self._transformar_ingresso_para_view(i) for i in a_venda]
            self.__view.mostra_ingressos(dados)
        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostra_mensagem(str(e))
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro: {e}")

    def recarregar_ingressos(self):
        try:
            from DAOs.ingresso_dao import IngressoDAO

            self.__ingresso_dao = IngressoDAO()
        except Exception as e:
            self.__view.mostra_mensagem(f"Falha ao recarregar ingressos: {e}")
