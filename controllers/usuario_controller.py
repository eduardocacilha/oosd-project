# Em: controllers/usuario_controller.py

import FreeSimpleGUI as sg
from views.usuario_view import UsuarioView
from models.usuario import Usuario
# Importe os outros models que você precisará
from models.ingresso import Ingresso
from models.venda import Venda
from datetime import date # Necessário para o histórico

class UsuarioController:
    
    def __init__(self, usuario_view: UsuarioView):
        self.__view = usuario_view
        # Nota: A lista de usuários é gerenciada pelo Model (Usuario.get_all())
        # então não precisamos de self.__usuarios aqui.

    # --- MÉTODO PRINCIPAL DESTE CONTROLLER ---
    # Este é o método que o MainController chama (evento '1')
    def rodar_menu_usuario(self):
        
        # Este loop é para MANTER O MENU ABERTO.
        while True:
            # 1. CORREÇÃO: Chamamos o novo método da GUI 'criar_janela_menu_usuario'
            evento = self.__view.criar_janela_menu_usuario() 

            # 2. O Controller reage ao evento que a View retornou
            if evento == '0':
                break # Quebra o loop do *controller* e volta pro Main
            
            if evento == '1':
                self.fluxo_incluir_usuario()
                
            if evento == '2':
                self.fluxo_listar_usuarios()
            
            if evento == '3':
                self.fluxo_alterar_usuario()
            
            if evento == '4':
                self.fluxo_excluir_usuario()
                
            if evento == '5':
                self.fluxo_ver_historico_compras()
                
            if evento == '6':
                self.fluxo_listar_meus_ingressos()
            
            if evento == '7':
                self.fluxo_avaliar_evento()

    # --- MÉTODOS DE FLUXO (Seus métodos antigos do Controller, agora adaptados) ---

    def fluxo_incluir_usuario(self):
        """
        Contém a lógica do seu método antigo 'incluir_usuario'.
        Ele chama a view 'pega_dados_usuario' e processa o resultado.
        """
        try:
            # 1. Pede os dados à View (que abre a janela de cadastro)
            dados_usuario = self.__view.pega_dados_usuario(pedindo_matricula=True)
            
            # 2. Se o usuário NÃO cancelou (retornou dados)
            if dados_usuario:
                # 3. Lógica de Negócio (exatamente como no seu controller antigo)
                if Usuario.get_by_matricula(dados_usuario["matricula"]):
                    self.__view.mostrar_popup("Erro", f"ERRO: A matrícula {dados_usuario['matricula']} já existe.")
                    return # Encerra o fluxo
                
                # 4. Chama o Model para criar a instância
                Usuario(
                    matricula=dados_usuario["matricula"],
                    nome=dados_usuario["nome"],
                    email=dados_usuario["email"]
                )
                self.__view.mostrar_popup("Sucesso", "Usuário incluído com sucesso!")
        
        except Exception as e:
            self.__view.mostrar_popup("Erro", f"Erro ao incluir usuário: {str(e)}")
    
    def fluxo_listar_usuarios(self):
        """Contém a lógica do seu método antigo 'listar_usuarios'."""
        
        usuarios_objetos = Usuario.get_all()
        
        # A própria View já trata a lista vazia, então não precisamos de IF aqui.
        
        dados_para_view = []
        for usuario in usuarios_objetos:
            dados_para_view.append({
                "matricula": usuario.matricula,
                "nome": usuario.nome,
                "email": usuario.email
            })
            
        self.__view.mostra_usuarios(dados_para_view)

    def fluxo_alterar_usuario(self):
        """Contém a lógica do seu método antigo 'alterar_usuario'."""
        try:
            matricula = self.__view.pega_matricula_usuario()
            if not matricula: # Usuário cancelou
                return

            usuario = Usuario.get_by_matricula(matricula)
            if not usuario:
                self.__view.mostrar_popup("Erro", "Usuário não encontrado.")
                return
            
            dados_atuais = {"matricula": usuario.matricula, "nome": usuario.nome, "email": usuario.email}
            self.__view.mostra_usuario(dados_atuais)

            novos_dados = self.__view.pega_dados_usuario(pedindo_matricula=False)
            if not novos_dados: # Usuário cancelou
                return
            
            usuario.nome = novos_dados["nome"]
            usuario.email = novos_dados["email"]
            
            self.__view.mostrar_popup("Sucesso", "Usuário alterado com sucesso!")
            
        except Exception as e:
            self.__view.mostrar_popup("Erro", f"Erro ao alterar usuário: {str(e)}")

    def fluxo_excluir_usuario(self):
        """Contém a lógica do seu método antigo 'excluir_usuario'."""
        try:
            # Adiciona a "guarda" que discutimos
            if not Usuario.get_all():
                self.__view.mostrar_popup("Aviso", "Não há usuários cadastrados para excluir.")
                return
            
            matricula = self.__view.pega_matricula_usuario()
            if not matricula: # Usuário cancelou
                return

            usuario = Usuario.get_by_matricula(matricula)
            if not usuario:
                self.__view.mostrar_popup("Erro", "Usuário não encontrado.")
                return
                
            if len(usuario.ingressos_comprados) > 0:
                self.__view.mostrar_popup("Erro", "ERRO: Não é possível excluir usuário que possui ingressos.")
                return
                
            Usuario.remove(usuario) # (Assumindo que 'Usuario.remove()' existe no seu Model)
            self.__view.mostrar_popup("Sucesso", "Usuário excluído com sucesso!")
            
        except Exception as e:
            self.__view.mostrar_popup("Erro", f"Erro ao excluir usuário: {str(e)}")

    def fluxo_ver_historico_compras(self):
        """Contém a lógica do seu método antigo 'ver_historico_compras'."""
        try:
            matricula = self.__view.pega_matricula_usuario()
            if not matricula: return

            usuario = Usuario.get_by_matricula(matricula)
            if not usuario:
                self.__view.mostrar_popup("Erro", "Usuário não encontrado.")
                return

            historico_ingressos = []
            for ingresso in usuario.ingressos_comprados:
                historico_ingressos.append({
                    "tipo": "Ingresso",
                    "descricao": f"Ingresso para {ingresso.evento.nome}",
                    "valor": ingresso.preco,
                    "data": ingresso.data_compra.strftime('%d/%m/%Y'),
                    "metodo": ingresso.metodo_pagamento
                })

            historico_vendas = []
            for venda in usuario.historico_compras:
                for item in venda.itens:
                    historico_vendas.append({
                        "tipo": "Produto",
                        "descricao": f"{item.quantidade}x {item.produto.nome} - {venda.evento.nome}",
                        "valor": item.subtotal,
                        "data": venda.data_hora.strftime('%d/%m/%Y'),
                        "metodo": venda.metodo_pagamento
                    })

            historico_completo = historico_ingressos + historico_vendas
            
            self.__view.mostra_historico_compras(historico_completo)
        
        except Exception as e:
            self.__view.mostrar_popup("Erro", f"Erro ao gerar histórico: {str(e)}")

    def fluxo_listar_meus_ingressos(self):
        """Contém a lógica do seu método antigo 'listar_meus_ingressos'."""
        try:
            matricula = self.__view.pega_matricula_usuario()
            if not matricula: return
            
            usuario = Usuario.get_by_matricula(matricula)
            if not usuario:
                self.__view.mostrar_popup("Erro", "Usuário não encontrado.")
                return

            ingressos_objetos = usuario.ingressos_comprados
            
            # A View já trata a lista vazia, mas podemos poupar processamento
            if not ingressos_objetos:
                 self.__view.mostra_ingressos_usuario([])
                 return

            dados_ingressos = []
            for ingresso in ingressos_objetos:
                dados_ingressos.append({
                    "evento_nome": ingresso.evento.nome,
                    "evento_data": ingresso.evento.data.strftime('%d/%m/%Y'),
                    "evento_local": ingresso.evento.local,
                    "preco": ingresso.preco,
                    "data_compra": ingresso.data_compra.strftime('%d/%m/%Y'),
                })
            
            self.__view.mostra_ingressos_usuario(dados_ingressos)
        
        except Exception as e:
            self.__view.mostrar_popup("Erro", f"Erro ao listar ingressos: {str(e)}")

    def fluxo_avaliar_evento(self):
        """Contém a lógica do seu método antigo 'avaliar_evento'."""
        try:
            # 1. Obter o usuário
            matricula = self.__view.pega_matricula_usuario()
            if not matricula: return
            
            usuario = Usuario.get_by_matricula(matricula)
            if not usuario:
                self.__view.mostrar_popup("Erro", "Usuário não encontrado.")
                return

            # 2. Obter o evento (PRECISA SER IMPLEMENTADO)
            # Você precisa de um 'EventoView' com 'seleciona_evento()'
            # Por enquanto, vamos pular esta parte
            self.__view.mostrar_popup("Aviso", "A seleção de evento ainda não foi implementada.")
            return 
            
        
            # evento = self.__evento_view.seleciona_evento() # (exemplo)
            # if not evento: return

    
            # dados_avaliacao = self.__view.pega_dados_avaliacao()
            # if not dados_avaliacao: return
            
            # usuario.avaliar_evento(
            #     evento, 
            #     dados_avaliacao['nota'], 
            #     dados_avaliacao['comentario']
            # )
            
            # self.__view.mostrar_popup("Sucesso", "Evento avaliado com sucesso!")
        
        except Exception as e:
            self.__view.mostrar_popup("Erro", f"Erro ao avaliar evento: {str(e)}")