from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .usuario import Usuario
    from .evento import Evento

from .item_venda import ItemVenda

class Venda:
    _registros = []
    _next_id = 1

    def __init__(self, usuario: 'Usuario', evento: 'Evento', metodo_pagamento: str):
        self.__id_venda = Venda._next_id
        Venda._next_id += 1
        
        self.__usuario = usuario
        self.__evento = evento
        self.__metodo_pagamento = metodo_pagamento
        self.__data_hora = datetime.now()
        self.__itens: List[ItemVenda] = []
        
        Venda._registros.append(self)
        
        usuario.adicionar_venda_historico(self)

    def adicionar_item(self, item: ItemVenda):
        
        if item.produto.verificar_estoque(item.quantidade):
            item.produto.baixar_estoque(item.quantidade)
            self.__itens.append(item)
        else:
            raise ValueError(f"Estoque insuficiente para {item.produto.nome}")

    @property
    def total(self) -> float:
        return sum(item.subtotal for item in self.__itens)

    @property
    def id_venda(self) -> int:
        return self.__id_venda

    @property
    def usuario(self) -> 'Usuario':
        return self.__usuario

    @property
    def evento(self) -> 'Evento':
        return self.__evento

    @property
    def metodo_pagamento(self) -> str:
        return self.__metodo_pagamento

    @property
    def data_hora(self) -> datetime:
        return self.__data_hora

    @property
    def itens(self) -> List[ItemVenda]:
        return self.__itens.copy()

    @classmethod
    def get_all(cls):
        return cls._registros.copy()

    @classmethod
    def get_by_usuario(cls, usuario: 'Usuario'):
        return [venda for venda in cls._registros if venda.usuario == usuario]

    def __str__(self) -> str:
        return f"Venda {self.__id_venda} - {self.__usuario.nome} - {self.__evento.nome} - R$ {self.total:.2f}"