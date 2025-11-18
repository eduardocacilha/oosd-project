from .produto import Produto
from exceptions.regraDeNegocioException import RegraDeNegocioException

class Copo(Produto):
    def __init__(self, nome: str, preco: float, estoque: int, capacidade_ml: int, material: str):

        if not isinstance(capacidade_ml, int) or capacidade_ml <= 0:
            raise RegraDeNegocioException("Capacidade deve ser um número inteiro positivo.")

        if not material or not material.strip():
            raise RegraDeNegocioException("Material do copo não pode estar vazio.")

        super().__init__(nome, preco, estoque)
        self.__capacidade_ml = capacidade_ml
        self.__material = material.strip()

    def calcular_preco_final(self) -> float:
        return self.preco

    @property
    def capacidade_ml(self) -> int:
        return self.__capacidade_ml

    @property
    def material(self) -> str:
        return self.__material

    def __str__(self) -> str:
        return f"Copo {self.nome} - {self.__material} - {self.__capacidade_ml}ml - R$ {self.preco:.2f} - Estoque: {self.estoque}"
