from datetime import date


class Feedback:
    def __init__(self, nota: int, comentario: str, data: date):
        self.__nota = int(nota)
        self.__comentario = comentario
        self.__data = data

    def get_detalhes(self) -> str:
        return f"Nota: {self.__nota} | {self.__data.isoformat()} - {self.__comentario}"

    @property
    def nota(self):
        return self.__nota

    @nota.setter
    def nota(self, value):
        if not (0 <= int(value) <= 10):
            raise ValueError("Nota deve estar entre 0 e 10")
        self.__nota = int(value)

    @property
    def comentario(self):
        return self.__comentario

    @comentario.setter
    def comentario(self, value):
        self.__comentario = str(value)

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        self.__data = value
