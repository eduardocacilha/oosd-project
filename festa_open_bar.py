try:
    from .festa import Festa
    from .bebida import Bebida
except ImportError:
    from festa import Festa  # type: ignore
    from bebida import Bebida  # type: ignore


class FestaOpenBar(Festa):
    def __init__(self, nome: str, data: str, local: str, preco_entrada: float, preco_unico: float, bebidas_inclusas: list):
        super().__init__(nome=nome, data=data, local=local, preco_entrada=preco_entrada)
        self.__preco_unico = float(preco_unico)
        self.__bebidas_inclusas = list(bebidas_inclusas) if bebidas_inclusas else []

    def registrar_venda(self, venda):
        self.__vendas_realizadas.append(venda)
