try:
    from .produto import Produto
except ImportError:
    from produto import Produto  # type: ignore


class Bebida(Produto):
    def __init__(self, id_produto: int, nome: str, preco: float, estoque: int, volume_ml: int, teor_alcoolico: float):
        super().__init__(id_produto=id_produto, nome=nome, preco=preco, estoque=estoque)
        self.__volume_ml = int(volume_ml)
        self.__teor_alcoolico = float(teor_alcoolico)

    def descricao(self):
        alc = f" {self.__teor_alcoolico:.1f}%" if self.__teor_alcoolico else ""
        return f"Bebida {self.nome} {self.__volume_ml}ml{alc}"

    @property
    def volume_ml(self):
        return self.__volume_ml

    @volume_ml.setter
    def volume_ml(self, value):
        self.__volume_ml = int(value)

    @property
    def teor_alcoolico(self):
        return self.__teor_alcoolico

    @teor_alcoolico.setter
    def teor_alcoolico(self, value):
        self.__teor_alcoolico = float(value)
