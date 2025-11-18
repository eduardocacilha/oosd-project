from typing import Dict, List
import FreeSimpleGUI as sg
from exceptions.entidadeNaoEncontradaException import EntidadeNaoEncontradaException
from exceptions.regraDeNegocioException import RegraDeNegocioException

from views.produto_view import ProdutoView
from controllers.evento_controller import EventoController
from controllers.usuario_controller import UsuarioController

from models.camisa import Camisa
from models.copo import Copo
from models.venda import Venda
from models.item_venda import ItemVenda
from models.produto import Produto

class ProdutoController:


    def __init__(self, produto_view: ProdutoView):
        self.__view = produto_view
        self.__evento_controller: EventoController = None
        self.__usuario_controller: UsuarioController = None
        self.__produtos_por_evento: Dict[str, List[Produto]] = {}
        self.__next_produto_id = 1

    def set_usuario_controller(self, usuario_controller: UsuarioController):
        self.__usuario_controller = usuario_controller

    def set_evento_controller(self, evento_controller: EventoController):
        self.__evento_controller = evento_controller

    def rodar_menu_produto(self):

        while True:
            opcao = self.__view.tela_opcoes()

            try:
                if opcao == 1:
                    self.adicionar_produto_evento()

                elif opcao == 2:
                    self.alterar_produto()

                elif opcao == 3:
                    self.listar_produtos_evento()

                elif opcao == 4:
                    self.excluir_produto()

                elif opcao == 5:
                    self.registrar_venda()

                elif opcao == 6:
                    self.relatorio_vendas()

                elif opcao == 0:
                    break

            except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
                self.__view.mostrar_popup("Erro", str(e))
            except Exception as e:
                self.__view.mostrar_popup("Erro Inesperado", f"Ocorreu um erro: {e}")


    def _gerar_id_produto(self) -> int:
        current_id = self.__next_produto_id
        self.__next_produto_id += 1
        return current_id

    def adicionar_produto_evento(self):

        try:
            evento_escolhido = self.__evento_controller.selecionar_evento_gui()
            if evento_escolhido is None:
                return

            tipo = self.__view.escolher_tipo_produto()
            if tipo == 0:
                return

            dados = None
            if tipo == 1:
                dados = self.__view.pega_dados_camisa()
            elif tipo == 2:
                dados = self.__view.pega_dados_copo()
            else:
                raise RegraDeNegocioException("Tipo de produto inválido.")

            if dados is not None:
                produto = None
                if tipo == 1:
                    produto = Camisa(
                        nome=dados["nome"], preco=dados["preco"], estoque=dados["estoque"],
                        tamanho=dados["tamanho"], cor=dados["cor"]
                    )
                elif tipo == 2:
                    produto = Copo(
                        nome=dados["nome"], preco=dados["preco"], estoque=dados["estoque"],
                        capacidade_ml=dados["capacidade_ml"], material=dados["material"]
                    )

                nome_evento = evento_escolhido.nome
                if nome_evento not in self.__produtos_por_evento:
                    self.__produtos_por_evento[nome_evento] = []

                self.__produtos_por_evento[nome_evento].append(produto)
                self.__view.mostrar_popup("Sucesso", f"Produto '{produto.nome}' adicionado ao evento '{nome_evento}'!")

        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostrar_popup("Erro", str(e))
        except Exception as e:
            self.__view.mostrar_popup("Erro", f"Erro inesperado ao adicionar produto: {str(e)}")

    def listar_produtos_evento(self):
        try:
            evento_escolhido = self.__evento_controller.selecionar_evento_gui()
            if evento_escolhido is None:
                return

            nome_evento = evento_escolhido.nome
            produtos = self.__produtos_por_evento.get(nome_evento, [])

            if not produtos:
                raise EntidadeNaoEncontradaException("Nenhum produto cadastrado para este evento.")

            dados_produtos = []
            for produto in produtos:
                dados_produtos.append({
                    "descricao": str(produto),
                    "preco": produto.preco,
                    "estoque": produto.estoque
                })

            self.__view.mostra_produtos(dados_produtos)

        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostrar_popup("Erro", str(e))
        except Exception as e:
            self.__view.mostrar_popup("Erro", f"Erro inesperado ao listar produtos: {str(e)}")

    def registrar_venda(self):

        try:
            evento_escolhido = self.__evento_controller.selecionar_evento_gui()
            if evento_escolhido is None: return

            nome_evento = evento_escolhido.nome
            produtos = self.__produtos_por_evento.get(nome_evento, [])
            if not produtos:
                raise EntidadeNaoEncontradaException("Nenhum produto cadastrado para este evento.")

            matricula = self.__usuario_controller.pega_matricula_usuario_gui()
            if not matricula: return

            usuario = self.__usuario_controller.buscar_usuario_por_matricula(matricula)
            if not usuario:
                raise EntidadeNaoEncontradaException("Usuário não encontrado.")

            metodo_pagamento = self.__view.pega_metodo_pagamento()
            if not metodo_pagamento: return

            venda = None

            while True:

                dados_produtos = []
                produtos_com_estoque = []
                for produto in produtos:
                    if produto.estoque > 0:
                        dados_produtos.append({
                            "descricao": str(produto),
                            "preco": produto.preco,
                            "estoque": produto.estoque
                        })
                        produtos_com_estoque.append(produto)

                if not dados_produtos:
                    raise EntidadeNaoEncontradaException("Nenhum produto com estoque disponível.")

                indice_produto = self.__view.seleciona_produto(dados_produtos)
                if indice_produto is None:
                    break

                produto_escolhido = produtos_com_estoque[indice_produto]

                try:
                    quantidade = self.__view.pega_quantidade_venda()
                    if quantidade is None:
                        continue

                    if venda is None:
                        venda = Venda(usuario, evento_escolhido, metodo_pagamento)

                    venda.adicionar_item(produto_escolhido, quantidade)

                    self.__view.mostrar_popup("Sucesso", f"Item adicionado: {quantidade}x {produto_escolhido.nome}")

                    if not self.__view.confirma_continuar_comprando():
                        break

                except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
                    self.__view.mostrar_popup("Erro", str(e))

            if venda is not None and venda.itens:

                evento_escolhido.registrar_venda(venda)

                dados_venda = {
                    "id_venda": venda.id_venda,
                    "cliente": usuario.nome,
                    "evento": evento_escolhido.nome,
                    "total": venda.total,
                    "metodo": metodo_pagamento
                }
                self.__view.mostra_venda_realizada(dados_venda)
            else:
                self.__view.mostrar_popup("Aviso", "Venda cancelada pois nenhum item foi adicionado.")

        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostrar_popup("Erro", str(e))
        except Exception as e:
            self.__view.mostrar_popup("Erro", f"Erro inesperado ao registrar venda: {str(e)}")

    def relatorio_vendas(self):

        try:
            vendas = Venda.get_all()

            if not vendas:
                raise EntidadeNaoEncontradaException("Nenhuma venda encontrada.")

            dados_vendas = []

            for venda in vendas:
                dados_vendas.append({
                    "id_venda": venda.id_venda,
                    "cliente": venda.usuario.nome,
                    "evento": venda.evento.nome,
                    "data": venda.data_hora.strftime('%d/%m/%Y %H:%M'),
                    "metodo": venda.metodo_pagamento,
                    "total": venda.total
                })

            self.__view.mostra_relatorio_vendas(dados_vendas)

        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostrar_popup("Erro", str(e))
        except Exception as e:
            self.__view.mostrar_popup("Erro", f"Erro inesperado ao gerar relatório: {str(e)}")

    def alterar_produto(self):

        try:

            evento_escolhido = self.__evento_controller.selecionar_evento_gui()
            if evento_escolhido is None: return

            nome_evento = evento_escolhido.nome
            produtos = self.__produtos_por_evento.get(nome_evento, [])
            if not produtos:
                raise EntidadeNaoEncontradaException("Nenhum produto cadastrado para este evento.")


            dados_produtos = []
            for produto in produtos:
                dados_produtos.append({
                    "descricao": str(produto),
                    "preco": produto.preco,
                    "estoque": produto.estoque
                })

            indice_produto = self.__view.seleciona_produto(dados_produtos)
            if indice_produto is None:
                return

            produto_escolhido = produtos[indice_produto]


            novos_dados = None
            if isinstance(produto_escolhido, Camisa):
                novos_dados = self.__view.pega_dados_camisa()
            elif isinstance(produto_escolhido, Copo):
                novos_dados = self.__view.pega_dados_copo()

            if novos_dados is None:
                return


            produto_escolhido.nome = novos_dados["nome"]
            produto_escolhido.preco = novos_dados["preco"]
            produto_escolhido.estoque = novos_dados["estoque"]
            if isinstance(produto_escolhido, Camisa):
                produto_escolhido.tamanho = novos_dados["tamanho"]
                produto_escolhido.cor = novos_dados["cor"]
            elif isinstance(produto_escolhido, Copo):
                produto_escolhido.capacidade_ml = novos_dados["capacidade_ml"]
                produto_escolhido.material = novos_dados["material"]

            self.__view.mostrar_popup("Sucesso", "Produto alterado com sucesso!")

        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostrar_popup("Erro", str(e))
        except Exception as e:
            self.__view.mostrar_popup("Erro", f"Erro inesperado ao alterar produto: {str(e)}")

    def excluir_produto(self):

        try:

            evento_escolhido = self.__evento_controller.selecionar_evento_gui()
            if evento_escolhido is None: return

            nome_evento = evento_escolhido.nome
            produtos = self.__produtos_por_evento.get(nome_evento, [])
            if not produtos:
                raise EntidadeNaoEncontradaException("Nenhum produto cadastrado para este evento.")


            dados_produtos = []
            for produto in produtos:
                dados_produtos.append({
                    "descricao": str(produto),
                    "preco": produto.preco,
                    "estoque": produto.estoque
                })

            indice_produto = self.__view.seleciona_produto(dados_produtos)
            if indice_produto is None:
                return

            produto_escolhido = produtos[indice_produto]


            resposta = sg.popup_yes_no(
                f"Deseja realmente excluir este produto?\n\n{str(produto_escolhido)}",
                title="Confirmar Exclusão",
                keep_on_top=True
            )

            if resposta == 'Yes':

                produtos.remove(produto_escolhido)
                self.__view.mostrar_popup("Sucesso", "Produto excluído com sucesso!")
            else:
                self.__view.mostrar_popup("Aviso", "Exclusão cancelada.")

        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostrar_popup("Erro", str(e))
        except Exception as e:
            self.__view.mostrar_popup("Erro", f"Erro inesperado ao excluir produto: {str(e)}")

    def get_produtos_por_evento_lista(self) -> Dict[str, List[Produto]]:
        return self.__produtos_por_evento
