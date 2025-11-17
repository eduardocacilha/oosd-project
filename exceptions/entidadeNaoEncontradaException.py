class EntidadeNaoEncontradaException(Exception):
  
    # Exceção lançada quando uma entidade (ex: Usuário, Evento, Produto)
    # não é encontrada no sistema.
    
    def __init__(self, entidade: str, identificador: str):
        # Constrói a mensagem de erro de forma padronizada
        mensagem = f"ERRO: {entidade} com identificador '{identificador}' não foi encontrado."
        
        # Chama o __init__ da classe pai (Exception)
        super().__init__(mensagem)