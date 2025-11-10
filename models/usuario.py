from __future__ import annotations
from datetime import date
from typing import List, Optional
from .venda import Venda
from .feedback import Feedback
from .evento import Evento

class Usuario:
    _registros: List['Usuario'] = []
    _next_id = 1

    def __init__(self, matricula: str, nome: str, email: str):
        if not matricula.isdigit():
            raise ValueError("Matrícula deve conter apenas números")
        
        self.__matricula = matricula
        self.__nome = nome
        self.__email = email
        self.__historico_compras: List[Venda] = []
        self.__ingressos_comprados: List['Ingresso'] = []
        Usuario._registros.append(self)

    @classmethod
    def get_by_matricula(cls, matricula: str) -> Optional['Usuario']:
        for u in cls._registros:
            if u.matricula == matricula:
                return u
        return None

    @classmethod
    def get_all(cls) -> List['Usuario']:
        return list(cls._registros)

    @classmethod
    def remove(cls, usuario: 'Usuario'):
        if usuario in cls._registros:
            cls._registros.remove(usuario)

    def comprar_ingresso(self, evento: Evento, preco: Optional[float] = None, metodo_pagamento: str = "Não informado") -> 'Ingresso':
        from .ingresso import Ingresso
        if preco is None:
            preco = getattr(evento, 'preco_entrada', 0.0)

        ingresso = Ingresso(evento, self, date.today(), preco, metodo_pagamento)
        self.__ingressos_comprados.append(ingresso)
        
        if hasattr(evento, 'registrar_compra_ingresso'):
            evento.registrar_compra_ingresso(ingresso)
        
        return ingresso
        
    def colocar_ingresso_a_venda(self, ingresso: 'Ingresso', novo_preco: float):
        if ingresso not in self.__ingressos_comprados:
            raise ValueError("Este ingresso não pertence a este usuário.")
        
        ingresso.preco = novo_preco
        ingresso.revendedor = self

    def remover_ingresso_da_venda(self, ingresso: 'Ingresso'):
        if ingresso.revendedor != self:
            raise ValueError("Este ingresso não está sendo revendido por você.")
        
        ingresso.revendedor = None

    def adicionar_venda_historico(self, venda: Venda):
        self.__historico_compras.append(venda)

    def listar_ingressos(self) -> List['Ingresso']:
        return list(self.__ingressos_comprados)
    @property
    def matricula(self) -> str:
        return self.__matricula

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, value: str):
        self.__nome = value

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str):
        self.__email = value
        
    @property
    def historico_compras(self) -> List[Venda]:
        return self.__historico_compras

    @property 
    def ingressos_comprados(self) -> List['Ingresso']:
        return self.__ingressos_comprados