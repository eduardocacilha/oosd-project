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
from models.produto import Produto
from DAOs.produto_dao import ProdutoDAO
from DAOs.venda_dao import VendaDAO


class ProdutoController:

    def __init__(self, produto_view: ProdutoView):
        self.__view = produto_view
        self.__evento_controller: EventoController = None
        self.__usuario_controller: UsuarioController = None
        self.__produto_dao = ProdutoDAO()
        self.__venda_dao = VendaDAO()

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
                elif opcao == 0:
                    break
            except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
                self.__view.mostrar_popup("Erro", str(e))
            except Exception as e:
                self.__view.mostrar_popup("Erro Inesperado", f"Ocorreu um erro: {e}")

    def _produtos_do_evento(self, nome_evento: str) -> List[Produto]:
        return [
            p
            for p in self.__produto_dao.get_all()
            if getattr(p, "evento_nome", None) == nome_evento
        ]

    def adicionar_produto_evento(self):
        try:
            evento = self.__evento_controller.selecionar_evento_gui()
            if not evento:
                return
            tipo = self.__view.escolher_tipo_produto()
            if tipo == 0:
                return
            if tipo == 1:
                dados = self.__view.pega_dados_camisa()
                if not dados:
                    return
                produto = Camisa(
                    nome=dados["nome"],
                    preco=dados["preco"],
                    estoque=dados["estoque"],
                    tamanho=dados["tamanho"],
                    cor=dados["cor"],
                )
            elif tipo == 2:
                dados = self.__view.pega_dados_copo()
                if not dados:
                    return
                produto = Copo(
                    nome=dados["nome"],
                    preco=dados["preco"],
                    estoque=dados["estoque"],
                    capacidade_ml=dados["capacidade_ml"],
                    material=dados["material"],
                )
            else:
                raise RegraDeNegocioException("Tipo inválido.")
            setattr(produto, "evento_nome", evento.nome)
            self.__produto_dao.add(produto)
            self.__view.mostrar_popup(
                "Sucesso",
                f"Produto '{produto.nome}' adicionado ao evento '{evento.nome}'.",
            )
        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostrar_popup("Erro", str(e))
        except Exception as e:
            self.__view.mostrar_popup("Erro", f"Falha ao adicionar produto: {e}")

    def listar_produtos_evento(self):
        try:
            evento = self.__evento_controller.selecionar_evento_gui()
            if not evento:
                return
            produtos = self._produtos_do_evento(evento.nome)
            if not produtos:
                raise EntidadeNaoEncontradaException("Nenhum produto para este evento.")
            dados = [
                {"descricao": str(p), "preco": p.preco, "estoque": p.estoque}
                for p in produtos
            ]
            self.__view.mostra_produtos(dados)
        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostrar_popup("Erro", str(e))
        except Exception as e:
            self.__view.mostrar_popup("Erro", f"Falha ao listar produtos: {e}")

    def alterar_produto(self):
        try:
            evento = self.__evento_controller.selecionar_evento_gui()
            if not evento:
                return
            produtos = self._produtos_do_evento(evento.nome)
            if not produtos:
                raise EntidadeNaoEncontradaException("Nenhum produto.")
            dados = [
                {"descricao": str(p), "preco": p.preco, "estoque": p.estoque}
                for p in produtos
            ]
            idx = self.__view.seleciona_produto(dados)
            if idx is None:
                return
            produto = produtos[idx]
            if isinstance(produto, Camisa):
                novos = self.__view.pega_dados_camisa()
            elif isinstance(produto, Copo):
                novos = self.__view.pega_dados_copo()
            else:
                novos = None
            if not novos:
                return
            old_nome = produto.nome
            produto.nome = novos["nome"]
            produto.preco = novos["preco"]
            produto.estoque = novos["estoque"]
            if isinstance(produto, Camisa):
                produto.tamanho = novos["tamanho"]
                produto.cor = novos["cor"]
            elif isinstance(produto, Copo):
                produto.capacidade_ml = novos["capacidade_ml"]
                produto.material = novos["material"]
            if old_nome != produto.nome:
                self.__produto_dao.remove(old_nome)
                self.__produto_dao.add(produto)
            else:
                self.__produto_dao.update(produto)
            self.__view.mostrar_popup("Sucesso", "Produto alterado.")
        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostrar_popup("Erro", str(e))
        except Exception as e:
            self.__view.mostrar_popup("Erro", f"Falha ao alterar: {e}")

    def excluir_produto(self):
        try:
            evento = self.__evento_controller.selecionar_evento_gui()
            if not evento:
                return
            produtos = self._produtos_do_evento(evento.nome)
            if not produtos:
                raise EntidadeNaoEncontradaException("Nenhum produto.")
            dados = [
                {"descricao": str(p), "preco": p.preco, "estoque": p.estoque}
                for p in produtos
            ]
            idx = self.__view.seleciona_produto(dados)
            if idx is None:
                return
            produto = produtos[idx]
            if (
                sg.popup_yes_no(
                    f"Excluir produto?\n\n{str(produto)}", title="Confirmar"
                )
                == "Yes"
            ):
                self.__produto_dao.remove(produto.nome)
                self.__view.mostrar_popup("Sucesso", "Produto excluído.")
            else:
                self.__view.mostrar_popup("Aviso", "Operação cancelada.")
        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostrar_popup("Erro", str(e))
        except Exception as e:
            self.__view.mostrar_popup("Erro", f"Falha ao excluir: {e}")

    def get_produtos_por_evento_lista(self) -> Dict[str, List[Produto]]:
        agrupado: Dict[str, List[Produto]] = {}
        for p in self.__produto_dao.get_all():
            ev = getattr(p, "evento_nome", None)
            if ev:
                agrupado.setdefault(ev, []).append(p)
        return agrupado

    def recarregar_produtos(self):
        try:
            from DAOs.produto_dao import ProdutoDAO

            self.__produto_dao = ProdutoDAO()
        except Exception as e:
            self.__view.mostrar_popup("Aviso", f"Falha ao recarregar produtos: {e}")
