from datetime import datetime

from models.evento import Evento

from views.evento_view import EventoView
from controllers.usuario_controller import UsuarioController

class EventoController:
    
    def __init__(self, evento_view: EventoView, usuario_controller: UsuarioController):
        self.__view = evento_view
        self.__usuario_controller = usuario_controller
        self.__eventos = []

    def _transformar_evento_para_view(self, evento: Evento) -> dict:
        
        return {
            "nome": evento.nome,
            "data": evento.data.strftime('%d/%m/%Y'),
            "local": evento.local,
            "preco_entrada": evento.preco_entrada
        }
    
    def buscar_evento_por_nome(self, nome: str) -> Evento | None:
        
        for evento in self.__eventos:
            if evento.nome.lower() == nome.lower():
                return evento
        return None

    def incluir_evento(self):
        dados_evento = self.__view.pega_dados_evento()

        if self.buscar_evento_por_nome(dados_evento["nome"]):
            self.__view.mostra_mensagem(f"ERRO: O evento '{dados_evento['nome']}' já existe.")
            return
        
        try:
            data_obj = datetime.strptime(dados_evento["data"], '%d/%m/%Y').date()
        except ValueError:
            self.__view.mostra_mensagem("ERRO: Formato de data inválido. Use DD/MM/AAAA.")
            return

        novo_evento = Evento(
            nome=dados_evento["nome"],
            data=data_obj,
            local=dados_evento["local"],
            preco_entrada=dados_evento["preco_entrada"]
        )

        self.__eventos.append(novo_evento)
        self.__view.mostra_mensagem("Evento incluído com sucesso!")

    def listar_eventos(self):
        if not self.__eventos:
            self.__view.mostra_mensagem("Nenhum evento cadastrado.")
            return
        
        dados_para_view = [self._transformar_evento_para_view(e) for e in self.__eventos]
        
        self.__view.mostra_eventos(dados_para_view)

    def ver_detalhes_evento(self):
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
        dados_para_selecao = [self._transformar_evento_para_view(e) for e in self.__eventos]
        indice_escolhido = self.__view.seleciona_evento(dados_para_selecao)

        if indice_escolhido is not None:
            evento_a_excluir = self.__eventos[indice_escolhido]
            
            if len(evento_a_excluir.ingressos_vendidos) > 0:
                self.__view.mostra_mensagem("ERRO: Não é possível excluir um evento que já possui ingressos vendidos.")
                return
                
            self.__eventos.remove(evento_a_excluir)
            self.__view.mostra_mensagem("Evento excluído com sucesso!")

        def alterar_evento(self):
            if not self.__eventos:
                self.__view.mostra_mensagem("Nenhum evento cadastrado.")
                return

            dados_para_view = [self._transformar_evento_para_view(e) for e in self.__eventos]
            indice_escolhido = self.__view.seleciona_evento(dados_para_view)
            if indice_escolhido is None:
                return

            evento = self.__eventos[indice_escolhido]
            self.__view.mostra_mensagem(f"Alterando evento: {evento.nome}")

            novos_dados = self.__view.pega_dados_evento()

            from datetime import datetime
            try:
                nova_data = datetime.strptime(novos_dados["data"], "%d/%m/%Y").date()
            except ValueError:
                self.__view.mostra_mensagem("ERRO: Formato de data inválido. Use DD/MM/AAAA.")
                return

            evento.data = nova_data
            evento.local = novos_dados["local"]
            evento.preco_entrada = novos_dados["preco_entrada"]

            self.__view.mostra_mensagem("Evento alterado com sucesso!")

    def avaliar_evento(self):
        
        from models.feedback import Feedback
        from datetime import date

        matricula = self.__usuario_controller._UsuarioController__view.pega_matricula_usuario()
        usuario = self.__usuario_controller.buscar_usuario_por_matricula(matricula)
        if not usuario:
            self.__view.mostra_mensagem("ERRO: Usuário não encontrado.")
            return

        if not self.__eventos:
            self.__view.mostra_mensagem("Nenhum evento cadastrado para avaliar.")
            return

        dados_para_view = [self._transformar_evento_para_view(e) for e in self.__eventos]
        indice_escolhido = self.__view.seleciona_evento(dados_para_view)
        if indice_escolhido is None:
            return

        evento_escolhido = self.__eventos[indice_escolhido]

        dados_avaliacao = self.__usuario_controller._UsuarioController__view.pega_dados_avaliacao()

        feedback = Feedback(
            usuario=usuario,
            evento=evento_escolhido,
            nota=dados_avaliacao["nota"],
            comentario=dados_avaliacao["comentario"],
            data=date.today()
        )

        evento_escolhido.adicionar_feedback(feedback)
        self.__view.mostra_mensagem(f"Avaliação registrada com sucesso para o evento '{evento_escolhido.nome}'!")