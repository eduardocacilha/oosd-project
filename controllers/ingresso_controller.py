from views.ingresso_view import IngressoView
from controllers.usuario_controller import UsuarioController
from controllers.evento_controller import EventoController
import FreeSimpleGUI as sg
from exceptions.entidadeNaoEncontradaException import EntidadeNaoEncontradaException
from exceptions.regraDeNegocioException import RegraDeNegocioException


from models.usuario import Usuario
from models.evento import Evento
from models.ingresso import Ingresso

class IngressoController:

    def __init__(self, ingresso_view: IngressoView):
        try:
            self.__view = ingresso_view

            self.__usuario_controller: UsuarioController = None
            self.__evento_controller: EventoController = None
        except Exception as e:
            print(f"Erro ao inicializar IngressoController: {e}")

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

            usuario = self.__usuario_controller.buscar_usuario_por_matricula(matricula_usuario)
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
                "nome_comprador": ingresso.comprador.nome if ingresso.comprador else "N/A",
                "data_compra": ingresso.data_compra.strftime('%d/%m/%Y') if ingresso.data_compra else "N/A",
                "preco": float(ingresso.preco) if ingresso.preco else 0.0,
                "nome_revendedor": ingresso.revendedor.nome if ingresso.revendedor else None
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

            if not matricula.strip():
                raise RegraDeNegocioException("Matrícula não pode estar vazia.")

            usuario = self.__usuario_controller.buscar_usuario_por_matricula(matricula)
            if not usuario:
                raise EntidadeNaoEncontradaException("Usuário não encontrado.")

            eventos = self.__evento_controller.get_eventos_lista()
            if not eventos:
                raise EntidadeNaoEncontradaException("Nenhum evento disponível para compra.")

            evento_escolhido = self.__evento_controller.selecionar_evento_gui()

            if evento_escolhido is None:
                return

            metodo_pagamento = self.__view.pega_metodo_pagamento()
            if not metodo_pagamento:
                return

            dados_compra = {
                'evento': evento_escolhido.nome,
                'preco': evento_escolhido.preco_entrada,
                'metodo_pagamento': metodo_pagamento
            }

            if not self.__view.confirma_compra_ingresso(dados_compra):
                return

            ingresso = usuario.comprar_ingresso(evento_escolhido, evento_escolhido.preco_entrada, metodo_pagamento)
            self.__view.mostra_mensagem(f"Ingresso para '{evento_escolhido.nome}' comprado com sucesso por R$ {ingresso.preco:.2f}!")

        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostra_mensagem(str(e))
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao comprar ingresso: {e}")

    def listar_meus_ingressos(self, matricula_usuario: str):
        try:
            if not matricula_usuario or not matricula_usuario.strip():
                raise RegraDeNegocioException("Matrícula do usuário não pode estar vazia.")

            usuario = self.__usuario_controller.buscar_usuario_por_matricula(matricula_usuario)
            if not usuario:
                raise EntidadeNaoEncontradaException("Usuário não encontrado.")

            ingressos_objetos = usuario.listar_ingressos()

            if not ingressos_objetos:
                raise EntidadeNaoEncontradaException("Você não possui ingressos.")

            dados_para_view = []
            for ingresso in ingressos_objetos:
                try:
                    dados_para_view.append(self._transformar_ingresso_para_view(ingresso))
                except (RegraDeNegocioException, EntidadeNaoEncontradaException) as e:

                    print(f"Erro ao processar ingresso: {e}")
                    continue

            if not dados_para_view:
                raise EntidadeNaoEncontradaException("Nenhum ingresso válido encontrado.")

            self.__view.mostra_ingressos(dados_para_view)

        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostra_mensagem(str(e))
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao listar ingressos: {e}")

    def colocar_ingresso_a_venda(self, matricula_usuario: str):
        try:
            if not matricula_usuario or not matricula_usuario.strip():
                raise RegraDeNegocioException("Matrícula do usuário não pode estar vazia.")

            usuario = self.__usuario_controller.buscar_usuario_por_matricula(matricula_usuario)
            if not usuario:
                raise EntidadeNaoEncontradaException("Usuário não encontrado.")

            ingressos_disponiveis = [ing for ing in usuario.listar_ingressos() if not ing.revendedor]
            if not ingressos_disponiveis:
                raise EntidadeNaoEncontradaException("Você não possui ingressos disponíveis para colocar à venda.")

            dados_para_view = []
            for ingresso in ingressos_disponiveis:
                try:
                    dados_para_view.append(self._transformar_ingresso_para_view(ingresso))
                except (RegraDeNegocioException, EntidadeNaoEncontradaException) as e:
                    print(f"Erro ao processar ingresso: {e}")
                    continue

            if not dados_para_view:
                raise EntidadeNaoEncontradaException("Nenhum ingresso válido disponível para venda.")

            indice_escolhido = self.__view.seleciona_ingresso(dados_para_view)

            if indice_escolhido is not None:
                if indice_escolhido < 0 or indice_escolhido >= len(ingressos_disponiveis):
                    raise RegraDeNegocioException("Índice de ingresso inválido.")

                ingresso_selecionado = ingressos_disponiveis[indice_escolhido]
                novo_preco = self.__view.pega_novo_preco_revenda()

                if novo_preco is not None:
                    try:
                        usuario.colocar_ingresso_a_venda(ingresso_selecionado, novo_preco)
                        self.__view.mostra_mensagem("Ingresso colocado à venda com sucesso!")
                    except ValueError as e:
                        raise RegraDeNegocioException(f"Erro ao colocar ingresso à venda: {e}")
                else:

                    pass

        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostra_mensagem(str(e))
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao colocar ingresso à venda: {e}")

    def comprar_ingresso_revenda(self, matricula_comprador: str):
        try:
            if not matricula_comprador or not matricula_comprador.strip():
                raise RegraDeNegocioException("Matrícula do comprador não pode estar vazia.")

            comprador = self.__usuario_controller.buscar_usuario_por_matricula(matricula_comprador)
            if not comprador:
                raise EntidadeNaoEncontradaException("Usuário comprador não encontrado.")

            todos_usuarios = self.__usuario_controller.listar_usuarios_objetos()
            if not todos_usuarios:
                raise EntidadeNaoEncontradaException("Nenhum usuário cadastrado no sistema.")

            ingressos_revenda_obj = []
            for u in todos_usuarios:
                try:
                    for i in u.ingressos_comprados:
                        if i.revendedor and i.revendedor != comprador:
                            ingressos_revenda_obj.append(i)
                except AttributeError as e:

                    continue

            if not ingressos_revenda_obj:
                raise EntidadeNaoEncontradaException("Não há ingressos de revenda disponíveis no momento.")

            dados_para_view = []
            for ingresso in ingressos_revenda_obj:
                try:
                    dados_para_view.append(self._transformar_ingresso_para_view(ingresso))
                except (RegraDeNegocioException, EntidadeNaoEncontradaException) as e:
                    print(f"Erro ao processar ingresso de revenda: {e}")
                    continue

            if not dados_para_view:
                raise EntidadeNaoEncontradaException("Nenhum ingresso de revenda válido disponível.")

            indice_escolhido = self.__view.seleciona_ingresso_revenda(dados_para_view)

            if indice_escolhido is not None:
                if indice_escolhido < 0 or indice_escolhido >= len(ingressos_revenda_obj):
                    raise RegraDeNegocioException("Índice de ingresso inválido.")

                ingresso_a_comprar = ingressos_revenda_obj[indice_escolhido]
                revendedor = ingresso_a_comprar.revendedor

                metodo_pagamento = self.__view.pega_metodo_pagamento()
                if not metodo_pagamento:
                    return

                dados_compra = {
                    'evento': ingresso_a_comprar.evento.nome,
                    'preco': ingresso_a_comprar.preco,
                    'metodo_pagamento': metodo_pagamento
                }

                if not self.__view.confirma_compra_ingresso(dados_compra):
                    return


                comprador.comprar_ingresso_revenda(ingresso_a_comprar)
                self.__view.mostra_mensagem(f"Ingresso comprado de {revendedor.nome} com sucesso!")

        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostra_mensagem(str(e))
        except Exception as e:
            self.__view.mostra_mensagem(f"Ocorreu um erro na compra: {e}")

    def remover_ingresso_da_venda(self, matricula_usuario: str):

        try:
            if not matricula_usuario or not matricula_usuario.strip():
                raise RegraDeNegocioException("Matrícula do usuário não pode estar vazia.")

            usuario = self.__usuario_controller.buscar_usuario_por_matricula(matricula_usuario)
            if not usuario:
                raise EntidadeNaoEncontradaException("Usuário não encontrado.")

            ingressos_a_venda = [ing for ing in usuario.listar_ingressos() if ing.revendedor == usuario]
            if not ingressos_a_venda:
                raise EntidadeNaoEncontradaException("Você não possui ingressos à venda.")

            dados_para_view = []
            for ingresso in ingressos_a_venda:
                try:
                    dados_para_view.append(self._transformar_ingresso_para_view(ingresso))
                except (RegraDeNegocioException, EntidadeNaoEncontradaException) as e:
                    print(f"Erro ao processar ingresso: {e}")
                    continue

            if not dados_para_view:
                raise EntidadeNaoEncontradaException("Nenhum ingresso válido à venda.")

            indice_escolhido = self.__view.seleciona_ingresso(dados_para_view)

            if indice_escolhido is not None:
                if indice_escolhido < 0 or indice_escolhido >= len(ingressos_a_venda):
                    raise RegraDeNegocioException("Índice de ingresso inválido.")

                ingresso = ingressos_a_venda[indice_escolhido]
                try:
                    usuario.remover_ingresso_da_venda(ingresso)
                    self.__view.mostra_mensagem("Ingresso removido da venda com sucesso!")
                except ValueError as e:
                    raise RegraDeNegocioException(f"Erro ao remover ingresso da venda: {e}")

        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostra_mensagem(str(e))
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao remover ingresso da venda: {e}")

    def listar_meus_ingressos_a_venda(self, matricula_usuario: str):

        try:
            if not matricula_usuario or not matricula_usuario.strip():
                raise RegraDeNegocioException("Matrícula do usuário não pode estar vazia.")

            usuario = self.__usuario_controller.buscar_usuario_por_matricula(matricula_usuario)
            if not usuario:
                raise EntidadeNaoEncontradaException("Usuário não encontrado.")

            ingressos_a_venda = [ing for ing in usuario.listar_ingressos() if ing.revendedor == usuario]
            if not ingressos_a_venda:
                raise EntidadeNaoEncontradaException("Você não possui ingressos à venda.")

            dados_para_view = []
            for ingresso in ingressos_a_venda:
                try:
                    dados_para_view.append(self._transformar_ingresso_para_view(ingresso))
                except (RegraDeNegocioException, EntidadeNaoEncontradaException) as e:
                    print(f"Erro ao processar ingresso: {e}")
                    continue

            if not dados_para_view:
                raise EntidadeNaoEncontradaException("Nenhum ingresso válido à venda.")

            self.__view.mostra_ingressos(dados_para_view)

        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostra_mensagem(str(e))
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao listar ingressos à venda: {e}")
