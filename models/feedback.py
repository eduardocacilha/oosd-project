from datetime import date
from exceptions.entidadeNaoEncontradaException import EntidadeNaoEncontradaException
from exceptions.regraDeNegocioException import RegraDeNegocioException

class Feedback:
    def __init__(self, usuario, evento, nota: int, comentario: str, data: date):
        if not usuario:
            raise RegraDeNegocioException("Usuário não pode ser nulo.")

        if not evento:
            raise RegraDeNegocioException("Evento não pode ser nulo.")

        if not isinstance(nota, int) or nota < 1 or nota > 5:
            raise RegraDeNegocioException("Nota deve ser um número inteiro entre 1 e 5.")

        if not comentario or not comentario.strip():
            raise RegraDeNegocioException("Comentário não pode estar vazio.")

        if not isinstance(data, date):
            raise RegraDeNegocioException("Data deve ser um objeto date válido.")

        self.__usuario = usuario
        self.__evento = evento
        self.__nota = nota
        self.__comentario = comentario.strip()
        self.__data = data

    @property
    def usuario(self):
        return self.__usuario

    @property
    def evento(self):
        return self.__evento

    @property
    def nota(self) -> int:
        return self.__nota

    @property
    def comentario(self) -> str:
        return self.__comentario

    @property
    def data(self) -> date:
        return self.__data

    def __str__(self) -> str:
        return f"Feedback de {self.__usuario.nome} para {self.__evento.nome}: {self.__nota}/5 - {self.__comentario}"
