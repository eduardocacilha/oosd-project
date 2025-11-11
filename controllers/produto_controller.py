from views.produto_view import ProdutoView
from controllers.evento_controller import EventoController
from controllers.usuario_controller import UsuarioController
from models.camisa import Camisa
from models.copo import Copo
from models.venda import Venda
from models.item_venda import ItemVenda
from typing import Dict, List
import FreeSimpleGUI as sg

class ProdutoController:
    def __init__(self, produto_view: ProdutoView, evento_controller: EventoController, usuario_controller: UsuarioController):
        self.__view = produto_view
        self.__evento_controller = evento_controller
        self.__usuario_controller = usuario_controller
        self.__produtos_por_evento: Dict[str, List] = {}
        self.__next_produto_id = 1

    def _gerar_id_produto(self) -> int:
        current_id = self.__next_produto_id
        self.__next_produto_id += 1
        return current_id

    def adicionar_produto_evento(self):
        
        try:
            eventos = self.__evento_controller._EventoController__eventos
            if not eventos:
                self.__view.mostra_mensagem("Nenhum evento cadastrado.")
                return

            dados_eventos = [self.__evento_controller._transformar_evento_para_view(e) for e in eventos]
            from views.evento_view import EventoView
            evento_view = EventoView()
            indice_evento = evento_view.seleciona_evento(dados_eventos)
            
            if indice_evento is None:
                return

            evento_escolhido = eventos[indice_evento]
            
            tipo = self.__view.escolher_tipo_produto()
            
            try:
                if tipo == 1:
                    dados = self.__view.pega_dados_camisa()
                    produto = Camisa(
                        id_produto=self._gerar_id_produto(),
                        nome=dados["nome"],
                        preco=dados["preco"],
                        estoque=dados["estoque"],
                        tamanho=dados["tamanho"],
                        cor=dados["cor"]
                    )
                elif tipo == 2:
                    dados = self.__view.pega_dados_copo()
                    produto = Copo(
                        id_produto=self._gerar_id_produto(),
                        nome=dados["nome"],
                        preco=dados["preco"],
                        estoque=dados["estoque"],
                        capacidade_ml=dados["capacidade_ml"],
                        material=dados["material"]
                    )
                else:
                    self.__view.mostra_mensagem("Tipo de produto inválido.")
                    return

                nome_evento = evento_escolhido.nome
                if nome_evento not in self.__produtos_por_evento:
                    self.__produtos_por_evento[nome_evento] = []
                
                self.__produtos_por_evento[nome_evento].append(produto)
                self.__view.mostra_mensagem(f"Produto '{produto.nome}' adicionado ao evento '{nome_evento}' com sucesso!")
                
            except (ValueError, KeyError) as e:
                self.__view.mostra_mensagem(f"Erro nos dados do produto: {str(e)}")
                
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro inesperado: {str(e)}")

    def listar_produtos_evento(self):
        
        try:
            eventos = self.__evento_controller._EventoController__eventos
            if not eventos:
                self.__view.mostra_mensagem("Nenhum evento cadastrado.")
                return

            dados_eventos = [self.__evento_controller._transformar_evento_para_view(e) for e in eventos]
            from views.evento_view import EventoView
            evento_view = EventoView()
            indice_evento = evento_view.seleciona_evento(dados_eventos)
            
            if indice_evento is None:
                return

            evento_escolhido = eventos[indice_evento]
            nome_evento = evento_escolhido.nome
            
            produtos = self.__produtos_por_evento.get(nome_evento, [])
            dados_produtos = []
            
            for produto in produtos:
                dados_produtos.append({
                    "descricao": produto.descricao(),
                    "preco": produto.preco,
                    "estoque": produto.estoque
                })
            
            self.__view.mostra_produtos(dados_produtos)
            
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro inesperado: {str(e)}")

    def registrar_venda(self):
        
        eventos = self.__evento_controller._EventoController__eventos
        if not eventos:
            self.__view.mostra_mensagem("Nenhum evento cadastrado.")
            return

        dados_eventos = [self.__evento_controller._transformar_evento_para_view(e) for e in eventos]
        from views.evento_view import EventoView
        evento_view = EventoView()
        indice_evento = evento_view.seleciona_evento(dados_eventos)
        
        if indice_evento is None:
            return

        evento_escolhido = eventos[indice_evento]
        nome_evento = evento_escolhido.nome
        
        produtos = self.__produtos_por_evento.get(nome_evento, [])
        if not produtos:
            self.__view.mostra_mensagem("Nenhum produto cadastrado para este evento.")
            return

        matricula = self.__usuario_controller._UsuarioController__view.pega_matricula_usuario()
        usuario = self.__usuario_controller.buscar_usuario_por_matricula(matricula)
        if not usuario:
            self.__view.mostra_mensagem("Usuário não encontrado.")
            return

        metodo_pagamento = self.__view.pega_metodo_pagamento()

        venda = None
        itens_adicionados = []

        while True:
            dados_produtos = []
            for produto in produtos:
                if produto.estoque > 0:
                    dados_produtos.append({
                        "descricao": produto.descricao(),
                        "preco": produto.preco,
                        "estoque": produto.estoque
                    })

            if not dados_produtos:
                self.__view.mostra_mensagem("Nenhum produto com estoque disponível.")
                break

            indice_produto = self.__view.seleciona_produto(dados_produtos)
            if indice_produto is None:
                break

            produto_escolhido = None
            contador = 0
            for produto in produtos:
                if produto.estoque > 0:
                    if contador == indice_produto:
                        produto_escolhido = produto
                        break
                    contador += 1

            if produto_escolhido is None:
                continue

            try:
                quantidade = self.__view.pega_quantidade_venda()
                if quantidade <= 0:
                    self.__view.mostra_mensagem("Quantidade deve ser maior que zero.")
                    continue

                if venda is None:
                    venda = Venda(usuario, evento_escolhido, metodo_pagamento)

             
                venda.adicionar_item(produto_escolhido, quantidade)
       
                
                self.__view.mostra_mensagem(f"Item adicionado: {quantidade}x {produto_escolhido.nome}")
                
                continuar = input("Deseja adicionar mais itens? (s/n): ").lower()
                
                if continuar != 's':
                    break

            except ValueError as e:
                self.__view.mostra_mensagem(f"Erro: {str(e)}")

    def relatorio_vendas(self):
        
        vendas = Venda.get_all()
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

    def alterar_produto(self):
        
        try:
            eventos = self.__evento_controller._EventoController__eventos
            if not eventos:
                self.__view.mostra_mensagem("Nenhum evento cadastrado.")
                return

            dados_eventos = [self.__evento_controller._transformar_evento_para_view(e) for e in eventos]
            from views.evento_view import EventoView
            evento_view = EventoView()
            indice_evento = evento_view.seleciona_evento(dados_eventos)
            
            if indice_evento is None:
                return

            evento_escolhido = eventos[indice_evento]
            nome_evento = evento_escolhido.nome
            
            produtos = self.__produtos_por_evento.get(nome_evento, [])
            if not produtos:
                self.__view.mostra_mensagem("Nenhum produto cadastrado para este evento.")
                return

            dados_produtos = []
            for produto in produtos:
                dados_produtos.append({
                    "descricao": produto.descricao(),
                    "preco": produto.preco,
                    "estoque": produto.estoque
                })

            indice_produto = self.__view.seleciona_produto(dados_produtos)
            if indice_produto is None:
                return

            produto_escolhido = produtos[indice_produto]
            
            try:
                if isinstance(produto_escolhido, Camisa):
                    novos_dados = self.__view.pega_dados_camisa()
                    produto_escolhido.nome = novos_dados["nome"]
                    produto_escolhido.preco = novos_dados["preco"]
                    produto_escolhido.estoque = novos_dados["estoque"]
                    produto_escolhido.tamanho = novos_dados["tamanho"]
                    produto_escolhido.cor = novos_dados["cor"]
                elif isinstance(produto_escolhido, Copo):
                    novos_dados = self.__view.pega_dados_copo()
                    produto_escolhido.nome = novos_dados["nome"]
                    produto_escolhido.preco = novos_dados["preco"]
                    produto_escolhido.estoque = novos_dados["estoque"]
                    produto_escolhido.capacidade_ml = novos_dados["capacidade_ml"]
                    produto_escolhido.material = novos_dados["material"]

                self.__view.mostra_mensagem("Produto alterado com sucesso!")
                
            except (ValueError, KeyError) as e:
                self.__view.mostra_mensagem(f"Erro ao alterar produto: {str(e)}")
                
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro inesperado: {str(e)}")

    def excluir_produto(self):
        
        try:
            eventos = self.__evento_controller._EventoController__eventos
            if not eventos:
                self.__view.mostra_mensagem("Nenhum evento cadastrado.")
                return

            dados_eventos = [self.__evento_controller._transformar_evento_para_view(e) for e in eventos]
            from views.evento_view import EventoView
            evento_view = EventoView()
            indice_evento = evento_view.seleciona_evento(dados_eventos)
            
            if indice_evento is None:
                return

            evento_escolhido = eventos[indice_evento]
            nome_evento = evento_escolhido.nome
            
            produtos = self.__produtos_por_evento.get(nome_evento, [])
            if not produtos:
                self.__view.mostra_mensagem("Nenhum produto cadastrado para este evento.")
                return

            dados_produtos = []
            for produto in produtos:
                dados_produtos.append({
                    "descricao": produto.descricao(),
                    "preco": produto.preco,
                    "estoque": produto.estoque
                })

            indice_produto = self.__view.seleciona_produto(dados_produtos)
            if indice_produto is None:
                return

            produto_escolhido = produtos[indice_produto]
            
            print(f"\nProduto selecionado: {produto_escolhido.descricao()}")
            confirmacao = input("Deseja realmente excluir este produto? (s/n): ").lower().strip()
            if confirmacao == 's':
                produtos.remove(produto_escolhido)
                self.__view.mostra_mensagem("Produto excluído com sucesso!")
            else:
                self.__view.mostra_mensagem("Exclusão cancelada.")
                
        except Exception as e:
            self.__view.mostra_mensagem(f"Erro inesperado: {str(e)}")