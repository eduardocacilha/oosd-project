try:
    from .venda import Venda
    from .feedback import Feedback
    from .evento import Evento
except ImportError:
    from venda import Venda  # type: ignore
    from feedback import Feedback  # type: ignore
    from evento import Evento  # type: ignore
from datetime import date
from typing import List


class Ingresso:
    def __init__(self, evento, usuario: str, data_compra: date, preco: float):
        self.evento = evento
        self.usuario_matricula = usuario
        self.data_compra = data_compra
        self.preco = preco


class Usuario:
    def __init__(self, matricula: str, nome: str, email: str, adm: bool):
        self.__matricula = matricula
        self.__nome = nome
        self.__email = email
        self.__adm = bool(adm)
        self.__historico_compras: List[Venda] = []
        self.__ingressos_comprados: List[Ingresso] = []

    def fazer_login(self):
        return True

    def avaliar_evento(self, evento: Evento, nota: int, comentario: str):
        fb = Feedback(nota = nota, comentario = comentario, data = date.today())
        evento.adicionar_feedback(fb)
        return fb

    def ver_historico_compras(self):
        return list(self.__historico_compras)

    def adicionar_compra(self, venda: Venda):
        self.__historico_compras.append(venda)

    def comprar_ingresso(self, evento, preco: float = None):
        if preco is None:
            if hasattr(evento, 'preco_entrada'):
                preco = evento.preco_entrada
            else:
                preco = 0.0

        ingresso = Ingresso(evento, self.__matricula, date.today(), preco)
        self.__ingressos_comprados.append(ingresso)
        
        if hasattr(evento, 'registrar_compra_ingresso'):
            evento.registrar_compra_ingresso(ingresso)
        
        return ingresso

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

    @property
    def email(self):
        return self.__email

    @property
    def adm(self):
        return self.__adm

    @adm.setter
    def adm(self, value):
        self.__adm = bool(value)

    @property
    def historico_compras(self):
        return self.__historico_compras

    @property 
    def ingressos_comprados(self):
        return self.__ingressos_comprados
