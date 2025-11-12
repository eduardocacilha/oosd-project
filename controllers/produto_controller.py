from typing import Dict, List
import FreeSimpleGUI as sg

from views.produto_view import ProdutoView
from controllers.evento_controller import EventoController
from controllers.usuario_controller import UsuarioController

from models.camisa import Camisa
from models.copo import Copo
from models.venda import Venda
from models.item_venda import ItemVenda
from models.produto import Produto # Para type hinting

class ProdutoController:
    

    def __init__(self, produto_view: ProdutoView):
        self.__view = produto_view
        self.__evento_controller: EventoController = None
        self.__usuario_controller: UsuarioController = None
        self.__produtos_por_evento: Dict[str, List[Produto]] = {} # Armazena os produtos por nome do evento
        self.__next_produto_id = 1

    def set_usuario_controller(self, usuario_controller: UsuarioController):
        self.__usuario_controller = usuario_controller
        
    def set_evento_controller(self, evento_controller: EventoController):
        self.__evento_controller = evento_controller

    def rodar_menu_produto(self):
        """Este é o método que o MainController chama (evento '4')"""
        
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
                    break # Volta para o MainController
            
            except Exception as e:
                self.__view.mostrar_popup("Erro Inesperado", f"Ocorreu um erro: {e}")


    def _gerar_id_produto(self) -> int:
        current_id = self.__next_produto_id
        self.__next_produto_id += 1
        return current_id

    def adicionar_produto_evento(self):
        """Fluxo de 'Adicionar Produto a um Evento'."""
        
        try:
            evento_escolhido = self.__evento_controller.selecionar_evento_gui()
            if evento_escolhido is None:
                return # Usuário cancelou

            tipo = self.__view.escolher_tipo_produto()
            if tipo == 0: # Cancelar
                return
            
            dados = None
            if tipo == 1:
                dados = self.__view.pega_dados_camisa()
            elif tipo == 2:
                dados = self.__view.pega_dados_copo()
            else:
                self.__view.mostrar_popup("Aviso", "Tipo de produto inválido.")
                return

            if dados is not None:
                produto = None
                if tipo == 1:
                    produto = Camisa(
                        id_produto=self._gerar_id_produto(),
                        nome=dados["nome"], preco=dados["preco"], estoque=dados["estoque"],
                        tamanho=dados["tamanho"], cor=dados["cor"]
                    )
                elif tipo == 2:
                    produto = Copo(
                        id_produto=self._gerar_id_produto(),
                        nome=dados["nome"], preco=dados["preco"], estoque=dados["estoque"],
                        capacidade_ml=dados["capacidade_ml"], material=dados["material"]
                    )

                nome_evento = evento_escolhido.nome
                if nome_evento not in self.__produtos_por_evento:
                    self.__produtos_por_evento[nome_evento] = []
                
                self.__produtos_por_evento[nome_evento].append(produto)
                self.__view.mostrar_popup("Sucesso", f"Produto '{produto.nome}' adicionado ao evento '{nome_evento}'!")
                
        except Exception as e:
            self.__view.mostrar_popup("Erro", f"Erro inesperado ao adicionar produto: {str(e)}")

    def listar_produtos_evento(self):
        try:
            evento_escolhido = self.__evento_controller.selecionar_evento_gui()
            if evento_escolhido is None:
                return

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
            self.__view.mostrar_popup("Erro", f"Erro inesperado ao listar produtos: {str(e)}")

    def registrar_venda(self):
        """Fluxo de 'Registrar Venda' (o mais complexo)."""
        
        evento_escolhido = self.__evento_controller.selecionar_evento_gui()
        if evento_escolhido is None: return

        nome_evento = evento_escolhido.nome
        produtos = self.__produtos_por_evento.get(nome_evento, [])
        if not produtos:
            self.__view.mostrar_popup("Erro", "Nenhum produto cadastrado para este evento.")
            return

        matricula = self.__usuario_controller.pega_matricula_usuario_gui()
        if not matricula: return
        
        usuario = self.__usuario_controller.buscar_usuario_por_matricula(matricula)
        if not usuario:
            self.__view.mostrar_popup("Erro", "Usuário não encontrado.")
            return

        metodo_pagamento = self.__view.pega_metodo_pagamento()
        if not metodo_pagamento: return

        venda = None # A venda só será criada se o usuário adicionar o primeiro item

        while True:
            
            dados_produtos = []
            produtos_com_estoque = []
            for produto in produtos:
                if produto.estoque > 0:
                    dados_produtos.append({
                        "descricao": produto.descricao(),
                        "preco": produto.preco,
                        "estoque": produto.estoque
                    })
                    produtos_com_estoque.append(produto)

            if not dados_produtos:
                self.__view.mostrar_popup("Aviso", "Nenhum produto com estoque disponível.")
                break

            indice_produto = self.__view.seleciona_produto(dados_produtos)
            if indice_produto is None:
                break 

            produto_escolhido = produtos_com_estoque[indice_produto]

            try:
                quantidade = self.__view.pega_quantidade_venda()
                if quantidade is None:
                    continue # Usuário cancelou a quantidade, volta a selecionar produto

                if venda is None:
                    venda = Venda(usuario, evento_escolhido, metodo_pagamento)

                venda.adicionar_item(produto_escolhido, quantidade) # (Assumindo que Venda.py tem 'adicionar_item')
                
                self.__view.mostrar_popup("Sucesso", f"Item adicionado: {quantidade}x {produto_escolhido.nome}")
                
                if not self.__view.confirma_continuar_comprando():
                    break 

            except ValueError as e:
                self.__view.mostrar_popup("Erro", f"Erro ao adicionar item: {str(e)}")

        if venda is not None and venda.itens:
            # Adiciona a venda ao Model do Evento (se necessário)
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

    def relatorio_vendas(self):
        """Fluxo de 'Relatório de Vendas'."""
        
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
        """Fluxo de 'Alterar Produto'."""
        
        try:
            # 1. Seleciona o Evento
            evento_escolhido = self.__evento_controller.selecionar_evento_gui()
            if evento_escolhido is None: return

            nome_evento = evento_escolhido.nome
            produtos = self.__produtos_por_evento.get(nome_evento, [])
            if not produtos:
                self.__view.mostrar_popup("Erro", "Nenhum produto cadastrado para este evento.")
                return

            # 2. Seleciona o Produto
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
            
            # 3. Pede os novos dados (usando o formulário específico)
            novos_dados = None
            if isinstance(produto_escolhido, Camisa):
                novos_dados = self.__view.pega_dados_camisa()
            elif isinstance(produto_escolhido, Copo):
                novos_dados = self.__view.pega_dados_copo()
            
            if novos_dados is None:
                return # Usuário cancelou

            # 4. Atualiza o Model
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
                
        except Exception as e:
            self.__view.mostrar_popup("Erro", f"Erro inesperado ao alterar produto: {str(e)}")

    def excluir_produto(self):
        """Fluxo de 'Excluir Produto'."""
        
        try:
            # 1. Seleciona o Evento
            evento_escolhido = self.__evento_controller.selecionar_evento_gui()
            if evento_escolhido is None: return

            nome_evento = evento_escolhido.nome
            produtos = self.__produtos_por_evento.get(nome_evento, [])
            if not produtos:
                self.__view.mostrar_popup("Erro", "Nenhum produto cadastrado para este evento.")
                return

            # 2. Seleciona o Produto
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
            
            # 3. Confirma a exclusão (Substituindo o 'input')
            resposta = sg.popup_yes_no(
                f"Deseja realmente excluir este produto?\n\n{produto_escolhido.descricao()}",
                title="Confirmar Exclusão",
                keep_on_top=True
            )
            
            if resposta == 'Yes':
                # 4. Remove o produto
                produtos.remove(produto_escolhido)
                self.__view.mostrar_popup("Sucesso", "Produto excluído com sucesso!")
            else:
                self.__view.mostrar_popup("Aviso", "Exclusão cancelada.")
                
        except Exception as e:
            self.__view.mostrar_popup("Erro", f"Erro inesperado ao excluir produto: {str(e)}")
            
    def get_produtos_por_evento_lista(self) -> Dict[str, List[Produto]]:
        """Retorna o dicionário de produtos por evento."""
        return self.__produtos_por_evento