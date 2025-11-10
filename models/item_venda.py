try:
    from .produto import Produto
except ImportError:
    from models.produto import Produto

class ItemVenda:
    def __init__(self, produto: Produto, quantidade: int, preco_unitario_momento: float):
        self.__produto = produto
        self.__quantidade = int(quantidade)
        self.__preco_unitario_momento = float(preco_unitario_momento)

    @property
    def subtotal(self) -> float:
        return round(self.__quantidade * self.__preco_unitario_momento, 2)

    @property
    def produto(self):
        return self.__produto

    @property
    def quantidade(self):
        return self.__quantidade

    @property
    def preco_unitario_momento(self):
        return self.__preco_unitario_momento