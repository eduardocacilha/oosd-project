class RegraDeNegocioException(Exception):
    #
    # Exceção genérica para violações de regras de negócio.
    # Ex: Estoque insuficiente, exclusão de usuário com ingressos, etc.
    #
    def __init__(self, mensagem: str):
        # Apenas repassa a mensagem de erro específica
        super().__init__(mensagem)