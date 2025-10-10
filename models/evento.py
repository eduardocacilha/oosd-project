class Evento:
    def __init__(self, nome: str, data: str, local: str, preco_entrada: float):
        self.__nome = nome
        self.__data = data
        self.__local = local
        self.__preco_entrada = preco_entrada
        self.__feedbacks = []

    def adicionar_feedback(self, feedback):
        self.__feedbacks.append(feedback)

    @property
    def nome(self):
        return self.__nome

    @property
    def data(self):
        return self.__data

    @property
    def local(self):
        return self.__local

    @property
    def preco_entrada(self):
        return self.__preco_entrada

    @property
    def feedbacks(self):
        return self.__feedbacks

    def __str__(self):
        return f"{self.nome} - {self.data} - {self.local} - R$ {self.preco_entrada:.2f}"