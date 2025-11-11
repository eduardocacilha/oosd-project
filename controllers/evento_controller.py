from datetime import datetime
import FreeSimpleGUI as sg
from models.evento import Evento
import FreeSimpleGUI as sg
from views.evento_view import EventoView
from controllers.usuario_controller import UsuarioController
from models.feedback import Feedback

class EventoController:
    
    def __init__(self, evento_view: EventoView, usuario_controller: UsuarioController):
        self.__view = evento_view
        self.__usuario_controller = usuario_controller
        self.__eventos = []
        
        
    def rodar_menu_evento(self):
        while True:
            # 1. Chama a View, que abre a janela de menu e retorna o NÚMERO (int)
            opcao = self.__view.tela_opcoes() # <--- Chama seu novo método da GUI

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
                    break # Volta para o MainController
            
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
        
        # 1. Pede os dados à View (que abre a janela de formulário)
        dados_evento = self.__view.pega_dados_evento()
        
        # 2. Se o usuário cancelou (View retornou None)
        if dados_evento is None:
            return # Simplesmente volta para o menu de eventos

        # 3. Lógica de Negócio (exatamente como no seu controller antigo)
        if self.buscar_evento_por_nome(dados_evento["nome"]):
            self.__view.mostrar_popup("Erro", f"ERRO: O evento '{dados_evento['nome']}' já existe.")
            return
        
        # 4. A View já validou o formato, agora o Controller converte o tipo
        try:
            data_obj = datetime.strptime(dados_evento["data"], '%d/%m/%Y').date()
        except ValueError:
            # Esta verificação é uma segurança extra caso a View falhe
            self.__view.mostrar_popup("Erro", "ERRO: Formato de data inválido. Use DD/MM/AAAA.")
            return

        # 5. Chama o Model para criar a instância
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
            # A View 'mostra_eventos' já trata isso, mas é bom ter a guarda.
            self.__view.mostra_eventos([])
            return
        
        # 1. Formata os dados para a View
        dados_para_view = [self._transformar_evento_para_view(e) for e in self.__eventos]
        
        # 2. Chama a View para exibir a janela da tabela
        self.__view.mostra_eventos(dados_para_view)

    def ver_detalhes_evento(self):
        """Fluxo para ver detalhes (incluindo nota média)."""
        
        # 1. Pede à View para selecionar um evento (retorna um índice)
        dados_para_selecao = [self._transformar_evento_para_view(e) for e in self.__eventos]
        indice_escolhido = self.__view.seleciona_evento(dados_para_selecao)

        # 2. Se o usuário selecionou algo (não cancelou)
        if indice_escolhido is not None:
            evento_selecionado = self.__eventos[indice_escolhido]

            # 3. Lógica de Negócio (exatamente como no seu controller antigo)
            feedbacks = evento_selecionado.feedbacks
            nota_media = None
            total_avaliacoes = len(feedbacks)
            if total_avaliacoes > 0:
                nota_media = sum([fb.nota for fb in feedbacks]) / total_avaliacoes

            # 4. Prepara os dados e chama a View
            dados_detalhados = self._transformar_evento_para_view(evento_selecionado)
            dados_detalhados['nota_media'] = nota_media
            dados_detalhados['total_avaliacoes'] = total_avaliacoes

            self.__view.mostra_detalhes_evento(dados_detalhados)

    def ver_feedbacks_evento(self):
        """Fluxo para ver feedbacks de um evento."""
        
        # 1. Pede à View para selecionar um evento
        dados_para_selecao = [self._transformar_evento_para_view(e) for e in self.__eventos]
        indice_escolhido = self.__view.seleciona_evento(dados_para_selecao)

        # 2. Se o usuário selecionou algo
        if indice_escolhido is not None:
            evento_selecionado = self.__eventos[indice_escolhido]
            feedbacks_objetos = evento_selecionado.feedbacks

            # 3. Formata os dados para a View
            dados_feedbacks = []
            for fb in feedbacks_objetos:
                dados_feedbacks.append({
                    "nome_usuario": fb.usuario.nome,
                    "nota": fb.nota,
                    "comentario": fb.comentario,
                    "data": fb.data.strftime('%d/%m/%Y')
                })
            
            # 4. Chama a View
            self.__view.mostra_feedbacks(dados_feedbacks)

    def excluir_evento(self):
        """Fluxo para excluir um evento."""
        
        # 1. Pede à View para selecionar um evento
        dados_para_selecao = [self._transformar_evento_para_view(e) for e in self.__eventos]
        indice_escolhido = self.__view.seleciona_evento(dados_para_selecao)

        # 2. Se o usuário selecionou algo
        if indice_escolhido is not None:
            evento_a_excluir = self.__eventos[indice_escolhido]
            
            # 3. Lógica de Negócio (exatamente como no seu controller antigo)
            if hasattr(evento_a_excluir, 'ingressos_vendidos') and len(evento_a_excluir.ingressos_vendidos) > 0:
                self.__view.mostrar_popup("Erro", "ERRO: Não é possível excluir um evento que já possui ingressos vendidos.")
                return
                
            # 4. Modifica o Model
            self.__eventos.remove(evento_a_excluir)
            self.__view.mostrar_popup("Sucesso", "Evento excluído com sucesso!")

    def alterar_evento(self):
        """Fluxo para alterar um evento."""
        
        if not self.__eventos:
            self.__view.mostrar_popup("Erro", "Nenhum evento cadastrado.")
            return

        # 1. Pede à View para selecionar
        dados_para_view = [self._transformar_evento_para_view(e) for e in self.__eventos]
        indice_escolhido = self.__view.seleciona_evento(dados_para_view)
        
        if indice_escolhido is None:
            return # Usuário cancelou a seleção

        evento = self.__eventos[indice_escolhido]
        self.__view.mostrar_popup("Alterando Evento", f"Alterando evento: {evento.nome}")

        # 2. Pede à View os novos dados
        novos_dados = self.__view.pega_dados_evento()
        if novos_dados is None:
            return # Usuário cancelou a alteração
        
        # 3. Lógica de Negócio (exatamente como no seu controller antigo)
        try:
            nova_data = datetime.strptime(novos_dados["data"], "%d/%m/%Y").date()
        except ValueError:
            self.__view.mostrar_popup("Erro", "ERRO: Formato de data inválido. Use DD/MM/AAAA.")
            return
        
        # 4. Modifica o Model (usando setters, se existirem)
        evento.data = nova_data
        evento.local = novos_dados["local"]
        evento.preco_entrada = novos_dados["preco_entrada"]
        # (O nome não é alterado para manter a consistência, mas poderia ser)

        self.__view.mostrar_popup("Sucesso", "Evento alterado com sucesso!")

    def avaliar_evento(self):
        """Fluxo para um usuário avaliar um evento."""
        
        # (Assumindo que seu UsuarioController tem 'buscar_usuario_por_matricula'
        # e seu UsuarioView tem 'pega_matricula_usuario' e 'pega_dados_avaliacao' ADAPTADOS)
        
        # 1. Obter o usuário
        matricula = self.__usuario_controller.pega_matricula_usuario_gui() # Método GUI do UsuarioView
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
        dados_avaliacao = self.__usuario_controller.pega_dados_avaliacao_gui() # Método GUI do UsuarioView
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