class IngressoController:
    def __init__(self, ingresso_model, usuario_model):
        self.ingresso_model = ingresso_model
        self.usuario_model = usuario_model

    def comprar_ingresso(self, usuario, evento, preco=None):
        return usuario.comprar_ingresso(evento, preco)

    def listar_ingressos_comprados(self, usuario):
        return usuario.listar_ingressos()

    def colocar_ingresso_a_venda(self, usuario, ingresso, novo_preco):
        return usuario.colocar_ingresso_a_venda(ingresso, novo_preco)

    def remover_ingresso_da_venda(self, usuario, ingresso):
        return usuario.remover_ingresso_da_venda(ingresso)

    def comprar_ingresso_revenda(self, usuario, ingresso):
        return usuario.comprar_ingresso_revenda(ingresso)