import FreeSimpleGUI as sg
from datetime import datetime, date
from typing import List, Optional, TYPE_CHECKING # <<< 1. MODIFIQUE ESTA LINHA
from models.evento import Evento
from models.feedback import Feedback
from views.evento_view import EventoView

if TYPE_CHECKING:
    from controllers.usuario_controller import UsuarioController

class EventoController:
    
 
    def __init__(self, evento_view: EventoView):
        self.__view = evento_view
        self.__usuario_controller: UsuarioController = None # Placeholder, será injetado
        self.__eventos: List[Evento] = []
        

    def set_usuario_controller(self, usuario_controller: 'UsuarioController'):
        """(Injetado pelo MainController) Recebe a instância do UsuarioController."""
        self.__usuario_controller = usuario_controller

    def get_view(self) -> EventoView:
        """Permite que outros controllers acessem a EventoView (para seleção)."""
        return self.__view

    def get_eventos_lista(self) -> List[Evento]:
        """Retorna a lista de objetos de evento."""
        return self.__eventos

    def selecionar_evento_gui(self) -> Evento | None:
        """
        Método público que o UsuarioController/IngressoController pode chamar.
        Ele usa a EventoView para selecionar um evento e retorna o OBJETO.
        """
        if not self.__eventos:
            self.__view.mostrar_popup("Erro", "Nenhum evento cadastrado.")
            return None
            
        dados_para_selecao = [self._transformar_evento_para_view(e) for e in self.__eventos]
        indice_escolhido = self.__view.seleciona_evento(dados_para_selecao)

        if indice_escolhido is not None:
            return self.__eventos[indice_escolhido]
        
        return None # Usuário cancelou
        

    def rodar_menu_evento(self):
        
        while True:
            opcao = self.__view.tela_opcoes() 

            try:
                if opcao == 1:
                    self.incluir_evento()
                
                elif opcao == 2:
                    self.alterar_evento() 
                
                elif opcao == 3:
                    self.listar_eventos()
                
                elif opcao == 4:
                    self.excluir_evento()
                    
                elif opcao == 5:
                    self.ver_detalhes_evento()
                    
                elif opcao == 6:
                    self.ver_feedbacks_evento()

                elif opcao == 0:
                    break 
            
            except Exception as e:
                self.__view.mostrar_popup("Erro Inesperado", f"Ocorreu um erro: {e}")



    def _transformar_evento_para_view(self, evento: Evento) -> dict:
        """Helper para formatar o objeto Evento para a View."""
        return {
            "nome": evento.nome,
            "data": evento.data.strftime('%d/%m/%Y'),
            "local": evento.local,
            "preco_entrada": evento.preco_entrada
        }
    
    def buscar_evento_por_nome(self, nome: str) -> Evento | None:
        """Busca um evento pelo nome, ignorando maiúsculas/minúsculas."""
        for evento in self.__eventos:
            if evento.nome.lower() == nome.lower():
                return evento
        return None

    def incluir_evento(self):
        """Fluxo de inclusão de evento."""
        
        dados_evento = self.__view.pega_dados_evento()
        
        if dados_evento is None:
            return 

        if self.buscar_evento_por_nome(dados_evento["nome"]):
            self.__view.mostrar_popup("Erro", f"ERRO: O evento '{dados_evento['nome']}' já existe.")
            return
        
        try:
            data_obj = datetime.strptime(dados_evento["data"], '%d/%m/%Y').date()
        except ValueError:
            self.__view.mostrar_popup("Erro", "ERRO: Formato de data inválido. A View deveria ter pego isso.")
            return

        novo_evento = Evento(
            nome=dados_evento["nome"],
            data=data_obj,
            local=dados_evento["local"],
            preco_entrada=dados_evento["preco_entrada"]
        )

        self.__eventos.append(novo_evento)
        self.__view.mostrar_popup("Sucesso", "Evento incluído com sucesso!")

    def listar_eventos(self):
        """Fluxo de listagem de eventos."""
        
        if not self.__eventos:
            self.__view.mostra_eventos([]) 
            return
        
        dados_para_view = [self._transformar_evento_para_view(e) for e in self.__eventos]
        self.__view.mostra_eventos(dados_para_view)

    def ver_detalhes_evento(self):
        """Fluxo para ver detalhes (incluindo nota média)."""
        
        dados_para_selecao = [self._transformar_evento_para_view(e) for e in self.__eventos]
        indice_escolhido = self.__view.seleciona_evento(dados_para_selecao)

        if indice_escolhido is not None:
            evento_selecionado = self.__eventos[indice_escolhido]

            feedbacks = evento_selecionado.feedbacks
            nota_media = None
            total_avaliacoes = len(feedbacks)
            if total_avaliacoes > 0:
                nota_media = sum([fb.nota for fb in feedbacks]) / total_avaliacoes

            dados_detalhados = self._transformar_evento_para_view(evento_selecionado)
            dados_detalhados['nota_media'] = nota_media
            dados_detalhados['total_avaliacoes'] = total_avaliacoes

            self.__view.mostra_detalhes_evento(dados_detalhados)

    def ver_feedbacks_evento(self):
        """Fluxo para ver feedbacks de um evento."""
        
        dados_para_selecao = [self._transformar_evento_para_view(e) for e in self.__eventos]
        indice_escolhido = self.__view.seleciona_evento(dados_para_selecao)

        if indice_escolhido is not None:
            evento_selecionado = self.__eventos[indice_escolhido]
            feedbacks_objetos = evento_selecionado.feedbacks

            dados_feedbacks = []
            for fb in feedbacks_objetos:
                dados_feedbacks.append({
                    "nome_usuario": fb.usuario.nome,
                    "nota": fb.nota,
                    "comentario": fb.comentario,
                    "data": fb.data.strftime('%d/%m/%Y')
                })
            
            self.__view.mostra_feedbacks(dados_feedbacks)

    def excluir_evento(self):
        """Fluxo para excluir um evento."""
        
        dados_para_selecao = [self._transformar_evento_para_view(e) for e in self.__eventos]
        indice_escolhido = self.__view.seleciona_evento(dados_para_selecao)

        if indice_escolhido is not None:
            evento_a_excluir = self.__eventos[indice_escolhido]
            
            # (Você precisará adicionar 'ingressos_vendidos' ao seu Model 'Evento')
            if hasattr(evento_a_excluir, 'ingressos_vendidos') and len(evento_a_excluir.ingressos_vendidos) > 0:
                self.__view.mostrar_popup("Erro", "ERRO: Não é possível excluir um evento que já possui ingressos vendidos.")
                return
                
            self.__eventos.remove(evento_a_excluir)
            self.__view.mostrar_popup("Sucesso", "Evento excluído com sucesso!")

    def alterar_evento(self):
        """Fluxo para alterar um evento."""
        
        if not self.__eventos:
            self.__view.mostrar_popup("Erro", "Nenhum evento cadastrado.")
            return

        dados_para_view = [self._transformar_evento_para_view(e) for e in self.__eventos]
        indice_escolhido = self.__view.seleciona_evento(dados_para_view)
        
        if indice_escolhido is None:
            return 

        evento = self.__eventos[indice_escolhido]
        self.__view.mostrar_popup("Alterando Evento", f"Alterando evento: {evento.nome}")

        novos_dados = self.__view.pega_dados_evento()
        if novos_dados is None:
            return 
        
        try:
            nova_data = datetime.strptime(novos_dados["data"], "%d/%m/%Y").date()
        except ValueError:
            self.__view.mostrar_popup("Erro", "ERRO: Formato de data inválido. Use DD/MM/AAAA.")
            return
        
        evento.data = nova_data
        evento.local = novos_dados["local"]
        evento.preco_entrada = novos_dados["preco_entrada"]

        self.__view.mostrar_popup("Sucesso", "Evento alterado com sucesso!")

    def avaliar_evento(self):
        """Fluxo para um usuário avaliar um evento."""
        
        if not self.__usuario_controller:
            self.__view.mostrar_popup("Erro", "Controlador de Usuário não inicializado.")
            return

        # 1. Obter o usuário
        matricula = self.__usuario_controller.pega_matricula_usuario_gui()
        if not matricula: return
        
        usuario = self.__usuario_controller.buscar_usuario_por_matricula(matricula)
        if not usuario:
            self.__view.mostrar_popup("Erro", "ERRO: Usuário não encontrado.")
            return

        # 2. Obter o evento
        if not self.__eventos:
            self.__view.mostrar_popup("Erro", "Nenhum evento cadastrado para avaliar.")
            return
        
        dados_para_view = [self._transformar_evento_para_view(e) for e in self.__eventos]
        indice_escolhido = self.__view.seleciona_evento(dados_para_view)
        if indice_escolhido is None:
            return

        evento_escolhido = self.__eventos[indice_escolhido]

        # 3. Obter os dados da avaliação
        dados_avaliacao = self.__usuario_controller.pega_dados_avaliacao_gui()
        if dados_avaliacao is None:
            return
            
        # 4. Chama o Model
        feedback = Feedback(
            usuario=usuario,
            evento=evento_escolhido,
            nota=dados_avaliacao["nota"],
            comentario=dados_avaliacao["comentario"],
            data=date.today()
        )

        evento_escolhido.adicionar_feedback(feedback)
        self.__view.mostrar_popup("Sucesso", f"Avaliação registrada com sucesso para o evento '{evento_escolhido.nome}'!")