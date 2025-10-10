from typing import Optional
from models.usuario import Usuario
from models.evento import Evento
from models.ingresso import Ingresso
from models.venda import Venda
from models.feedback import Feedback
from views.main_view import MainView
from views.usuario_view import UsuarioView
from views.evento_view import EventoView
from views.ingresso_view import IngressoView
from controllers.usuario_controller import UsuarioController
from controllers.evento_controller import EventoController
from controllers.ingresso_controller import IngressoController

class MainController:
    def __init__(self):
        self.main_view = MainView()
        self.usuario_view = UsuarioView()
        self.evento_view = EventoView()
        self.usuario_controller = UsuarioController()
        self.evento_controller = EventoController(Evento, self.evento_view)
        self.ingresso_controller = IngressoController(Ingresso, self.ingresso_view)
        self.eventos = []

    def adicionar_usuario(self, matricula: str, nome: str, email: str):
        dados = {"matricula": matricula, "nome": nome, "email": email}
        resultado = self.usuario_controller.incluir_usuario(dados)
        self.usuario_view.mostra_mensagem(resultado["mensagem"])

    def adicionar_evento(self, nome, data, local, preco_entrada):
        evento = Evento(nome, data, local, preco_entrada)
        self.eventos.append(evento)
        self.evento_view.mostra_evento(evento)

    def comprar_ingresso(self, matricula: str, evento: Evento, preco=None):
        resultado = self.usuario_controller.comprar_ingresso(matricula, evento, preco)
        if resultado["sucesso"]:
            self.ingresso_view.mostra_ingresso(resultado["ingresso"])
        else:
            self.ingresso_view.mostra_mensagem(resultado["mensagem"])

    def avaliar_evento(self, matricula: str, evento: Evento, nota: int, comentario: str):
        resultado = self.usuario_controller.avaliar_evento(matricula, evento, nota, comentario)
        if resultado["sucesso"]:
            self.evento_view.mostra_mensagem("Avaliação realizada com sucesso.")
        else:
            self.evento_view.mostra_mensagem(resultado["mensagem"])

    def listar_ingressos_usuario(self, matricula: str):
        resultado = self.usuario_controller.listar_ingressos_usuario(matricula)
        if resultado["sucesso"]:
            self.ingresso_view.mostra_ingressos(resultado["ingressos"])
        else:
            self.ingresso_view.mostra_mensagem(resultado["mensagem"])

    def iniciar(self):
        while True:
            opcao = self.main_view.mostrar()
            if opcao == 1:
                while True:
                    sub_opcao = self.usuario_view.tela_opcoes()
                    if sub_opcao == 1:
                        dados = self.usuario_view.pega_dados_usuario()
                        self.adicionar_usuario(dados["matricula"], dados["nome"], dados["email"])
                    elif sub_opcao == 2:
                        matricula = self.usuario_view.pega_matricula_usuario()
                        usuario = self.usuario_controller.buscar_usuario_por_matricula(matricula)
                        if usuario:
                            novos_dados = self.usuario_view.pega_dados_usuario()
                            usuario._Usuario__nome = novos_dados["nome"]
                            usuario._Usuario__email = novos_dados["email"]
                            self.usuario_view.mostra_usuario({"matricula": usuario.matricula, "nome": usuario.nome, "email": usuario.email})
                        else:
                            self.usuario_view.mostra_mensagem("Usuário não encontrado.")
                    elif sub_opcao == 3:
                        lista = self.usuario_controller.listar_usuarios()
                        self.usuario_view.mostra_usuarios(lista)
                    elif sub_opcao == 4:
                        matricula = self.usuario_view.pega_matricula_usuario()
                        resultado = self.usuario_controller.excluir_usuario(matricula)
                        self.usuario_view.mostra_mensagem(resultado["mensagem"])
                    elif sub_opcao == 5:
                        matricula = self.usuario_view.pega_matricula_usuario()
                        usuario = self.usuario_controller.buscar_usuario_por_matricula(matricula)
                        if usuario:
                            if not self.eventos:
                                self.usuario_view.mostra_mensagem("Nenhum evento disponível.")
                                continue
                            self.evento_view.mostra_eventos(self.eventos)
                            idx = int(input("Escolha o número do evento: ")) - 1
                            if 0 <= idx < len(self.eventos):
                                evento = self.eventos[idx]
                                self.comprar_ingresso(matricula, evento)
                            else:
                                self.usuario_view.mostra_mensagem("Evento inválido.")
                        else:
                            self.usuario_view.mostra_mensagem("Usuário não encontrado.")
                    elif sub_opcao == 6:
                        matricula = self.usuario_view.pega_matricula_usuario()
                        self.listar_ingressos_usuario(matricula)
                    elif sub_opcao == 7:
                        matricula = self.usuario_view.pega_matricula_usuario()
                        usuario = self.usuario_controller.buscar_usuario_por_matricula(matricula)
                        if usuario:
                            if not self.eventos:
                                self.usuario_view.mostra_mensagem("Nenhum evento disponível.")
                                continue
                            self.evento_view.mostra_eventos(self.eventos)
                            idx = int(input("Escolha o número do evento: ")) - 1
                            if 0 <= idx < len(self.eventos):
                                evento = self.eventos[idx]
                                dados = self.usuario_view.pega_dados_avaliacao()
                                self.avaliar_evento(matricula, evento, dados["nota"], dados["comentario"])
                            else:
                                self.usuario_view.mostra_mensagem("Evento inválido.")
                        else:
                            self.usuario_view.mostra_mensagem("Usuário não encontrado.")
                    elif sub_opcao == 0:
                        break
                    else:
                        self.usuario_view.mostra_mensagem("Opção inválida. Tente novamente.")
            elif opcao == 2:
                while True:
                    sub_opcao = self.evento_view.tela_opcoes()
                    if sub_opcao == 1:
                        dados = self.evento_view.pega_dados_evento()
                        self.adicionar_evento(dados["nome"], dados["data"], dados["local"], dados["preco_entrada"])
                    elif sub_opcao == 3:
                        self.evento_view.mostra_eventos(self.eventos)
                    elif sub_opcao == 0:
                        break
                    else:
                        self.evento_view.mostra_mensagem("Opção inválida. Tente novamente.")
            elif opcao == 3:
                while True:
                    print("-------- INGRESSOS ----------")
                    print("1 - Listar Ingressos de Usuário")
                    print("0 - Retornar")
                    sub_opcao = int(input("Escolha a opção: "))
                    if sub_opcao == 1:
                        matricula = input("Matrícula do usuário: ")
                        self.listar_ingressos_usuario(matricula)
                    elif sub_opcao == 0:
                        break
                    else:
                        self.ingresso_view.mostra_mensagem("Opção inválida. Tente novamente.")
            elif opcao == 0:
                self.main_view.mostra_mensagem_encerramento()
                break
            else:
                self.main_view.mostra_mensagem("Opção inválida. Tente novamente.")