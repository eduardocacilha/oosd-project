from typing import List, Dict
from datetime import datetime
import FreeSimpleGUI as sg
from views.venda_view import VendaView
from controllers.evento_controller import EventoController
from controllers.usuario_controller import UsuarioController
from controllers.produto_controller import ProdutoController
from DAOs.venda_dao import VendaDAO
from DAOs.produto_dao import ProdutoDAO
from models.venda import Venda
from models.item_venda import ItemVenda
from exceptions.regraDeNegocioException import RegraDeNegocioException
from exceptions.entidadeNaoEncontradaException import EntidadeNaoEncontradaException


class VendaController:
    def __init__(
        self,
        venda_view: VendaView,
        evento_controller: EventoController,
        usuario_controller: UsuarioController,
        produto_controller: ProdutoController,
    ):
        self.__view = venda_view
        self.__evento_controller = evento_controller
        self.__usuario_controller = usuario_controller
        self.__produto_controller = produto_controller
        self.__venda_dao = VendaDAO()
        self.__produto_dao = ProdutoDAO()

    def rodar_menu_venda(self):
        while True:
            opcao = self.__view.tela_opcoes()
            try:
                if opcao == 1:
                    self.nova_venda()
                elif opcao == 2:
                    self.listar_vendas()
                elif opcao == 0:
                    break
            except (RegraDeNegocioException, EntidadeNaoEncontradaException) as e:
                self.__view.mostrar_popup("Erro", str(e))
            except Exception as e:
                self.__view.mostrar_popup("Erro Inesperado", f"Falha: {e}")

    def _filtrar_produtos_evento(self, nome_evento: str):
        return [
            p
            for p in self.__produto_dao.get_all()
            if getattr(p, "evento_nome", None) == nome_evento and p.estoque > 0
        ]

    def nova_venda(self):
        evento = self.__evento_controller.selecionar_evento_gui()
        if not evento:
            return
        usuario = self.__usuario_controller.selecionar_usuario_gui()
        if not usuario:
            return
        metodo = self.__view.escolher_metodo_pagamento()
        if not metodo:
            return
        produtos = self._filtrar_produtos_evento(evento.nome)
        if not produtos:
            raise EntidadeNaoEncontradaException("Evento sem produtos disponíveis.")
        venda = Venda(usuario, evento, metodo)
        while True:
            produtos_atual = self._filtrar_produtos_evento(evento.nome)
            if not produtos_atual:
                break
            dados = [
                {"descricao": str(p), "preco": p.preco, "estoque": p.estoque}
                for p in produtos_atual
            ]
            idx = self.__view.selecionar_produto_para_venda(dados)
            if idx is None:
                break
            produto_escolhido = produtos_atual[idx]
            qtd = self.__view.pegar_quantidade()
            if qtd is None:
                continue
            venda.adicionar_item(produto_escolhido, qtd)
            from DAOs.produto_dao import ProdutoDAO

            ProdutoDAO().update(produto_escolhido)
            if not self.__view.confirmar_continuar():
                break
        if not venda.itens:
            self.__view.mostrar_popup("Aviso", "Venda sem itens cancelada.")
            return
        self.__venda_dao.add(venda)
        resumo_itens = [
            {
                "produto": it.produto.nome,
                "quantidade": it.quantidade,
                "subtotal": it.subtotal,
            }
            for it in venda.itens
        ]
        dados_resumo = {
            "id_venda": venda.id_venda,
            "cliente": usuario.nome,
            "evento": evento.nome,
            "metodo": metodo,
            "total": venda.total,
            "itens": resumo_itens,
            "data": venda.data_hora.strftime("%d/%m/%Y %H:%M"),
        }
        self.__view.mostrar_resumo_venda(dados_resumo)

    def listar_vendas(self):
        vendas = list(self.__venda_dao.get_all())
        lista = [
            {
                "id_venda": v.id_venda,
                "cliente": v.usuario.nome,
                "evento": v.evento.nome,
                "data": v.data_hora.strftime("%d/%m/%Y %H:%M"),
                "metodo": v.metodo_pagamento,
                "total": v.total,
            }
            for v in vendas
        ]
        self.__view.mostrar_lista_vendas(lista)

    def criar_venda_teste(
        self, usuario, evento, itens: List[tuple], metodo: str
    ) -> Venda:
        if not usuario or not evento:
            raise RegraDeNegocioException("Usuário e Evento são obrigatórios.")
        venda = Venda(usuario, evento, metodo)
        for produto, qtd in itens:
            venda.adicionar_item(produto, qtd)

            self.__produto_dao.update(produto)
        self.__venda_dao.add(venda)
        return venda

    def recarregar_vendas(self):
        try:
            from DAOs.venda_dao import VendaDAO

            self.__venda_dao = VendaDAO()
        except Exception as e:
            self.__view.mostrar_popup("Aviso", f"Falha ao recarregar vendas: {e}")
