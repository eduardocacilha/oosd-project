try:
    from .item_venda import ItemVenda
    from .produto import Produto
except ImportError:
    from item_venda import ItemVenda  # type: ignore
    from produto import Produto  # type: ignore
from datetime import datetime
from typing import List

class Venda:
    def __init__(self, id_venda: int, metodo_pagamento: str, data_hora: datetime):
        self.__id_venda = id_venda
        self.__metodo_pagamento = metodo_pagamento
        self.__data_hora = data_hora or datetime.now()
        self.__itens: List[ItemVenda] = []

    @property
    def valor_total(self):
        return round(sum(i.subtotal for i in self.__itens), 2)

    @property
    def itens(self):
        return self.__itens

    @property
    def id_venda(self):
        return self.__id_venda

    @property
    def metodo_pagamento(self):
        return self.__metodo_pagamento

    @property
    def data_hora(self):
        return self.__data_hora

    def adicionar_item(self, produto: Produto, quantidade: int):
        if quantidade <= 0:
            print("Quantidade deve ser positiva")
            return
        if not produto.verificar_estoque(quantidade):
            print("Estoque insuficiente")
            return
        produto.baixar_estoque(quantidade)
        self.__itens.append(ItemVenda(produto=produto, quantidade=quantidade, preco_unitario_momento=produto.preco))

    def finalizar_venda(self):
        return self.valor_total

    def calcular_total(self):
        return self.valor_total
