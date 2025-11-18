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
            raise RegraDeNegocioException("Estoque deve ser um número inteiro não negativo.")

        self.__nome = nome.strip()
        self.__preco = float(preco)
        self.__estoque = estoque

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def preco(self) -> float:
        return self.__preco

    @property
    def estoque(self) -> int:
        return self.__estoque
    
    def verificar_estoque(self, quantidade: int = 1) -> bool:
        """Verifica se há estoque suficiente"""
        return self.__estoque >= quantidade

    def baixar_estoque(self, quantidade: int):
        """Reduz o estoque - usado pela classe Venda"""
        if not self.verificar_estoque(quantidade):
            raise RegraDeNegocioException(f"Estoque insuficiente. Disponível: {self.__estoque}")
        self.__estoque -= quantidade

    @abstractmethod
    def calcular_preco_final(self) -> float:
        pass

    def __str__(self) -> str:
        return f"{self.__nome} - R$ {self.__preco:.2f} - Estoque: {self.__estoque}"