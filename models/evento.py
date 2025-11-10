from datetime import date
from typing import List
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .ingresso import Ingresso

from .feedback import Feedback

class Evento:
    _registros = []
    _next_id = 1
    def __init__(self, nome: str, data: date, local: str, preco_entrada: float):
        self.__nome = nome
        self.__data = data
        self.__local = local
        self.__preco_entrada = preco_entrada

        self.__feedbacks: List[Feedback] = []
        self.__ingressos: List["Ingresso"] = []
        self.__ingressos_vendidos: List["Ingresso"] = []

        self.id_evento = Evento._next_id
        Evento._next_id += 1
        Evento._registros.append(self)

    @classmethod
    def add(cls, evento: "Evento"):
        cls._registros.append(evento)

    @classmethod
    def get_by_id(cls, id_evento: int):
        for ev in cls._registros:
            if getattr(ev, "id_evento", None) == id_evento:
                return ev
        return None

    @classmethod
    def get_all(cls):
        return list(cls._registros)

    @classmethod
    def remove(cls, evento: "Evento"):
        if evento in cls._registros:
            cls._registros.remove(evento)

    def adicionar_feedback(self, feedback: Feedback):
        self.__feedbacks.append(feedback)

    def registrar_compra_ingresso(self, ingresso: "Ingresso"):
        self.__ingressos_vendidos.append(ingresso)

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def data(self) -> date:
        return self.__data

    @property
    def local(self) -> str:
        return self.__local

    @property
    def preco_entrada(self) -> float:
        return self.__preco_entrada

    @property
    def feedbacks(self) -> List[Feedback]:
        return self.__feedbacks

    @property
    def ingressos_vendidos(self) -> List["Ingresso"]:
        return self.__ingressos_vendidos

    @property
    def ingressos(self) -> List["Ingresso"]:
        return self.__ingressos

    @data.setter
    def data(self, nova_data: date):
        self.__data = nova_data

    @local.setter
    def local(self, novo_local: str):
        self.__local = novo_local

    @preco_entrada.setter
    def preco_entrada(self, novo_preco: float):
        if novo_preco >= 0:
            self.__preco_entrada = novo_preco

    def __str__(self) -> str:
        data_formatada = self.__data.strftime('%d/%m/%Y')
        return f"{self.nome} - {data_formatada} - {self.local} - R$ {self.preco_entrada:.2f}"