from views.relatorio_view import RelatorioView
from controllers.evento_controller import EventoController
from controllers.usuario_controller import UsuarioController
from controllers.produto_controller import ProdutoController
from models.usuario import Usuario
from models.evento import Evento
from models.venda import Venda
from models.ingresso import Ingresso
from typing import List
from collections import defaultdict
import FreeSimpleGUI as sg


class RelatorioController:
    def __init__(self, relatorio_view: RelatorioView, evento_controller: EventoController, 
                 usuario_controller: UsuarioController, produto_controller: ProdutoController):
        self.__view = relatorio_view
        self.__evento_controller = evento_controller
        self.__usuario_controller = usuario_controller
        self.__produto_controller = produto_controller

    # Este é o método que o MainController chama (evento '5')
    def rodar_menu_relatorios(self):
        
        while True:
            # 1. Chama a View, que abre a janela de menu e retorna o NÚMERO (int)
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
                    break # Volta para o MainController
            
            except Exception as e:
                self.__view.mostra_mensagem(f"Erro Inesperado: {e}")
                

    def relatorio_eventos_preco(self):
        
        try:
            # ATENÇÃO: Acessar '__eventos' diretamente viola o encapsulamento.
            # O ideal é usar o 'get_eventos_lista()' que criamos no EventoController.
            eventos = self.__evento_controller.get_eventos_lista()
            if not eventos:
                self.__view.mostra_mensagem("Nenhum evento cadastrado.")
                return

            eventos_ordenados = sorted(eventos, key=lambda e: e.preco_entrada)
            
            mais_baratos = []
            mais_caros = []
            
            for evento in eventos_ordenados[:5]:
                mais_baratos.append({
                    'nome': evento.nome,
                    'preco': evento.preco_entrada,
                    'data': evento.data.strftime('%d/%m/%Y'),
                    'local': evento.local
                })
            
            for evento in reversed(eventos_ordenados[-5:]):
                mais_caros.append({
                    'nome': evento.nome,
                    'preco': evento.preco_entrada,
                    'data': evento.data.strftime('%d/%m/%Y'),
                    'local': evento.local
                })
            
            self.__view.mostra_eventos_preco(mais_caros, mais_baratos)
            
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao gerar relatório: {str(e)}")

    def relatorio_eventos_avaliacao(self):
        
        try:
            eventos = self.__evento_controller.get_eventos_lista()
            if not eventos:
                self.__view.mostra_mensagem("Nenhum evento cadastrado.")
                return

            eventos_com_nota = []
            
            for evento in eventos:
                if evento.feedbacks:
                    nota_media = sum(f.nota for f in evento.feedbacks) / len(evento.feedbacks)
                    eventos_com_nota.append({
                        'nome': evento.nome,
                        'nota_media': nota_media,
                        'total_avaliacoes': len(evento.feedbacks),
                        'data': evento.data.strftime('%d/%m/%Y'),
                        'local': evento.local,
                        'preco': evento.preco_entrada
                    })
            
            eventos_com_nota.sort(key=lambda e: e['nota_media'], reverse=True)
            
            self.__view.mostra_eventos_avaliacao(eventos_com_nota)
            
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao gerar relatório: {str(e)}")

    def relatorio_eventos_vendas(self):
        
        try:
            eventos = self.__evento_controller.get_eventos_lista()
            if not eventos:
                self.__view.mostra_mensagem("Nenhum evento cadastrado.")
                return

            vendas_por_evento = {}
            
            for ingresso in Ingresso.get_all():
                nome_evento = ingresso.evento.nome
                if nome_evento not in vendas_por_evento:
                    vendas_por_evento[nome_evento] = {
                        'ingressos_vendidos': 0,
                        'faturamento': 0,
                        'evento': ingresso.evento
                    }
                vendas_por_evento[nome_evento]['ingressos_vendidos'] += 1
                vendas_por_evento[nome_evento]['faturamento'] += ingresso.preco

            eventos_ordenados = []
            for nome, dados in vendas_por_evento.items():
                evento = dados['evento']
                eventos_ordenados.append({
                    'nome': nome,
                    'ingressos_vendidos': dados['ingressos_vendidos'],
                    'faturamento': dados['faturamento'],
                    'data': evento.data.strftime('%d/%m/%Y'),
                    'local': evento.local
                })
            
            eventos_ordenados.sort(key=lambda e: e['ingressos_vendidos'], reverse=True)
            
            self.__view.mostra_eventos_vendas(eventos_ordenados)
            
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao gerar relatório: {str(e)}")

    def relatorio_ranking_eventos(self):
        
        try:
            eventos = self.__evento_controller.get_eventos_lista()
            if not eventos:
                self.__view.mostra_mensagem("Nenhum evento cadastrado.")
                return

            ranking = []
            
            for evento in eventos:
                nota_media = 0
                if evento.feedbacks:
                    nota_media = sum(f.nota for f in evento.feedbacks) / len(evento.feedbacks)
                
                ingressos_vendidos = len([i for i in Ingresso.get_all() if i.evento == evento])
                faturamento = sum(i.preco for i in Ingresso.get_all() if i.evento == evento)
                
                ranking.append({
                    'nome': evento.nome,
                    'nota_media': nota_media,
                    'ingressos_vendidos': ingressos_vendidos,
                    'faturamento': faturamento,
                    'data': evento.data.strftime('%d/%m/%Y'),
                    'local': evento.local,
                    'preco': evento.preco_entrada
                })
            
            ranking.sort(key=lambda e: (e['nota_media'], e['ingressos_vendidos'], e['faturamento']), reverse=True)
            
            self.__view.mostra_ranking_eventos(ranking)
            
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao gerar relatório: {str(e)}")

    def relatorio_produtos_preco(self):
        
        try:
            todos_produtos = []
            # ATENÇÃO: Acessar '_ProdutoController__produtos_por_evento' viola o encapsulamento.
            # O ideal é o ProdutoController ter um 'get_todos_produtos()'
            produtos_por_evento = self.__produto_controller.get_produtos_por_evento_lista() # Supondo que este método exista

            for nome_evento, produtos in produtos_por_evento.items():
                for produto in produtos:
                    todos_produtos.append({
                        'nome': produto.nome,
                        'preco': produto.preco,
                        'estoque': produto.estoque,
                        'evento': nome_evento
                    })
            
            if not todos_produtos:
                self.__view.mostra_mensagem("Nenhum produto cadastrado.")
                return
            
            produtos_ordenados = sorted(todos_produtos, key=lambda p: p['preco'])
            
            mais_baratos = produtos_ordenados[:5]
            mais_caros = list(reversed(produtos_ordenados[-5:]))
            
            self.__view.mostra_produtos_preco(mais_caros, mais_baratos)
            
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao gerar relatório: {str(e)}")

    def relatorio_produtos_vendidos(self):
        
        try:
            vendas_por_produto = defaultdict(lambda: {'quantidade': 0, 'faturamento': 0, 'produto': None})
            
            for venda in Venda.get_all():
                for item in venda.itens:
                    produto_nome = item.produto.nome
                    vendas_por_produto[produto_nome]['quantidade'] += item.quantidade
                    vendas_por_produto[produto_nome]['faturamento'] += item.subtotal
                    vendas_por_produto[produto_nome]['produto'] = item.produto
            
            if not vendas_por_produto:
                self.__view.mostra_mensagem("Nenhuma venda de produto encontrada.")
                return
            
            produtos_ordenados = []
            for nome, dados in vendas_por_produto.items():
                produto = dados['produto']
                produtos_ordenados.append({
                    'nome': nome,
                    'quantidade_vendida': dados['quantidade'],
                    'faturamento': dados['faturamento'],
                    'estoque': produto.estoque if produto else 0
                })
            
            produtos_ordenados.sort(key=lambda p: p['quantidade_vendida'], reverse=True)
            
            self.__view.mostra_produtos_vendidos(produtos_ordenados)
            
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao gerar relatório: {str(e)}")

    def relatorio_produtos_faturamento(self):
        
        try:
            vendas_por_produto = defaultdict(lambda: {'quantidade': 0, 'faturamento': 0, 'produto': None})
            
            for venda in Venda.get_all():
                for item in venda.itens:
                    produto_nome = item.produto.nome
                    vendas_por_produto[produto_nome]['quantidade'] += item.quantidade
                    vendas_por_produto[produto_nome]['faturamento'] += item.subtotal
                    vendas_por_produto[produto_nome]['produto'] = item.produto
            
            if not vendas_por_produto:
                self.__view.mostra_mensagem("Nenhuma venda de produto encontrada.") # Corrigido: mostra_mensagem
                return
            
            produtos_ordenados = []
            for nome, dados in vendas_por_produto.items():
                produto = dados['produto']
                produtos_ordenados.append({
                    'nome': nome,
                    'quantidade_vendida': dados['quantidade'],
                    'faturamento': dados['faturamento'],
                    'preco': produto.preco if produto else 0
                })
            
            produtos_ordenados.sort(key=lambda p: p['faturamento'], reverse=True)
            
            self.__view.mostra_produtos_faturamento(produtos_ordenados)
            
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao gerar relatório: {str(e)}")

    def relatorio_estoque(self):
        
        try:
            todos_produtos = []
            produtos_por_evento = self.__produto_controller.get_produtos_por_evento_lista() # Supondo que este método exista
            
            for nome_evento, produtos in produtos_por_evento.items():
                for produto in produtos:
                    todos_produtos.append({
                        'nome': produto.nome,
                        'estoque': produto.estoque,
                        'preco': produto.preco,
                        'evento': nome_evento
                    })
            
            if not todos_produtos:
                self.__view.mostra_mensagem("Nenhum produto cadastrado.")
                return
            
            todos_produtos.sort(key=lambda p: p['estoque'])
            
            self.__view.mostra_relatorio_estoque(todos_produtos)
            
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao gerar relatório: {str(e)}")

    def relatorio_vendas_pagamento(self):
        
        try:
            vendas_por_metodo = defaultdict(float)
            
            for venda in Venda.get_all():
                vendas_por_metodo[venda.metodo_pagamento] += venda.total
            
            for ingresso in Ingresso.get_all():
                if ingresso.metodo_pagamento:
                    vendas_por_metodo[ingresso.metodo_pagamento] += ingresso.preco
            
            if not vendas_por_metodo:
                self.__view.mostra_mensagem("Nenhuma venda encontrada.")
                return
            
            vendas_ordenadas = dict(sorted(vendas_por_metodo.items(), key=lambda x: x[1], reverse=True))
            
            self.__view.mostra_vendas_pagamento(vendas_ordenadas)
            
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao gerar relatório: {str(e)}")

    def relatorio_faturamento_evento(self):
        
        try:
            faturamento_por_evento = defaultdict(lambda: {'ingressos': 0, 'produtos': 0, 'evento': None})
            
            for ingresso in Ingresso.get_all():
                nome_evento = ingresso.evento.nome
                faturamento_por_evento[nome_evento]['ingressos'] += ingresso.preco
                faturamento_por_evento[nome_evento]['evento'] = ingresso.evento
            
            for venda in Venda.get_all():
                nome_evento = venda.evento.nome
                faturamento_por_evento[nome_evento]['produtos'] += venda.total
                faturamento_por_evento[nome_evento]['evento'] = venda.evento
            
            if not faturamento_por_evento:
                self.__view.mostra_mensagem("Nenhuma venda encontrada.")
                return
            
            eventos_ordenados = []
            for nome, dados in faturamento_por_evento.items():
                total = dados['ingressos'] + dados['produtos']
                eventos_ordenados.append({
                    'nome': nome,
                    'faturamento_ingressos': dados['ingressos'],
                    'faturamento_produtos': dados['produtos'],
                    'faturamento_total': total
                })
            
            eventos_ordenados.sort(key=lambda e: e['faturamento_total'], reverse=True)
            
            self.__view.mostra_faturamento_evento(eventos_ordenados) # Corrigido: mostra_faturamento_evento
            
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao gerar relatório: {str(e)}")

    def relatorio_top_clientes(self):
        
        try:
            dados_clientes = defaultdict(lambda: {
                'total_gasto': 0,
                'ingressos_comprados': 0,
                'produtos_comprados': 0,
                'usuario': None
            })
            
            for ingresso in Ingresso.get_all():
                matricula = ingresso.comprador.matricula
                dados_clientes[matricula]['total_gasto'] += ingresso.preco
                dados_clientes[matricula]['ingressos_comprados'] += 1
                dados_clientes[matricula]['usuario'] = ingresso.comprador
            
            for venda in Venda.get_all():
                matricula = venda.usuario.matricula
                dados_clientes[matricula]['total_gasto'] += venda.total
                dados_clientes[matricula]['produtos_comprados'] += sum(item.quantidade for item in venda.itens)
                dados_clientes[matricula]['usuario'] = venda.usuario
            
            if not dados_clientes:
                self.__view.mostra_mensagem("Nenhuma compra encontrada.")
                return
            
            clientes_ordenados = []
            for matricula, dados in dados_clientes.items():
                usuario = dados['usuario']
                clientes_ordenados.append({
                    'nome': usuario.nome,
                    'matricula': matricula,
                    'total_gasto': dados['total_gasto'],
                    'ingressos_comprados': dados['ingressos_comprados'],
                    'produtos_comprados': dados['produtos_comprados']
                })
            
            clientes_ordenados.sort(key=lambda c: c['total_gasto'], reverse=True)
            clientes_ordenados = clientes_ordenados[:10]
            
            self.__view.mostra_top_clientes(clientes_ordenados)
            
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao gerar relatório: {str(e)}")

    def relatorio_geral_sistema(self):
        
        try:
            total_usuarios = len(Usuario.get_all())
            total_eventos = len(self.__evento_controller.get_eventos_lista())
            
            total_produtos = 0
            produtos_por_evento = self.__produto_controller.get_produtos_por_evento_lista() # Supondo que este método exista
            for produtos in produtos_por_evento.values():
                total_produtos += len(produtos)
            
            total_ingressos_vendidos = len(Ingresso.get_all())
            total_produtos_vendidos = sum(
                sum(item.quantidade for item in venda.itens) 
                for venda in Venda.get_all()
            )
            
            faturamento_ingressos = sum(i.preco for i in Ingresso.get_all())
            faturamento_produtos = sum(v.total for v in Venda.get_all())
            faturamento_total = faturamento_ingressos + faturamento_produtos
            
            evento_mais_popular = ""
            produto_mais_vendido = ""
            melhor_cliente = ""
            
            vendas_eventos = defaultdict(int)
            for ingresso in Ingresso.get_all():
                vendas_eventos[ingresso.evento.nome] += 1
            if vendas_eventos:
                evento_mais_popular = max(vendas_eventos, key=vendas_eventos.get)
            
            vendas_produtos = defaultdict(int)
            for venda in Venda.get_all():
                for item in venda.itens:
                    vendas_produtos[item.produto.nome] += item.quantidade
            if vendas_produtos:
                produto_mais_vendido = max(vendas_produtos, key=vendas_produtos.get)
            
            gastos_clientes = defaultdict(float)
            for ingresso in Ingresso.get_all():
                gastos_clientes[ingresso.comprador.nome] += ingresso.preco
            for venda in Venda.get_all():
                gastos_clientes[venda.usuario.nome] += venda.total
            if gastos_clientes:
                melhor_cliente = max(gastos_clientes, key=gastos_clientes.get)
            
            dados_relatorio = {
                'total_usuarios': total_usuarios,
                'total_eventos': total_eventos,
                'total_produtos': total_produtos,
                'total_ingressos_vendidos': total_ingressos_vendidos,
                'total_produtos_vendidos': total_produtos_vendidos,
                'faturamento_ingressos': faturamento_ingressos,
                'faturamento_produtos': faturamento_produtos,
                'faturamento_total': faturamento_total,
                'evento_mais_popular': evento_mais_popular,
                'produto_mais_vendido': produto_mais_vendido,
                'melhor_cliente': melhor_cliente
            }
            
            self.__view.mostra_relatorio_geral(dados_relatorio)
            
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro ao gerar relatório: {str(e)}")


    def rodar_menu_eventos(self):
        
        while True:
            # Chama a View, que abre a janela de menu e retorna o NÚMERO (int)
            opcao = self.__view.tela_opcoes_eventos()
                
            if opcao == 1:
                self.relatorio_eventos_preco()
            elif opcao == 2:
                self.relatorio_eventos_avaliacao()
            elif opcao == 3:
                self.relatorio_eventos_vendas() # Seu código original não tinha essa opção
            elif opcao == 4:
                self.relatorio_ranking_eventos() # Seu código original não tinha essa opção
            elif opcao == 0:
                break
            else:
                self.__view.mostra_mensagem("Opcao invalida.")

    def rodar_menu_produtos(self):
        
        while True:
            # Chama a View, que abre a janela de menu e retorna o NÚMERO (int)
            opcao = self.__view.tela_opcoes_produtos()
                
            if opcao == 1:
                self.relatorio_produtos_preco()
            elif opcao == 2:
                self.relatorio_produtos_vendidos()
            elif opcao == 3:
                self.relatorio_produtos_faturamento() # Seu código original não tinha essa opção
            elif opcao == 4:
                self.relatorio_estoque() # Seu código original não tinha essa opção
            elif opcao == 5:
                # self.relatorio_ranking_produtos() # Você precisa criar este método
                self.__view.mostra_mensagem("Função ainda não implementada.")
            elif opcao == 0:
                break
            else:
                self.__view.mostra_mensagem("Opcao invalida.")

    def rodar_menu_vendas(self):
        
        while True:
            # Chama a View, que abre a janela de menu e retorna o NÚMERO (int)
            opcao = self.__view.tela_opcoes_vendas()
                
            if opcao == 1:
                self.relatorio_vendas_pagamento()
            elif opcao == 2:
                self.relatorio_faturamento_evento()
            elif opcao == 3:
                # self.relatorio_vendas_periodo() # Você precisa criar este método
                self.__view.mostra_mensagem("Função ainda não implementada.")
            elif opcao == 4:
                self.relatorio_top_clientes() # Seu código original não tinha essa opção
            elif opcao == 0:
                break
            else:
                self.__view.mostra_mensagem("Opcao invalida.")

    def rodar_menu_usuarios(self):
        
        while True:
            # Chama a View, que abre a janela de menu e retorna o NÚMERO (int)
            opcao = self.__view.tela_opcoes_usuarios()
                
            if opcao == 1:
                self.relatorio_top_clientes()
            elif opcao == 2:
                 self.__view.mostra_mensagem("Função 'Usuários Mais Ativos' ainda não implementada.")
            elif opcao == 3:
                 self.__view.mostra_mensagem("Função 'Usuários por Ingressos' ainda não implementada.")
            elif opcao == 0:
                break
            else:
                self.__view.mostra_mensagem("Opcao invalida.")