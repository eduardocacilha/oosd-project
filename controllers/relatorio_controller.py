from views.relatorio_view import RelatorioView
from controllers.evento_controller import EventoController
from controllers.usuario_controller import UsuarioController
from controllers.produto_controller import ProdutoController
from typing import List
from collections import defaultdict
import FreeSimpleGUI as sg
from exceptions.entidadeNaoEncontradaException import EntidadeNaoEncontradaException
from exceptions.regraDeNegocioException import RegraDeNegocioException
from DAOs.ingresso_dao import IngressoDAO
from DAOs.venda_dao import VendaDAO


class RelatorioController:

    def __init__(
        self,
        relatorio_view: RelatorioView,
        evento_controller: EventoController,
        usuario_controller: UsuarioController,
        produto_controller: ProdutoController,
    ):
        self.__view = relatorio_view
        self.__evento_controller = evento_controller
        self.__usuario_controller = usuario_controller
        self.__produto_controller = produto_controller

    def rodar_menu_relatorios(self):
        while True:
            opcao = self.__view.tela_opcoes()
            try:
                if opcao == 1:
                    self.rodar_menu_eventos()
                elif opcao == 2:
                    self.rodar_menu_produtos()
                elif opcao == 3:
                    self.rodar_menu_vendas()
                elif opcao == 4:
                    self.rodar_menu_usuarios()
                elif opcao == 0:
                    break
            except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
                self.__view.mostra_mensagem(str(e))
            except Exception as e:
                self.__view.mostra_mensagem(f"Erro Inesperado: {e}")

    def relatorio_eventos_preco(self):
        try:
            eventos = self.__evento_controller.get_eventos_lista()
            if not eventos:
                raise EntidadeNaoEncontradaException("Nenhum evento cadastrado.")
            eventos_ordenados = sorted(eventos, key=lambda e: e.preco_entrada)
            mais_baratos = []
            mais_caros = []
            for evento in eventos_ordenados[:5]:
                mais_baratos.append(
                    {
                        "nome": evento.nome,
                        "preco": evento.preco_entrada,
                        "data": evento.data.strftime("%d/%m/%Y"),
                        "local": evento.local,
                    }
                )
            for evento in reversed(eventos_ordenados[-5:]):
                mais_caros.append(
                    {
                        "nome": evento.nome,
                        "preco": evento.preco_entrada,
                        "data": evento.data.strftime("%d/%m/%Y"),
                        "local": evento.local,
                    }
                )
            self.__view.mostra_eventos_preco(mais_caros, mais_baratos)
        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostra_mensagem(str(e))
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao gerar relatório: {str(e)}")

    def relatorio_eventos_avaliacao(self):
        try:
            eventos = self.__evento_controller.get_eventos_lista()
            if not eventos:
                raise EntidadeNaoEncontradaException("Nenhum evento cadastrado.")
            eventos_com_nota = []
            for evento in eventos:
                if evento.feedbacks:
                    nota_media = sum((f.nota for f in evento.feedbacks)) / len(
                        evento.feedbacks
                    )
                    eventos_com_nota.append(
                        {
                            "nome": evento.nome,
                            "nota_media": nota_media,
                            "total_avaliacoes": len(evento.feedbacks),
                            "data": evento.data.strftime("%d/%m/%Y"),
                            "local": evento.local,
                            "preco": evento.preco_entrada,
                        }
                    )
            eventos_com_nota.sort(key=lambda e: e["nota_media"], reverse=True)
            self.__view.mostra_eventos_avaliacao(eventos_com_nota)
        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostra_mensagem(str(e))
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao gerar relatório: {str(e)}")

    def relatorio_eventos_vendas(self):
        try:
            eventos = self.__evento_controller.get_eventos_lista()
            if not eventos:
                raise EntidadeNaoEncontradaException("Nenhum evento cadastrado.")
            ingresso_dao = IngressoDAO()
            vendas_por_evento = {}
            for ingresso in ingresso_dao.get_all():
                nome_evento = ingresso.evento.nome
                if nome_evento not in vendas_por_evento:
                    vendas_por_evento[nome_evento] = {
                        "ingressos_vendidos": 0,
                        "faturamento": 0,
                        "evento": ingresso.evento,
                    }
                vendas_por_evento[nome_evento]["ingressos_vendidos"] += 1
                vendas_por_evento[nome_evento]["faturamento"] += ingresso.preco
            ordenado = []
            for nome, dados in vendas_por_evento.items():
                ev = dados["evento"]
                ordenado.append(
                    {
                        "nome": nome,
                        "ingressos_vendidos": dados["ingressos_vendidos"],
                        "faturamento": dados["faturamento"],
                        "data": ev.data.strftime("%d/%m/%Y"),
                        "local": ev.local,
                    }
                )
            ordenado.sort(key=lambda e: e["ingressos_vendidos"], reverse=True)
            self.__view.mostra_eventos_vendas(ordenado)
        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostra_mensagem(str(e))
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao gerar relatório: {e}")

    def relatorio_produtos_preco(self):
        try:
            todos_produtos = []
            produtos_por_evento = (
                self.__produto_controller.get_produtos_por_evento_lista()
            )
            for nome_evento, produtos in produtos_por_evento.items():
                for produto in produtos:
                    todos_produtos.append(
                        {
                            "nome": produto.nome,
                            "preco": produto.preco,
                            "estoque": produto.estoque,
                            "evento": nome_evento,
                        }
                    )
            if not todos_produtos:
                raise EntidadeNaoEncontradaException("Nenhum produto cadastrado.")
            produtos_ordenados = sorted(todos_produtos, key=lambda p: p["preco"])
            mais_baratos = produtos_ordenados[:5]
            mais_caros = list(reversed(produtos_ordenados[-5:]))
            self.__view.mostra_produtos_preco(mais_caros, mais_baratos)
        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostra_mensagem(str(e))
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao gerar relatório: {str(e)}")

    def relatorio_produtos_vendidos(self):
        try:
            venda_dao = VendaDAO()
            vendas_por_produto = defaultdict(
                lambda: {"quantidade": 0, "faturamento": 0, "produto": None}
            )
            for venda in venda_dao.get_all():
                for item in venda.itens:
                    nome = item.produto.nome
                    vendas_por_produto[nome]["quantidade"] += item.quantidade
                    vendas_por_produto[nome]["faturamento"] += item.subtotal
                    vendas_por_produto[nome]["produto"] = item.produto
            if not vendas_por_produto:
                raise EntidadeNaoEncontradaException("Nenhuma venda de produto.")
            ordenado = []
            for nome, dados in vendas_por_produto.items():
                produto = dados["produto"]
                ordenado.append(
                    {
                        "nome": nome,
                        "quantidade_vendida": dados["quantidade"],
                        "faturamento": dados["faturamento"],
                        "estoque": produto.estoque if produto else 0,
                    }
                )
            ordenado.sort(key=lambda p: p["quantidade_vendida"], reverse=True)
            self.__view.mostra_produtos_vendidos(ordenado)
        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostra_mensagem(str(e))
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao gerar relatório: {e}")

    def relatorio_produtos_faturamento(self):
        try:
            venda_dao = VendaDAO()
            vendas_por_produto = defaultdict(
                lambda: {"quantidade": 0, "faturamento": 0, "produto": None}
            )
            for venda in venda_dao.get_all():
                for item in venda.itens:
                    nome = item.produto.nome
                    vendas_por_produto[nome]["quantidade"] += item.quantidade
                    vendas_por_produto[nome]["faturamento"] += item.subtotal
                    vendas_por_produto[nome]["produto"] = item.produto
            if not vendas_por_produto:
                raise EntidadeNaoEncontradaException("Nenhuma venda de produto.")
            ordenado = []
            for nome, dados in vendas_por_produto.items():
                produto = dados["produto"]
                ordenado.append(
                    {
                        "nome": nome,
                        "quantidade_vendida": dados["quantidade"],
                        "faturamento": dados["faturamento"],
                        "preco": produto.preco if produto else 0,
                    }
                )
            ordenado.sort(key=lambda p: p["faturamento"], reverse=True)
            self.__view.mostra_produtos_faturamento(ordenado)
        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostra_mensagem(str(e))
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao gerar relatório: {e}")

    def relatorio_estoque(self):
        try:
            todos_produtos = []
            produtos_por_evento = (
                self.__produto_controller.get_produtos_por_evento_lista()
            )
            for nome_evento, produtos in produtos_por_evento.items():
                for produto in produtos:
                    todos_produtos.append(
                        {
                            "nome": produto.nome,
                            "estoque": produto.estoque,
                            "preco": produto.preco,
                            "evento": nome_evento,
                        }
                    )
            if not todos_produtos:
                raise EntidadeNaoEncontradaException("Nenhum produto cadastrado.")
            todos_produtos.sort(key=lambda p: p["estoque"])
            self.__view.mostra_relatorio_estoque(todos_produtos)
        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostra_mensagem(str(e))
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao gerar relatório: {str(e)}")

    def relatorio_vendas_pagamento(self):
        try:
            venda_dao = VendaDAO()
            ingresso_dao = IngressoDAO()
            vendas_por_metodo = defaultdict(float)
            for venda in venda_dao.get_all():
                vendas_por_metodo[venda.metodo_pagamento] += venda.total
            for ingresso in ingresso_dao.get_all():
                if getattr(ingresso, "metodo_pagamento", None):
                    vendas_por_metodo[ingresso.metodo_pagamento] += ingresso.preco
            if not vendas_por_metodo:
                raise EntidadeNaoEncontradaException("Nenhuma venda.")
            ordenado = dict(
                sorted(vendas_por_metodo.items(), key=lambda x: x[1], reverse=True)
            )
            self.__view.mostra_vendas_pagamento(ordenado)
        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostra_mensagem(str(e))
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao gerar relatório: {e}")

    def relatorio_faturamento_evento(self):
        try:
            ingresso_dao = IngressoDAO()
            venda_dao = VendaDAO()
            fat_por_evento = defaultdict(
                lambda: {"ingressos": 0, "produtos": 0, "evento": None}
            )
            for ing in ingresso_dao.get_all():
                nome = ing.evento.nome
                fat_por_evento[nome]["ingressos"] += ing.preco
                fat_por_evento[nome]["evento"] = ing.evento
            for venda in venda_dao.get_all():
                nome = venda.evento.nome
                fat_por_evento[nome]["produtos"] += venda.total
                fat_por_evento[nome]["evento"] = venda.evento
            if not fat_por_evento:
                raise EntidadeNaoEncontradaException("Sem vendas.")
            ordenado = []
            for nome, dados in fat_por_evento.items():
                total = dados["ingressos"] + dados["produtos"]
                ordenado.append(
                    {
                        "nome": nome,
                        "faturamento_ingressos": dados["ingressos"],
                        "faturamento_produtos": dados["produtos"],
                        "faturamento_total": total,
                    }
                )
            ordenado.sort(key=lambda e: e["faturamento_total"], reverse=True)
            self.__view.mostra_faturamento_evento(ordenado)
        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostra_mensagem(str(e))
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao gerar relatório: {e}")


    def relatorio_geral_sistema(self):
        try:
            ingresso_dao = IngressoDAO()
            venda_dao = VendaDAO()
            total_usuarios = len(self.__usuario_controller.listar_usuarios_objetos())
            total_eventos = len(self.__evento_controller.get_eventos_lista())
            produtos_por_evento = (
                self.__produto_controller.get_produtos_por_evento_lista()
            )
            total_produtos = sum(len(v) for v in produtos_por_evento.values())
            ingressos = list(ingresso_dao.get_all())
            vendas = list(venda_dao.get_all())
            total_ingressos_vendidos = len(ingressos)
            total_produtos_vendidos = sum(
                sum(item.quantidade for item in v.itens) for v in vendas
            )
            faturamento_ingressos = sum(i.preco for i in ingressos)
            faturamento_produtos = sum(v.total for v in vendas)
            faturamento_total = faturamento_ingressos + faturamento_produtos
            vendas_eventos = defaultdict(int)
            for ing in ingressos:
                vendas_eventos[ing.evento.nome] += 1
            evento_mais_popular = (
                max(vendas_eventos, key=vendas_eventos.get) if vendas_eventos else ""
            )
            vendas_produtos = defaultdict(int)
            for v in vendas:
                for item in v.itens:
                    vendas_produtos[item.produto.nome] += item.quantidade
            produto_mais_vendido = (
                max(vendas_produtos, key=vendas_produtos.get) if vendas_produtos else ""
            )
            gastos_clientes = defaultdict(float)
            for ing in ingressos:
                gastos_clientes[ing.comprador.nome] += ing.preco
            for v in vendas:
                gastos_clientes[v.usuario.nome] += v.total
            melhor_cliente = (
                max(gastos_clientes, key=gastos_clientes.get) if gastos_clientes else ""
            )
            dados = {
                "total_usuarios": total_usuarios,
                "total_eventos": total_eventos,
                "total_produtos": total_produtos,
                "total_ingressos_vendidos": total_ingressos_vendidos,
                "total_produtos_vendidos": total_produtos_vendidos,
                "faturamento_ingressos": faturamento_ingressos,
                "faturamento_produtos": faturamento_produtos,
                "faturamento_total": faturamento_total,
                "evento_mais_popular": evento_mais_popular,
                "produto_mais_vendido": produto_mais_vendido,
                "melhor_cliente": melhor_cliente,
            }
            self.__view.mostra_relatorio_geral(dados)
        except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
            self.__view.mostra_mensagem(str(e))
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao gerar relatório: {e}")

    def rodar_menu_eventos(self):
        while True:
            try:
                opcao = self.__view.tela_opcoes_eventos()
                if opcao == 1:
                    self.relatorio_eventos_preco()
                elif opcao == 2:
                    self.relatorio_eventos_avaliacao()
                elif opcao == 3:
                    self.relatorio_eventos_vendas()
                elif opcao == 0:
                    break
                else:
                    self.__view.mostra_mensagem("Opcao invalida.")
            except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
                self.__view.mostra_mensagem(str(e))
            except Exception as e:
                self.__view.mostra_mensagem(f"Erro inesperado: {e}")

    def rodar_menu_produtos(self):
        while True:
            try:
                opcao = self.__view.tela_opcoes_produtos()
                if opcao == 1:
                    self.relatorio_produtos_preco()
                elif opcao == 2:
                    self.relatorio_produtos_vendidos()
                elif opcao == 3:
                    self.relatorio_produtos_faturamento()
                elif opcao == 4:
                    self.relatorio_estoque()
                elif opcao == 0:
                    break
                else:
                    self.__view.mostra_mensagem("Opcao invalida.")
            except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
                self.__view.mostra_mensagem(str(e))
            except Exception as e:
                self.__view.mostra_mensagem(f"Erro inesperado: {e}")

    def rodar_menu_vendas(self):
        while True:
            try:
                opcao = self.__view.tela_opcoes_vendas()
                if opcao == 1:
                    self.relatorio_vendas_pagamento()
                elif opcao == 2:
                    self.relatorio_faturamento_evento()
                elif opcao == 4:
                    self.relatorio_top_clientes()
                elif opcao == 0:
                    break
                else:
                    self.__view.mostra_mensagem("Opcao invalida.")
            except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
                self.__view.mostra_mensagem(str(e))
            except Exception as e:
                self.__view.mostra_mensagem(f"Erro inesperado: {e}")

    def rodar_menu_usuarios(self):
        while True:
            try:
                opcao = self.__view.tela_opcoes_usuarios()
                if opcao == 1:
                    self.relatorio_top_clientes()
                elif opcao == 0:
                    break
                else:
                    self.__view.mostra_mensagem("Opcao invalida.")
            except (EntidadeNaoEncontradaException, RegraDeNegocioException) as e:
                self.__view.mostra_mensagem(str(e))
            except Exception as e:
                self.__view.mostra_mensagem(f"Erro inesperado: {e}")
