from datetime import datetime
from typing import List, TYPE_CHECKING
from exceptions.entidadeNaoEncontradaException import EntidadeNaoEncontradaException
from exceptions.regraDeNegocioException import RegraDeNegocioException

if TYPE_CHECKING:
    from .usuario import Usuario
    from .evento import Evento

from .item_venda import ItemVenda
from .produto import Produto

class Venda:
    _registros = []
    _next_id = 1

    def __init__(self, usuario: 'Usuario', evento: 'Evento', metodo_pagamento: str):

        if not usuario:
            raise RegraDeNegocioException("Usuário não pode ser nulo.")

        if not evento:
            raise RegraDeNegocioException("Evento não pode ser nulo.")

        if not metodo_pagamento or not metodo_pagamento.strip():
            raise RegraDeNegocioException("Método de pagamento não pode estar vazio.")

        self.__id_venda = Venda._next_id
        Venda._next_id += 1

        self.__usuario = usuario
        self.__evento = evento
        self.__metodo_pagamento = metodo_pagamento.strip()
        self.__data_hora = datetime.now()
        self.__itens: List[ItemVenda] = []

        Venda._registros.append(self)

        usuario.adicionar_venda_historico(self)

    def adicionar_item(self, produto: Produto, quantidade: int):

        if not produto:
            raise RegraDeNegocioException("Produto não pode ser nulo.")

        if not isinstance(quantidade, int) or quantidade <= 0:
            raise RegraDeNegocioException("Quantidade deve ser um número inteiro positivo.")

        preco_do_momento = produto.preco
        itemvenda = ItemVenda(produto, quantidade, preco_do_momento)

        if itemvenda.produto.verificar_estoque(itemvenda.quantidade):
            itemvenda.produto.baixar_estoque(itemvenda.quantidade)
            self.__itens.append(itemvenda)
        else:
            raise RegraDeNegocioException(f"Estoque insuficiente para {itemvenda.produto.nome}")

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
        if not usuario:
            raise RegraDeNegocioException("Usuário não pode ser nulo.")
        return [venda for venda in cls._registros if venda.usuario == usuario]

    def __str__(self) -> str:
        return f"Venda {self.__id_venda} - {self.__usuario.nome} - {self.__evento.nome} - R$ {self.total:.2f}"
