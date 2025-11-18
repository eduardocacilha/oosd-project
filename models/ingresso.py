from __future__ import annotations
from datetime import date
from typing import Optional
from exceptions.entidadeNaoEncontradaException import EntidadeNaoEncontradaException
from exceptions.regraDeNegocioException import RegraDeNegocioException

from .evento import Evento

class Ingresso:
    _contador_id = 0
    _ingressos = []

    def __init__(self, evento: Evento, comprador: 'Usuario', data_compra: date, preco: float, metodo_pagamento: str = "Não informado"):

        if not evento:
            raise RegraDeNegocioException("Evento não pode ser nulo.")

        if not comprador:
            raise RegraDeNegocioException("Comprador não pode ser nulo.")

        if not isinstance(data_compra, date):
            raise RegraDeNegocioException("Data de compra deve ser um objeto date válido.")

        if data_compra > date.today():
            raise RegraDeNegocioException("Data de compra não pode ser no futuro.")

        if not isinstance(preco, (int, float)) or preco <= 0:
            raise RegraDeNegocioException("Preço deve ser um número maior que zero.")

        if not metodo_pagamento or not metodo_pagamento.strip():
            raise RegraDeNegocioException("Método de pagamento não pode estar vazio.")

        self.__id_ingresso = Ingresso._gerar_id()
        self.__evento = evento
        self.__comprador = comprador
        self.__data_compra = data_compra
        self.__preco = preco
        self.__metodo_pagamento = metodo_pagamento.strip()
        self.__revendedor: Optional['Usuario'] = None
        Ingresso._ingressos.append(self)

    @classmethod
    def _gerar_id(cls):
        cls._contador_id += 1
        return cls._contador_id

    @property
    def id_ingresso(self) -> int:
        return self.__id_ingresso

    @property
    def evento(self) -> Evento:
        return self.__evento

    @property
    def comprador(self) -> 'Usuario':
        return self.__comprador

    @property
    def data_compra(self) -> date:
        return self.__data_compra

    @property
    def preco(self) -> float:
        return self.__preco

    @property
    def metodo_pagamento(self) -> str:
        return self.__metodo_pagamento

    @property
    def revendedor(self) -> Optional['Usuario']:
        return self.__revendedor

    @preco.setter
    def preco(self, novo_preco: float):
        if not isinstance(novo_preco, (int, float)) or novo_preco <= 0:
            raise RegraDeNegocioException("Preço deve ser um número maior que zero.")
        self.__preco = novo_preco

    @revendedor.setter
    def revendedor(self, novo_revendedor: Optional['Usuario']):
        self.__revendedor = novo_revendedor

    @comprador.setter
    def comprador(self, novo_comprador: 'Usuario'):
        if not novo_comprador:
            raise RegraDeNegocioException("Comprador não pode ser nulo.")
        self.__comprador = novo_comprador

    @classmethod
    def get_all(cls):
        return cls._ingressos.copy()

    def __repr__(self) -> str:
        nome_comprador = self.comprador.nome if self.comprador else "N/A"
        return (f"Ingresso(id={self.id_ingresso}, evento={self.evento.nome}, "
                f"comprador={nome_comprador}, preco={self.preco})")
