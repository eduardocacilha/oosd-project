from .produto import Produto
from exceptions.regraDeNegocioException import RegraDeNegocioException

class Camisa(Produto):
    def __init__(self, nome: str, preco: float, estoque: int, tamanho: str, cor: str):

        if not tamanho or not tamanho.strip():
            raise RegraDeNegocioException("Tamanho da camisa não pode estar vazio.")

        if not cor or not cor.strip():
            raise RegraDeNegocioException("Cor da camisa não pode estar vazia.")

        super().__init__(nome, preco, estoque)
        self.__tamanho = tamanho.strip()
        self.__cor = cor.strip()

    def calcular_preco_final(self) -> float:
        return self.preco

    @property
    def tamanho(self) -> str:
        return self.__tamanho

    @property
    def cor(self) -> str:
        return self.__cor

    def __str__(self) -> str:
        return f"Camisa {self.nome} - {self.__cor} - {self.__tamanho} - R$ {self.preco:.2f} - Estoque: {self.estoque}"
