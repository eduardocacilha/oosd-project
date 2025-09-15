from abc import ABC, abstractmethod
from typing import List
try:
    from .produto import Produto
    from .venda import Venda
    from .feedback import Feedback
except ImportError:
    from produto import Produto  # type: ignore
    from venda import Venda  # type: ignore
    from feedback import Feedback  # type: ignore


class Evento(ABC):
    def __init__(self, nome: str, data: str, local: str):
        self.__nome = nome
        self.__data = data
        self.__local = local
        self.__produtos: List[Produto] = []
        self.__feedbacks: List[Feedback] = []
        self.__ingressos_vendidos: List = []

    def adicionar_produto(self, produto: Produto):
        self.__produtos.append(produto)

    def adicionar_feedback(self, feedback: Feedback):
        self.__feedbacks.append(feedback)

    def listar_feedback(self):
        return list(self.__feedbacks)

    def registrar_compra_ingresso(self, ingresso):
        self.__ingressos_vendidos.append(ingresso)

    def listar_compradores_ingressos(self):
        return [(ing.usuario_matricula, ing.data_compra, ing.preco) for ing in self.__ingressos_vendidos]

    def obter_total_ingressos_vendidos(self):
        return len(self.__ingressos_vendidos)

    def obter_receita_ingressos(self):
        return sum(ing.preco for ing in self.__ingressos_vendidos)

    @property
    def produtos(self):
        return self.__produtos

    @property
    def feedbacks(self):
        return self.__feedbacks

    @property
    def ingressos_vendidos(self):
        return self.__ingressos_vendidos

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, value):
        self.__nome = str(value)

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        self.__data = value

    @property
    def local(self):
        return self.__local

    @local.setter
    def local(self, value):
        self.__local = str(value)

    def registrar_venda(self, venda: Venda):
        pass

    @abstractmethod
    def get_faturamento_total(self):
        ...
