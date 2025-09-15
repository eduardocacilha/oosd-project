try:
    from .produto import Produto
except ImportError:
    from produto import Produto  # type: ignore


class Copo(Produto):
    def __init__(self, id_produto: int, nome: str, preco: float, estoque: int, capacidade_ml: int, material: str):
        super().__init__(id_produto=id_produto, nome=nome, preco=preco, estoque=estoque)
        self.__capacidade_ml = int(capacidade_ml)
        self.__material = material

    def descricao(self):
        return f"Copo {self.nome} {self.__capacidade_ml}ml {self.__material}"

    @property
    def capacidade_ml(self):
        return self.__capacidade_ml

    @capacidade_ml.setter
    def capacidade_ml(self, value):
        self.__capacidade_ml = int(value)

    @property
    def material(self):
        return self.__material

    @material.setter
    def material(self, value):
        self.__material = str(value)
