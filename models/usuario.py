from datetime import date
from typing import List, Optional
from .venda import Venda
from .feedback import Feedback
from .evento import Evento
from .ingresso import Ingresso 

class Usuario:
    def __init__(self, matricula: str, nome: str, email: str): 
        self.__matricula = matricula
        self.__nome = nome
        self.__email = email
        self.__historico_compras: List[Venda] = []
        self.__ingressos_comprados: List[Ingresso] = []

    def avaliar_evento(self, evento: Evento, nota: int, comentario: str):
        fb = Feedback(
            usuario=self,
            evento=evento,
            nota=nota, 
            comentario=comentario, 
            data=date.today()
        )
        evento.adicionar_feedback(fb)
        return fb

    def ver_historico_compras(self):
        return list(self.__historico_compras)

    def adicionar_compra(self, venda: Venda):
        self.__historico_compras.append(venda)

    def comprar_ingresso(self, evento, preco: Optional[float] = None):
        if preco is None:
            if hasattr(evento, 'preco_entrada'):
                preco = evento.preco_entrada
            else:
                preco = 0.0

        ingresso = Ingresso(evento, self, date.today(), preco) 
        self.__ingressos_comprados.append(ingresso)
        
        if hasattr(evento, 'registrar_compra_ingresso'):
            evento.registrar_compra_ingresso(ingresso)
        
        return ingresso
        
    def listar_ingressos_a_venda(self, lista_ingressos_geral: List[Ingresso]):
        return [ing for ing in lista_ingressos_geral if ing.revendedor == self]

    def colocar_ingresso_a_venda(self, ingresso: Ingresso, novo_preco: float):
        if ingresso not in self.__ingressos_comprados:
            raise ValueError("Este ingresso não pertence a este usuário.")
            
        ingresso.preco = novo_preco
        ingresso.revendedor = self 
        return True

    def remover_ingresso_da_venda(self, ingresso: Ingresso):
        if ingresso.revendedor != self:
            raise ValueError("Este ingresso não está sendo revendido por você.")
        
        ingresso.revendedor = None
        return True

    def comprar_ingresso_revenda(self, ingresso: Ingresso):
        revendedor = ingresso.revendedor
        if revendedor is None:
            raise ValueError("Este ingresso não está em revenda.")
        
        if self == revendedor:
            raise ValueError("Você não pode comprar um ingresso de si mesmo.")
            
        venda_simulada = Venda(
            id_venda=0,
            metodo_pagamento="revenda", 
            data_hora=date.today()
        )
        self.adicionar_compra(venda_simulada)
        
        if ingresso in revendedor.ingressos_comprados:
            revendedor.ingressos_comprados.remove(ingresso)

        ingresso.revendedor = None
        ingresso.comprador = self 
        
        self.__ingressos_comprados.append(ingresso)
        
        return True

    def listar_ingressos(self):
        return list(self.__ingressos_comprados)

    def obter_ingressos_por_evento(self, evento):
        return [ing for ing in self.__ingressos_comprados if ing.evento == evento]

    @property
    def matricula(self):
        return self.__matricula

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, value):
        self._nome = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self._email = value
        
    @property
    def historico_compras(self):
        return self.__historico_compras

    @property 
    def ingressos_comprados(self):
        return self.__ingressos_comprados