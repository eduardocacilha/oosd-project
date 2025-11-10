try:
    from .produto import Produto
except ImportError:
    from models.produto import Produto

class Camisa(Produto):
    def __init__(self, id_produto: int, nome: str, preco: float, estoque: int = 0, tamanho: str = "M", cor: str = "branca"):
        super().__init__(id_produto=id_produto, nome=nome, preco=preco, estoque=estoque)
        self.__tamanho = tamanho
        self.__cor = cor

    def descricao(self):
        return f"Camisa {self.nome} tam {self.__tamanho} cor {self.__cor}"

    @property
    def tamanho(self):
        return self.__tamanho

    @tamanho.setter
    def tamanho(self, value):
        self.__tamanho = str(value)

    @property
    def cor(self):
        return self.__cor

    @cor.setter
    def cor(self, value):
        self.__cor = str(value)