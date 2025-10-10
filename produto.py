from abc import ABC, abstractmethod


class Produto(ABC):
    def __init__(self, id_produto: int, nome: str, preco: float, estoque: int):
        self.__id_produto = id_produto
        self.__nome = nome
        self.__preco = float(preco)
        self.__estoque = int(estoque)

    def verificar_estoque(self, quantidade: int):
        return self.__estoque >= quantidade

    def baixar_estoque(self, quantidade: int):
        if quantidade < 0:
            raise ValueError("Quantidade negativa")
        if not self.verificar_estoque(quantidade):
            raise ValueError("Estoque insuficiente")
        self.__estoque -= quantidade

    @abstractmethod
    def descricao(self) -> str:
        ...

    @property
    def id_produto(self):
        return self.__id_produto

    @property
    def nome(self):
        return self.__nome

    @property
    def preco(self):
        return self.__preco

    @preco.setter
    def preco(self, value):
        self.__preco = float(value)

    @property
    def estoque(self):
        return self.__estoque

    @estoque.setter
    def estoque(self, value):
        self.__estoque = int(value)
