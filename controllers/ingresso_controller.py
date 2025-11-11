from views.ingresso_view import IngressoView

from controllers.usuario_controller import UsuarioController
from controllers.evento_controller import EventoController
import FreeSimpleGUI as sg


class IngressoController:
    
    def __init__(self, ingresso_view: IngressoView, usuario_controller: UsuarioController, evento_controller: EventoController):
        self.__view = ingresso_view
        self.__usuario_controller = usuario_controller
        self.__evento_controller = evento_controller
        self.__ingressos_sistema = []

    def _transformar_ingresso_para_view(self, ingresso):
        
        return {
            "id_ingresso": id(ingresso),
            "nome_evento": ingresso.evento.nome,
            "nome_comprador": ingresso.comprador.nome,
            "data_compra": ingresso.data_compra.strftime('%d/%m/%Y'),
            "preco": ingresso.preco,
            "nome_revendedor": ingresso.revendedor.nome if ingresso.revendedor else None
        }

    def comprar_ingresso_de_evento(self):
        
        matricula = self.__view.pega_matricula_comprador()
        usuario = self.__usuario_controller.buscar_usuario_por_matricula(matricula)
        if not usuario:
            self.__view.mostra_mensagem("ERRO: Usuário não encontrado.")
            return

        eventos = self.__evento_controller._EventoController__eventos
        if not eventos:
            self.__view.mostra_mensagem("Nenhum evento disponível para compra.")
            return

        dados_para_view = [self.__evento_controller._transformar_evento_para_view(e) for e in eventos]
        indice_escolhido = self.__evento_controller._EventoController__view.seleciona_evento(dados_para_view)
        if indice_escolhido is None:
            return
        
        evento_escolhido = eventos[indice_escolhido]
        
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

    def listar_meus_ingressos(self, matricula_usuario: str):
        usuario = self.__usuario_controller.buscar_usuario_por_matricula(matricula_usuario)
        if not usuario:
            self.__view.mostra_mensagem("ERRO: Usuário não encontrado.")
            return

        ingressos_objetos = usuario.listar_ingressos()
        
        dados_para_view = [self._transformar_ingresso_para_view(ing) for ing in ingressos_objetos]
        
        self.__view.mostra_ingressos(dados_para_view)

    def colocar_ingresso_a_venda(self, matricula_usuario: str):
        usuario = self.__usuario_controller.buscar_usuario_por_matricula(matricula_usuario)
        if not usuario:
            self.__view.mostra_mensagem("ERRO: Usuário não encontrado.")
            return

        ingressos_disponiveis = [ing for ing in usuario.listar_ingressos() if not ing.revendedor]
        if not ingressos_disponiveis:
            self.__view.mostra_mensagem("Você não possui ingressos disponíveis para colocar à venda.")
            return

        dados_para_view = [self._transformar_ingresso_para_view(ing) for ing in ingressos_disponiveis]
        
        indice_escolhido = self.__view.seleciona_ingresso(dados_para_view)

        if indice_escolhido is not None:
            ingresso_selecionado = ingressos_disponiveis[indice_escolhido]
            novo_preco = self.__view.pega_novo_preco_revenda()

            if novo_preco is not None and novo_preco > 0:
                try:
                    usuario.colocar_ingresso_a_venda(ingresso_selecionado, novo_preco)
                    self.__view.mostra_mensagem("Ingresso colocado à venda com sucesso!")
                except ValueError as e:
                    self.__view.mostra_mensagem(f"ERRO: {e}")
            else:
                self.__view.mostra_mensagem("Preço inválido. Operação cancelada.")

    def comprar_ingresso_revenda(self, matricula_comprador: str):
        comprador = self.__usuario_controller.buscar_usuario_por_matricula(matricula_comprador)
        if not comprador:
            self.__view.mostra_mensagem("ERRO: Usuário comprador não encontrado.")
            return
            
        todos_usuarios = self.__usuario_controller.listar_usuarios_objetos()
        ingressos_revenda_obj = []
        for u in todos_usuarios:
            for i in u.ingressos_comprados:
                if i.revendedor and i.revendedor != comprador:
                    ingressos_revenda_obj.append(i)

        if not ingressos_revenda_obj:
            self.__view.mostra_mensagem("Não há ingressos de revenda disponíveis no momento.")
            return

        dados_para_view = [self._transformar_ingresso_para_view(ing) for ing in ingressos_revenda_obj]
        indice_escolhido = self.__view.seleciona_ingresso_revenda(dados_para_view)

        if indice_escolhido is not None:
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
            
            try:
                revendedor.ingressos_comprados.remove(ingresso_a_comprar)
                comprador.ingressos_comprados.append(ingresso_a_comprar)
                ingresso_a_comprar.comprador = comprador
                ingresso_a_comprar.revendedor = None
                ingresso_a_comprar.metodo_pagamento = metodo_pagamento
                
                self.__view.mostra_mensagem(f"Ingresso comprado de {revendedor.nome} com sucesso!")
            except Exception as e:
                self.__view.mostra_mensagem(f"Ocorreu um erro na compra: {e}")

    def remover_ingresso_da_venda(self, matricula_usuario: str):
        
        usuario = self.__usuario_controller.buscar_usuario_por_matricula(matricula_usuario)
        if not usuario:
            self.__view.mostra_mensagem("ERRO: Usuário não encontrado.")
            return

        ingressos_a_venda = [ing for ing in usuario.listar_ingressos() if ing.revendedor == usuario]
        if not ingressos_a_venda:
            self.__view.mostra_mensagem("Você não possui ingressos à venda.")
            return

        dados_para_view = [self._transformar_ingresso_para_view(i) for i in ingressos_a_venda]
        indice_escolhido = self.__view.seleciona_ingresso(dados_para_view)

        if indice_escolhido is not None:
            ingresso = ingressos_a_venda[indice_escolhido]
            try:
                usuario.remover_ingresso_da_venda(ingresso)
                self.__view.mostra_mensagem("Ingresso removido da venda com sucesso!")
            except ValueError as e:
                self.__view.mostra_mensagem(f"ERRO: {e}")
                
    def listar_meus_ingressos_a_venda(self, matricula_usuario: str):
        
        usuario = self.__usuario_controller.buscar_usuario_por_matricula(matricula_usuario)
        if not usuario:
            self.__view.mostra_mensagem("ERRO: Usuário não encontrado.")
            return

        ingressos_a_venda = [ing for ing in usuario.listar_ingressos() if ing.revendedor == usuario]
        if not ingressos_a_venda:
            self.__view.mostra_mensagem("Você não possui ingressos à venda.")
            return

        dados_para_view = [self._transformar_ingresso_para_view(ing) for ing in ingressos_a_venda]
        self.__view.mostra_ingressos(dados_para_view)