from views.main_view import MainView
from views.usuario_view import UsuarioView
from views.evento_view import EventoView
from views.ingresso_view import IngressoView
from views.produto_view import ProdutoView
from views.relatorio_view import RelatorioView
from controllers.usuario_controller import UsuarioController
from controllers.evento_controller import EventoController
from controllers.ingresso_controller import IngressoController
from controllers.produto_controller import ProdutoController
from controllers.relatorio_controller import RelatorioController
import FreeSimpleGUI as sg

class MainController:
    
    def __init__(self):
        self.__main_view = MainView()
        self.__usuario_view = UsuarioView()
        self.__evento_view = EventoView()
        self.__ingresso_view = IngressoView()
        self.__produto_view = ProdutoView()
        self.__relatorio_view = RelatorioView()

        self.__usuario_controller = UsuarioController(self.__usuario_view)
        self.__evento_controller = EventoController(self.__evento_view) # Removido o UsuarioController daqui
        self.__ingresso_controller = IngressoController(self.__ingresso_view) # Removido os controllers daqui
        self.__produto_controller = ProdutoController(self.__produto_view) # Removido os controllers daqui
        self.__relatorio_controller = RelatorioController(
            self.__relatorio_view,
            self.__evento_controller,
            self.__usuario_controller,
            self.__produto_controller
        )

        self.__evento_controller.set_usuario_controller(self.__usuario_controller)
        
        self.__usuario_controller.set_evento_controller(self.__evento_controller)
        
        self.__ingresso_controller.set_usuario_controller(self.__usuario_controller)
        self.__ingresso_controller.set_evento_controller(self.__evento_controller)
        
        self.__produto_controller.set_usuario_controller(self.__usuario_controller)
        self.__produto_controller.set_evento_controller(self.__evento_controller)
        
    def iniciar(self):

        janela_principal = self.__main_view.janela_principal()
          
        while True:
            evento, valores = janela_principal.read()
            
            if evento == sg.WINDOW_CLOSED or evento == '0':
                self.__main_view.mostrar_mensagem_encerramento()
                break 
            
            elif evento == '1':
                janela_principal.hide() 
                self.__usuario_controller.rodar_menu_usuario() 
                janela_principal.un_hide()

            
            elif evento == '2':
                 janela_principal.hide()
                 self.__evento_controller.rodar_menu_evento() 
                 janela_principal.un_hide()

            elif evento == '3':
                 janela_principal.hide()
                 self.__ingresso_controller.rodar_menu_ingresso() 
                 janela_principal.un_hide()

            elif evento == '4':
                janela_principal.hide()
                self.__produto_controller.rodar_menu_produto() 
                janela_principal.un_hide()

            elif evento == '5':
                janela_principal.hide()
                self.__relatorio_controller.rodar_menu_relatorios() 
                janela_principal.un_hide()

        janela_principal.close()
            
    def rodar_submenu_usuario(self):
        
        while True:
            opcao = self.__usuario_view.tela_opcoes()
            
            if opcao == 1:
                self.__usuario_controller.incluir_usuario()
            elif opcao == 2:
                self.__usuario_controller.alterar_usuario()
            elif opcao == 3:
                self.__usuario_controller.listar_usuarios()
            elif opcao == 4:
                self.__usuario_controller.excluir_usuario()
            elif opcao == 5:
                self.__usuario_controller.listar_meus_ingressos()
            elif opcao == 6:
                self.__usuario_controller.ver_historico_compras()
            elif opcao == 7:
                self.__evento_controller.avaliar_evento()
            elif opcao == 0:
                break
            else:
                self.__usuario_view.mostra_mensagem("Opção de usuário inválida.")
                
    def rodar_submenu_evento(self):
        
        while True:
            opcao = self.__evento_view.tela_opcoes()
            if opcao == 1:
                self.__evento_controller.incluir_evento()
            elif opcao == 2:
                self.__evento_controller.alterar_evento()
            elif opcao == 3:
                self.__evento_controller.listar_eventos()
            elif opcao == 4:
                self.__evento_controller.excluir_evento()
            elif opcao == 5:
                self.__evento_controller.ver_detalhes_evento()
            elif opcao == 6:
                self.__evento_controller.ver_feedbacks_evento()
            elif opcao == 0:
                break
            else:
                self.__evento_view.mostra_mensagem("Opção de evento inválida.")
    
    def rodar_submenu_revenda_ingresso(self):
        
        matricula = self.__usuario_view.pega_matricula_usuario()
        if not self.__usuario_controller.buscar_usuario_por_matricula(matricula):
             self.__usuario_view.mostra_mensagem("Usuário não encontrado.")
             return

        while True:
            opcao = self.__ingresso_view.tela_opcoes_revenda()
            if opcao == 1:
                self.__ingresso_controller.colocar_ingresso_a_venda(matricula)
            elif opcao == 2:
                self.__ingresso_controller.remover_ingresso_da_venda(matricula)
            elif opcao == 3:
                self.__ingresso_controller.comprar_ingresso_revenda(matricula)
            elif opcao == 4:
                self.__ingresso_controller.listar_meus_ingressos_a_venda(matricula)
            elif opcao == 0:
                break
            else:
                self.__ingresso_view.mostra_mensagem("Opção de revenda inválida.")

    def rodar_submenu_produto(self):
        
        while True:
            opcao = self.__produto_view.tela_opcoes()
            if opcao == 1:
                self.__produto_controller.adicionar_produto_evento()
            elif opcao == 2:
                self.__produto_controller.alterar_produto()
            elif opcao == 3:
                self.__produto_controller.listar_produtos_evento()
            elif opcao == 4:
                self.__produto_controller.excluir_produto()
            elif opcao == 5:
                self.__produto_controller.registrar_venda()
            elif opcao == 6:
                self.__produto_controller.relatorio_vendas()
            elif opcao == 0:
                break
            else:
                self.__produto_view.mostra_mensagem("Opção de produto inválida.")

    def rodar_submenu_ingresso(self):
        
        while True:
            print("\n-------- MENU INGRESSOS ----------")
            print("1 - Comprar Ingresso")
            print("2 - Gerenciar Revenda")
            print("0 - Retornar")
            
            try:
                opcao = int(input("Escolha a opção: "))
            except ValueError:
                opcao = -1

            if opcao == 1:
                self.__ingresso_controller.comprar_ingresso_de_evento()
            elif opcao == 2:
                self.rodar_submenu_revenda_ingresso()
            elif opcao == 0:
                break
            else:
                print("Opção inválida.")

    def rodar_submenu_relatorios(self):
        
        while True:
            opcao = self.__relatorio_view.tela_opcoes()
            
            if opcao == 1:
                self.__relatorio_controller.rodar_menu_eventos()
            elif opcao == 2:
                self.__relatorio_controller.rodar_menu_produtos() 
            elif opcao == 3:
                self.__relatorio_controller.rodar_menu_vendas()
            elif opcao == 4:
                self.__relatorio_controller.rodar_menu_usuarios()
            elif opcao == 0:
                break
            else:
                self.__relatorio_view.mostra_mensagem("Opção inválida.")