class EntidadeNaoEncontradaException(Exception):
    def __init__(self, mensagem: str, entidade: str = None, identificador: str = None):
        """
        Exceção lançada quando uma entidade não é encontrada no sistema.
        
        Args:
            mensagem: Mensagem de erro personalizada
            entidade: Tipo de entidade (opcional, para compatibilidade)
            identificador: Identificador da entidade (opcional, para compatibilidade)
        """
        if entidade and identificador:
            # Formato antigo com entidade e identificador
            mensagem_completa = f"ERRO: {entidade} com identificador '{identificador}' não foi encontrado."
        else:
            # Formato novo com mensagem direta
            mensagem_completa = mensagem
        
        super().__init__(mensagem_completa)
        self.mensagem = mensagem_completa
        self.entidade = entidade
        self.identificador = identificador