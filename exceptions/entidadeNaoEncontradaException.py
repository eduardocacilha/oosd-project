class EntidadeNaoEncontradaException(Exception):

    def __init__(self, mensagem: str, entidade: str = None, identificador: str = None):
        if entidade and identificador:
            mensagem_completa = f"ERRO: {entidade} com identificador '{identificador}' não foi encontrado."
        else:
            mensagem_completa = mensagem
        super().__init__(mensagem_completa)
        self.mensagem = mensagem_completa
        self.entidade = entidade
        self.identificador = identificador
