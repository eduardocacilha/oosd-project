class EventoController:
    def __init__(self, evento_model, evento_view):
        self.evento_model = evento_model
        self.evento_view = evento_view

    def listar_eventos(self):
        eventos = self.evento_model.obter_todos_eventos()
        self.evento_view.exibir_eventos(eventos)

    def criar_evento(self, nome, data, local, preco_entrada):
        novo_evento = self.evento_model.criar_evento(nome, data, local, preco_entrada)
        self.evento_view.exibir_evento_criado(novo_evento)

    def avaliar_evento(self, evento, usuario, nota, comentario):
        feedback = usuario.avaliar_evento(evento, nota, comentario)
        self.evento_view.exibir_feedback(feedback)

    def registrar_compra_ingresso(self, ingresso):
        self.evento_model.registrar_compra_ingresso(ingresso)
        self.evento_view.exibir_compra_registrada(ingresso)