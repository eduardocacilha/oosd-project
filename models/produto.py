from abc import ABC, abstractmethod
from exceptions.entidadeNaoEncontradaException import EntidadeNaoEncontradaException
from exceptions.regraDeNegocioException import RegraDeNegocioException


class Produto(ABC):

    def __init__(self, nome: str, preco: float, estoque: int):
        if not nome or not nome.strip():
            raise RegraDeNegocioException("Nome do produto não pode estar vazio.")
        if not isinstance(preco, (int, float)) or preco < 0:
            raise RegraDeNegocioException("Preço deve ser um número não negativo.")
        if not isinstance(estoque, int) or estoque < 0:
            raise RegraDeNegocioException(
                "Estoque deve ser um número inteiro não negativo."
            )
        self.__nome = nome.strip()
        self.__preco = float(preco)
        self.__estoque = estoque

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise RegraDeNegocioException("Nome do produto não pode estar vazio.")
        self.__nome = valor.strip()

    @property
    def preco(self) -> float:
        return self.__preco

    @preco.setter
    def preco(self, valor: float):
        if not isinstance(valor, (int, float)) or valor < 0:
            raise RegraDeNegocioException("Preço deve ser um número não negativo.")
        self.__preco = float(valor)

    @property
    def estoque(self) -> int:
        return self.__estoque

    @estoque.setter
    def estoque(self, valor: int):
        if not isinstance(valor, int) or valor < 0:
            raise RegraDeNegocioException(
                "Estoque deve ser um número inteiro não negativo."
            )
        self.__estoque = valor

    def verificar_estoque(self, quantidade: int = 1) -> bool:
        return self.__estoque >= quantidade

    def baixar_estoque(self, quantidade: int):
        if not self.verificar_estoque(quantidade):
            raise RegraDeNegocioException(
                f"Estoque insuficiente. Disponível: {self.__estoque}"
            )
        self.__estoque -= quantidade

    @abstractmethod
    def calcular_preco_final(self) -> float:
        pass

    def __str__(self) -> str:
        return f"{self.__nome} - R$ {self.__preco:.2f} - Estoque: {self.__estoque}"
