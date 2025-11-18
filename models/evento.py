from datetime import date
from typing import List
from typing import TYPE_CHECKING
from exceptions.entidadeNaoEncontradaException import EntidadeNaoEncontradaException
from exceptions.regraDeNegocioException import RegraDeNegocioException

if TYPE_CHECKING:
    from .ingresso import Ingresso

from .feedback import Feedback

class Evento:
    _registros = []
    _next_id = 1

    def __init__(self, nome: str, data: date, local: str, preco_entrada: float):

        if not nome or not nome.strip():
            raise RegraDeNegocioException("Nome do evento não pode estar vazio.")

        if not isinstance(data, date):
            raise RegraDeNegocioException("Data deve ser um objeto date válido.")

        if data < date.today():
            raise RegraDeNegocioException("Data do evento não pode ser no passado.")

        if not local or not local.strip():
            raise RegraDeNegocioException("Local do evento não pode estar vazio.")

        if preco_entrada < 0:
            raise RegraDeNegocioException("Preço de entrada não pode ser negativo.")

        self.__nome = nome.strip()
        self.__data = data
        self.__local = local.strip()
        self.__preco_entrada = preco_entrada

        self.__feedbacks: List[Feedback] = []
        self.__ingressos: List["Ingresso"] = []
        self.__ingressos_vendidos: List["Ingresso"] = []

        self.id_evento = Evento._next_id
        Evento._next_id += 1
        Evento._registros.append(self)

    @classmethod
    def add(cls, evento: "Evento"):
        if not isinstance(evento, Evento):
            raise RegraDeNegocioException("Objeto deve ser uma instância de Evento.")
        cls._registros.append(evento)

    @classmethod
    def get_by_id(cls, id_evento: int):
        if not isinstance(id_evento, int) or id_evento <= 0:
            raise RegraDeNegocioException("ID do evento deve ser um número inteiro positivo.")

        for ev in cls._registros:
            if getattr(ev, "id_evento", None) == id_evento:
                return ev
        raise EntidadeNaoEncontradaException(f"Evento com ID {id_evento} não encontrado.")

    @classmethod
    def get_all(cls):
        return list(cls._registros)

    @classmethod
    def remove(cls, evento: "Evento"):
        if not isinstance(evento, Evento):
            raise RegraDeNegocioException("Objeto deve ser uma instância de Evento.")

        if evento not in cls._registros:
            raise EntidadeNaoEncontradaException("Evento não encontrado na lista de registros.")

        cls._registros.remove(evento)

    def adicionar_feedback(self, feedback: Feedback):
        if not isinstance(feedback, Feedback):
            raise RegraDeNegocioException("Feedback deve ser uma instância válida.")

        for fb in self.__feedbacks:
            if fb.usuario == feedback.usuario:
                raise RegraDeNegocioException("Usuário já avaliou este evento.")

        if self.__data > date.today():
            raise RegraDeNegocioException("Só é possível avaliar eventos que já ocorreram.")

        self.__feedbacks.append(feedback)

    def registrar_compra_ingresso(self, ingresso: "Ingresso"):
        if not ingresso:
            raise RegraDeNegocioException("Ingresso deve ser uma instância válida.")

        self.__ingressos_vendidos.append(ingresso)

    def registrar_venda(self, venda):
        """Registra uma venda no evento"""
        pass

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
        return self.__feedbacks.copy()

    @property
    def ingressos_vendidos(self) -> List["Ingresso"]:
        return self.__ingressos_vendidos.copy()

    @property
    def ingressos(self) -> List["Ingresso"]:
        return self.__ingressos.copy()

    @data.setter
    def data(self, nova_data: date):
        if not isinstance(nova_data, date):
            raise RegraDeNegocioException("Data deve ser um objeto date válido.")

        if nova_data < date.today():
            raise RegraDeNegocioException("Nova data não pode ser no passado.")

        if len(self.__ingressos_vendidos) > 0:
            raise RegraDeNegocioException("Não é possível alterar a data de um evento com ingressos vendidos.")

        self.__data = nova_data

    @local.setter
    def local(self, novo_local: str):
        if not novo_local or not novo_local.strip():
            raise RegraDeNegocioException("Local não pode estar vazio.")

        if len(self.__ingressos_vendidos) > 0:
            raise RegraDeNegocioException("Não é possível alterar o local de um evento com ingressos vendidos.")

        self.__local = novo_local.strip()

    @preco_entrada.setter
    def preco_entrada(self, novo_preco: float):
        if novo_preco < 0:
            raise RegraDeNegocioException("Preço de entrada não pode ser negativo.")

        if len(self.__ingressos_vendidos) > 0:
            raise RegraDeNegocioException("Não é possível alterar o preço de um evento com ingressos vendidos.")

        self.__preco_entrada = novo_preco

    def __str__(self) -> str:
        data_formatada = self.__data.strftime('%d/%m/%Y')
        return f"{self.nome} - {data_formatada} - {self.local} - R$ {self.preco_entrada:.2f}"